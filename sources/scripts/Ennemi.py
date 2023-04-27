import pygame
from pygame.math import Vector2
from tire import *
import random

###################################################################################################################

class EnnemiTraqueur(pygame.sprite.Sprite):
    """
    Permet de créer un ennemi qui suit le joueur et lui tire dessus
    """
    def __init__(self, pos, vitesse, image, vitesse_tire, temps_tire, vie, dimension):
        """
        Initialise la classe EnnemiTraqueur.

        entrée --> self : l'objet EnnemiTraqueur.
                   pos(tuple) : position initiale de l'EnnemiTraqueur.
                   vitesse(entier) : vitesse de déplacement de l'EnnemiTraqueur
                   image(chaine de caractères) : chemin d'accès de l'image
                   vitesse_tire (entier): La vitesse du tire.
                   temps_tire(entier) : le temps d'attente entre chaque tire
                   vie(entier) : vie de l'ennemi
                   dimension(entier) : longueur de l'écran qui va nous servir à dimensionner l'EnnemiTraqueur

        sortie --> initialisation de l'EnnemiTraqueur.
        """
        # Initialisation de la classe parent Sprite()
        super().__init__()
        
        # Vie de l'EnnemiTraqueur
        self.vie = vie
        # Vitesse de tir
        self.vitesse_tire = vitesse_tire
        # Longueur de l'écran qui sert à dimensionner l'EnnemiTraqueur
        self.dimension = dimension
        # Vitesse de déplacement de l'EnnemiTraqueur
        self.vitesse = vitesse
        
        # Chargement de l'image et ajustement de la taille
        self.original_image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.dimension/45.6, self.dimension/22.8))
        # Image affichée à l'écran
        self.image = self.original_image
        # Positionnement de l'image à l'écran
        self.rect = self.image.get_rect(center=pos)
        
        # Vecteur de direction initialisé à (0, 0)
        self.direction = Vector2(0, 0)
        
        # Initialisation du groupe de projectiles
        self.projectiles = pygame.sprite.Group()
        
        # Initialisation du temps du dernier tir
        self.last_shot_time = 0
        # Durée d'attente entre chaque tir en secondes.
        self.time_between_shots = temps_tire
    
    def update(self, joueur, murs):
        """
        Met à jour la position et la direction de l'EnnemiTraqueur et/ou met à jour la position du/des tire/s de l'EnnemiTraqueur.

        entrée --> self : l'objet EnnemiTraqueur.
                   joueur(pygame.sprite.Sprite) : le tank du joueur à suivre.
                   murs(pygame.sprite.Group) : groupe des murs sur lesquels l'EnnemiTraqueur peut entrer en collision.

        sortie -> rien ou modification de la position de l'EnnemiTraqueur si il bouge et/ou modification de la position du/des tire/s de l'EnnemiTraqueur.
        """
        # Calcul de la direction pour diriger EnnemiTraqueur vers le joueur
        self.direction = Vector2(joueur.rect.center) - Vector2(self.rect.center)
        # Vérification pour éviter qu'une erreur se produise en vérifiant que la direction n'est pas un vecteur nul avant de normaliser le vecteur
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.direction *= self.vitesse
        # Déplacement de l'EnnemiTraqueur
        self.rect.move_ip(self.direction)
        # Empêchement de l'EnnemiTraqueur de sortir de la fenêtre
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        # Tourne l'image de l'EnnemiTraqueur dans la direction souhaitée
        self.rotate(self.direction.angle_to(Vector2(0, -1)))
        # Vérifie s'il y a une collision avec un mur
        collisions = pygame.sprite.spritecollide(self, murs, False)
        if collisions:
            # Vérifie s'il y a une collision avec un mur
            for mur in collisions:
                if pygame.sprite.collide_rect(self, mur):
                    # Empêche l'EnnemiTraqueur d'avancer
                    self.rect.move_ip(-self.direction)
                    # Remettre l'EnnemiTraqueur dans la fenêtre
                    self.rect.clamp_ip(pygame.display.get_surface().get_rect())
                    break
        else:
            # Met à jour la position de l'EnnemiTraqueur
            self.rect.clamp_ip(pygame.display.get_surface().get_rect())
            
        # Récupère le temps actuel en millisecondes
        current_time = pygame.time.get_ticks()

        # Vérifie si le temps écoulé depuis le dernier tir est supérieur ou égal au temps entre chaque tir en millisecondes
        if current_time - self.last_shot_time >= self.time_between_shots * 1_000:
            
            # Met à jour le temps du dernier tir
            self.last_shot_time = current_time
            
            # Bruit de tire
            bruit_tire = pygame.mixer.Sound('../musique/bruit_tire.mp3')
            bruit_tire.play()
            
            # Crée un nouveau projectile à partir du centre de l'objet courant, de sa direction, de sa vitesse de tir et de ses dimensions
            projectile = Projectile(self.rect.center, self.direction, self.vitesse_tire, self.dimension)
            
            # Ajoute le projectile au groupe de projectiles
            self.projectiles.add(projectile)
            
    def rotate(self, angle):
        """
        Tourne l'EnnemiTraqueur selon un certain angle.

        entrée --> self : l'objet EnnemiTraqueur.
                   angle(int ou float) : l'angle de rotation.

        sortie --> rotation de l'EnnemiTraqueur
        """
        # Tourne l'image de l'EnnemiTraqueur
        self.image = pygame.transform.rotate(self.original_image, angle)
        
        # Met à jour le rectangle de collision de l'EnnemiTraqueur avec la nouvelle position du centre de l'image
        # On utilise self.rect.center pour que le centre reste le même malgré la rotation
        self.rect = self.image.get_rect(center=self.rect.center)
        
###################################################################################################################

class EnnemiAleatoire(pygame.sprite.Sprite):
    """
    Permet de créer un ennemi qui se déplace aléatoirement et qui tire devant lui
    """
    def __init__(self, pos, vitesse, image, vitesse_tire, temps_tire, vie, dimension):
        """
        Initialise la classe EnnemiAleatoire.

        entrée --> self : l'objet EnnemiAleatoire.
                   pos(tuple) : position initiale de l'EnnemiAleatoire.
                   vitesse(entier) : vitesse de déplacement de l'EnnemiAleatoire.
                   image(chaine de caractères) : chemin d'accès de l'image.
                   vitesse_tire (entier): La vitesse du tire.
                   temps_tire(entier) : le temps d'attente entre chaque tire.
                   vie(entier) : vie de l'EnnemiAleatoire.
                   dimension(entier) : longueur de l'écran qui va nous servir à dimensionner l'EnnemiAleatoire.

        sortie --> initialisation de l'EnnemiAleatoire.
        """
        super().__init__()
        self.vie = vie
        self.vitesse_tire = vitesse_tire
        self.vitesse = vitesse
        self.dimension = dimension
        # Charge l'image à partir du chemin d'accès et dimensionne-la
        self.original_image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.dimension/22.8, self.dimension/45.6))
        self.image = self.original_image
        # Positionne l'EnnemiAleatoire à "pos"
        self.rect = self.image.get_rect(center=pos)
        # Initialise la direction à (0,0)
        self.direction = Vector2(0, 0)
        
        # Initialise un groupe de projectiles
        self.projectiles = pygame.sprite.Group()
        
        # Initialise le temps du dernier tir à 0
        self.last_shot_time = 0
        # Initialise le temps entre les tirs en secondes
        self.time_between_shots = temps_tire
        # Initialise le dernier update du sprite à 0
        self.last_update = 0
        
        # Définit le temps aléatoire avant le prochain changement de direction
        self.random_direction_timer = random.randint(1000, 3000)
        # Initialise le temps passé depuis le dernier changement de direction à 0
        self.direction_timer = 0
        # Définit la durée de la direction aléatoire
        self.direction_duration = random.uniform(2, 4) * 1000
        
        # Initialise la direction aléatoire
        self.randomize_direction()

    def update(self, _, murs):
        """
        Met à jour la position de l'EnnemiAleatoire et ses projectiles.

        entrée --> self : l'objet EnnemiAleatoire.
                   _(pygame.sprite.Group) : variable poubelle qui est utilisé pour le fonctionnement de la fonction evenement_joueur_ennemi de la classe Jeu.
                   murs(pygame.sprite.Group): Les murs du niveau.
                   
        sortie -> rien ou modification de la position de l'EnnemiAleatoire si il bouge et/ou met à jour la position du/des tire/s de l'EnnemiAleatoire.
        """
        # Calcul de la direction pour diriger l'EnnemiAleatoire 
        self.direction_timer += pygame.time.get_ticks() - self.last_update
        # Si le temps écoulé est supérieur ou égal à la durée de la direction aléatoire
        if self.direction_timer >= self.direction_duration:
            # Réinitialise le timer
            self.direction_timer = 0
            # Calcule une nouvelle direction aléatoire
            self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * self.vitesse
            # Définit une nouvelle durée de direction aléatoire
            self.direction_duration = random.uniform(2, 4) * 1000
            
        # Déplacement de l'EnnemiAleatoire
        self.rect.move_ip(self.direction)
        # Empêchement de l'EnnemiAleatoire de sortir de la fenêtre
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        # Vérifie s'il y a une collision avec un mur
        collisions = pygame.sprite.spritecollide(self, murs, False)
        if collisions:
            # Vérifie s'il y a une collision avec un mur
            for mur in collisions:
                if pygame.sprite.collide_rect(self, mur):
                    # Empêche l'EnnemiAleatoire d'avancer
                    self.rect.move_ip(-self.direction)
                    # Remettre l'EnnemiAleatoire dans la fenêtre
                    self.rect.clamp_ip(pygame.display.get_surface().get_rect())
                    self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * self.vitesse
                    break
        else:
            # Met à jour la position de l'EnnemiAleatoire
            self.rect.clamp_ip(pygame.display.get_surface().get_rect())
            
        # Récupération du temps actuel en millisecondes
        current_time = pygame.time.get_ticks()

        # Vérifie si le temps écoulé depuis le dernier tir est supérieur ou égal au temps minimum entre deux tirs
        if current_time - self.last_shot_time >= self.time_between_shots * 1000:

            # Enregistre le temps du dernier tir
            self.last_shot_time = current_time
            
            # Bruit de tire
            bruit_tire = pygame.mixer.Sound('../musique/bruit_tire.mp3')
            bruit_tire.play()
            
            # Crée un nouveau projectile en lui passant la position et la direction de l'EnnemiAleatoire, ainsi que la vitesse et la taille du projectile
            projectile = Projectile(self.rect.center, self.direction, self.vitesse_tire, self.dimension)

            # Ajoute le projectile au groupe de projectiles de l'objet
            self.projectiles.add(projectile)

        # Tourne l'EnnemiAleatoire en fonction de sa direction
        self.rotate(self.direction.angle_to(Vector2(1, 0)))

        # Enregistre le temps actuel pour la prochaine mise à jour
        self.last_update = pygame.time.get_ticks()
    
    def randomize_direction(self):
        """
        Choisit aléatoirement une direction pour l'EnnemiAleatoire en générant un vecteur aléatoire
        de norme 1, et le multiplie par la vitesse de l'EnnemiAleatoire.
        
        entrée --> self : l'objet EnnemiAleatoire.
        
        sortie --> Modification de self.direction de l'objet EnnemiAleatoire.
        """
        # Choisit une direction aléatoire et la normalise
        direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        # Multiplie la direction par la vitesse de l'EnnemiAleatoire
        self.direction = direction * self.vitesse
    
    def rotate(self, angle):
        """
        Tourne l'EnnemiAleatoire selon un certain angle.

        entrée --> self : l'objet EnnemiAleatoire.
                   angle(int ou float) : l'angle de rotation.

        sortie --> rotation de l'EnnemiAleatoire.
        """
        # Tourne l'image de l'EnnemiAleatoire
        self.image = pygame.transform.rotate(self.original_image, angle)
        
        # Met à jour le rectangle de collision de l'EnnemiAleatoire avec la nouvelle position du centre de l'image
        # On utilise self.rect.center pour que le centre reste le même malgré la rotation
        self.rect = self.image.get_rect(center=self.rect.center)