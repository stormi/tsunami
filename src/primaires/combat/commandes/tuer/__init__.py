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


"""Package contenant la commande 'tuer'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdTuer(Commande):

    """Commande 'tuer'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "tuer", "kill")
        self.schema = "<personnage_present>"
        self.nom_categorie = "combat"
        self.aide_courte = "attaque un personnage présent"
        self.aide_longue = \
            "Cette commande attaque un personnage présent dans la pièce, " \
            "si vous pouvez le faire. Le combat se terminera plus " \
            "vraisemblablement par la fuite ou la mort d'un des deux " \
            "combattants."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        from primaires.joueur.joueur import Joueur
        attaque = dic_masques["personnage_present"].personnage
        if attaque.est_mort() or not attaque.peut_etre_attaque():
            personnage << "|err|Vous ne pensez pas que c'est suffisant ?|ff|"
            return

        salle = personnage.salle
        if not personnage.est_immortel() and salle.a_flag("anti combat"):
            personnage << "|err|Vous ne pouvez combattre ici.|ff|"
            return

        if not personnage.est_immortel() and not personnage.pk and \
                isinstance(attaque, Joueur):
            personnage << "|err|Votre flag PK n'est pas actif.|ff|"
            return

        if not attaque.pk:
            personnage << "|err|Vous ne pouvez attaquer un joueur qui " \
                    "n'a pas le flag PK activé.|ff|"
            return

        personnage.agir("tuer")
        personnage.attaquer(attaque)
