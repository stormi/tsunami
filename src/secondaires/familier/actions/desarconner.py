﻿# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant l'action desarconner."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Désarçonne un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.desarconner, "Personnage")

    @staticmethod
    def desarconner(personnage):
        """Désarçonne un personnage.

        Cette action désarçonne un personnage, c'est-à-dire le fait
        descendre de sa monture. Cette action crée une alerte si le
        personnage ne chevauche aucun familier, il est donc préférable de
        s'assurer qu'il chevauche bien une monture au préalable (voir
        l'exemple plus bas).

        Paramètres à préciser :

          * personnage : le personnage que l'on veut désarçonner

        Exemple d'utilisation :

          monture = monture(personnage)
          si monture:
            desarconner personnage
            dire personnage "Vous êtes jeté à terre !"

        """
        if "chevauche" in personnage.etats:
            personnage.etats.retirer("chevauche")
        else:
            raise ErreurExecution("le personnage {} ne chevauche aucune " \
                    "monture".format(personnage))