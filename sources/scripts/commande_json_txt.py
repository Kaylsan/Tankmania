import json

def charger_donnees_json(chemin):
    """
    Cette fonction permet de récuperer et de renvoyer les données du fichier JSON "chemin".
    
    entree --> chemin(chaine de caractères) : chemin d'accès au fichier JSON à lire.
    
    sortie --> Renvoie les données du fichier JSON "chemin".
    """
    # Spécifie le type d'encodage utilisé dans le fichier "chemin"
    with open(chemin, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)
        return donnees
    
def ecrire_dans_fichier_json(chemin, donnee):
    """
    Cette fonction permet d'écrire dans un fichier json en écrasant les infos qu'il y avait.
    
    entree --> chemin(chaine de caractères) : chemin d'accès au fichier JSON à lire.
               donnee(type contruit) : type contruit à écrire dans le fichier "chemin".
               
    sortie --> Fichier "chemin" modifié.
    """
    # w signit qu'on veut écrire dans le fichiers
    with open(chemin, 'w', encoding='utf-8') as fichier:
        json.dump(donnee, fichier)

def lire_fichier_txt(chemin):
    """
    Cette fonction permet de lire le fichier txt "chemin" et renvoie le texte du fichier txt "chemin".
    
    entree --> chemin(chaine de caractères) : chemin d'accès au fichier txt à lire.
    
    sortie --> Renvoie une chaine de caractères qui corespond au texte du fichier "chemin".
    """
    # r pour une ouverture en lecture
    with open(chemin, "r", encoding='utf-8') as fichier:
        texte = fichier.read()
        return texte
        
def ecrire_fichier_txt(chemin, texte):
    """
    Cette fonction permet d'écrire dans un fichier txt en écrasant les infos qu'il y avait.
    
    entree --> chemin(chaine de caractères) : chemin d'accès au fichier txt à modifier.
               texte(chaine de caractères) : texte à écrire dans le fichier "chemin".
               
    sortie --> Modification du fichier "chemin".
    """
    # w pour une ouverture en mode écriture, à chaque ouverture le contenu du fichier est écrasé
    with open(chemin,"w", encoding='utf-8') as fichier:
        fichier.write(texte)

def modifier_valeur_json(chemin, clé_primaire, cle_à_modifier, nouvelle_valeur):
    """
    Cette fonction permet de modifier la valeur d'une clé qui est la valeur d'une autre clé dans un fichier JSON qui est un dictionnaire.
    
    entree --> chemin(chaine de caractères) : chemin d'accès au fichier json à modifier.
               clé_primaire(chaine de caractères) : clé qui contient la clé à modifier.
               cle_à_modifier(chaine de caractères) : clé à modifier.
               nouvelle_valeur(chaine de caractères) : nouvelle valeur à assigner à la clé.
               
    sortie --> Modification du fichier "chemin".
    """
    # Récupère un dictionnaire dans le fichier "chemin"
    donnees = charger_donnees_json(chemin)
    # Modification de la valeur de la clé "cle_à_modifier" pour le nom de sauvegarde "clé_primaire" dans le dictionnaire donnees avec la valeur "nouvelle_valeur"
    donnees[clé_primaire][cle_à_modifier] = nouvelle_valeur
    ecrire_dans_fichier_json(chemin, donnees)
