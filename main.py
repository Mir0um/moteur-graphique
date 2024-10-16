import time
import platform
from keyboard_library import KeyboardController  # Importer notre bibliothèque personnalisée
import moteur_graphique as mg
from lib_math import *
import math

# Initialisation de la caméra et de la source de lumière
cam = mg.Camera(vec3(0, 6, 15), 0.0, 3.2)
light = mg.LightSource(vec3(0, 5, 0))

sunlight = mg.LightSource(vec3(4, 20, 20), (255, 255, 170),0.8)  # Soleil jaune
lamp = mg.LightSource(vec3(0, 5, 0), (0, 0, 255),0.4)   # Lampe bleu
lamp2 = mg.LightSource(vec3(0, 5, 0), (255, 0, 0),0.4)   # Lampe rouge
sunlight2 = mg.LightSource(vec3(-4, -20, -20), (255, 255, 170),0.8)  # Soleil jaune


lights = [sunlight,lamp,lamp2,sunlight2]

# Chargement du mesh du cube
cube = mg.loadObj("Man.obj")

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
            elif key == "j":
                cam.focalLenth += 0.1
            elif key == 'k':
                cam.focalLenth-= 0.1
            elif key == '\x1b' or key == '\x1b\x1b':  # Touche ESC
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

def animate_lights(t, lights):
    t += 0.1
    t %= 6  # Réinitialiser t pour éviter qu'il ne devienne trop grand

    # Calculer une seule fois les fonctions trigonométriques
    sin_t = math.sin(t) * 2.5
    cos_t = math.cos(t) * 2.5

    # Positionner la première lampe bleue
    lights[1].position.x = sin_t
    lights[1].position.z = cos_t + 7

    # Positionner la deuxième lampe rouge face à la première
    lights[2].position.x = -sin_t
    lights[2].position.z = -cos_t + 7

    return t

def main():
    """
    Fonction principale qui initialise le contrôleur clavier et gère la boucle principale.
    """
    print("Appuyez sur les touches pour voir lesquelles sont pressées (Appuyez sur ESC pour quitter).")
    controller = KeyboardController()  # Initialiser le contrôleur clavier
    t = 0
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
            mg.putMesh(cube, cam, lights)

            # Dessiner le frame
            mg.draw()

            #animer la position de la lumière en cercle
            t = animate_lights(t, lights)


            if True: #print info
                print(mg.color(255,255,255) + "time", t,  "light", light.position.printco(),"cam", cam.position.printco(), "camdir", (cam.pitch, cam.yaw),"FOV", (cam.focalLenth))
            else:
                print()

            # Petite pause pour limiter l'utilisation CPU
            time.sleep(0.033)
    except KeyboardInterrupt:
        print("\nInterruption clavier détectée. Fermeture du programme.")
    finally:
        controller.stop()  # Arrêter le thread du contrôleur clavier

if __name__ == "__main__":
    main()
