# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'lever' de la commande 'ancre'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmLever(Parametre):

    """Commande 'ancre lever'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "lever", "weigh")
        self.aide_courte = "lève l'ancre présente"
        self.aide_longue = \
            "Cette commande lève l'ancre présente dans la salle où " \
            "vous vous trouvez."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        etendue = navire.etendue
        if not hasattr(salle, "ancre"):
            personnage << "|err|Il n'y a pas de ancre ici.|ff|"
            return

        ancre = salle.ancre
        if not ancre:
            personnage << "|err|Vous ne voyez aucune ancre ici.|ff|"
            return

        vitesse = navire.vitesse
        if not ancre.jetee:
            personnage << "|err|Cette ancre n'est pas jetée.|ff|"
        elif navire.passerelle:
            personnage << "|err|La passerelle est dépliée.|ff|"
        else:
            if navire.proprietaire and not navire.a_le_droit(personnage,
                    si_present=True):
                personnage << "|err|Vous ne pouvez lever l'ancre de ce " \
                        "navire.|ff|"
                return

            navire.immobilise = False
            ancre.jetee = False
            personnage << "Vous levez l'ancre."
            personnage.salle.envoyer("{} lève l'ancre.", personnage)
