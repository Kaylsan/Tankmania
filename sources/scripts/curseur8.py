import pygame


def curseur(couleur_rgb, ecran):
    """
    permet de faire un curseur en croix, avec la couleur rgb choisit.
    
    entrée --> couleur_rgb(tuple) : intensité des couleurs rouge ensuite vert et ensuite bleu. L'intensité est un entier qui vari entre 0 et 255.
               ecran(pygame.Surface) : surface graphique pouvant être dessinée dessus.
               
    sortie --> affichage d'un curseur sous la forme d'une croix.
    """
    # Récupérer la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Dessiner le curseur en forme de croix à la position de la souris
    pygame.draw.line(ecran, couleur_rgb, (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 2)
    pygame.draw.line(ecran, couleur_rgb, (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 2)
    
    #On rend invisible la souris
    pygame.mouse.set_visible(False)