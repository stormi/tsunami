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


"""Fichier contenant le masque <nombre>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class Nombre(Masque):
    
    """Masque <nombre>.
    On attend un nombre en paramètre.
    
    """
    
    nom = "nombre"
    nom_complet = "nombre"
    
    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.proprietes["limite_inf"] = "1"
        self.proprietes["limite_sup"] = "None"
    
    def init(self):
        """Initialisation des attributs"""
        self.nombre = None
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        str_nombre = liste_vers_chaine(commande).lstrip()
        str_nombre = str_nombre.split(" ")[0]
        
        if not str_nombre:
            raise ErreurValidation(
                "Précisez un nombre.", False)
        
        self.a_interpreter = str_nombre
        if str_nombre.startswith("-"):
            str_nombre = str_nombre[1:]
        if not str_nombre.isdigit():
            raise ErreurValidation(
                "|err|Ceci n'est pas un nombre.|ff|", False)
        
        commande[:] = commande[len(str_nombre):]
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        str_nombre = self.a_interpreter
        
        try:
            nombre = int(str_nombre)
            if self.limite_inf is not None:
                assert nombre >= self.limite_inf
            if self.limite_sup is not None:
                assert nombre <= self.limite_sup
        except (ValueError, AssertionError):
            raise ErreurValidation( \
                "|err|Ce nombre est invalide.|ff|")
        
        self.nombre = nombre
        
        return True
