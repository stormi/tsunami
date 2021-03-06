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


"""Fichier contenant le paramètre 'liste' de la commande 'module'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):
    
    """Commande 'module liste'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "affiche la liste des modules chargés"
        self.aide_longue = \
            "Affiche la liste des modules actuellement chargés et un petit " \
            "descriptif sur chacun. Si vous déchargez un module, il " \
            "n'apparaîtra plus dans cette liste."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère les modules chargés
        modules = type(self).importeur.modules
        # On prépare le tableau d'exécution
        lignes = []
        for module in modules:
            lignes.append(
                "  |cy|{nom}|ff| | {statut}".format(
                nom=module.nom.ljust(20), statut=module.str_statut.ljust(10)))
        
        if lignes:
            personnage.envoyer("Liste des modules chargés :\n\n" + \
                    "\n".join(sorted(lignes)))
        else:
            personnage.envoyer("|att|Aucun module n'est chargé. Ce semble " \
                "très improbable.|ff|")
