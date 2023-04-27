import pygame
from pygame.math import Vector2
from tire import*

# Initialisation de pygame
pygame.init()

# Liste à deux dimensions où il y est stocké les différents conditions liées au déplacement du joueur 1(liste[0]) et 2(liste[1])
# On les stocke sous forme de chaîne de caractères car on utilisera la fonction intégrée "eval()" pour évaluer ses conditions
touche_joueur =[['pygame.K_RIGHT in self.pressed and self.pressed[pygame.K_RIGHT]',
                 'pygame.K_LEFT in self.pressed and self.pressed[pygame.K_LEFT]',
                 'pygame.K_UP in self.pressed and self.pressed[pygame.K_UP]',
                 'pygame.K_DOWN in self.pressed and self.pressed[pygame.K_DOWN]',
                 'pygame.mouse.get_pressed()[0]'],
                ['pygame.K_d in self.pressed and self.pressed[pygame.K_d]',
                 'pygame.K_q in self.pressed and self.pressed[pygame.K_q]',
                 'pygame.K_z in self.pressed and self.pressed[pygame.K_z]',
                 'pygame.K_s in self.pressed and self.pressed[pygame.K_s]',
                 'pygame.K_SPACE in self.pressed and self.pressed[pygame.K_SPACE]']]


################################################################################################################################
################################################################################################################################

class Joueur(pygame.sprite.Sprite):
    """
    La classe Joueur représente un joueur dans le jeu.
    Le joueur est représenté par un tank qui peut se déplacer et tirer sur les ennemis.
    """
    def __init__(self, pos, joueur, design_joueur, vitesse_tire, dimension):
        """
        Initialise la classe Joueur.

        entrée --> self(pygame.sprite.Sprite) : l'objet Joueur.
                   pos(tuple) : position initiale du joueur.
                   joueur(entier) : numéro 1 ou 2 qui correspond au joueur 1 ou 2.
                   design_joueur(chaîne de caractères) : chemin où est stockée l'image qui correspondra au tank du joueur "joueur".
                   vitesse_tire (int): La vitesse du tire.
                   dimension(entier) : longueur de l'écran qui va nous servir à dimensionner le Joueur.
                   
        sortie --> initialisation du Joueur.
        """
        super().__init__()
        # Dictionnaire des touches claviers pressées.
        self.pressed = {}
        
        self.dimension = dimension
        # Initialisation des attributs du Joueur
        self.vie = 3
        self.vitesse = 4
        # Chargement de l'image du tank du joueur et mise à l'échelle
        self.original_image = pygame.transform.scale(pygame.image.load(design_joueur).convert_alpha(), (self.dimension/45.6, self.dimension/22.8))
        self.image = self.original_image
        
        # Placement du tank du joueur sur la fenêtre
        self.rect = self.image.get_rect(center=pos)
        
        # Initialisation de la direction du Joueur
        self.direction = Vector2(0, 0)
        
        self.projectiles = pygame.sprite.Group()
        self.last_shot_time = 0
        # Vitesse du tire
        self.vitesse_tire = vitesse_tire
        
        # 3 secondes minimums entre chaques tirs
        self.time_between_shots = 3
        self.joueur = joueur
        # Selon si le joueur est le joueur 1 ou 2, on affecte à la variable self.touche_joueur une liste qui correspond aux différents
        # touches que le joueur "joueur" peut utiliser pour se déplacer ou tirer/poser une mine
        if self.joueur == 1:
            self.touche_joueur = touche_joueur[0]
        else:
            self.touche_joueur = touche_joueur[1]
            

    def update(self, taille_fenetre, murs):
        """
        Met à jour la position et la direction du Joueur.

        entrée --> self(pygame.sprite.Sprite) : l'objet Joueur.
                   taille_fenetre(tuple) : taille de l'écran en pixels.
                   murs(pygame.sprite.Group) : groupe des murs sur lesquels le joueur peut entrer en collision mais ne peut pas traverser.

        sortie -> rien ou modification de la position du Joueur s'il appuie sur une touche adéquate.
        """
        # Réinitialisation de la direction à chaque appel de la méthode update
        self.direction = Vector2(0, 0)
        # Vérification des touches pressées pour changer la direction du Joueur
        if eval(self.touche_joueur[0]):
            self.direction += Vector2(1, 0) 
        if eval(self.touche_joueur[1]):
            self.direction += Vector2(-1, 0)
        if eval(self.touche_joueur[2]):
            self.direction += Vector2(0, -1)
        if eval(self.touche_joueur[3]):
            self.direction += Vector2(0, 1)
            
        # On gére le tire ici
        souris_pos = pygame.mouse.get_pos()
        
        # Vérifier si la touche du joueur pour tirer ou poser une mine est enfoncée pour permettre le tir/ de poser un mine
        if eval(self.touche_joueur[4]):
            current_time = pygame.time.get_ticks()

            # Vérifier si le temps écoulé depuis le dernier tir est suffisant
            if current_time - self.last_shot_time >= self.time_between_shots * 1000:
                self.last_shot_time = current_time

                # Calculer la direction vers la position du curseur
                direction = Vector2(souris_pos) - Vector2(self.rect.center)

                # Vérifier si la direction est valide pour éviter les erreurs de calcul
                if direction.length() > 0:
                    direction.normalize_ip()
                    
                    # Bruit de tire
                    bruit_tire = pygame.mixer.Sound('../musique/bruit_tire.mp3')
                    bruit_tire.play()
                    
                    # Créer un nouveau projectile et l'ajouter au groupe de projectiles
                    projectile = Projectile(self.rect.center, direction, self.vitesse_tire, self.dimension)
                    self.projectiles.add(projectile)

        # Si une direction est sélectionnée, déplace le Joueur et le fait tourner
        if self.direction:
            # Normalisation de la direction pour avoir une vitesse constante
            self.direction.normalize_ip()
            self.direction *= self.vitesse
            
            # Déplace le joueur dans la direction souhaitée
            self.rect.move_ip(self.direction)
            
            # Empêche le Joueur de sortir de la fenêtre
            self.rect.clamp_ip(pygame.Rect(0, 0, *taille_fenetre))
            
            # Tourne le Joueur dans la direction souhaitée
            self.rotate(self.direction.angle_to(Vector2(0, -1)))
            
            # Vérifie si le Joueur entre en collision avec un mur
            collisions = pygame.sprite.spritecollide(self, murs, False)
            if collisions:
                # Si il y a une collision avec un mur, empêche le joueur d'avancer dans cette direction
                for mur in collisions:
                    if pygame.sprite.collide_rect(self, mur):
                        self.rect.move_ip(-self.direction)
                        # Remettre le Joueur dans la fenêtre
                        self.rect.clamp_ip(pygame.Rect(0, 0, *taille_fenetre))
                        break
            else:
                # Si il n'y a pas de collision, met à jour la position du Joueur
                self.rect.clamp_ip(pygame.Rect(0, 0, *taille_fenetre))
        
    def rotate(self, angle):
        """
        Tourne le Joueur selon un certain angle.

        entrée --> self(pygame.sprite.Sprite) : l'objet Joueur.
                   angle(int ou float) : l'angle de rotation.

        sortie --> rotation du Joueur.
        """
        # Tourne l'image du Joueur
        self.image = pygame.transform.rotate(self.original_image, angle)
        # Met à jour la position du Joueur après rotation
        self.rect = self.image.get_rect(center=self.rect.center)