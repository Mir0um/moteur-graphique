import time
import platform
from keyboard_library import KeyboardController  # Importer notre bibliothèque personnalisée
import moteur_graphique as mg
from lib_math import *

# Initialisation de la caméra et de la source de lumière
cam = mg.Camera(vec3(-1000, 0, -500), 0.0, -2.0,2)
light = mg.LightSource(vec3(0, 20, 0))

# Chargement du mesh du cube
cube = mg.loadObj("ele.obj")

def process_input(controller, dt):
    """
    Traite les événements de touches et met à jour la caméra en conséquence.

    Args:
        controller (KeyboardController): Instance du contrôleur clavier.
        dt (float): Delta temps depuis la dernière mise à jour.
    
    Returns:
        bool: False si la touche ESC est pressée pour quitter, True sinon.
    """
    key_info = controller.get_key()
    if key_info:
        key_type, key = key_info
        if key_type == 'normal':
            if key.lower() == 'z':
                cam.position += cam.getForwardDirection() * 0.01 * dt
            elif key.lower() == 's':
                cam.position -= cam.getForwardDirection() * 0.01 * dt
            elif key.lower() == 'd':
                cam.position += cam.getRightDirection() * 0.01 * dt
            elif key.lower() == 'q':
                cam.position -= cam.getRightDirection() * 0.01 * dt
            elif key == ' ':
                cam.position.y += 0.01 * dt
            elif key.lower() == 'c':
                cam.position.y -= 0.01 * dt
            elif key == '\x1b':  # Touche ESC
                print("Touche ESC détectée. Fermeture du programme.")
                return False
        elif key_type == 'special':
            # Gérer les touches spéciales comme les flèches
            if platform.system() == 'Windows':
                # Sous Windows, les touches spéciales sont renvoyées sous forme de bytes
                if key == b'\xe0H':  # Flèche Haut
                    if cam.pitch < 1.57:
                        cam.pitch += 0.01 * dt
                elif key == b'\xe0P':  # Flèche Bas
                    if cam.pitch > -1.57:
                        cam.pitch -= 0.01 * dt
                elif key == b'\xe0K':  # Flèche Gauche
                    cam.yaw += 0.01 * dt
                elif key == b'\xe0M':  # Flèche Droite
                    cam.yaw -= 0.01 * dt
            else:
                # Sous Unix-like, les touches spéciales sont des séquences d'échappement
                if key == 'A':  # Flèche Haut
                    if cam.pitch < 1.57:
                        cam.pitch += 0.01 * dt
                elif key == 'B':  # Flèche Bas
                    if cam.pitch > -1.57:
                        cam.pitch -= 0.01 * dt
                elif key == 'D':  # Flèche Gauche
                    cam.yaw += 0.01 * dt
                elif key == 'C':  # Flèche Droite
                    cam.yaw -= 0.01 * dt
    return True

def main():
    """
    Fonction principale qui initialise le contrôleur clavier et gère la boucle principale.
    """
    print("Appuyez sur les touches pour voir lesquelles sont pressées (Appuyez sur ESC pour quitter).")
    controller = KeyboardController()  # Initialiser le contrôleur clavier
    try:
        last = time.time()
        running = True
        while running:
            current = time.time()
            dt = (current - last) * 500  # Calculer le delta temps (ajusté comme dans le script original)
            last = current

            # Traiter les entrées clavier
            running = process_input(controller, dt)

            # Effacer l'écran
            mg.clear(' ')

            # Afficher le mesh du cube avec la caméra et la lumière
            mg.putMesh(cube, cam, light)

            # Dessiner le frame
            mg.draw()

            # Petite pause pour limiter l'utilisation CPU
            time.sleep(0.033)
    except KeyboardInterrupt:
        print("\nInterruption clavier détectée. Fermeture du programme.")
    finally:
        controller.stop()  # Arrêter le thread du contrôleur clavier

if __name__ == "__main__":
    main()
