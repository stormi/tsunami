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


"""Fichier contenant la classe Navire, détaillée plus bas."""

from abstraits.id import ObjetID
from primaires.vehicule.vehicule import Vehicule
from .element import Element
from .salle import SalleNavire

class Navire(Vehicule):
    
    """Classe représentant un navire ou une embarcation.
    
    Un navire est un véhicule se déplaçant sur une éttendue d'eau,
    propulsé par ses voiles ou des rameurs.
    
    Le navire est un véhicule se déplaçant sur un repère en 2D.
    
    Chaque navire possède un modèle (qui détermine ses salles, leurs
    descriptions, la position des éléments, leur qualité, l'aérodynamisme
    du navire...). Chaque navire est lié à son modèle en se créant.
    
    """
    
    groupe = "navire"
    sous_rep = "navires/navires"
    def __init__(self, modele):
        """Constructeur du navire."""
        Vehicule.__init__(self)
        self.etendue = None
        self.elements = []
        if modele:
            self.modele = modele
            modele.vehicules.append(self)
            self.cle = "{}_{}".format(modele.cle, len(modele.vehicules))
            # On recopie les salles
            for r_coords, salle in modele.salles.items():
                n_salle = SalleNavire(self.cle,
                        salle.mnemonic, salle.r_x, salle.r_y, salle.r_z,
                        modele, self)
                n_salle.titre = salle.titre
                n_salle.description = salle.description
                
                # On recopie les éléments
                for t_elt in salle.elements:
                    n_salle.elements.append(Element(t_elt))
                
                self.salles[r_coords] = n_salle
                type(self).importeur.salle.ajouter_salle(n_salle)
            
            # On recopie les sorties
            for salle in modele.salles.values():
                n_salle = self.salles[salle.r_coords]
                for dir, sortie in salle.sorties._sorties.items():
                    if sortie and sortie.salle_dest:
                        c_salle = self.salles[sortie.salle_dest.r_coords]
                        print(dir, n_salle, c_salle)
                        n_salle.sorties.ajouter_sortie(dir, sortie.nom,
                                sortie.article, c_salle,
                                sortie.correspondante)
    
    def __getnewargs__(self):
        return (None, )
    
    def detruire(self):
        """Destruction du navire."""
        Vehicule.detruire(self)
        self.modele.vehicules.remove(self)


ObjetID.ajouter_groupe(Navire)