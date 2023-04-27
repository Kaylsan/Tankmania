from curseur8 import curseur
from gerer_compte import *
from parametre import lanceur_parametre
from mvt_joueur import*
from tire import*
from Ennemi import*
from commande_json_txt import modifier_valeur_json
from moviepy.editor import*
from random import randint
from gérer_map import *
import webbrowser
import pygame
import tkinter as tk

class Jeu:
    """
    La classe Jeu permet de gérer la partie et elle est la fonction principale du jeu Tankmania
    """
    def __init__(self):
        """
        Initialise la classe Jeu.

        entrée --> self : l'objet Jeu.
                   
        sortie --> initialisation de Jeu.
        """
        # Initialise le module Pygame
        pygame.init()

        # Crée une fenêtre en plein écran et récupère sa taille
        self.ecran = pygame.display.set_mode((0, 0))
        self.longueur_fenetre = self.ecran.get_size()[0]
        self.largeur_fenetre = self.ecran.get_size()[1]
        
        # Changement du titre de la fenêtre
        pygame.display.set_caption("Tankmania")
        self.clock = pygame.time.Clock() # Crée un objet Clock pour gérer le temps
        
        # Variable de boucle pour continuer ou quitter le jeu
        self.continuer = True
        
        # Indique où l'utilisateur se trouve, si une de ces trois variable égale True,
        # ça signifie que l'on se trouve dans une des boucles du jeu associé à la variable 
        self.ecran_accueil = True  # Indique si on est sur l'écran d'accueil
        self.ecran_chargement_compte = False  # Indique si on est sur l'écran de chargement de compte
        self.ecran_jeu = False  # Indique si on est sur l'écran de jeu
        self.ecran_1vs1 = False # Indique si on est dans le mode de jeu 1 vs 1
        
        # On a deux image pour l'écran d'accueil alors on choisit aléatoirement
        numéro_background = str(randint(1,2))
        self.fond_ecran = pygame.transform.scale(pygame.image.load('../graphisme/tankmania'+numéro_background+'.png'), (self.longueur_fenetre, self.largeur_fenetre))
        
        # Le fond de l'écran où on charge un compte sera une couleur unie mais aléatoire
        r,g,b = randint(0,255), randint(0,255), randint(0,255)
        self.couleur_ecran_chargement_compte = (r, g, b)
        
        # On définit nos constantes par rapport aux images
        self.IMAGE_BOUTON_PLAY = pygame.transform.scale(pygame.image.load('../graphisme/start_marron.png'), (self.longueur_fenetre*1/4, self.longueur_fenetre*1/16))
        self.IMAGE_BOUTON_PLAY_HOVER = pygame.transform.scale(pygame.image.load('../graphisme/start_orange.png'), (self.longueur_fenetre*1/4, self.longueur_fenetre*1/16))
        
        self.IMAGE_BOUTON_CHARGEMENT_COMPTE = pygame.transform.scale(pygame.image.load('../graphisme/load_marron.png'), (self.longueur_fenetre*1/4, self.longueur_fenetre*1/16))
        self.IMAGE_BOUTON_CHARGEMENT_COMPTE_HOVER = pygame.transform.scale(pygame.image.load('../graphisme/load_orange.png'), (self.longueur_fenetre*1/4, self.longueur_fenetre*1/16))
        
        self.IMAGE_BOUTON_NOUVEAU_COMPTE = pygame.transform.scale(pygame.image.load('../graphisme/new_marron.png'), (self.longueur_fenetre*1/4, self.longueur_fenetre*1/16))
        self.IMAGE_BOUTON_NOUVEAU_COMPTE_HOVER = pygame.transform.scale(pygame.image.load('../graphisme/new_orange.png'), (self.longueur_fenetre*1/4, self.longueur_fenetre*1/16))

        self.IMAGE_BOUTON_1VS1 = pygame.transform.scale(pygame.image.load('../graphisme/1vs1_marron.png'), (self.longueur_fenetre*1/4, self.longueur_fenetre*1/16))
        self.IMAGE_BOUTON_1VS1_HOVER = pygame.transform.scale(pygame.image.load('../graphisme/1vs1_orange.png'), (self.longueur_fenetre*1/4, self.longueur_fenetre*1/16))

        # Création des listes qui contiendront des informations pour créer des boutons clickables
        self.parametre = self.bouton_clickable(self.longueur_fenetre-self.longueur_fenetre*1/32, self.largeur_fenetre-self.longueur_fenetre*1/32, self.longueur_fenetre*1/16, self.longueur_fenetre*1/16,"../graphisme/parametre.png")
        self.bouton_play = self.bouton_clickable(self.longueur_fenetre/2, self.largeur_fenetre*2/5, self.longueur_fenetre*1/4, self.longueur_fenetre*1/16, '../graphisme/start_marron.png')
        self.bouton_1vs1 = self.bouton_clickable(self.longueur_fenetre/2, self.largeur_fenetre*3/5, self.longueur_fenetre*1/4, self.longueur_fenetre*1/16, '../graphisme/1vs1_marron.png')
        self.bouton_chargement_compte = self.bouton_clickable(self.longueur_fenetre*4/5, self.largeur_fenetre/2, self.longueur_fenetre*1/4, self.longueur_fenetre*1/16,'../graphisme/load_marron.png')
        self.bouton_nouveau_compte = self.bouton_clickable(self.longueur_fenetre*1/5, self.largeur_fenetre/2, self.longueur_fenetre*1/4, self.longueur_fenetre*1/16,'../graphisme/new_marron.png')
        self.bouton_home = self.bouton_clickable(0+self.longueur_fenetre*1/32, self.largeur_fenetre-self.longueur_fenetre*1/32, self.longueur_fenetre*1/16, self.longueur_fenetre*1/16,"../graphisme/home.png")
        self.bouton_aide = self.bouton_clickable(self.longueur_fenetre-self.longueur_fenetre*1/32, 0+self.longueur_fenetre*1/32, self.longueur_fenetre*1/16, self.longueur_fenetre*1/16,"../graphisme/aide.png")
        
        # On charge ici nos mur
        mur_bois_fonce = pygame.transform.scale(pygame.image.load('../graphisme/mur_bois_fonce.png'), (int(self.longueur_fenetre/32)+1, int(self.largeur_fenetre/18)+1))
        mur_bois_clair = pygame.transform.scale(pygame.image.load('../graphisme/mur_bois_claire.png'), (int(self.longueur_fenetre/32)+1, int(self.largeur_fenetre/18)+1))
        # Tab où on stocke les éléments qui va apparaitre sur la map
        self.tab_déco = [mur_bois_fonce,mur_bois_clair]
        
        # On défénit presence_2_joueur à False
        self.presence_2_joueur = False
        
        # On lance la musique de fond du jeu
        self.lancer_musique("../musique/musique_puissante.mp3", 0.05)
    
    
    def run(self):
        """
        Lance la boucle principale du jeu et gère les différents écrans à afficher.
        La boucle continue tant que la variable self.continuer est à True.
        
        Cette fonction gère les événements, dessine les différents écrans en fonction des variables self.ecran_jeu, self.ecran_accueil et self.ecran_chargement_compte.
        Elle met également à jour l'affichage de la souris et contrôle le nombre maximal de FPS pour limiter la consommation de ressources de l'ordinateur utilisé.
        
        entrée --> self : l'objet Jeu.
                   
        sortie --> Gére les événements du jeu et dessine les différents écrans en fonction des variables
                   self.ecran_jeu, self.ecran_accueil et self.ecran_chargement_compte.
        """
        while self.continuer:
            self.evenements()
            if self.ecran_jeu:
                self.dessine_ecran_jeu()
            elif self.ecran_accueil:
                self.dessine_ecran_accueil()
            elif self.ecran_1vs1:
                self.combat_1v1()
            else:
                self.dessine_ecran_chargement_compte()
            
            # Affiche les boutons qui seront visibles tout le temps
            self.ecran.blit(self.parametre[0], self.parametre[1])
            self.ecran.blit(self.bouton_home[0], self.bouton_home[1])
            self.ecran.blit(self.bouton_aide[0], self.bouton_aide[1])
            
            # Dessine le curseur en forme de croix à l'emplacement du curseur de la souris
            curseur((255,0,255), self.ecran)
            
            # Controle les FPS maximums
            self.clock.tick(80)
            
            # Mettre à jour l'écran
            pygame.display.update()
        # Ferme la fenêtre Pygame et quitte le programme
        pygame.display.quit()
        
        
    def dessine_ecran_accueil(self):
        """
        Cette fonction dessine l'écran d'accueil du jeu, qui comprend le fond d'écran et le bouton play.
        
        entrée --> self : l'objet Jeu.
                   
        sortie --> Affichage des éléments présents sur l'écran d'accueil.
        """
        self.ecran.blit(self.fond_ecran,(0,0))
        self.ecran.blit(self.bouton_play[0], self.bouton_play[1])
        self.ecran.blit(self.bouton_1vs1[0], self.bouton_1vs1[1])
    
    
    def dessine_ecran_chargement_compte(self):
        """
        Dessine l'écran de chargement de compte avec le fond, les boutons de chargement de compte et de création de nouveau compte.
        
        entrée --> self : l'objet Jeu.
                   
        sortie --> Affichage des éléments présents sur l'écran de chargement de compte.
        """
        self.ecran.fill(self.couleur_ecran_chargement_compte)
        self.ecran.blit(self.bouton_chargement_compte[0], self.bouton_chargement_compte[1])
        self.ecran.blit(self.bouton_nouveau_compte[0], self.bouton_nouveau_compte[1])
    
    
    def combat_1v1(self):
        """
        Dessine l'écran du mode 1 vs 1.
        
        entrée --> self : l'objet Jeu.
                   
        sortie --> Affichage des éléments présents sur l'écran du mode 1 vs 1.
        """
        # Dessiner le fond d'écran
        self.ecran.fill((224, 205, 169))
        
        self.map.dessine_niveau(self.ecran)
        self.groupe_murs = self.map.groupe_murs
        self.evenement_mode_1vs1(self.joueur, self.groupe_joueur2)
        self.evenement_mode_1vs1(self.joueur2, self.groupe_joueur1)
        
        # Ecrire les informations des joueurs sur l'écran
        self.ecrire_sur_ecran("Vie Joueur 1: "+str(self.joueur.vie), (self.longueur_fenetre*1/4, self.largeur_fenetre*29/30), (255, 0, 0))
        self.ecrire_sur_ecran("Vie Joueur 2: "+str(self.joueur2.vie), (self.longueur_fenetre*3/4, self.largeur_fenetre*29/30), (255, 0, 0))
        self.ecrire_sur_ecran("Victoire Joueur 1: "+str(self.victoire_joueur), (self.longueur_fenetre*1/3, self.largeur_fenetre*1/30), (0, 0, 0))
        self.ecrire_sur_ecran("Victoire Joueur 2: "+str(self.victoire_joueur2), (self.longueur_fenetre*2/3, self.largeur_fenetre*1/30), (0, 0, 0))
        
        
    def evenement_mode_1vs1(self, joueur, groupe_adversaire):
        """
        Gère les événements liés aux deux joueurs du mode 1 vs 1.
        
        entrée --> self : l'objet Jeu.
                   joueur(pygame.sprite.Sprite) = joueur dont on vérifie ses événements.
                   groupe_adversaire(pygame.sprite.Group) = un groupe de sprites contenant les sprites des adversaires du joueur "joueur".

                   
        sortie --> Affichage du joueur "joueur" et/ou affichage du tir du joueur "joueur" et/ou
                   modification des variables qui contient le nombre de victoire de chaques joueurs et/ou
                   modification des vies des deux joueurs du mode 1 vs 1.
        """
        # Vérification que le joueur n'a plus de vie
        if joueur.vie <= 0:
            # Un des deux joueurs a gagné ducoup on joue une son de victoire
            bruit_victoire = pygame.mixer.Sound('../musique/piece/piece.wav')
            bruit_victoire.play()
            
            # Vérification de quel joueur est n'a plus de vie
            if joueur == self.joueur:
                self.victoire_joueur2 += 1
            else:
                self.victoire_joueur += 1
            # On remet la vie des deux joueurs à 3
            self.joueur.vie = 3
            self.joueur2.vie = 3
        else:
            # On affiche le joueur à l'écran
            self.ecran.blit(joueur.image, joueur.rect)
            # On met à jour la position des projectiles du sprite
            joueur.update(self.ecran.get_size(), self.groupe_murs)
            joueur.projectiles.update(self.groupe_murs, groupe_adversaire)
            joueur.projectiles.draw(self.ecran)
        
        
    def dessine_ecran_jeu(self):
        """
        Cette fonction permet de dessiner l'écran de jeu en remplissant le fond d'écran et en affichant
        le niveau en cours, le pseudo du joueur, ainsi que les groupes de joueurs et ennemis sur la map.
        Elle appelle également la fonction evenement_joueur_ennemi pour gérer les évènements entre les joueurs et les ennemis.
        
        entrée --> self : l'objet Jeu.
                   
        sortie --> Affichage des éléments présents sur l'écran de jeu.
        """
        self.ecran.fill((167,220,101))# Dessiner la couleur de fond d'écran
        # Si il le deuxième joueur n'est pas sur la map, on regarde si il veut rejoindre la partie
        if self.presence_2_joueur == False:
            self.info_joueur_2()
        
        self.map.dessine_niveau(self.ecran)
        self.groupe_murs = self.map.groupe_murs
        self.ecrire_sur_ecran(self.pseudo, (self.longueur_fenetre*1/20, self.largeur_fenetre*1/30), (0, 0, 0))
        self.ecrire_sur_ecran("level "+str(self.level), (self.longueur_fenetre//2, self.largeur_fenetre*1/30), (0, 0, 0))
        self.evenement_joueur_ennemi(self.groupe_joueur, self.groupe_ennemis)
        self.evenement_joueur_ennemi(self.groupe_ennemis, self.groupe_joueur)
        
        if self.presence_2_joueur == False:
            self.ecrire_sur_ecran("Vie Joueur : "+str(self.joueur.vie), (self.longueur_fenetre//2, self.largeur_fenetre*29/30), (255, 0, 0))
        else:
            self.ecrire_sur_ecran("Vie Joueur 1: "+str(self.joueur.vie), (self.longueur_fenetre*1/4, self.largeur_fenetre*29/30), (255, 0, 0))
            self.ecrire_sur_ecran("Vie Joueur 2: "+str(self.joueur2.vie), (self.longueur_fenetre*3/4, self.largeur_fenetre*29/30), (255, 0, 0))
    
    
    def ecrire_sur_ecran(self, texte, position, couleur):
        """
        Cette fonction permet d'écrire un texte à l'écran, à la position donnée.
        Le texte est créé à partir de la chaîne de caractères `text`, et la police et la taille de caractères sont définies par la variable `font`.
        
        entrée --> self : l'objet Jeu.
                   texte (str) = le texte à afficher à l'écran.
                   position (tuple) = les coordonnées (x,y) du milieu du texte à afficher à l'écran;
                   couleur (tuple) = la couleur sous forme rgb, par exemple : (50,170,235).
        
        sortie --> Affichage du texte 'texte' sur l'écran 'self.ecran'.
        """
        font = pygame.font.Font(None, 36)
        text = font.render(texte, True, couleur)
        text_rect = text.get_rect()
        text_rect.center = position
        self.ecran.blit(text, text_rect)
        
        
    def evenement_joueur_ennemi(self, groupe_sprite, groupe_adversaire):
        """
        Cette fonction gère les événements entre les sprites du joueur et ceux des ennemis, en fonction des groupes de sprites fournis.
        La fonction vérifie si le groupe de sprites est vide ou non. Si le groupe est vide, la fonction met à jour le niveau et réinitialise la position des joueurs et ennemis.
        Si le groupe de sprites n'est pas vide, la fonction boucle sur chaque sprite, vérifie si sa vie est inférieure ou égale à 0, et le supprime si tel est le cas.
        Si la vie du sprite est supérieure à 0, la fonction met à jour la position du sprite et de ses projectiles en fonction des groupes de murs et d'adversaires fournis, puis l'affiche à l'écran.
        
        entrée --> self : l'objet Jeu.
                   groupe_sprite(pygame.sprite.Group) = un groupe de sprites contenant les sprites du/des joueur/s ou des ennemis.
                   groupe_adversaire(pygame.sprite.Group) = un groupe de sprites contenant les sprites des adversaires du groupe_sprite.
        
        sortie --> Affichage du "groupe_sprite" si il n'est pas vide et possible affichage du/des projectile/s.
        """
        if not groupe_sprite.sprites():  # Si le groupe de sprites est vide
            # On vérifie que ce n'est pas le joueur qui est éliminé comme ça on indente self.level de 1 et on passe au niveau suivant
            if groupe_sprite == self.groupe_ennemis:
                self.level += 1
                # On met à jour le niveau où le joueur se trouve
                modifier_valeur_json("../json/data.json", self.nom_sauvegarde, "level", self.level)
                # Vérifier que l'utilisateur n'a pas fini tous les niveaux
                if self.level>25:
                    self.fin_jeu()
                    return # Quitter la fonction
            else:
                # Lecture et affichage d'une vidéo de game over
                video_game_over = VideoFileClip("../graphisme/video/game_over.mp4").resize((self.longueur_fenetre, self.largeur_fenetre))
                video_game_over.preview()
                self.lancer_musique("../musique/musique_puissante.mp3", 0.05)
            
            # On met à jour les infos sur le joueur
            self.info_joueur()
            # On met à jour le niveau
            self.placer_joueur_ennemis_et_recuperer_map()
        else:
            # Si le groupe de sprites n'est pas vide, on boucle sur chaque sprite
            for sprite in groupe_sprite:
                if sprite.vie <= 0:
                    # Si la vie du sprite est inférieure ou égale à 0, on le supprime
                    groupe_sprite.remove(sprite)
                else:
                    if groupe_sprite != self.groupe_joueur:
                        # Si le sprite n'appartient pas au groupe de joueurs, on met à jour sa position en fonction de la position du joueur ou du joueur 2
                        if self.presence_2_joueur and self.joueur.vie == 0:# Si il y a deux joueur et que le joueur est mort, alors on déplace l'ennemi vers le joueur 2
                            sprite.update(self.joueur2, self.groupe_murs)
                        else:
                            sprite.update(self.joueur, self.groupe_murs)# Sinon on le déplace vers le joueur 1
                    else:
                        # Si le sprite appartient au groupe de joueurs, on met à jour sa position en fonction de la taille de l'écran
                        sprite.update(self.ecran.get_size(), self.groupe_murs)

                    # On affiche le sprite à l'écran
                    self.ecran.blit(sprite.image, sprite.rect)
                    # On met à jour la position des projectiles du sprite
                    sprite.projectiles.update(self.groupe_murs, groupe_adversaire)
                    sprite.projectiles.draw(self.ecran)
        
        
    def info_joueur(self):
        """
        Permet de garder en mémoire le nom de la sauvegarde de l'utilisateur, son pseudo et son niveau.
        
        entrée --> self : l'objet Jeu.
                   
        sortie --> Modification ou création des variables : self.nom_sauvegarde, self.pseudo et self.level.
        """
        self.nom_sauvegarde = lire_fichier_txt("../txt/nom_sauvegarde.txt")
        # Garde en mémoire le dictionnaire ou il y a tout les informations des différents utilisateur
        donnees = charger_donnees_json("../json/data.json")
        
        # On récupère le pseudo de l'utilisateur
        self.pseudo = donnees[self.nom_sauvegarde]["name"]
        
        # On récupère le niveau de l'utilisateur
        self.level = donnees[self.nom_sauvegarde]["level"]
        
    
    def placer_joueur_ennemis_et_recuperer_map(self):
        """
        Place les joueurs et les ennemis sur la carte en fonction du niveau actuel et récupère les informations de la map, du joueur et des l'ennemis
        depuis le fichier 'level.json'.
        
        entrée --> self : l'objet Jeu.
                   
        sortie --> Modification ou création des variables :
                    - self.joueur.
                    - self.groupe_joueur.
                    - self.groupe_ennemis.
                    - self.carte_niveau.
                    - self.map.
                    - self.presence_2_joueur.
        """
        # Garde en mémoire le dictionnaire ou il y a les différentes informations sur les niveaux
        donnees = charger_donnees_json("../json/level.json")
        # Eval() permet d'évaluer une chaîne de caractères et de renvoyer le résultat de cette expression
        self.joueur = eval(donnees[str(self.level)]["joueur"])
        self.groupe_joueur = pygame.sprite.Group(self.joueur)
        self.groupe_ennemis = eval(donnees[str(self.level)]["ennemi"])
        self.carte_niveau = donnees[str(self.level)]["map"]
        self.map = Map(self.longueur_fenetre, self.largeur_fenetre, self.tab_déco, self.carte_niveau)
        self.presence_2_joueur = False
        
        
    def info_joueur_2(self):
        """
        Permet de créer un deuxième joueur si sa couleur de tank est enregistrer dans un fichier TXT.
        
        entrée --> self : l'objet Jeu.
        
        sortie --> Rien ou création d'un deuxième joueur.
        """
        if self.presence_2_joueur == False:
            couleur_2_joueur = lire_fichier_txt("../txt/info_joueur2.txt")
            if couleur_2_joueur != "":
                self.joueur2 = Joueur(Vector2(self.longueur_fenetre*1/4, self.largeur_fenetre*3/5), 2, '../graphisme/tank/tank_'+couleur_2_joueur+'.png', 1, self.longueur_fenetre)
                self.groupe_joueur.add(self.joueur2)
                self.presence_2_joueur = True
        
        
    def revenir_ecran_accueil(self):
        """
        Permet de revenir à l'écran d'accueil.
        
        entrée --> self : l'objet Jeu.
        
        sortie --> Modification des variables : self.ecran_jeu, self.ecran_chargement_compte, self.ecran_1vs1, self.ecran_accueil.
        """
        self.ecran_jeu = False
        self.ecran_chargement_compte = False
        self.ecran_1vs1 = False
        # Mettre la variable self.ecran_accueil à True pour rentrer dans la boucle qui gère l'écran d'accueil
        self.ecran_accueil = True
        
        
    def fin_jeu(self):
        """
        Jouer la vidéo pour indiquer que l'utilisateur à finit tout les niveaux et revenir à l'écran d'accueil.
        
        entrée --> self : l'objet Jeu.
        
        sortie --> Affichage de la vidéo finish et retour à l'écran d'accueil.
        """
        video_finish = VideoFileClip("../graphisme/video/finish.mp4").resize((self.longueur_fenetre, self.largeur_fenetre))
        video_finish.preview()
        # On lance la musique de base de fond du jeu
        self.lancer_musique("../musique/musique_puissante.mp3", 0.05)
        self.revenir_ecran_accueil()
        
        
    def evenements(self):
        """
        Gère les événements Pygame enregistrés dans la file d'événements Pygame.
        Cette fonction parcourt la liste des événements Pygame et exécute les actions associées en fonction du type d'événement.
        
        - Si l'événement est de type QUIT (fermeture de la fenêtre) ou si la touche Echap est enfoncée, la variable self.continuer est mise à False, ce qui arrête la boucle principale du jeu.
        - Si l'événement est de type MOUSEBUTTONUP (relâchement d'un bouton de la souris) et que le bouton relâché est le bouton gauche de la souris :
            - Si le bouton des paramètres a été cliqué, la fonction choix_parametre() est appelée.
            - Si l'écran d'accueil est affiché et que le bouton Play a été cliqué, l'écran d'accueil est désactivé et l'écran de chargement du compte est activé.
            - Si l'écran de chargement de compte est affiché et que le bouton de chargement de compte a été cliqué, le compte de l'utilisateur est chargé à partir des fichiers "data.json" et "nom_sauvegarde.txt", les informations sur le joueur sont mises à jour et le jeu commence.
              Si le bouton de création d'un nouveau compte a été cliqué, une nouvelle partie est créée en écrasant les fichiers "data.json" et "nom_sauvegarde.txt".
        - Si l'écran de jeu est affiché et que la touche d'un clavier est enfoncée, la variable pressed correspondante du joueur est mise à True.
        - Si l'écran de jeu est affiché et que la touche d'un clavier est relâchée, la variable pressed correspondante du joueur est mise à False.
        - Si l'événementest de type MOUSEMOTION on vérifie que un bouton qui peut changer de couleur est survolé, si il est survolé on change sa couleur, sinon on le remet à sa couleur initial.
        """
        key = pygame.key.get_pressed()# Raccourcie pour les touches
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                # On arrête la musique si elle est en cour
                pygame.mixer.music.stop()
                # On met le fichier info_joueur2.txt vide
                ecrire_fichier_txt('../txt/info_joueur2.txt', "")
                self.continuer = False
                    
            elif evenement.type == pygame.MOUSEBUTTONUP: # Quand on relache le bouton
                if evenement.button == 1: # 1= clique gauche
                    if self.parametre[1].collidepoint(evenement.pos):
                        lanceur_parametre(self.longueur_fenetre, self.largeur_fenetre)
                    
                    elif self.bouton_home[1].collidepoint(evenement.pos):
                        self.revenir_ecran_accueil()
                    elif self.bouton_aide[1].collidepoint(evenement.pos):
                        self.fenetre_aide()
                        
                    elif self.ecran_accueil:
                        if self.bouton_play[1].collidepoint(evenement.pos):
                            self.ecran_accueil = False
                            self.ecran_chargement_compte = True
                            
                        elif self.bouton_1vs1[1].collidepoint(evenement.pos):
                            # Garde en mémoire le dictionnaire ou il y a les différentes informations sur les niveaux
                            donnees = charger_donnees_json("../json/level.json")
                            
                            # Récupération de la map et enregistrement avec les collisions dans une variable
                            self.carte_niveau = donnees["1vs1"]["map"]
                            self.map = Map(self.longueur_fenetre, self.largeur_fenetre, self.tab_déco, self.carte_niveau)
                            
                            # Création de deux joueurs pour le mode 1vs1
                            self.joueur =  Joueur(Vector2(self.longueur_fenetre*1/5, self.largeur_fenetre/2), 1, '../graphisme/tank/tank_bas3.png', 4, self.longueur_fenetre)
                            self.joueur2 = Joueur(Vector2(self.longueur_fenetre*4/5, self.largeur_fenetre/2), 2, '../graphisme/tank/tank_violet.png', 1, self.longueur_fenetre)
                            # Création de groupe pour que lorsqu'on appel projectile.update du joueur 1 ou 2, il a un élément itérable pour si il y a une collision entre l'adversaire et le tir
                            self.groupe_joueur1 = pygame.sprite.Group(self.joueur)
                            self.groupe_joueur2 = pygame.sprite.Group(self.joueur2)
                            
                            # Création d'un groupe qui contient les deux joueurs pour qu'on puisse gérer les événements liés aux touches
                            self.groupe_joueur = pygame.sprite.Group(self.joueur, self.joueur2)
                            
                            # Garder en mémoire le nombre de victoire de chaque joueur
                            self.victoire_joueur = 0
                            self.victoire_joueur2 = 0
                            
                            self.ecran_accueil = False
                            self.ecran_1vs1 = True
                            
                    elif self.ecran_chargement_compte:
                        if self.bouton_chargement_compte[1].collidepoint(evenement.pos):
                            chargement_compte = ChargementCompte("../json/data.json", "../txt/nom_sauvegarde.txt", self.longueur_fenetre)
                            chargement_compte.mainloop()
                            self.info_joueur()
                            
                            # On vérifie que l'utilisateur n'a pas fini tous les niveaux
                            if self.level>25:
                                # Si le joueur à finit le jeu, on le dirige vers l'écran d'accueil
                                self.fin_jeu()
                            else:
                                self.placer_joueur_ennemis_et_recuperer_map()
                                self.ecran_chargement_compte = False
                                self.ecran_jeu = True
                            
                        elif self.bouton_nouveau_compte[1].collidepoint(evenement.pos):
                            nouvelle_partie = NouvellePartie("../json/data.json", self.longueur_fenetre)
                            nouvelle_partie.mainloop()
            
            # Si il y a un mouvement de la souris
            elif evenement.type == pygame.MOUSEMOTION:
                # Si on est actuellement à l'écran d'accueil
                if self.ecran_accueil:
                    if self.bouton_play[1].collidepoint(evenement.pos):
                        self.bouton_play[0] = self.IMAGE_BOUTON_PLAY_HOVER
                    else:
                        self.bouton_play[0] = self.IMAGE_BOUTON_PLAY
                        
                    if self.bouton_1vs1[1].collidepoint(evenement.pos):
                        self.bouton_1vs1[0] =  self.IMAGE_BOUTON_1VS1_HOVER
                    else:
                        self.bouton_1vs1[0] = self.IMAGE_BOUTON_1VS1
                # Si on est à l'écran de chargement de compte
                elif self.ecran_chargement_compte:
                    if self.bouton_chargement_compte[1].collidepoint(evenement.pos):
                        self.bouton_chargement_compte[0] = self.IMAGE_BOUTON_CHARGEMENT_COMPTE_HOVER
                    else:
                        self.bouton_chargement_compte[0] = self.IMAGE_BOUTON_CHARGEMENT_COMPTE
                        
                    if self.bouton_nouveau_compte[1].collidepoint(evenement.pos):
                        self.bouton_nouveau_compte[0] = self.IMAGE_BOUTON_NOUVEAU_COMPTE_HOVER
                    else:
                        self.bouton_nouveau_compte[0] = self.IMAGE_BOUTON_NOUVEAU_COMPTE
                        
            elif self.ecran_jeu or self.ecran_1vs1:
                for joueur in self.groupe_joueur:
                    if evenement.type == pygame.KEYDOWN:
                        joueur.pressed[evenement.key] = True
                    elif evenement.type == pygame.KEYUP:
                        joueur.pressed[evenement.key] = False
          
          
    def bouton_clickable(self,x, y, longueur, largeur, chemin_image):
        """
        La fonction bouton_clickable permet de créer et de renvoyer un tuple contenant l'image du bouton et
        les informations sur son objet Rect correspondant, de manière à ce que ce bouton soit cliquable.
        
        entrée --> self : l'objet Jeu.
                   x(int ou float) : abcsisse de la position du coin nord ouest du bouton.
                   y(int ou float) : entier qui sera l'ordonné de la position du coin nord ouest du bouton.
                   longueur(int ou float) : entier qui sera la longueur du bouton.
                   largeur(int ou float) : entier qui sera la largeur du bouton.
                   chemin_image(chaine de caractères) : chemin d'accès de l'image qu'on veut charger.
                   
        sortie --> la fonction renvoie une liste contenant les informations de l'objet qui a été créé selon les arguments mis, l'image et le Rect de l'image.
        """
        # Charge l'image et la redimensionne
        image =  pygame.transform.scale(pygame.image.load(chemin_image), (longueur, largeur))
        
        # Récupère le rectangle de collision de l'image
        image_rect = image.get_rect()
        
        # Modifie les coordonnées du centre du rectangle de collision de l'image
        image_rect.centerx = x
        image_rect.centery = y
        
        # Renvoie une liste qui contient une image et son rectangle de collision
        return [image, image_rect]
    
    
    def lancer_musique(self, chemin, volume):
        """
        Lance la musique "chemin" en boucle et on modifie son volume sonore.
        
        entrée --> self : l'objet Jeu.
                   chemin(chaîne de caractères) : chemin d'accès de la musique qu'on veut lancer.
                   volume(int ou float) : niveau du volume de la musique, entre 0 et 1, qu'on veut lancer.
        
        sortie --> Modification de la musique joué en fond.
        """
        pygame.mixer.music.load(chemin)
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(volume)
        
        
    def ouvrir_discord(self):
        """
        Ouvre une page web et dirige l'utilisateur vers un lien discord qui correspond à un serveur où il pourra poser des questions.
        
        entrée --> self : l'objet Jeu.
        
        sortie --> Ouverture d'une page web et dirige l'utilisateur à "https://discord.gg/bAdqTwud2Q".
        """
        webbrowser.open("https://discord.gg/bAdqTwud2Q")
        
        
    def ouvrir_site(self):
        """
        Ouvre une page web et dirige l'utilisateur vers un lien qui correspond au site du jeu.
        Une fois sur le site, il pourra télécharger les dernières versions du jeu et suivre les actualités.
        
        entrée --> self : l'objet Jeu.
        
        sortie --> Ouverture d'une page web et dirige l'utilisateur vers le site de Tankmania.
        """
        webbrowser.open("https://headeraser413.wixsite.com/tankmania")
        
        
    def fenetre_aide(self):
        """
        Crée une fenêtre aide avec tkinter.
        Il y a deux liens, un pour diriger l'utilisateur vers le site Tankmania et l'autre pour diriger
        l'utilisateur vers le serveur discord Tankmania.
        
        entrée --> self : l'objet Jeu.
        
        sortie --> Affichage d'une fenêtre tkinter.
        """
        igu = tk.Tk()
        
        # on définit la longueur et la largeur de la fenêtre tkinter selon la taille de l'écran de l'utilisateur et un coefficient
        longueur_fenetre_tkinter = round(self.longueur_fenetre * 300/1366)
        largeur_fenetre = round(self.longueur_fenetre * 150/1366)
        
        # Centrer la fenetre
        igu.geometry(str(longueur_fenetre_tkinter)+"x"+str(largeur_fenetre)+"+{}+{}".format(int(igu.winfo_screenwidth() / 2 - longueur_fenetre_tkinter/2), int(igu.winfo_screenheight() / 2 - largeur_fenetre/2)))
        
        # Création des widgets
        label_aide = tk.Label(igu, text="BESOIN D'AIDE ?", width=int(self.longueur_fenetre * 40/1366), font=("Helvetica", round(longueur_fenetre_tkinter/25)), fg="#2C5234")
        lien_label_aide = tk.Label(igu, text="Cliquez ici pour trouver de l'aide", fg="blue", cursor="hand2")
        label_site = tk.Label(igu, text="DERNIÈRE VERSION DU JEU", width=int(self.longueur_fenetre * 40/1366), font=("Helvetica", round(longueur_fenetre_tkinter/25)), fg="#2C5234")
        lien_label_site = tk.Label(igu, text="Cliquez ici visiter notre site", fg="blue", cursor="hand2")
        bouton_quitter = tk.Button(igu, text="QUITTER", font=("Helvetica", int(igu.winfo_screenheight() * 0.02)), bg="#8CB369", fg="white", command=igu.destroy)
        
        # Affichage des widgets
        label_aide.pack()
        lien_label_aide.pack()
        label_site.pack()
        lien_label_site.pack()
        bouton_quitter.pack(side="bottom", pady=int(igu.winfo_screenheight() * 0.005))
        
        # Configurer les widgets qui servent de liens
        lien_label_aide.bind("<Button-1>", lambda e: self.ouvrir_discord())# "<Button-1>" correspond au clic gauche de la souris
        lien_label_site.bind("<Button-1>", lambda e: self.ouvrir_site())
        
        igu.mainloop()
