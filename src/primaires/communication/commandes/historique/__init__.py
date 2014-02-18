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
# LIABLE FOR ANY historiqueCT, INhistoriqueCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'historique'."""

from datetime import datetime

from primaires.interpreteur.commande.commande import Commande
from primaires.format.tableau import Tableau, GAUCHE, DROITE

class CmdHistorique(Commande):

    """Commande 'historique'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "historique", "history")
        self.nom_categorie = "parler"
        self.aide_courte = "affiche les derniers messages reçus"
        self.aide_longue = \
            "Cette commande permet de voir les dix derniers messages reçus " \
            "dans divers canaux (que ce soient les canaux HRP auxquels " \
            "vous êtes connectés, les messages dits RP dans la salle grâce " \
            "à la commande %dire% où ceux qui vous sont transmis " \
            "directement par %parler%)."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        messages = importeur.communication.messages.get(personnage, [])
        if len(messages) == 0:
            personnage << "|err|Vous n'avez encore aucune conversation " \
                    "à rappeler."
            return

        messages = messages[-10:]
        tableau = Tableau("|tit|Derniers messages reçus|ff|")
        tableau.ajouter_colonne("|tit|Il y a|ff|")
        tableau.ajouter_colonne("|tit|Canal|ff|")
        tableau.ajouter_colonne("|tit|Nom|ff|")
        tableau.ajouter_colonne("|tit|Message|ff|")
        for date, auteur, canal, message in messages:
            delta = datetime.now() - date
            secondes = delta.total_seconds()
            duree = 0
            unite = "seconde"
            msg_duree = None
            if secondes < 3:
                msg_duree = "quelques secondes"
            elif secondes < 60:
                duree = secondes // 5 * 5
            elif secondes < 300:
                duree = secondes // 60
                unite = "minute"
            elif secondes < 3600:
                duree = secondes / 60 // 5 * 5
                unite = "minute"
            elif secondes < 86400:
                duree = secondes // 3600
                unite = "heure"
            else:
                duree = secondes // 86400
                unite = "jour"

            s = "s" if duree > 1 else ""
            if msg_duree is None:
                msg_duree = "{} {}{s}".format(duree, unite, s=s)

            tableau.ajouter_ligne(msg_duree, auteur.nom, canal, message)

        personnage << tableau.afficher()