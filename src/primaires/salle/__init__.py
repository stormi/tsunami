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


"""Fichier contenant le module primaire salle."""

import re

from abstraits.module import *
from primaires.format.fonctions import format_nb

from .salle import Salle, ZONE_VALIDE, MNEMONIC_VALIDE
from .sorties import NOMS_SORTIES
from .etendue import Etendue
from .config import cfg_salle
from .templates.terrain import Terrain
from . import commandes
from .editeurs.redit import EdtRedit
from .coordonnees import Coordonnees
from . import masques
from .porte import Porte

class Module(BaseModule):
    
    """Classe utilisée pour gérer des salles.
    Dans la terminologie des MUDs, les salles sont des "cases" avec une
    description et une liste de sorties possibles, que le joueur peut
    emprunter. L'ensemble des salles consiste l'univers, auquel il faut
    naturellement rajouter des PNJ et objets pour qu'il soit riche un minimum.
    
    Pour plus d'informations, consultez le fichier
    src/primaires/salle/salle.py contenant la classe Salle.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "salle", "primaire")
        self._salles = {} # ident:salle
        self._coords = {} # coordonnee:salle
        self.commandes = []
        self.salle_arrivee = ""
        self.salle_retour = ""
        self.aliases = {
            "e": "est",
            "se": "sud-est",
            "s": "sud",
            "so": "sud-ouest",
            "o": "ouest",
            "no": "nord-ouest",
            "n": "nord",
            "ne": "nord-est",
            "b": "bas",
            "h": "haut",
            "s-e": "sud-est",
            "s-o": "sud-ouest",
            "n-o": "nord-ouest",
            "n-e": "nord-est",
        }
        
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "salles", "salles")
        self.terrains = {}
        self.etendues = {}
    
    def config(self):
        """Méthode de configuration du module"""
        type(self.importeur).anaconf.get_config("salle", \
            "salle/salle.cfg", "config salle", cfg_salle)
        self.importeur.hook.ajouter_hook("salle:regarder",
                "Hook appelé dès qu'on regarde une salle.")
        
        # Ajout des terrain
        self.ajouter_terrain("ville", "quelques maisons")
        self.ajouter_terrain("route", "une route")
        self.ajouter_terrain("forêt", "des forêts denses")
        self.ajouter_terrain("plaine", "des plaines verdoyantes")
        self.ajouter_terrain("rive", "une rive basse")
        
        BaseModule.config(self)
    
    def init(self):
        """Méthode d'initialisation du module"""
        # On récupère les portes
        portes = self.importeur.supenr.charger_groupe(Porte)
        # On récupère les salles
        salles = self.importeur.supenr.charger_groupe(Salle)
        for salle in salles:
            self.ajouter_salle(salle)
        
        nb_salles = len(self._salles)
        self.logger.info(format_nb(nb_salles, "{nb} salle{s} récupérée{s}", \
                fem=True))
        
        # On récupère les étendues
        etendues = self.importeur.supenr.charger_groupe(Etendue)
        for etendue in etendues:
            self.ajouter_etendue(etendue)
        
        nb_etendues = len(self.etendues)
        self.logger.info(format_nb(nb_etendues, "{nb} étendue{s} " \
                "d'eau{x} récupérée{s}", fem=True))
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.addroom.CmdAddroom(),
            commandes.carte.CmdCarte(),
            commandes.chsortie.CmdChsortie(),
            commandes.etendue.CmdEtendue(),
            commandes.fermer.CmdFermer(),
            commandes.goto.CmdGoto(),
            commandes.ouvrir.CmdOuvrir(),
            commandes.redit.CmdRedit(),
            commandes.regarder.CmdRegarder(),
            commandes.supsortie.CmdSupsortie(),
            commandes.verrouiller.CmdVerrouiller(),
            commandes.deverrouiller.CmdDeverrouiller(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'redit'
        self.importeur.interpreteur.ajouter_editeur(EdtRedit)
    
    def preparer(self):
        """Préparation du module.
        On vérifie que :
        -   les salles de retour et d'arrivée sont bien créés (sinon,
            on les recrée)
        -   les personnages présents dans self._personnages soient
            toujours là
        
        """
        # On récupère la configuration
        conf_salle = type(self.importeur).anaconf.get_config("salle")
        salle_arrivee = conf_salle.salle_arrivee
        salle_retour = conf_salle.salle_retour
        
        if salle_arrivee not in self:
            # On crée la salle d'arrivée
            zone, mnemonic = salle_arrivee.split(":")
            salle_arrivee = self.creer_salle(zone, mnemonic, valide=False)
            salle_arrivee.titre = "La salle d'arrivée"
            salle_arrivee = salle_arrivee.ident
        
        if salle_retour not in self:
            # On crée la salle de retour
            zone, mnemonic = salle_retour.split(":")
            salle_retour = self.creer_salle(zone, mnemonic, valide=False)
            salle_retour.titre = "La salle de retour"
            salle_retour = salle_retour.ident
        
        self.salle_arrivee = salle_arrivee
        self.salle_retour = salle_retour
        
        for salle in self._salles.values():
            for personnage in salle.personnages:
                if personnage.salle is not salle:
                    salle.retirer_personnage(personnage)
    
    def __len__(self):
        """Retourne le nombre de salles"""
        return len(self._salles)
    
    def __getitem__(self, cle):
        """Retourne la salle correspondante à la clé.
        Celle-ci peut être de différents types :
        *   une chaîne : c'est l'identifiant 'zone:mnemonic'
        *   un objet Coordonnees
        *   un tuple représentant les coordonnées
        
        """
        if type(cle) is str:
            return self._salles[cle]
        elif type(cle) is Coordonnees:
            return self._coords[cle.tuple()]
        elif type(cle) is tuple:
            return self._coords[cle]
        else:
            raise TypeError("un type non traité sert d'identifiant " \
                    "({})".format(repr(cle)))
    
    def __contains__(self, cle):
        """Retourne True si la clé se trouve dans l'un des dictionnaires de
        salles. Voir la méthode __getitem__ pour connaître les types acceptés.
        
        """
        if type(cle) is str:
            return cle in self._salles.keys()
        elif type(cle) is Coordonnees:
            return cle.tuple() in self._coords.keys()
        elif type(cle) is tuple:
            return cle in self._coords.keys()
        else:
            raise TypeError("un type non traité sert d'identifiant " \
                    "({})".format(repr(cle)))
    
    def ajouter_salle(self, salle):
        """Ajoute la salle aux deux dictionnaires
        self._salles et self._coords.
        
        """
        self._salles[salle.ident] = salle
        if salle.coords.valide:
            self._coords[salle.coords.tuple()] = salle
    
    def creer_salle(self, zone, mnemonic, x=0, y=0, z=0, valide=True):
        """Permet de créer une salle"""
        ident = zone + ":" + mnemonic
        if ident in self._salles.keys():
            raise ValueError("la salle {} existe déjà".format(ident))
        if not re.search(ZONE_VALIDE, zone):
            raise ValueError("Zone {} invalide".format(zone))
        if not re.search(MNEMONIC_VALIDE, mnemonic):
            raise ValueError("Mnémonic {} invalide ({})".format(mnemonic,
                    MNEMONIC_VALIDE))
        
        salle = Salle(zone, mnemonic, x, y, z, valide)
        self.ajouter_salle(salle)
        return salle
    
    def supprimer_salle(self, cle):
        """Supprime la salle.
        La clé est l'identifiant de la salle.
        
        """
        salle = self._salles[cle]
        coords = salle.coords
        if coords.valide and coords.tuple() in self._coords.keys():
            del self._coords[coords.tuple()]
        del self._salles[cle]
        salle.detruire()
    
    def traiter_commande(self, personnage, commande):
        """Traite les déplacements"""
        
        # Si la commande est vide, on ne se déplace pas
        if len(commande) == 0:
            return False
        
        commande = commande.lower()
        salle = personnage.salle
        if commande in self.aliases.keys():
            commande = self.aliases[commande]
            try:
                sortie = salle.sorties.get_sortie_par_nom(commande,
                        cachees=False)
            except KeyError:
                pass
            else:
                personnage.deplacer_vers(sortie.nom)
                return True
        
        for nom, sortie in salle.sorties.iter_couple():
            if sortie:
                if (sortie.cachee and sortie.nom == commande) or ( \
                        not sortie.cachee and sortie.nom.startswith(commande)):
                    personnage.deplacer_vers(sortie.nom)
                    return True
        
        if commande in NOMS_SORTIES.keys():
            personnage << "Vous ne pouvez aller par là..."
            return True
        
        return False
    
    def changer_ident(self, ancien_ident, nouveau_ident):
        """Change l'identifiant d'une salle"""
        salle = self._salles[ancien_ident]
        del self._salles[ancien_ident]
        self._salles[nouveau_ident] = salle
    
    def changer_coordonnees(self, ancien_tuple, nouvelles_coords):
        """Change les coordonnées d'une salle.
        Les anciennes coordonnées sont données sous la forme d'un tuple
            (x, y, z, valide)
        Les nouvelles sont un objet Coordonnees.
        
        """
        a_x, a_y, a_z, a_valide = ancien_tuple
        salle = nouvelles_coords.parent
        if a_valide and (a_x, a_y, a_z) in self._coords:
            # on va supprimer les anciennes coordonnées
            del self._coords[a_x, a_y, a_z]
        if salle and nouvelles_coords.valide:
            self._coords[nouvelles_coords.tuple()] = salle
    
    def ajouter_terrain(self, nom, survol):
        """Ajoute un terrain."""
        if nom in self.terrains:
            raise KeyError("le terrain {] existe déjà".format(repr(nom)))
        
        terrain = Terrain(nom, survol)
        self.terrains[nom] = terrain
    
    def creer_etendue(self, cle):
        """Crée une étendue d'eau."""
        if cle in self.etendues.keys():
            raise KeyError("l'étendue d'eau {} existe déjà".format(cle))
        
        etendue = Etendue(cle)
        self.ajouter_etendue(etendue)
        return etendue
    
    def ajouter_etendue(self, etendue):
        """Ajoute une étendue au dictionnaire."""
        if etendue.cle in self.etendues.keys():
            raise KeyError("l'étendue d'eau {} existe déjà".format(
                    etendue.cle))
        
        self.etendues[etendue.cle] = etendue
    
    def supprimer_etendue(self, cle):
        """Supprime l'étendue d'eau."""
        etendue = self.etendues[cle]
        etendue.detruire()
        del self.etendues[cle]
