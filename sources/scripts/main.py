from jeu import Jeu

def main():
    """
    Cette fonction permet de lancer le jeu.
    Elle crée une instance de la classe Jeu et exécute la méthode run() de cette instance.
    
    sortie --> lance le jeu en exécutant sa méthode run().
    """
    jeu = Jeu()
    jeu.run()

# Vérifier si le programme est exécuté en tant que script principal et appeler la fonction "main()"
if __name__ == "__main__":
    main()