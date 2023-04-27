import tkinter as tk
from pygame import mixer
from commande_json_txt import ecrire_fichier_txt

# Initialiser mixer
mixer.init()

class Parametre(tk.Frame):
    """
    Cette classe permet de créer une fenêtre tkinter où l'utilisateur pourra choisir dans quelle partie des paramètres il veut aller
    soit dans les paramètre en rapport avec la musique ou soit les paramètre en rapport avec la création du deuxième joueur.
    De plus, il y a un bouton quitter pour fermer la fenetre.
    """
    def __init__(self, igu, longueur_fenetre, largeur_fenetre):
        """
        Initialise la classe Parametre.

        entrée --> self : l'objet Parametre.
                   igu (tk.Tk): L'objet Tk sur lequel la fenêtre doit être créée.
                   longueur_fenetre(int) : longueur des futur fenetre qui onta être crée.
                   largeur_fenetre(int) : largeur des futur fenetre qui vont être crée.
                   
        sortie --> initialisation de Parametre.
        """
        # Appel à la méthode __init__() de la classe parent (tk.Frame) pour initialiser les attributs de l'objet.
        super().__init__(igu)
        self.igu = igu
        self.pack(fill="both", expand=True)
        self.creation_widgets()
        self.longueur_fenetre = longueur_fenetre
        self.largeur_fenetre = largeur_fenetre

    def creation_widgets(self):
        """
        Permet de créer les différents widgets présent sur la fenêtre Parametre.

        entrée --> self : l'objet Parametre.
                   
        sortie --> création des widgets suivants : un label "PARAMETRE", un bouton "MUSIQUE", un bouton "2 JOUEURS" et un bouton "QUITTER".
        """
        # Créer un label "PARAMETRE"
        self.label = tk.Label(self, text="PARAMETRE", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.03)), fg="#2C5234")
        self.label.pack(side="top", pady=int(self.igu.winfo_screenheight() * 0.03))

        # Créer un bouton "MUSIQUE"
        self.bouton_musique = tk.Button(self, text="MUSIQUE", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.parametre_musique)
        self.bouton_musique.pack(pady=int(self.igu.winfo_screenheight() * 0.02))

        # Créer un bouton "2 JOUEURS"
        self.bouton_2_joueurs = tk.Button(self, text="2 JOUEURS", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.parametre_joueur_2)
        self.bouton_2_joueurs.pack(pady=int(self.igu.winfo_screenheight() * 0.02))

        # Créer un bouton "QUITTER"
        self.bouton_quitter = tk.Button(self, text="QUITTER", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.igu.destroy)
        self.bouton_quitter.pack(side="bottom", pady=int(self.igu.winfo_screenheight() * 0.03))

    def parametre_musique(self):
        """
        Ouvre une fenêtre pour paramétrer la musique.

        entrée --> self : l'objet Parametre.
                   
        sortie --> Instanciation de la classe ParametreMusique avec la fenêtre principale comme parent.
        """
        # Créer une instance de la classe ParametreMusique
        ParametreMusique(self.igu, self.longueur_fenetre, self.largeur_fenetre)

    def parametre_joueur_2(self):
        """
        Crée une instance de la classe Parametre2Joueurs et l'affiche sur la fenêtre Parametre.

        entrée --> self : l'objet Parametre.

        sortie --> Instanciation de la classe Parametre2Joueurs avec la fenêtre Parametre comme parent.
        """
        # Créer une instance de la classe Parametre2Joueurs
        ParametreJoueur2(self.igu, self.longueur_fenetre, self.largeur_fenetre)

class ParametreMusique(tk.Toplevel):
    """
    Cette classe permet de créer une fenêtre tkinter où l'utilisateur pourra choisir la musique qu'il veut,
    stopper la musique en cours ou régler le volume de la musique en cours.
    De plus, il y a un bouton retour pour fermer la fenetre.
    """
    def __init__(self, igu, longueur_fenetre, largeur_fenetre):
        """
        Initialise la classe ParametreMusique.

        entrée --> self : l'objet ParametreMusique.
                   igu (tk.Tk) : L'objet Tk sur lequel la fenêtre doit être créée.
                   longueur_fenetre(int) : longueur de la fenetre qui va être crée.
                   largeur_fenetre(int) : largeur de la fenetre qui va être crée.
                   
        sortie --> initialisation de ParametreMusique.
        """
        # L'appel à super().__init__(igu) permet de passer l'objet Tk parent en tant que paramètre à la méthode __init__() de la superclasse Toplevel
        super().__init__(igu)
        self.igu = igu
        self.title("Paramètres de la musique")
        self.geometry(str(longueur_fenetre)+"x"+str(largeur_fenetre)+"+{}+{}".format(int(self.igu.winfo_screenwidth() / 2 - longueur_fenetre/2), int(self.igu.winfo_screenheight() / 2 - largeur_fenetre/2)))
        # Mettre la fenetre tkinter devant la fenetre pygame
        self.wm_attributes("-topmost", True)
        self.creation_widgets()

    def creation_widgets(self):
        """
        Permet de créer les différents widgets présent sur la fenêtre ParametreMusique.

        entrée --> self : l'objet ParametreMusique.
                   
        sortie --> création des widgets suivants : un label "PARAMETRE MUSIQUE", un bouton "RETOUR", un bouton "MUSIQUE CALME", un bouton "MUSIQUE EPIC", un bouton "MUSIQUE STOP" et un widget scale pour gérer le volume.
        """
        # Créer un label "PARAMETRE MUSIQUE"
        self.label = tk.Label(self, text="PARAMETRE MUSIQUE", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.03)), fg="#2C5234")
        self.label.pack(side="top", pady=int(self.igu.winfo_screenheight() * 0.03))

        # Créer un bouton "RETOUR"
        self.bouton_retour = tk.Button(self, text="RETOUR", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.destroy)
        self.bouton_retour.pack(side="bottom", pady=int(self.igu.winfo_screenheight() * 0.005))

        # Créer un bouton "MUSIQUE CALME"
        self.bouton_musique_calme = tk.Button(self, text="MUSIQUE CALME", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.jouer_musique_calme)
        self.bouton_musique_calme.pack(pady=int(self.igu.winfo_screenheight() * 0.02))

        # Créer un bouton "MUSIQUE EPIC"
        self.bouton_musique_epic = tk.Button(self, text="MUSIQUE EPIC", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.jouer_musique_epic)
        self.bouton_musique_epic.pack(pady=int(self.igu.winfo_screenheight() * 0.02))
        
        # Créer un bouton "MUSIQUE STOP"
        self.bouton_musique_stop = tk.Button(self, text="MUSIQUE STOP", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.musique_stop)
        self.bouton_musique_stop.pack(pady=int(self.igu.winfo_screenheight() * 0.02))

        # Créer un widget scale pour changer le volume sonore de la musique en cours
        self.volume_scale = tk.Scale(self, from_=0, to=100, orient="horizontal", length=200, command=self.set_volume)
        self.volume_scale.pack(pady=int(self.igu.winfo_screenheight() * 0.002))
        self.volume_scale.set(50) # Initialiser le volume à 50%

    def jouer_musique_calme(self):
        """
        Joue une musique d'ambiance calme en boucle.

        entrée --> self : l'objet ParametreMusique.
        
        sortie --> Musique "musique_poser.mp3" est jouée en boucle.
        """
        mixer.music.load("../musique/musique_poser.mp3")
        mixer.music.play(-1, 0.0)

    def jouer_musique_epic(self):
        """
        Joue une musique d'ambiance epic en boucle.

        entrée --> self : l'objet ParametreMusique.
        
        sortie --> Musique "musique_epic.mp3" est jouée en boucle.
        """
        mixer.music.load("../musique/musique_epic.mp3")
        mixer.music.play(-1, 0.0)

    def set_volume(self, volume):
        """
        Modifie le volume de la musique en cours en fonction de la valeur passée en paramètre.

        entrée --> self : l'objet ParametreMusique.
                   volume (str) : la valeur de la widget scale représentant le volume (entre 0 et 100).

        sortie --> Modification du volume de la musique qui est en cours.
        """
        # Convertir la valeur de la widget scale de chaîne de caractères en nombre décimal
        volume_decimal = float(volume) / 100
        # Définir le volume de la musique en cours
        mixer.music.set_volume(volume_decimal)
        
    def musique_stop(self):
        """
        Permet de stopper la musique en cours.

        entrée --> self : l'objet ParametreMusique.
        
        sortie --> Si une musique est en cours, elle est stopper
        """
        mixer.music.stop()
        
class ParametreJoueur2(tk.Toplevel):
    """
    Cette classe permet de créer une fenêtre tkinter où l'utilisateur pourra choisir la couleur de tank qu'il veut.
    De plus, il y a un bouton retour pour fermer la fenetre.
    """
    def __init__(self, igu, longueur_fenetre, largeur_fenetre):
        """
        Initialise la classe ParametreJoueur2.

        entrée --> self : l'objet ParametreJoueur2.
                   igu (tk.Tk): L'objet Tk sur lequel la fenêtre doit être créée.
                   longueur_fenetre(int) : longueur de la fenetre qui va être crée.
                   largeur_fenetre(int) : largeur de la fenetre qui va être crée.
                   
        sortie --> initialisation de ParametreJoueur2.
        """
        super().__init__(igu)
        self.igu = igu
        self.title("Paramètres joueur 2")
        self.geometry(str(longueur_fenetre)+"x"+str(largeur_fenetre)+"+{}+{}".format(int(self.igu.winfo_screenwidth() / 2 - longueur_fenetre/2), int(self.igu.winfo_screenheight() / 2 - largeur_fenetre/2)))
        # Mettre la fenetre tkinter devant la fenetre pygame
        self.wm_attributes("-topmost", True)
        self.creation_widgets()

    def creation_widgets(self):
        """
        Permet de créer les différents widgets présent sur la fenêtre ParametreJoueur2.

        entrée --> self : l'objet ParametreJoueur2.
                   
        sortie --> création des widgets suivants : un label "PARAMETRE JOUEUR 2", un bouton "RETOUR", une liste déroulante et un bouton "Enregistrer".
        """
        # Créer un label "PARAMETRE JOUEUR 2"
        self.label = tk.Label(self, text="PARAMETRE JOUEUR 2", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.03)), fg="#2C5234")
        self.label.pack(side="top", pady=int(self.igu.winfo_screenheight() * 0.03))

        # Créer un bouton "RETOUR"
        self.bouton_retour = tk.Button(self, text="RETOUR", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.destroy)
        self.bouton_retour.pack(side="bottom", pady=int(self.igu.winfo_screenheight() * 0.03))

        # Créer une liste déroulante pour choisir la couleur du tank du deuxième joueur
        self.couleur_label = tk.Label(self, text="Couleur de votre tank :", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#F1ECE9")
        self.couleur_label.pack(pady=int(self.igu.winfo_screenheight() * 0.02))
        self.couleur_options = ["violet", "bleu", "rose"]
        self.couleur_selection = tk.StringVar(self)
        self.couleur_menu = tk.OptionMenu(self, self.couleur_selection, *self.couleur_options)
        self.couleur_menu.pack()

        # Créer un bouton pour enregistrer le choix de boisson
        self.couleur_bouton = tk.Button(self, text="Enregistrer", font=("Helvetica", int(self.igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=self.enregistrer_couleur_joueur_2)
        self.couleur_bouton.pack(pady=int(self.igu.winfo_screenheight() * 0.02))

    def enregistrer_couleur_joueur_2(self):
        """
        Enregistre la couleur sélectionnée pour le joueur 2 dans un fichier texte et ferme la fenêtre.

        entrée --> self : l'objet ParametreJoueur2.
                   
        sortie --> la couleur sélectionnée par l'utilisateur est enregistré dans un fichier texte 'info_joueur2.txt' et ferme la fenêtre tkinter.
        """
        # Récupérer le choix de boisson
        choix_couleur = self.couleur_selection.get()
        
        # Enregistrer la couleur du tank dans un fichier txt
        ecrire_fichier_txt("../txt/info_joueur2.txt", choix_couleur)
        
        # Destruction la fenêtre tkinter
        self.destroy()
        
def lanceur_parametre(longueur_ecran, largeur_ecran):
    """
    Configure la fenetre pour les paramètres et lance la classe Paramètre.
    
    entrée --> longueur_ecran (int): longueur de l'écran de l'utilisateur en pixels.
               largeur_ecran (int): largeur de l'écran de l'utilisateur en pixels.
    
    sortie --> Instanciation de la classe Paramètre et lancement en mode "mainloop".
    """
    igu = tk.Tk()
    # On définit les dimensions de la fenetre ici pour simplifier la lecture du code de l'utilisateur,
    # Les dimensions de la fenêtre dépendent des dimensions de l'écran et d'un coefficient pour mettre à l'échelle
    LONGUEUR_FENETRE_PARAMETRE = round(longueur_ecran/2.732)
    LARGEUR_FENETRE_PARAMETRE = round(longueur_ecran/3.415)# Même pour la largeur, on la gère selon la longueur de l'écran pour éviter un étirement selon la résolution de l'écran de l'utilisateur
    
    # Centrer la fenêtre tkinter par rapport à l'écran de l'utilisateur
    coordonnée_x = int((longueur_ecran / 2) - (LONGUEUR_FENETRE_PARAMETRE / 2))
    coordonnée_y = int((largeur_ecran / 2) - (LARGEUR_FENETRE_PARAMETRE / 2))
    igu.geometry(str(LONGUEUR_FENETRE_PARAMETRE)+"x"+str(LARGEUR_FENETRE_PARAMETRE)+"+{}+{}".format(coordonnée_x, coordonnée_y))
    
    # Mettre la fenetre tkinter devant la fenetre pygame
    igu.wm_attributes("-topmost", True)
    
    parametre = Parametre(igu, LONGUEUR_FENETRE_PARAMETRE, LARGEUR_FENETRE_PARAMETRE)
    parametre.mainloop()
