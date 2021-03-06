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


"""Fichier contenant la classe Chemins, détaillée plus bas."""

from math import sin, atan, radians, sqrt

from vector import Vector, mag


from abstraits.obase import BaseObj
from primaires.vehicule.vecteur import Vecteur
from .chemin import Chemin

class Chemins(BaseObj):

    """Classe représentant une liste de chemins."""

    def __init__(self):
        """Constructeur des chemins."""
        self.chemins = []
        self._construire()

    def __repr__(self):
        """Affichage des chemins."""
        chemins = [str(c) for c in self.chemins]
        return "<chemins [" + ", ".join(chemins) + "]>"

    def __iter__(self):
        return iter(self.chemins)

    def get(self, salle):
        """Retourne si trouvé le chemin dont la destination est salle.

        Si non trouvé retourne None.

        """
        for chemin in self.chemins:
            if chemin.destination is salle:
                return chemin

        return None

    @classmethod
    def salles_autour(cls, salle, rayon=15, absolu=False, empruntable=True):
        """Retourne les chemins autour de salle dans un rayon donné."""
        o_chemins = cls()
        salles = {} # {salle: chemin}
        o_salle = salle

        # Fonction explorant une salle et retournant ses sorties récursivement
        def get_sorties_rec(salle, rayon=0, max=15, salles=None, \
                empruntable=True):
            salles = salles or {}
            chemin = salles.get(salle)
            if chemin:
                sorties = list(chemin.sorties)
            else:
                sorties = []
            for sortie in salle.sorties:
                if empruntable and not sortie.empruntable:
                    continue

                t_salle = sortie.salle_dest
                n_chemin = Chemin()
                n_chemin.sorties.extend(sorties + [sortie])
                a_chemin = salles.get(t_salle)
                if a_chemin:
                    if a_chemin.longueur > n_chemin.longueur:
                        salles[t_salle] = n_chemin
                else:
                    salles[t_salle] = n_chemin

            if rayon < max - 1:
                for sortie in salle.sorties:
                    if empruntable and not sortie.empruntable:
                        continue

                    t_salle = sortie.salle_dest
                    get_sorties_rec(t_salle, rayon + 1, max, salles, \
                            empruntable=empruntable)

            return salles

        sorties = get_sorties_rec(salle, max=rayon, empruntable=empruntable)
        for salle, chemin in sorties.items():
            # Constitution du chemin
            if chemin.origine is not chemin.destination:
                salles[salle] = chemin

        o_chemins.chemins.extend(list(salles.values()))

        # Si la salle d'origine a des coordonnées valides
        if not absolu and salle.coords.valide:
            o_x, o_y, o_z = salle.coords.tuple()
            for coords, d_salle in importeur.salle._coords.items():
                if d_salle is o_salle or d_salle in salles.keys():
                    continue

                x, y, z = coords
                if sqrt((x - o_x) ** 2 + (y - o_y) ** 2 + (z - o_z) ** 2) <= \
                        rayon:
                    chemin = Chemin()
                    d_chemin = salle.trouver_chemin_absolu(d_salle, 2)
                    if d_chemin is None:
                        vecteur = Vecteur(*d_salle.coords.tuple()) - \
                                Vecteur(*salle.coords.tuple())
                        sortie = salle.get_sortie(vecteur, d_salle)
                        chemin.sorties.append(sortie)
                    else:
                        chemin.sorties.extend(d_chemin.sorties)

                    if empruntable and not chemin.empruntable:
                        continue

                    o_chemins.chemins.append(chemin)

        return o_chemins

    @classmethod
    def get_salles_entre(cls, origine, destination, d3=True, sensibilite=0.5):
        """Retourne une liste [1] de salles entre origine et destination.

        Les paramètres origine et destination doivent être des salles.
        Sont retournées toutes les salles situées approximativement sur une
        ligne droite entre ces deux salles, à la sensibilité près [2].

        Par exemple, si origine est (0, 2, 0) et destination est (2, 2, 0),
        les salles retournées seront origine et destination, et potentiellement
        une salle (0, 1, 0) si elle existe.

        Le paramètre d3 (3D) (à True par défaut) permet de tenir compte
        de l'information Z d'une coordonnée (l'altitude de la salle).
        Si ce paramètre est à False, on ne tient pas compte de l'altitude et
        la trajectoire retournée est en deux dimensions.

        [1] La liste est triée en fonction de la distance à l'origine ;
            ainsi, on retourne réellement une trajectoire de l'origine
            vers la destination.

        [2] La sensibilité ne prendra pas en compte les salles situées
            en-dehors d'un pavé délimité par origine et destination.

        """
        if origine is destination:
            return [origine]

        o_vec = Vector(*origine.coords.tuple())
        d_vec = Vector(*destination.coords.tuple())
        o_coords = origine.coords.tuple()
        d_coords = destination.coords.tuple()
        if not d3:
            o_coords = o_coords[:1] + (0, )
            d_coords = d_coords[:1] + (0, )

        # On récupère les salles dans un rectangle autour d'origine et
        # destination, sans parcourir toutes les salles de l'univers
        salles = []
        o_x, o_y, o_z = o_coords
        d_x, d_y, d_z = d_coords
        for coords, salle in importeur.salle._coords.items():
            x, y, z = coords
            if x <= max(o_x, d_x) and x >= min(o_x, d_x) \
                and y <= max(o_y, d_y) and y >= min(o_y, d_y) \
                and z <= max(o_z, d_z) and z >= min(o_z, d_z):
                salles.append(salle)

        # On parcourt les salles
        trajectoire = []
        for salle in salles:
            p_vec = Vector(*salle.coords.tuple())
            d = o_vec.distance(d_vec, p_vec)
            if d <= sensibilite:
                trajectoire.append(salle)

        # Fonction retournant la distance de la salle à l'origine
        def distance(salle):
            x, y, z = salle.coords.tuple()
            return mag(x, y, z, o_x, o_y, o_z)

        trajectoire = sorted(trajectoire, key=distance)
        return trajectoire
