# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Package contenant l'éditeur 'famedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

"""

from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.selection import Selection
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.editeurs.edt_script import EdtScript
from secondaires.familier.constantes import *

class EdtFamedit(Presentation):

    """Classe définissant l'éditeur de fiche de familier famedit."""

    nom = "famedit"

    def __init__(self, personnage, fiche):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, fiche)
        if personnage and fiche:
            self.construire(fiche)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, fiche):
        """Construction de l'éditeur"""
        # Régimes
        regime = self.ajouter_choix("régime alimentaire", "r", Choix, fiche,
                "regime", REGIMES)
        regime.parent = self
        regime.prompt = "Régime alimentaire du familier : "
        regime.apercu = "{objet.regime}"
        regime.aide_courte = \
            "Entrez le |ent|régime|ff| du familier ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nRégimes disponibles : {}.\n\n" \
            "Régime actuel : |bc|{{objet.regime}}|ff|".format(
            ", ".join(REGIMES))

        # Harnachements supportés
        harnachements = self.ajouter_choix("harnachement supportés", "h",
                Selection, fiche, "harnachements", TYPES_HARNACHEMENT)
        harnachements.parent = self
        harnachements.prompt = "Harnachements supportés : "
        harnachements.apercu = "{objet.str_harnachements}"
        harnachements.aide_courte = \
            "Entrez un |ent|harnachement supporté|ff| pour l'ajouter " \
            "ou le retirer\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nHarnachements possibles : " + \
            ", ".join(sorted(TYPES_HARNACHEMENT)) + "\nHarnachements " \
            "supportés actuellement : {objet.str_harnachements}"

        # Stats pouvant progresser
        stats = self.ajouter_choix("stats pouvant progresser", "st",
                Selection, fiche, "stats_progres", ["force", "agilite",
                "robustesse", "intelligence", "charisme", "sensibilite"])
        stats.parent = self
        stats.prompt = "Stats pouvant augmenter automatiquement : "
        stats.apercu = "{objet.str_stats_progres}"
        stats.aide_courte = \
            "Entrez un |ent|nom de stat|ff| pour l'ajouter " \
            "ou le retirer\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nQuand le familier gagne un niveau, il va " \
            "choisir aléatoirement parmi ces stats et les\naugmenter " \
            "si il a des points d'entraînement disponibles\n\nStats " \
            "automatiques actuelles : {objet.str_stats_progres}"

        # Monture
        monture = self.ajouter_choix("peut être monté", "m", Flag, fiche,
                "monture")
        monture.parent = self

        # Sorties verticales
        verticales = self.ajouter_choix(
                "peut emprunter les sorties verticales", "v", Flag, fiche,
                "sorties_verticales")
        verticales.parent = self

        # Aller en intérieur
        interieur = self.ajouter_choix("peut aller en intérieur", "l",
                Flag, fiche, "aller_interieur")
        interieur.parent = self

        # Difficulté d'apprivoisement
        difficulte = self.ajouter_choix("difficulté d'apprivoisement", "d",
                Entier, fiche, "difficulte_apprivoisement")
        difficulte.parent = self
        difficulte.apercu = "{objet.difficulte_apprivoisement}%"
        difficulte.prompt = "Entrez la difficulté d'apprivoisement du " \
                "familier : "
        difficulte.aide_courte = \
            "Entrez |ent|la difficulté d'apprivoisement|ff| du familier\n" \
            "(entre |ent|1|ff| et |ent|100|ff|) ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nDifficulté actuelle : " \
            "{objet.difficulte_apprivoisement}%"

        # Prix unitaire
        prix = self.ajouter_choix("prix unitaire", "u",
                Entier, fiche, "m_valeur")
        prix.parent = self
        prix.apercu = "{objet.m_valeur} pièces de bronze"
        prix.prompt = "Entrez le prix unitaire du familier : "
        prix.aide_courte = \
            "Entrez |ent|le prix unitaire|ff| du familier" \
            "ou |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Prix unitaire actuel : {objet.m_valeur}"

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                fiche.script)
        scripts.parent = self
