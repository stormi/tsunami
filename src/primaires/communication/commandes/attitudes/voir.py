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


"""Fichier contenant le paramètre 'voir' de la commande 'attitudes'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.communication.attitude import *

class PrmVoir(Parametre):
    
    """Commande 'attitudes voir'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<attitude>"
        self.aide_courte = "offre un aperçu d'une attitude"
        self.aide_longue = \
            "Cette sous-commande donne un aperçu d'une attitude, visible par " \
            "vous uniquement."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        attitude = dic_masques["attitude"].attitude
        res = "Statut de l'attitude : " + STATUTS[attitude.statut] + "\n"
        if attitude.statut == FONCTIONNELLE or attitude.statut == SANS_CIBLE:
            res += attitude.independant["aim"]
        elif attitude.statut == CIBLE_OBLIGATOIRE:
            res += attitude.dependant["adm"].replace("_b_cible_b_",
                    "quelqu'un").replace("_b_de_b_", "de ")
        else:
            res += "|err|Cette attitude n'est pas disponible.|ff|"
        personnage << res
