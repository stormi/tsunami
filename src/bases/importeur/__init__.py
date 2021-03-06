# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Ce fichier définit un objet 'importeur', chargé de contrôler le mécanisme
d'importation, initialisation, configuration, déroulement et arrêt
des modules primaires et secondaires.

On parcourt les sous-dossiers définis dans les variables :
- REP_PRIMAIRES : répertoire des modules primaires
- REP_SECONDAIRES : répertoire des modules secondaires

Il est possible de changer ces variables mais dans ce cas, une réorganisation
du projet s'impose.

Dans chaque module, on s'occupera de charger l'objet le représentant.
Par exemple, le module diffact se définit comme suit :
*   un package diffact contenu dans REP_PRIMAIRES
    *   un fichier __init__.py
        *   une classe Module

On crée un objet chargé de représenter le module. C'est cet objet qui
possède les méthodes génériques chargées d'initialiser, configurer, lancer
et arrêter un module. Les autres fichiers du module sont une boîte noire
inconnue pour l'importeur.

"""

from imp import reload
import importlib
import os
import sys
import traceback
import py_compile

from abstraits.module import *
from abstraits.obase import BaseObj, objets_base
from corps.arborescence import getcwd

# Constantes
REP_PRIMAIRES = "primaires"
REP_SECONDAIRES = "secondaires"

class Importeur:

    """Classe chargée de créer un objet Importeur.

    Il contient sous la forme d'attributs les modules primaires et
    secondaires chargés. Les modules primaires et secondaires ne sont
    pas distingués.

    On ne doit créer qu'un seul objet Importeur.

    """

    nb_importeurs = 0
    parser_cmd = None # parser de la ligne de commande
    anaconf = None # analyseur des fichiers de configuration
    man_logs = None # gestionnaire des loggers
    logger = None # le logger de l'importeur
    serveur = None
    nb_hotboot = 0
    chemins_modules = {
        "primaire": REP_PRIMAIRES,
        "secondaire": REP_SECONDAIRES,
    }
    py_modules = {}
    sauvegarde = True

    def __init__(self, parser_cmd, anaconf, man_logs, serveur,
            sauvegarde=True):
        """Constructeur de l'importeur. Il vérifie surtout
        qu'un seul est créé.

        Il prend en paramètre :
        -   le parser de commande
        -   l'analyseur des fichiers de configuration
        -   le gestionnaire des loggers
        -   le serveur
        Ces informations sont stockées comme des attributs de classe.
        Si un module souhaite y faire appel il n'aura qu'à faire
        'Importeur.attribut'.

        """
        Importeur.nb_importeurs += 1
        if Importeur.nb_importeurs > 1:
            raise RuntimeError("{0} importeurs ont été créés".format( \
                Importeur.nb_importeurs))

        Importeur.parser_cmd = parser_cmd
        Importeur.anaconf = anaconf
        Importeur.man_logs = man_logs
        Importeur.serveur = serveur
        Importeur.logger = man_logs.creer_logger("", "importeur", "")
        Importeur.sauvegarde = sauvegarde
        BaseObj.importeur = self
        __builtins__["importeur"] = self

    def __str__(self):
        """Retourne sous une forme un peu plus lisible les modules importés."""
        ret = []
        for nom_module in self.__dict__.keys():
            ret.append("{0}: {1}".format(nom_module, getattr(self, \
                    nom_module)))
        ret.sort()
        return "\n".join(ret)

    def tout_charger(self):
        """Méthode appelée pour charger les modules primaires et secondaires.
        Par défaut, on importe tout mais on ne crée rien.

        """
        # On commence par parcourir les modules primaires
        Importeur.logger.debug("Chargement des modules :")
        for nom_package in os.listdir(getcwd() + "/" + REP_PRIMAIRES):
            if not nom_package.startswith("__"):
                self.charger_module("primaire", nom_package)
                Importeur.logger.debug("  Le module {0} a été chargé".format( \
                        nom_package))
        # On fait de même avec les modules secondaires
        for nom_package in os.listdir(getcwd() + "/" + REP_SECONDAIRES):
            if not nom_package.startswith("__"):
                self.charger_module("secondaire", nom_package)
                Importeur.logger.debug("  Le module {0} a été chargé".format( \
                        nom_package))

    def tout_instancier(self):
        """Cette méthode permet d'instancier les modules chargés auparavant.
        On se base sur le type du module (classe ou objet)
        pour le créer ou non.

        En effet, cette méthode doit pouvoir être appelée quand certains
        modules sont instanciés, et d'autres non.

        NOTE IMPORTANTE: on passe au constructeur de chaque module
        self, c'est-à-dire l'importeur. Les modules en ont en effet
        besoin pour interagir entre eux et avoir accès au parser de
        la ligne de commande, à l'analyseur des fichiers de configuration
        et au gestionnaire des loggers.

        L'ordre d'instanciation des modules est contenu dans la configuration
        globale ('modules_a_instancier').
        Les modules à ignorer sont également définis dans cette configuration
        globale. Leur instance est supprimée de l'importeur.

        """
        conf_glb = Importeur.anaconf.get_config("globale")
        # On supprime avant tout les modules à ignorer
        Importeur.logger.debug("Suppression des modules à ignorer :")
        for nom_module in conf_glb.modules_a_ignorer:
            if hasattr(self, nom_module): # le module est chargé
                delattr(self, nom_module)
                Importeur.logger.debug("  Le module {0} a été ignoré et " \
                        "supprimé de l'importeur".format(nom_module))
            else:
                Importeur.logger.warning("  Le module {0} n'a pas été " \
                        "instancié et ne peut être ignoré".format(nom_module))

        # On instancie d'abord les modules prioritaires
        # (c'est-à-dire ceux définis dans la donnée de configuration)
        Importeur.logger.debug("Instanciation des modules prioritaires :")
        for nom_module in conf_glb.modules_a_instancier:
            if hasattr(self, nom_module): # le module est chargé
                module = getattr(self, nom_module)
                if type(module) is type: # on doit l'instancier
                    setattr(self, nom_module, module(self))
                    Importeur.logger.debug("  Le module {0} a été " \
                            "instancié".format(nom_module))
                elif isinstance(module, BaseModule):
                    pass
                else:
                    Importeur.logger.warning("  Le module {0} n'a pas été " \
                            "instancié".format(nom_module))

        # On charge les modules restants
        Importeur.logger.debug("Instanciation des modules restants :")
        for nom_module, module in self.__dict__.items():
            if type(module) is type: # on doit l'instancier
                setattr(self, nom_module, module(self))
                Importeur.logger.debug("  Le module {0} a été " \
                        "instancié".format(nom_module))

    def executer_script(self, script=None):
        """Exécute le script spécifié."""
        if script:
            with open(script, "r") as fichier:
                code = fichier.read()

            try:
                exec(code, {"importeur": self})
            except Exception as err:
                print(traceback.format_exc())

    def tout_configurer(self):
        """Méthode permettant de configurer tous les modules qui en ont besoin.
        Les modules qui doivent être configurés sont ceux instanciés.

        Attention: les modules non encore instanciés sont à l'état de classe.
        Tous les modules doivent donc être instanciés au minimum avant
        que cette méthode ne soit appelée. Autrement dit, la méthode
        tout_instancier doit être appelée auparavant.

        """
        conf_glb = Importeur.anaconf.get_config("globale")
        Importeur.logger.debug("Configuration des modules :")
        # On configure d'abord les modules à configurer en priorité
        Importeur.logger.debug("Configuration des modules prioritaires :")
        for nom_module in conf_glb.modules_a_configurer:
            if hasattr(self, nom_module): # le module est chargé
                module = getattr(self, nom_module)
                if module.statut == INSTANCIE:
                    module.config()
                    Importeur.logger.debug("  Le module {0} a été " \
                            "configuré".format(nom_module))
        # Configuration des modules restants
        Importeur.logger.debug("Configuration des modules restants :")
        for module in self.__dict__.values():
            if module.statut == INSTANCIE:
                module.config()
                Importeur.logger.debug("  Le module {0} a été " \
                        "configuré".format(module.nom))

    def tout_initialiser(self):
        """Méthode permettant d'initialiser tous les modules qui en ont besoin.

        Les modules à initialiser sont ceux configurés.

        """
        conf_glb = Importeur.anaconf.get_config("globale")
        Importeur.logger.debug("Initialisation des modules :")
        # On initialise d'abord les modules à initialiser en priorité
        Importeur.logger.debug("Initialisation des modules prioritaires :")
        a_initialiser = conf_glb.modules_a_initialiser
        for nom_module in a_initialiser:
            if nom_module == "*":
                break

            if hasattr(self, nom_module): # le module est chargé
                module = getattr(self, nom_module)
                if module.statut == CONFIGURE:
                    module.init()
                    Importeur.logger.debug("  Le module {0} a été " \
                            "initialisé".format(nom_module))

        # Initialisation des modules restants
        if "*" in a_initialiser:
            indice = a_initialiser.index("*")
            a_initialiser = a_initialiser[indice:]
        else:
            a_initialiser = []

        Importeur.logger.debug("Initialisation des modules non spécifiés :")
        for module in self.__dict__.values():
            if module.statut == CONFIGURE and module.nom not in a_initialiser:
                module.init()
                Importeur.logger.debug("  Le module {0} a été " \
                        "initialisé".format(module.nom))

        # On initialise les modules restants
        Importeur.logger.debug("Initialisation des modules restants :")
        for nom_module in a_initialiser:
            if hasattr(self, nom_module): # le module est chargé
                module = getattr(self, nom_module)
                if module.statut == CONFIGURE:
                    module.init()
                    Importeur.logger.debug("  Le module {0} a été " \
                            "initialisé".format(nom_module))

        for module in self.__dict__.values():
            if module.statut == INITIALISE:
                module.ajouter_commandes()

    def tout_preparer(self):
        """Méthode permettant de préparer tous les modules.

        """
        Importeur.logger.debug("Préparation des modules :")
        self.supenr.preparer()
        prepares = [self.supenr]
        for module in self.__dict__.values():
            if module not in prepares and module.statut == INITIALISE:
                for autre in module.preparer_apres:
                    autre_m = getattr(self, autre)
                    if autre_m in prepares:
                        continue

                    autre_m.preparer()
                    prepares.append(autre_m)
                    Importeur.logger.debug("  Le module {0} a été " \
                            "préparé".format(autre))

                module.preparer()
                prepares.append(module)
                Importeur.logger.debug("  Le module {0} a été " \
                        "préparé".format(module.nom))

    def tout_detruire(self):
        """Méthode permettant de détruire tous les modules qui en ont besoin.
        Les modules à détruire sont ceux initialisés.

        NOTE IMPORTANTE: on peut préciser dans le fichier de configuration
        globale une liste des modules à détruire. Les modules de cette liste
        seront détruits après les autres, et non avant.

        """
        conf_glb = Importeur.anaconf.get_config("globale")
        Importeur.logger.debug("Destruction des modules :")
        a_detruire = conf_glb.modules_a_detruire
        autres = ["supenr"]
        for nom in autres:
            if nom not in a_detruire:
                a_detruire.append(nom)

        # On détruit d'abord les modules qui ne sont pas à garder en priorité
        for nom, module in tuple(self.__dict__.items()):
            if module.statut == INITIALISE and \
                    module.nom not in a_detruire:
                module.detruire()
                Importeur.logger.debug("  Le module {0} a été " \
                        "détruit".format(module.nom))
                delattr(self, nom)

        # On détruit enfin les modules à détruire en dernier
        Importeur.logger.debug("Destruction des modules à détruire en " \
                "dernier :")
        for nom_module in a_detruire:
            if hasattr(self, nom_module): # le module est chargé
                module = getattr(self, nom_module)
                if module.statut == INITIALISE:
                    module.detruire()
                    Importeur.logger.debug("  Le module {0} a été " \
                            "détruit".format(nom_module))

    def tout_arreter(self):
        """Méthode permettant d'arrêter tous les modules.
        Cette méthode ne doit être appelée qu'en cas d'arrêt complet du MUD,
        en cas de reboot total par exemple.

        """
        for module in self.__dict__.values():
            module.arreter()
            Importeur.logger.debug("  Le module {0} a été " \
                        "arrêté".format(module.nom))

    def deconnecter_joueurs(self):
        """Déconnecte tous les joueurs connectés"""
        for instance in self.connex.instances.values():
            instance.envoyer("\n|att|Arrêt du MUD en cours, vous allez être " \
                    "déconnecté...|ff|")
            instance.deconnecter("Arrêt du MUD")

    def tout_decharger(self):
        """Méthode déchargeant tous les modules"""
        for module in self.modules:
            self.decharger_module(module.type, module.nom)

    def tout_recharger(self):
        """Méthode appelée pour recharger TOUS les modules"""
        logger = type(self).man_logs.get_logger("sup")
        res = False
        Importeur.nb_hotboot += 1
        objets_base.clear()
        try:
             for nom_package in os.listdir(getcwd() + "/" + REP_PRIMAIRES):
                 if not nom_package.startswith("__"):
                     py_compile.compile(getcwd() + "/" + \
                            REP_PRIMAIRES + "/" + nom_package + \
                            "/__init__.py", doraise=True)
        except py_compile.PyCompileError:
            logger.fatal(
                "Une erreur s'est produite lors de l'hotboot.")
            logger.fatal(traceback.format_exc())
        else:
            self.tout_detruire()
            self.tout_decharger()
            self.tout_charger()
            self.tout_instancier()
            self.tout_configurer()
            self.tout_initialiser()
            res = True
        return res

    def boucle(self):
        """Méthode appelée à chaque tour de boucle synchro.
        Elle doit faire appel à la méthode boucle de chaque module primaire
        ou secondaire.

        """
        for module in self.__dict__.values():
            module.boucle()

    def module_est_charge(self, nom):
        """Retourne True si le module est déjà chargé, False sinon.
        On n'a pas besoin du type du module, les modules primaires
        et secondaires étant stockés de la même façon.

        Attention: un module peut être chargé sans être instancié,
        configuré ou initialisé.

        """
        return nom in self.__dict__.keys()

    def charger_module(self, m_type, nom):
        """Méthode permettant de charger un module en fonction de son type et
        de son nom.

        Si le module est déjà chargé, on le recharge.

        Note: à la différence de tout_charger, cette méthode crée directement
        l'objet gérant le module.

        """
        if m_type == "primaire":
            rep = REP_PRIMAIRES
        elif m_type == "secondaire":
            rep = REP_SECONDAIRES
        else:
            raise ValueError("le type {0} n'est ni primaire ni secondaire" \
                    .format(type))

        py_chemin = rep + "." + nom
        if py_chemin in type(self).py_modules:
            reload(type(self).py_modules[py_chemin])

        module = importlib.import_module(py_chemin)
        type(self).py_modules[py_chemin] = module
        c_module = getattr(module, "Module")
        setattr(self, nom, c_module(self))

    def decharger_module(self, m_type, nom):
        """Méthode permettant de décharger un module.

        Elle se charge :
        -   d'appeler la méthode detruire du module
        -   de supprimer le module des modules dans sys.modules
        -   de supprimer l'instance du module dans self

        """
        if self.module_est_charge(nom):
            getattr(self, nom).detruire()
            delattr(self, nom)
        else:
            print("{0} n'est pas dans les attributs de l'importeur".format(nom))

    def recharger_module(self, m_type, nom):
        """Cette méthode permet de recharger un module.

        Elle passe par :
        -   decharger_module
        -   recharge le module grâce à imp.reload
        -   charger_module
        -   config_module
        -   init_module

        """
        if m_type == "primaire":
            rep = "primaires"
        else:
            rep = "secondaires"

        self.decharger_module(m_type, nom)
        self.charger_module(m_type, nom)
        self.config_module(nom)
        self.init_module(nom)

    def config_module(self, nom):
        """Méthode chargée de configurer ou reconfigurer un module."""
        if self.module_est_charge(nom):
            getattr(self, nom).config()
        else:
            print("{0} n'existe pas ou n'est pas chargé.".format(nom))

    def init_module(self, nom):
        """Méthode chargée d'initialiser un module."""
        if self.module_est_charge(nom) and getattr(self, nom).statut == \
                CONFIGURE:
            getattr(self, nom).init()
        else:
            print("{0} n'existe pas ou n'est pas configuré.".format(nom))

    @property
    def modules(self):
        """Retourne un tuple contenant les modules chargés"""
        modules = []
        for module in self.__dict__.values():
            modules.append(module)

        return tuple(modules)
