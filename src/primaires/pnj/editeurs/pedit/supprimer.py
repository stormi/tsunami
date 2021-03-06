# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant le contexte éditeur Supprimer"""

from primaires.interpreteur.editeur.supprimer import Supprimer

class NSupprimer(Supprimer):

    """Classe définissant le contexte éditeur 'supprimer'.

    Ce contexte permet spécifiquement de supprimer un prototype de PNJ.

    """

    def interpreter(self, msg):
        """Interprétation du contexte"""
        msg = msg.lower()
        prototype = self.objet
        if msg == "oui":
            objet = type(self).importeur
            for nom in self.action.split("."):
                objet = getattr(objet, nom)

            nb_objets = len(prototype.pnj)
            if nb_objets > 0:
                s = nb_objets > 1 and "s" or ""
                nt = nb_objets > 1 and "nt" or ""
                self.pere << "|err|{} PNJ{s} existe{nt} modelé{s} sur ce " \
                        "prototype. Opération annulée.|ff|".format(nb_objets,
                        s=s, nt=nt)
                self.migrer_contexte(self.opts.rci_ctx_prec)
            else:
                objet(self.objet.cle)
                self.fermer()
                self.pere << self.confirme
        elif msg == "non":
            self.migrer_contexte(self.opts.rci_ctx_prec)
        else:
            self.pere << "|err|Choix invalide.|ff|"
