# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'liste' de la commande 'rapport'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.format.fonctions import oui_ou_non

class PrmListe(Parametre):
    
    """Commande 'rapport liste'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "liste les rapports existants"
        self.aide_longue = \
            "Cette commande liste les rapports existants."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        rapports = list(importeur.rapport.rapports.values())
        if rapports:
            lignes = [
                "+-" + "-" * 5 + "-+-" + "-" * 10 + "-+-" + "-" * 40 + "-+",
                "|    ID | Créateur   | Sujet" + " " * 35 + " |",
                "+-" + "-" * 5 + "-+-" + "-" * 10 + "-+-" + "-" * 40 + "-+",
            ]
            for rapport in rapports:
                createur = rapport.createur and rapport.createur.nom or \
                        "inconnu"
                lignes.append(
                    "| {:>5} | {:<10} | {:<40} |".format(
                    rapport.id, createur, rapport.titre))
            
            lignes.append(
                "+-" + "-" * 5 + "-+-" + "-" * 10 + "-+-" + "-" * 40 + "-+")
            personnage << "\n".join(lignes)
        else:
            personnage << "Aucun rapport n'est actuellement défini."
