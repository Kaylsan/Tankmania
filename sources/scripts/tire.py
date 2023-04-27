import pygame

class Projectile(pygame.sprite.Sprite):
    """
    Classe représentant un projectile qui peut être tiré par un joueur.
    """
    def __init__(self, pos, direction, vitesse, dimension):
        """
        Initialise la classe Projectile.

        entrée --> self : l'objet Projectile.
                   pos(tuple) : position initiale du Projectile.
                   direction(Vector2) : direction initiale du Projectile.
                   vitesse(int) : vitesse du Projectile.
                   dimension(entier) : longueur de l'écran qui va nous servir à dimensionner le Projectile.

        sortie --> initialisations du Projectile.
        """
        super().__init__()
        # Si la vitesse est égale à 1, alors le tire sera une mine, sinon ça sera un boulet de canon
        if vitesse <= 1:
            self.image = pygame.transform.scale(pygame.image.load("../graphisme/tire/mine.png").convert_alpha(), (dimension/91.2, dimension/91.2))
        else:
            self.image = pygame.transform.scale(pygame.image.load("../graphisme/tire/boulet.png").convert_alpha(), (dimension/91.2, dimension/91.2))
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.vitesse = vitesse
        self.collision_count = 0 # nombre de collisions avec un mur
        self.destruction = False 

    def update(self, murs, adversaires):
        """
        Met à jour la position du projectile.

        entrée --> self : l'objet Projectile.
                   murs(pygame.sprite.Group) : groupe des murs sur lesquels le Projectile peut entrer en collision.
                   adversaire(pygame.sprite.Group) : le/s adversaire/s qui peut/peuvent être touché par le Projectile.

        sortie -> rien ou suppression du Projectile si il sort de la fenêtre ou s'il entre en collision avec un mur une deuxième fois ou un adversaire.
        """
        self.rect.move_ip(self.direction * self.vitesse)
        # Vérifie si le Projectile sort de la fenêtre, si il sort on le détruit
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()
        # Vérifie s'il y a une collision avec un sprite mur qui est dans le groupe murs, si il y a une collision alors collisions = True
        collisions = pygame.sprite.spritecollide(self, murs, False)
        if collisions:
            if self.destruction == True:
                # Supprime l'objet
                self.kill()
            else:
                for mur in collisions:
                    # Vérifie si le sprite représenté par l'objet "self", le Projectile,
                    # rentre en collision avec le sprite "mur"
                    if pygame.sprite.collide_rect(self, mur):
                        
                        # Convertir mur.rect en Vector2
                        mur_center = mur.rect.center
                        # Le symbole * avant mur_center est utilisé pour "déplier" le tuple et
                        # passer ses éléments comme deux arguments distincts à la fonction pygame.math.Vector2
                        mur_center_vec = pygame.math.Vector2(*mur_center)
                        
                        # Réfléchir la direction du Projectile pour que l'utilisateur a l'impression que le tire à rebondi
                        self.direction = self.direction.reflect(mur_center_vec - self.rect.center)
                        
                        # Vérifier si le Projectile doit être détruit
                        self.destruction = True  # on marque le projectile comme étant à détruire la prochaine fois qui touche un mur
                        # On sort de la boucle pour éviter de continuer à détecter des collisions avec d'autres murs
                        return
            
        for adversaire in adversaires:
            # Vérifie si le sprite représenté par l'objet "self", le Projectile,
            # rentre en collision avec le sprite "adversaire"
            if pygame.sprite.collide_rect(self, adversaire):
                # Si il rentre en collision, alors le sprite adversaire perd une vie
                adversaire.vie-=1
                # Supprime le sprite Projectile de tous les groupes auxquels il appartient 
                self.kill()
