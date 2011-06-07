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


"""Fichier contenant la classe Joueur, détaillée plus bas."""

from abstraits.id import ObjetID

from .vecteur import Vecteur
from .force import Propulsion, Frottement

class Vehicule(ObjetID):
    """Classe représentant un véhicule
    
    """
    groupe = "vehicules"
    sous_rep = "vehicules"
    
    def __init__(self):
        """Constructeur du véhicule
            
            Initialise les valeurs et crée deux forces toujours présente
            la propulsion qui serre à faire avance le véhicule ainsi
            que les forttements qui servent à garantir que la vitesse
            ne pourra pas augmenter indéfiniment
            
        """
        ObjetID.__init__(self)
        self.masse = 1
        self.position = Vecteur(0, 0, 0)
        self.vitesse = Vecteur(0, 0, 0)
        
        self.propulsion = Propulsion()
        self.frottement = Frottement(self,0.7)
        
        self.forces = [self.propulsion, self.frottement]
    
    def __getnewargs__(self):
        return ()
    
    def avancer(self):
        """Fait avancer le vehicule"""
        
        #Calcul la nouvelle position
        self.position += self.vitesse
        
        #Si on a une masse nulle c'est la bazar
        if self.masse == 0:
            raise(Exception("Vehicule de masse nulle, au secours !"))
        
        #On calcul l'accélération à partir des forces
        acceleration = Vecteur(0,0,0)
        for force in self.forces:
            acceleration += (1 / self.masse) * force.valeur
        
        #On calcul la nouvelle vitesse à partir de l'accélération
        self.vitesse += acceleration
        
        #On renvoit la nouvelle position
        return self.position
    
    def get_prochaine_coordonnees(self):
        return self.position + self.vitesse
        
    
# On ajoute le groupe à ObjetID
ObjetID.ajouter_groupe(Vehicule)
