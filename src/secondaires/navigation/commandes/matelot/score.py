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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'score' de la commande 'matelot'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.perso.montrer.score import MontrerScore

class PrmScore(Parametre):

    """Commande 'matelot score'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "score", "score")
        self.schema = "<nom_matelot>"
        self.tronquer = True
        self.aide_courte = "affiche le score du matelot"
        self.aide_longue = \
            "Cette commande permet d'afficher les stats complètes du " \
            "matelot. Le rendu est identiqué au rendu de votre fiche score."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le matelot
        matelot = dic_masques["nom_matelot"].matelot
        pnj = matelot.personnage
        personnage << MontrerScore.montrer(pnj, nom=matelot.nom)
