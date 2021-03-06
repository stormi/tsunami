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


"""Package contenant la commande 'skedit'."""

from primaires.interpreteur.commande.commande import Commande

class CmdSkedit(Commande):
    
    """Commande 'skedit'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "skedit", "skedit")
        self.groupe = "administrateur"
        self.schema = "<ident>"
        self.nom_categorie = "batisseur"
        self.aide_courte = "ouvre l'éditeur de squelette"
        self.aide_longue = \
            "Cette commande ouvre l'éditeur de squelette. Elle permet " \
            "donc d'ajouter et éditer des squelettes. Ceux-ci peuvent " \
            "ensuite être utilisés comme base pour des races ou " \
            "des PNJ. Dans chaque squelette se trouve, notamment, une " \
            "liste des membres du personnage qui sera créé sur ce " \
            "modèle."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle = dic_masques["ident"].ident
        if cle in type(self).importeur.perso.squelettes.keys():
            squelette = type(self).importeur.perso.squelettes[cle]
        else:
            squelette = type(self).importeur.perso.creer_squelette(cle)
        
        editeur = type(self).importeur.interpreteur.construire_editeur(
                "skedit", personnage, squelette)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()
