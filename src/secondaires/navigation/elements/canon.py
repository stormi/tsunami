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


"""Fichier contenant la classe Canon, détaillée plus bas."""

from bases.objet.attribut import Attribut
from primaires.vehicule.vecteur import Vecteur
from .base import BaseElement

# Charge minimum pour que le combustible part
CHARGE_MIN = 2

class Canon(BaseElement):
    
    """Classe représentant un canon fixe sur un navire.
    
    Les canons sont soit :
    *   Des éléments statiques (définis ici)
    *   Des objets amovibles.
    
    """
    
    nom_type = "canon"
    
    def __init__(self, cle=""):
        """Constructeur d'un type"""
        BaseElement.__init__(self, cle)
        # Attributs propres aux canons
        self.charge_max = 1
        self._attributs = {
            "h_angle": Attribut(lambda: 0),
            "v_angle": Attribut(lambda: 0),
            "projectile": Attribut(lambda: None),
            "charge": Attribut(lambda: 0),
        }
    
    @property
    def facteur_charge(self):
        """Retourne le facteur de charge, en pourcent."""
        if self.charge_max == 0:
            return 0
        
        return self.charge / self.charge_max * 100
    
    @property
    def message_charge(self):
        """Retourne le message correspondant à la charge du canon."""
        messages = [
            (5, "Une explosion assez discrète se fait entendre."),
            (20, "Une explosion assez sonore retentit"),
            (50, "Une explosion assez forte fait frémir le navire"),
            (75, "Une violente détonation fait trembler le navire"),
            (95, "Une détonnation assourdissante fait trembler le " \
                    "bois sous vos pieds."),
        ]
        
        facteur = self.facteur_charge
        for t_facteur, message in messages:
            if facteur < t_facteur:
                return message
        
        return messages[-1][1]
    
    @property
    def vecteur(self):
        """Retourne le vecteur anticipé de la direction du projectile.
        
        On se base sur la charge et le poids du projectile pour estimer
        la distance à laquelle le projectile peut être tiré. On se base
        sur l'alignement pour estimer la direction du projectile.
        
        Sans le nuancer avec la direction du navire et sa position, ce
        vecteur ne peut pas être utilisé.
        
        """
        # D'abord, on calcule la longueur du vecteur (sa norme)
        vec_nul = Vecteur(0, 0, 0)
        if self.charge == 0:
            return vec_nul
        
        if self.projectile is None:
            return vec_nul
        
        norme = self.charge * 15 / self.projectile.poids
        
        # À présent, oriente le vecteur en fonction de l'angle du canon
        vecteur = Vecteur(1, 0, 0, self)
        vecteur = norme * vecteur
        vecteur.orienter(self.h_angle)
        return vecteur
    
    @property
    def cible(self):
        """Retourne la cible du canon.
        
        La cible est soit :
            Une salle (salle de navire ou non)
            Une côte d'une étendue
            None si rien n'est trouvé comme cible.
        
        """
        # On calcul le vecteur du boulet
        direction = self.vecteur
        
        # On le nuance avec la direction du navire
        salle = self.parent
        if salle is None:
            return None
        
        navire = parent.navire
        if navire is None:
            return None
        
        direction.tourner_autour_z(navire.direction.direction)
        direction = direction + navire.position
        
        # On récupère toutes les salles avec coordonnées
        cibles = importeur.salle._coords
        if navire.etendue:
            etendue = navire.etendue
            for o_coords, obstacle in etendue.obstacles.items():
                cibles[(o_coords + etendue.altitude)] = obstacle
        
        
    def tirer(self, navire):
        """Le projectile part."""
        if self.projectile is None:
            raise ValueError("aucun projectile")
        
        if self.charge == 0:
            raise ValueError("charge nulle")
        
        # On calcul la tension du projectile en fonction de son poids
        # et de la charge de poudre
        # Le rapport est 1 kg de poudre propulse 5 kg de projectile à XY=1
        msg = self.message_charge