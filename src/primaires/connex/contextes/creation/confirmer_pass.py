﻿# -*-coding:Utf-8 -*

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

from primaires.interpreteur.contexte import Contexte

class ConfirmerPass(Contexte):
    """Contexte de changement d'encodage.
    On affiche au client plusieurs possibilités d'encodage.
    Il est censé afficher celui qu'il voit correctement.
    On part du principe que l'encodage de sortie est le même que l'encodage
    d'entrée. Ainsi, une fois que le client a choisi son encodage, on le
    répercute sur l'encodage du client.
    
    """
    def __init__(self):
        """Constructeur du contexte"""
        Contexte.__init__(self, "connex:creation:confirmer_pass")
        self.opts.rci_ctx_prec = "connex:creation:choisir_pass"
    
    def get_prompt(self, emt):
        """Message de prompt"""
        # Comme l'option ncod est activée, le préfixe est affiché en dur
        return "Confirmez le mot de passe : "
    
    def accueil(self, emt):
        """Message d'accueil"""
        return \
            "\n|tit|---------= Confirmation =-----------|ff|\n" \
            "Entrez une nouvelle fois votre mot de passe pour éviter une " \
            "faute de frappe."
    
    def deconnecter(self, emt):
        """En cas de décnonexion du joueur, on supprime son compte"""
        type(self).importeur.connex.supprimer_compte(emt.emetteur)
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand un message est réceptionné"""
        config_connex = type(self).importeur.anaconf.get_config("connex")
        type_chiffrement = config_connex.type_chiffrement
        clef_salage = config_connex.clef_salage
        if emt.emetteur.mot_de_passe == emt.emetteur.hash_mot_de_pass(clef_salage,type_chiffrement,msg):
            self.migrer_contexte(emt, "connex:creation:entrer_email")
        else:
            self.envoyer(emt, "Votre confirmation est invalide ! Si cette " \
                            "erreur persiste, vous vous\n" \
                            "êtes peut-être trompé en indiquant votre mot de " \
                            "passe à l'étape précédente. Dans ce\n" \
                            "cas, entrez |grf|/|ff| pour retourner en arrière.")
