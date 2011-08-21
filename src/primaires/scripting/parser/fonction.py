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


"""Fichier contenant la classe Fonction, détaillée plus bas."""

from .expression import Expression
from . import expressions
from .variable import RE_VARIABLE

class Fonction(Expression):
    
    """Expression fonction."""
    
    nom = "fonction"
    def __init__(self):
        """Constructeur de l'expression."""
        self.nom = None
        self.arguments = ()
    
    @classmethod
    def parsable(cls, chaine):
        """Retourne True si la chaîne est parsable, False sinon."""
        fin_nom = chaine.find("(")
        nom = chaine[:fin_nom]
        chaine = chaine[:fin_nom + 1]
        return fin_nom >= 0  and RE_VARIABLE.search(nom)
    
    @classmethod
    def parser(cls, fonction):
        """Parse la chaîne.
        
        Retourne l'objet créé et la partie non interprétée de la chaîne.
        
        """
        objet = cls()
        fin_nom = fonction.find("(")
        nom = fonction[:fin_nom]
        chaine = fonction[fin_nom + 1:]
        objet.nom = nom
        
        # Parsage des arguments
        types = ("variable", "nombre", "chaine")
        types = tuple([expressions[nom] for nom in types])
        arguments = []
        while True:
            chaine = chaine.lstrip(" ")
            if chaine.startswith(")"):
                chaine = chaine[1:]
                break
            
            types_app = [type for type in types if type.parsable(chaine)]
            if not types_app:
                raise ValueError("impossible de parser {}".format(fonction))
            elif len(types_app) > 1:
                raise ValueError("la fonction {] peut être différemment interprétée".format(fonction))
            
            type = types_app[0]
            arg, chaine = type.parser(chaine)
            
            chaine.lstrip(" ")
            if chaine.startswith(", "):
                chaine = chaine[1]
            elif chaine.startswith(")"):
                chaine = chaine[1:]
                break
            else:
                raise ValueError("erreur de syntaxe dans la fonction " \
                        "{}".format(fonction))
        
        objet.arguments = tuple(arguments)
        
        return objet, chaine
    
    def __repr__(self):
        return self.nom + str(self.arguments)
