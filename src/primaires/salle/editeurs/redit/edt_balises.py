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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier contient l'éditeur EdtBalises, détaillé plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_balise import EdtBalise

class EdtBalises(Editeur):
    
    """Contexte-éditeur des balises d'une salle.
    Ces balises sont observables avec la commande look ; voir ./edt_balise.py
    pour l'édition des balises une par une.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("d", self.opt_supprimer_balise)
        self.ajouter_option("a", self.opt_ajouter_synonymes)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        salle = self.objet
        msg = "| |tit|" + "Edition des balises de {}".format(salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Balises existantes :\n"
        
        # Parcours des balises
        balises = salle.balises
        liste_balises = ""
        for nom, balise in balises.iter():
            b_nom = "\n |ent|" + nom.ljust(10) + "|ff| : "
            synonymes = "(" + ", ".join(balise.synonymes) + ")"
            description = ""
            liste_balises += b_nom
            liste_balises += synonymes
            liste_balises += description
        if not liste_balises:
            liste_balises += "\n Aucune balise pour l'instant."
        msg += liste_balises
        
        return msg
    
    def opt_supprimer_balise(self, arguments):
        """Supprime la balise passée en paramètre.
        Syntaxe : /d <balise existante>
        
        """
        salle = self.objet
        balises = salle.balises
        nom = arguments
        
        if not balises.balise_existe(nom):
            self.pere << "|err|La balise spécifiée n'existe pas.|ff|"
        else:
            del balises[nom]
            self.actualiser()
    
    def opt_ajouter_synonymes(self, arguments):
        """Ajoute un ou plusieurs synonymes à la balise passée en paramètre.
        Syntaxe :
            /a <balise existante> / <synonyme 1> (/ <synonyme 2> / ...)
        
        """
        salle = self.objet
        balises = salle.balises
        a_synonymes = []
        a_synonymes = arguments.split(" / ")
        nom_balise = a_synonymes[0]
        del a_synonymes[0]
        
        if not balises.balise_existe(nom_balise):
            self.pere << \
                "|err|La balise spécifiée n'existe pas.|ff|"
            return
        if not a_synonymes:
            self.pere << \
                "|err|Vous devez préciser au moins un synonyme à ajouter.|ff|"
            return
        
        balise = balises.get_balise(nom_balise)
        for synonyme in a_synonymes:
            if synonyme in balise.synonymes or balises.balise_existe(synonyme):
                self.pere << \
                    "|err|Le synonyme '{}' est déjà utilisé.|ff|".format(synonyme)
                return
            balise.synonymes.append(synonyme)
        self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        salle = self.objet
        balises = salle.balises
        
        balise = balises.get_balise(msg)
        if balise is None:
            balise = balises.ajouter_balise(msg)
        enveloppe = EnveloppeObjet(EdtBalise, balise, "description")
        enveloppe.parent = self
        enveloppe.aide_courte = \
            "Entrez |ent|/|ff| pour revenir à la fenêtre parente.\n"
        contexte = enveloppe.construire(self.pere)
        
        self.migrer_contexte(contexte)
