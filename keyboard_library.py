import sys
import threading
import time
import platform

# Importer les modules spécifiques au système d'exploitation
if platform.system() == 'Windows':
    import msvcrt  # Module pour la gestion des entrées clavier sous Windows
else:
    import select   # Module pour surveiller les entrées sous Unix
    import tty      # Module pour configurer le terminal
    import termios  # Module pour les attributs du terminal

class KeyboardController:
    """
    Classe pour contrôler et lire les entrées du clavier en arrière-plan.
    Fonctionne à la fois sous Windows et les systèmes Unix-like.
    """

    def __init__(self):
        """
        Initialisation du contrôleur clavier.
        Démarre un thread pour lire les touches en continu.
        """
        self.key = None           # Variable pour stocker la dernière touche pressée
        self.running = True       # Indicateur pour contrôler l'exécution du thread
        self.thread = threading.Thread(target=self.read_key)  # Création du thread
        self.thread.daemon = True  # Permet au thread de se fermer avec le programme principal
        self.thread.start()         # Démarrage du thread

    def read_key(self):
        """
        Méthode exécutée dans un thread séparé pour lire les touches du clavier.
        Gère les différences entre Windows et les systèmes Unix-like.
        """
        if platform.system() == 'Windows':
            self._read_key_windows()
        else:
            self._read_key_unix()

    def _read_key_windows(self):
        """
        Lecture des touches sous Windows en utilisant le module msvcrt.
        """
        while self.running:
            if msvcrt.kbhit():  # Vérifie si une touche a été pressée
                first_char = msvcrt.getch()  # Lit le premier caractère
                if first_char in (b'\x00', b'\xe0'):
                    # Une touche spéciale a été pressée (comme les flèches)
                    second_char = msvcrt.getch()  # Lit le deuxième caractère
                    self.key = ('special', first_char + second_char)  # Stocke la touche spéciale
                else:
                    # Une touche normale a été pressée
                    try:
                        decoded_char = first_char.decode('utf-8', errors='ignore')
                    except UnicodeDecodeError:
                        decoded_char = ''  # En cas d'erreur de décodage
                    self.key = ('normal', decoded_char)  # Stocke la touche normale
            time.sleep(0.01)  # Petite pause pour éviter une utilisation CPU excessive

    
    def _read_key_unix(self):
        """
        Lecture des touches sous Unix-like en utilisant les modules select, tty et termios.
        """
        fd = sys.stdin.fileno()  # Obtenir le descripteur de fichier standard d'entrée
        old_settings = termios.tcgetattr(fd)  # Sauvegarder les paramètres actuels du terminal
        try:
            tty.setcbreak(fd)  # Configurer le terminal en mode cbreak (lecture caractère par caractère)
            while self.running:
                # Utiliser select pour vérifier si une touche a été pressée
                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                if rlist:
                    ch1 = sys.stdin.read(1)  # Lire le premier caractère
                    if ch1 == '\x1b':
                        # Détecter une séquence d'échappement (comme les flèches)
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[':
                            ch3 = sys.stdin.read(1)
                            if ch3 in 'ABCD':
                                self.key = ('special', ch3)
                            else:
                                self.key = ('special', ch1 + ch2 + ch3)  # Autres séquences spéciales
                        else:
                            self.key = ('escape', ch1 + ch2)  # Séquence d'échappement simple
                    else:
                        self.key = ('normal', ch1)  # Touche normale
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restaurer les paramètres du terminal

    def get_key(self):
        """
        Récupère la dernière touche pressée et réinitialise la variable key.
        
        Returns:
            tuple or None: Un tuple contenant le type de touche ('normal', 'special', 'escape')
                           et la valeur de la touche, ou None si aucune touche n'a été pressée.
        """
        key = self.key
        self.key = None  # Réinitialiser la touche après la lecture
        return key

    def stop(self):
        """
        Arrête le thread de lecture des touches et attend sa terminaison.
        """
        self.running = False  # Indiquer au thread de s'arrêter
        self.thread.join()    # Attendre que le thread se termine
