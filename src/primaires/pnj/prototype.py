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


"""Ce fichier contient la classe Prototype, détaillée plus bas."""

from abstraits.id import ObjetID
from bases.collections.liste_id import ListeID
from primaires.format.description import Description

class Prototype(ObjetID):
    
    """Classe représentant un prototype de PNJ.
    
    """
    
    groupe = "prototypes_pnj"
    sous_rep = "pnj/prototypes"
    def __init__(self, cle=""):
        """Constructeur d'un type"""
        ObjetID.__init__(self)
        self.cle = cle
        self._attributs = {}
        self.no = 0 # nombre de PNJ créés sur ce prototype
        self.nom_singulier = "quelqu'un"
        self.etat_singulier = "se tient ici"
        self.nom_pluriel = "quelques-uns"
        self.etat_pluriel = "se tiennent ici"
        self.description = Description(parent=self)
        self.pnj = ListeID(self)
    
    def __getnewargs__(self):
        return ()
    
    def __str__(self):
        return self.cle
    
    def get_nom(self, nombre):
        """Retourne le nom complet en fonction du nombre.
        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel
        
        """
        if nombre <= 0:
            raise ValueError("la focntion get_nom_pluriel a été appelée " \
                    "avec un nombre négatif ou nul.")
        elif nombre == 1:
            return self.nom_singulier
        else:
            return str(nombre) + " " + self.nom_pluriel
    
    def get_nom_etat(self, nombre):
        """Retourne le nom et l'état en fonction du nombre."""
        nom = self.get_nom(nombre)
        if nombre == 1:
            return nom + " " + self.etat_singulier
        else:
            return nom + " " + self.etat_pluriel

ObjetID.ajouter_groupe(Prototype)
