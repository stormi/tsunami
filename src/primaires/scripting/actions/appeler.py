# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant l'action appeler."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Appelle un bloc d'instructions.

    Cette action est un peu particulière en ce qu'elle appelle un bloc
    d'instructions définis. De ce fait, elle peut prendre un nombre variable
    de paramètres.

    """

    verifier = False
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.appeler)

    @staticmethod
    def appeler(appelant, nom, *parametres):
        """Appelle un bloc d'instruction.

        Cette action prend au moins deux paramètres :

          * Le script contenant le bloc. Si le bloc est défini dans le script
            d'une salle précis, passez en premier paramètre cette salle.
          * Le nom du bloc à appeler.

        Les autres paramètres dépendent du bloc : celui-ci peut avoir aucun,
        un ou plusieurs paramètres. Vous devez les appeler dans l'ordre dans
        cette action.

        Exemple d'utilisation :

          # si salle contient une salle, pour appeler son bloc 'transmettre'
          appeler salle "transmettre"
          # ou avec ds paramètres
          appeler salle "transmettre" "une chaîne" 5

        Notez qu'à la place de l'appelant (premier paramètre),
        vous pouvez préciser un nom (chaîne) identifiant le scriptable.
        Par exemple, "zone picte" ou "salle picte:8". Ces noms doivent
        être sous la forme d'une chaîne, constituée de deux éléments
        séparés par un espace : le nom du type de scriptable (comme
        salle, prototype d'objet...) et l'identifiant du scriptable
        (comme "prototype d'objet pomme_rouge").

        Exeple d'utilisation :

          appeler "salle depart:5" "transmettre"

        """
        scriptables = importeur.scripting.valeurs

        if isinstance(appelant, str):
            appelant = supprimer_accents(appelant).lower()
            trouve = False
            for t_nom, dictionnaire in scriptables.items():
                if appelant.startswith(t_nom):
                    cle = appelant[len(t_nom) + 1:].lower()
                    if cle not in dictionnaire:
                        raise ErreurExecution("Impossible de trouver " \
                                "le scriptable {} : clé {} " \
                                "introuvable".format(repr(appelant), repr(cle)))

                    trouve = True
                    appelant = dictionnaire[cle]
                    break

            if not trouve:
                raise ErreurExecution("Impossible de trouver le scriptable " \
                        "{} : type d'information introuvable".format(
                        repr(appelant)))
        elif not hasattr(appelant, "script"):
            raise ErreurExecution("l'appelant {} ne semble pas avoir " \
                    "de script".format(appelant))


        script = appelant.script
        try:
            bloc = script.blocs[nom]
        except KeyError:
            raise ErreurExecution("le bloc {} ne peut être trouvé dans " \
                    "l'appelant {}".format(repr(nom), appelant))

        bloc.executer(*parametres)
