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


"""Package contenant l'éditeur 'sbedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.uniligne import Uniligne
from .edt_etats import EdtEtats
from .edt_elements import EdtElements

class EdtSbedit(Presentation):
    
    """Classe définissant l'éditeur de bonhomme de neige 'sbedit'.
    
    """
    
    nom = "sbedit"
    
    def __init__(self, personnage, prototype):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, prototype)
        if personnage and prototype:
            self.construire(prototype)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, prototype):
        """Construction de l'éditeur."""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, prototype, "nom")
        nom.parent = self
        nom.prompt = "Nom de construction du bonhomme de neige : "
        nom.apercu = "{objet.nom}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| du bonhomme de neige ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "Nom actuel : |bc|{objet.nom}|ff|"
        
        # Utilisable par les joueurs
        utilisable = self.ajouter_choix("utilisable par les joueurs", "u",
                Flag, prototype, "utilisable_joueurs")
        utilisable.parent = self
        
        # États
        etats = self.ajouter_choix("états", "t", EdtEtats, prototype)
        etats.parent = self
        etats.apercu = "{objet.str_etats}"
        
        # Éléments
        elements = self.ajouter_choix("éléments", "l", EdtElements,
                prototype)
        elements.parent = self
        elements.apercu = "{objet.str_elements}"
