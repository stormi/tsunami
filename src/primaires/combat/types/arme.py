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


"""Fichier contenant le type arme."""

from random import randint

from bases.objet.attribut import Attribut
from corps.aleatoire import *
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from primaires.objet.types.base import BaseType
from primaires.perso.exceptions.stat import DepassementStat
from primaires.perso.personnage import Personnage

class Arme(BaseType):

    """Type d'objet: arme.

    """

    nom_type = "arme"
    cle_talent = ""
    nom_talent = ""
    niveau_talent = "combat"
    difficulte_talent = 0
    empilable_sur = ["vêtement"]

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.emplacement = "mains"
        self.positions = (1, 2)
        self.degats_fixes = 5
        self.degats_variables = 0
        self.bonus_lance = 0
        self.peut_depecer = False

        # Editeurs
        self.etendre_editeur("f", "dégâts fixes", Entier, self, "degats_fixes")
        self.etendre_editeur("v", "dégâts variables", Entier, self,
                "degats_variables")
        self.etendre_editeur("bo", "bonus au lancé", Entier, self, \
                "bonus_lance", None)
        self.etendre_editeur("pe", "peut dépecer", Flag, self, "peut_depecer")

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        fixes = enveloppes["f"]
        fixes.apercu = "{objet.degats_fixes}"
        fixes.prompt = "Dégâts fixes de l'arme : "
        fixes.aide_courte = \
            "Entrez les |ent|dégâts fixes|ff| de l'arme. Ils représentent,\n" \
            "ajoutés aux dégâts variables, les dégâts infligés par cette " \
            "arme.\n" \
            "Si une arme a |cmd|5|ff| de dégâts fixes et |cmd|2|ff| " \
            "de dégâts variables,\nses dégâts réels se situeront entre 5 " \
            "et 7.\n\n" \
            "Dégâts fixes actuels : {objet.degats_fixes}"

        variables = enveloppes["v"]
        variables.apercu = "{objet.degats_variables}"
        variables.prompt = "Dégâts variables de l'arme : "
        variables.aide_courte = \
            "Entrez les |ent|dégâts variables|ff| de l'arme. Ils " \
            "représentent, ajoutés aux dégâts fixes,\nles dégâts " \
            "infligés par cette arme.\n" \
            "Si une arme a |cmd|5|ff| de dégâts fixes et |cmd|2|ff| " \
            "de dégâts variables,\nses dégâts réels se situeront entre 5 " \
            "et 7.\n\n" \
            "Dégâts variables actuels : {objet.degats_variables}"

        bonus = enveloppes["bo"]
        bonus.apercu = "{objet.bonus_lance}"
        bonus.prompt = "Bonus au lancé de l'arme : "
        bonus.aide_courte = \
            "Entrez le |ent|bonus au lancé|ff| de l'arme. Il représentent\n" \
            "les dommages ajoutés au dégâts si l'arme est lancé.\n\n" \
            "Bonus au lancé actuel : {objet.bonus_lance}"

    def veut_jeter(self, personnage, sur):
        """Le personnage veut jeter l'objet sur sur."""
        if not isinstance(sur, Personnage):
            return ""

        return "jeter_personnage"

    def jeter(self, personnage, elt):
        """Jette l'arme sur un élément."""
        fact = varier(personnage.agilite, 20) / 100
        fact *= (1.6 - personnage.poids / personnage.poids_max)
        fact_adv = varier(elt.agilite, 20) / 100
        fact_adv *= (1.6 - elt.poids / elt.poids_max)
        reussite = fact >= fact_adv
        if reussite:
            personnage.envoyer("Vous lancez {} sur {{}}.".format(
                    self.get_nom()), elt)
            elt.envoyer("{{}} lance {} droit sur vous.".format(
                    self.get_nom()), personnage)
            personnage.salle.envoyer("{{}} envoie {} sur {{}}.".format(
                    self.get_nom()), personnage, elt)
        else:
            personnage.envoyer("Vous lancez {} mais manquez {{}}.".format(
                    self.get_nom()), elt)
            elt.envoyer("{{}} lance {} mais vous manque.".format(
                    self.get_nom()), personnage)
            personnage.salle.envoyer("{{}} envoie {} mais manque {{}}.".format(
                    self.get_nom()), personnage, elt)

        personnage.salle.objets_sol.ajouter(self)
        return reussite

    def jeter_personnage(self, personnage, cible):
        """Jette l'arme sur un personnage."""
        degats = self.bonus_lance + int(self.degats_fixes * 0.8)
        if self.degats_variables > 0:
            degats += randint(0, self.degats_variables)

        # Sélection du membre
        membres = cible.equipement.membres
        membre = choix_probable(membres, attribut="probabilite_atteint")

        # Calcul des dégâts encaissés
        objets = len(membre.equipe) and membre.equipe or []
        for objet in objets:
            if objet and objet.est_de_type("armure"):
                encaisse = objet.encaisser(personnage, self, degats)
                degats -= encaisse

        cible.envoyer_lisser("{} vous atteint à {} !".format(
                self.get_nom().capitalize(), membre.nom_complet))
        personnage.salle.envoyer_lisser("{} atteint {{}} à {} !".format(
                self.get_nom().capitalize(), membre.nom_complet), cible)

        try:
            cible.stats.vitalite -= degats
        except DepassementStat:
            cible << "Trop, c'est trop ! Vous perdez conscience."
            cible.salle.envoyer("{} s'écroule sur le sol.", cible)
            cible.mourir(adversaire=personnage)
        else:
            cible.reagir_attaque(personnage)
