# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Package contenant l'éditeur 'rapporteur'.
"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne

from .enregistrer import Enregistrer

class EdtRapporteur(Presentation):
    
    """Classe définissant l'éditeur de rapport 'rapporteur'.
    
    """
    
    nom = "rapporteur"
    
    def __init__(self, personnage, bug):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, bug)
        if personnage and bug:
            self.construire(bug)
    
    def __getinitargs__(self):
        return (None, None)
    
    def construire(self, bug):
        """Construction de l'éditeur"""
        
        # Titre
        resume = self.ajouter_choix("résumé", "r", Uniligne, bug,"resume")
        resume.parent = self
        resume.prompt = "Resumé du bug : "
        resume.apercu = "{objet.resume}"
        resume.aide_courte = \
            "Entrez le |ent|résumé|ff| du bug |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nRésumé actuel : |bc|{objet.resume}|ff|"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, bug)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du bug"
        
        # Enregistrer
        enregistrer = self.ajouter_choix("enregistrer le bug", "e", \
            Enregistrer, bug)
        enregistrer.parent = self
        enregistrer.aide_courte = "| |tit|" + "Enregistrer le bug."
            
            
