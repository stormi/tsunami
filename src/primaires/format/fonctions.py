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


"""Ce fichier définit plusieurs fonctions propres au formatage des messages
à envoyer.

Fonctions à appliquer à la réception d'un message :
-   echapper_sp_cars : échapper les caractères spéciaux utilisés pour les codes
    couleurs ou les codes de formatage

Fonctions à appliquer à l'émission d'un message :
-   convertir_nl : convertir les sauts de ligne '\n' dans un format
    universellement interprété
-   ajouter_couleurs : ajoute les couleurs en fonction des codes de
    formatage
-   replacer_sp_cars : reconvertir les caractères d'échappement

"""

# Constantes de formatage
sp_cars_a_echapper = { # Caractères à échapper
    "|": "_b_",
}

sp_cars_a_remplacer = {} # Dictionnaire miroir de sp_cars_a_echapper
for cle, val in sp_cars_a_echapper.items():
    sp_cars_a_remplacer[val] = cle

NL = b"\r\n"

ACCENTS = {
    # accent:lettre non accentuée
    # Lettres majuscules
    "É": "E",
    "À":"A",
    "È":"E",
    "Ù":"U",
    "Â":"A",
    "Ê":"E",
    "Î":"I",
    "Ô":"O",
    "Û":"U",
    "Ä":"A",
    "Ë":"E",
    "Ï":"I",
    "Ç":"C",
    
    # Lettres minuscules
    "é":"e",
    "à":"a",
    "è":"e",
    "ù":"u",
    "â":"a",
    "ê":"e",
    "î":"i",
    "ô":"o",
    "û":"u",
    "ä":"a",
    "ë":"e",
    "ï":"i",
    "ç":"c",
}

# Couleurs
COULEURS = {
    # balise: code ANSI
    b"|nr|": b"\x1b[0;30m",  # noir
    b"|rg|": b"\x1b[0;31m",  # rouge
    b"|vr|": b"\x1b[0;32m",  # vert
    b"|mr|": b"\x1b[0;33m",  # marron
    b"|bl|": b"\x1b[0;34m",  # bleu
    b"|mg|": b"\x1b[0;35m",  # magenta
    b"|cy|": b"\x1b[0;36m",  # cyan
    b"|gr|": b"\x1b[0;37m",  # gris
    b"|grf|": b"\x1b[1;30m", # gris foncé
    b"|rgc|": b"\x1b[1;31m", # rouge clair
    b"|vrc|": b"\x1b[1;32m", # vert clair
    b"|jn|": b"\x1b[1;33m",  # jaune
    b"|blc|": b"\x1b[1;34m", # bleu clair
    b"|mgc|": b"\x1b[1;35m", # magenta clair
    b"|cyc|": b"\x1b[1;36m", # cyan clair
    b"|bc|": b"\x1b[1;37m",  # blanc
    
    b"|ff|": b"\x1b[0m",  # fin de formattage
}

def get_bytes(msg, ncod_optionnel):
    """Retourne un type bytes.
    Peut prendre en paramètre :
    -   un type bytes (on le retourne sans rien changer)
    -   un type str (on l'encode avec l'encodage optionnel)
    
    """
    if type(msg) is str:
        msg = msg.encode(ncod_optionnel)
    return msg

# Fonctions à appliquer à la réception de messages

def echapper_sp_cars(msg):
    """Fonction appelée pour échapper les caractères spéciaux d'une
    chaîne.
    
    Elle doit être appliquée sur les messages réceptionnés, mais pas sur tous.
    Certains messages réceptionnés depuis des personnages immortels doivent
    avoir la possibilité d'ajouter ces codes de formattage.
    
    Pour connaître les caractères à échapper, on se base sur le dictionnaire
    sp_cars_a_echapper.
    
    """
    for car, a_repl in sp_cars_a_echapper.items():
        msg = msg.replace(car, a_repl)
    return msg

def convertir_nl(msg):
    """Cette fonction est appelée pour convertir les sauts de ligne '\n'
    en sauts de ligne compris par tous les clients (y compris telnet).
    
    """
    msg = msg.replace(b"\n", NL)
    return msg

def ajouter_couleurs(msg, config):
    """Cette fonction est appelée pour convertir les codes de formatage
    couleur en leur équivalent ANSI. Elle gère aussi le formatage des
    raccourcis de mise en forme (voir config.py). Le deuxième argument est
    le dictionnaire de ces raccourcis.
    On se base sur la constante dictionnaire 'COULEURS'.
    
    """
    # Création du dictionnaire des options
    FORMAT = {
        b"|tit|": config.couleur_titre.encode(),
        b"|cmd|": config.couleur_cmd.encode(),
        b"|ent|": config.couleur_entree.encode(),
        b"|att|": config.couleur_attention.encode(),
        b"|err|": config.couleur_erreur.encode()
    }
    
    # On transforme les raccourcis de mise en forme, puis on colorise en ANSI
    for balise, couleur in FORMAT.items():
        msg = msg.replace(balise, couleur)
    
    for balise, code_ansi in COULEURS.items():
        msg = msg.replace(balise, code_ansi)
    
    return msg

def remplacer_sp_cars(msg):
    """On remplace les caractères d'échappement d'un message, ceux échappés
    par la méthode 'echapper_sp_cars' à la réception du message.
    
    On se base sur le dictionnaire miroir 'sp_cars_a_remplacer'.
    
    """
    for code_car, a_repl in sp_cars_a_remplacer.items():
        msg = msg.replace(code_car.encode(), a_repl.encode())
    
    return msg

def supprimer_accents(msg):
    """Cette fonction permet, avant émission du message, de retirer
    les accents. On se base pour ce faire sur ACCENTS.
    ATTENTION : cette fonction doit accepter 'str' et 'bytes'.
    
    """
    for acc, non_acc in ACCENTS.items():
        if type(msg) == bytes:
            acc, non_acc = acc.encode(), non_acc.encode()
        msg = msg.replace(acc, non_acc)
    
    return msg

def souligner_sauts_de_ligne(msg):
    """Cette fonciton souligne les sauts de ligne pour les utilisateurs de
    lecteurs d'écran.
    
    Quand on utilise Jaws avec par exemple MushClient, les lignes complètement
    vides sont ignorées. C'est pratique la plupart du temps, mais il peut
    être bien de voir les lignes vides également. Pour cela, on se contente
    de rendre la ligne non vide, en y insérant un simple espace.
    
    """
    while "\n\n" in msg:
        msg = msg.replace("\n\n", "\n \n")
    
    return msg