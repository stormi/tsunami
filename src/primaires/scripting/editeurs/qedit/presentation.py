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


"""Fichier contenant la classe EdtPresentation, détaillée plus bas.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_etape import EdtEtape
from .edt_ordonnee import EdtOrdonnee

class EdtPresentation(Presentation):
    
    """Classe définissant l'éditeur d'une quête.
    
    """
    
    def __init__(self, personnage, quete, attribut=""):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, quete)
        self.personnage = personnage
        
        # Options
        self.ajouter_option("e", self.ajouter_etape)
        self.ajouter_option("d", self.supprimer_etape)
        self.ajouter_option("q", self.ajouter_sous_quete)
        self.ajouter_option("d", self.opt_supprimer_etape)
        
        if personnage and quete:
            self.construire(quete)
    
    def __getnewargs__(self):
        return (None, None)
    
    def supprimer_etape(self, argument):
        """Supprimer une étape ou une quête.
        
        L'argument doit contenir le numéro de l'étape/quête.
        
        """
        try:
            num = int(argument.strip())
        except ValueError:
            self.pere << "|err|Précisez le numéro de l'étape ou de la " \
                "sous-quête.|ff|"
        else:
            self.objet.supprimer_etape(num)
            self.actualiser()
    
    def ajouter_etape(self, argument):
        """Ajoute une étape.
        
        L'argument doit contenir le titre de l'étape.
        
        """
        if not argument.strip():
            self.pere << "|err|Précisez un titre pour cette étape.|ff|"
        else:
            self.objet.ajouter_etape(argument.strip())
            self.actualiser()
    
    def ajouter_sous_quete(self, argument):
        """Ajoute une sous-quête.
        
        L'argument doit contenir le titre de la sous-quête.
        
        """
        if not argument.strip():
            self.pere << "|err|Précisez un titre pour cette sous-quête.|ff|"
        else:
            self.objet.ajouter_sous_quete(argument.strip())
            self.actualiser()
    
    def opt_supprimer_etape(self, arguments):
        """Supprime une étape.
        
        Syntaxe : /d <niveau>
        
        """
        try:
            etape = self.objet.etapes[arguments]
        except KeyError:
            self.pere << "|err|Etape inconnue.|ff|"
        else:
            parent = etape.parent
            parent.supprimer_etape(etape.str_niveau)
            self.actualiser()
    
    def accueil(self):
        """Message d'accueil de l'éditeur."""
        quete = self.objet
        msg = Presentation.accueil(self)
        quitter = msg.split("\n")[-1]
        intro = "| |tit|"
        intro += "Edition de la quête {}".format(str(quete)).ljust(76)
        intro += "|ff||\n" + self.opts.separateur + "\n"
        intro += "Entrez |cmd|/|ff| pour revenir à la fenêtre précédente.\n" \
                "Options :\n" \
                " - |cmd|/e <titre de l'étape>|ff| : ajoute une étape " \
                "simple à la quête\n" \
                " - |cmd|/d <niveau de l'étape>|ff| : supprime l'étape\n" \
                " - |cmd|/q <titre de la sous-quête>|ff| : ajoute une " \
                "sous-quête (qui pourra elle-même\n" \
                "   contenir sous-quêtes et étapes simples)\n" \
                "Pour éditer une étape ou une sous-quête, entrez simplement " \
                "son niveau.\n"
        msg = intro + "\n".join(msg.split("\n")[2:-1]) + "\n\n"
        msg += " |tit|Etapes de la quête :|ff|\n"
        etapes = quete.afficher_etapes(quete)
        if not etapes:
            etapes = "   |att|Aucune pour le moment|ff|"
        
        msg += etapes
        
        msg += "\n\n" + quitter
        return msg
    
    def construire(self, quete):
        """Construction de l'éditeur"""
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, quete, "titre")
        titre.parent = self
        titre.prompt = "Titre de la quête : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| de la quête ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nTitre actuel : |bc|{objet.titre}|ff|"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                quete)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description de la quête {}".format(quete.cle).ljust(
            76) + "|ff||\n" + self.opts.separateur
        
        # Ordonnee
        ordonnee = self.ajouter_choix("ordonnée", "o", EdtOrdonnee, quete)
        ordonnee.parent = self
        ordonnee.apercu = "{objet.aff_ordonnee}"
    
    def autre_interpretation(self, msg):
        """On peut aussi interpréter des niveaux d'étapes."""
        try:
            etape = self.objet.etapes[msg]
        except KeyError:
            self.pere << "|err|L'étape {} n'existe pas.|ff|".format(msg)
        else:
            if etape.type == "etape":
                enveloppe = EnveloppeObjet(EdtEtape, etape)
            elif etape.type == "quete":
                enveloppe = EnveloppeObjet(EdtPresentation, etape)
            else:
                raise TypeError("type d'étape inconnu {}".format(type(etape)))
            
            enveloppe.parent = self
            contexte = enveloppe.construire(self.personnage)
            
            self.migrer_contexte(contexte)
