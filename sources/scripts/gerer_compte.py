from tkinter import*
from commande_json_txt import charger_donnees_json, ecrire_dans_fichier_json, ecrire_fichier_txt, lire_fichier_txt

class NouvellePartie(Tk):
    """
    Fenêtre tkinter pour créer une nouvelle partie.
    """
    def __init__(self, chemin_json, dimension):
        """
        Initialise la classe NouvellePartie.

        entrée --> self : l'objet NouvellePartie.
                   chemin_json(chaîne de caractères): Chemin d'accès vers le fichier JSON où on sauvegarde les informations de la partie créé.
                   dimension(entier) : longueur de l'écran qui va nous servir à dimensionner la fençetre tkinter.
                   
        sortie --> initialisation de NouvellePartie.
        """
        super().__init__()
        
        # on définit la longueur et la largeur de la fenêtre tkinter selon la taille de l'écran de l'utilisateur et un coefficient
        longueur_fenetre = round(dimension * 300/1366)
        largeur_fenetre = round(dimension * 150/1366)
        
        self.title("Nouvelle partie")
        
        # On redimensionne la fenêtre tkinter et on la centre
        self.geometry(str(longueur_fenetre)+"x"+str(largeur_fenetre)+"+{}+{}".format(int(self.winfo_screenwidth() / 2 - longueur_fenetre/2), int(self.winfo_screenheight() / 2 - largeur_fenetre/2)))
        
        # On la met devant la fenêtre pygame
        self.wm_attributes("-topmost", True)
        
        self.chemin_json = chemin_json
        
        # Création des widgets
        self.label_nom_sauvegarde = Label(self, text="NOM SAUVEGARDE", width=int(dimension * 40/1366), font=("Helvetica", round(longueur_fenetre/25)), fg="#2C5234")
        self.label_pseudo = Label(self, text="PSEUDO", width=int(dimension * 40/1366), font=("Helvetica", round(longueur_fenetre/25)), fg="#2C5234")
        self.entree_utilisateur = Entry(self, width=int(dimension * 40/1366))
        self.entree_utilisateur_1 = Entry(self, width=int(dimension * 40/1366))
        self.bouton_enregistrer = Button(self, text="Sauvegarder", command=self.obtenir_entree, bg="#8CB369", fg="white", font=('Helvetica', round(longueur_fenetre/25)), padx=round(longueur_fenetre/30), pady=round(longueur_fenetre/60), relief='groove')
        
        # Affichage des widgets sur la fenêtre tkinter
        self.label_nom_sauvegarde.pack()
        self.entree_utilisateur.pack(pady=int(dimension * 5/1366))
        self.label_pseudo.pack(pady=int(dimension * 5/1366))
        self.entree_utilisateur_1.pack(pady=int(dimension * 5/1366))
        self.bouton_enregistrer.pack()

    def obtenir_entree(self):
        """
        Obtient les informations saisies et sauvegarde une nouvelle partie dans le fichier JSON "self.chemin_json".
        
        entrée --> L'objet NouvellePartie.
        
        sortie --> Fermeture de la fenêtre tkinter et modification du fichier JSON "self.chemin_json".
        """
        # Obtention des informations saisies dans les champs de saisie.
        nom_sauvegard = self.entree_utilisateur.get()
        pseudo = self.entree_utilisateur_1.get()
        
        # Vérifie si les champs sont remplis
        if nom_sauvegard and pseudo:
            # Fermeture de la fenêtre tkinter.
            self.destroy()
            
            # Chargement des données JSON depuis le fichier "self.chemin_json".
            donnees = charger_donnees_json(self.chemin_json)

            # Création d'un dictionnaire avec le pseudo et le niveau du joueur pour le nom de sauvegarde saisi.
            info_compte = {"name": pseudo, "level" : 1}

            # Ajout du dictionnaire créé ci-dessus dans le dictionnaire de données chargé depuis le fichier JSON.
            donnees[nom_sauvegard] = info_compte

            # Écriture des données mises à jour dans le fichier JSON situé à "self.chemin_json".
            ecrire_dans_fichier_json(self.chemin_json, donnees)
            

class ChargementCompte(Tk):
    """
    Fenêtre tkinter pour charger une partie.
    """
    def __init__(self, chemin_json, chemin_texte, dimension):
        """
        Initialise la classe ChargementCompte.

        entrée --> self : l'objet ChargementCompte.
                   chemin_json(chaîne de caractères): Chemin d'accès vers le fichier JSON où on sauvegarde les informations des différentes parties crée.
                   chemin_texte(chaîne de caractères) : Chemin d'accès vers le fichier TXT qui va nous permettre de sauvegarder le nom de la sauvegarde que l'utilisateur a choisi.
                   dimension(entier) : longueur de l'écran qui va nous servir à dimensionner la fençetre tkinter.
                   
        sortie --> initialisation de ChargementCompte.
        """
        super().__init__()
        self.chemin_json = chemin_json
        self.chemin_texte = chemin_texte
        self.title("Choix sauvegarde")
        
        # On définit la longueur et la largeur de la fenêtre tkinter selon la taille de l'écran de l'utilisateur et un coefficient
        longueur_fenetre = round(dimension * 500/1366)
        largeur_fenetre = round(dimension * 400/1366)
        
        # On redimensionne la fenêtre tkinter et on la centre
        self.geometry(str(longueur_fenetre)+"x"+str(largeur_fenetre)+"+{}+{}".format(int(self.winfo_screenwidth() / 2 - longueur_fenetre/2), int(self.winfo_screenheight() / 2 - largeur_fenetre/2)))
        
        # On la met devant la fenêtre pygame
        self.wm_attributes("-topmost", True)
        
        # Empêche l'utilisateur de fermer la fenêtre en clickant sur la croix rouge en haut à droite
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Création et configuration des différents widgets
        self.liste = Listbox(self, width=round(longueur_fenetre * 0.1), height=round(largeur_fenetre * 0.1), selectmode = BROWSE, fg='#2C5234', font=('Arial', round(longueur_fenetre/25)))
        self.barre_defilement = Scrollbar(self, command=self.liste.yview)
        self.liste.config(yscrollcommand=self.barre_defilement.set)
        self.bouton_charger = Button(self, text="Charger", command=self.sauvegarder_choix_utilisateur, bg="#8CB369", fg="white", font=('Helvetica', round(longueur_fenetre/25)), padx=round(longueur_fenetre/30), pady=round(longueur_fenetre/60), relief='groove')
        
        # Remplissage de la liste des sauvegardes
        donnees = charger_donnees_json(self.chemin_json)
        for cle in donnees.keys():
            self.liste.insert(END, cle)
        
        # Affichage des widgets sur la fenêtre tkinter
        self.bouton_charger.pack()
        self.liste.pack()
        self.barre_defilement.pack(side=RIGHT, fill=Y)

    def sauvegarder_choix_utilisateur(self):
        """
        Ecrit le nom de la sauvegarde choisie dans le fichier texte "self.chemin_texte".
        
        entrée --> l'objet ChargementCompte.
        
        sortie --> Fermeture de la fenêtre tkinter et modification du fichier TXT "self.chemin_texte"
        """
        # Récupération du numéro de la sauvegarde sélectionnée dans la liste
        numero_choix = self.liste.curselection()
        
        # Si l'utilisateur a sélectionné une sauvegarde
        if numero_choix:
            # Récupération de la valeur de la sauvegarde sélectionnée
            valeur_choix = self.liste.get(numero_choix[0])
            
            # Écriture de la valeur de la sauvegarde sélectionnée dans le fichier TXT "self.chemin_texte"
            ecrire_fichier_txt(self.chemin_texte, valeur_choix)
            
            # Fermeture de la fenêtre tkinter
            self.destroy()
