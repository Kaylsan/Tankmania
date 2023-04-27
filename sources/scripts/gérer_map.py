import pygame

class Mur(pygame.sprite.Sprite):
    """
    Cette classe définit un mur qui peut être dessiné sur une surface pygame.
    """
    def __init__(self, x, y, largeur, hauteur, couleur):
        """
        Initialise une instance de la classe Mur.

        entrée --> x (int): La position en x du coin supérieur gauche du mur.
                   y (int): La position en y du coin supérieur gauche du mur.
                   largeur (int): La largeur du mur en pixels.
                   hauteur (int): La hauteur du mur en pixels.
                   couleur (tuple): Un tuple représentant la couleur du mur au format (R, G, B).
        
        sortie --> initialisation du Mur.
        """
        super().__init__()  # Appel du constructeur de la classe parente Sprite.
        self.image = pygame.Surface([largeur, hauteur])  # Création d'une surface pour le mur.
        self.image.fill(couleur)  # Remplissage de la surface avec la couleur donnée.
        self.rect = self.image.get_rect()  # Récupération du rectangle englobant la surface.
        self.rect.x = x  # Positionnement du rectangle en x.
        self.rect.y = y  # Positionnement du rectangle en y.



class Map:
    """
    Classe représentant la carte du jeu.
    """

    def __init__(self, longueur_fenetre, largeur_fenetre, tab_déco, tab_niveau):
        """
        Initialise la classe Map avec les paramètres passés.

        entrée --> longueur_fenetre (int): Longueur de la fenêtre de jeu en pixels.
                   largeur_fenetre (int): Largeur de la fenêtre de jeu en pixels.
                   tab_déco (list): Liste contenant les images des différentes décorations de la carte.
                   tab_niveau (list): Liste contenant les données pour générer la carte
                            (0 pour un espace vide, 1 pour le haut d'un mur, 2 pour le devant d'un mur).
        
        sortie --> initialisation de Map.
        """
         # initialise le groupe de sprites qui contiendra les murs
        self.groupe_murs = pygame.sprite.Group()
        
        self.longueur_fenetre = longueur_fenetre
        self.largeur_fenetre = largeur_fenetre
        self.tab_déco = tab_déco
        self.tab_niveau = tab_niveau

    def dessine_niveau(self, ecran):
        """
        Dessine la carte en fonction des données de tab_niveau et met à jour le groupe de sprites des murs.
        
        entrée --> self : l'objet Map.
                   ecran(pygame.Surface) : surface graphique pouvant être dessinée dessus.
                   
        sortie -> modification de l'écran "ecran" de l'utilisateur.
        """
        # Vide le groupe de sprites des murs pour le mettre à jour
        self.groupe_murs.empty()

        y = 0
        for i in range(len(self.tab_niveau)):
            x = 0
            for v in self.tab_niveau[i]:
                if v != 0:
                    # Créer un sprite pour chaque mur
                    mur = Mur(x, y, int(self.longueur_fenetre/32)+1, int(self.largeur_fenetre/18)+1, (255, 255, 255))
                    self.groupe_murs.add(mur)
                    
                    # Dessine l'image en fonction de la valeur de la "case",
                    # car l'écran est virtuellement quadrillé en 32 cases en longueur et en 18 cases en largeur
                    if v == 1:
                        ecran.blit(self.tab_déco[1], (x, y))
                    else:
                        ecran.blit(self.tab_déco[0], (x, y))
                # On décale l'abscisse du point du haut à gauche du prochain mur
                x += int(self.longueur_fenetre/32)+1 # On rajoute 1 pour être sur qu'il n'y a pas de problème d'affichage
            # On décale l'ordonnée du point du haut à gauche des prochains murs
            y += int(self.largeur_fenetre/18)+1 # On rajoute 1 pour être sur qu'il n'y a pas de problème d'affichage
