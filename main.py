import time
import platform
import sys
import os
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


lights = [sunlight, lamp, lamp2, sunlight2]


def select_obj_file() -> str:
    """Return the name of an OBJ file chosen by the user or automatically."""
    obj_files = [f for f in os.listdir("object") if f.endswith(".obj")]
    if not obj_files:
        raise FileNotFoundError("No .obj files found in 'object' directory")

    if not sys.stdin.isatty():
        # Non-interactive mode - choose the first file
        print(f"Automatically selecting {obj_files[0]}")
        return obj_files[0]

    print("Select an OBJ file:")
    for idx, name in enumerate(obj_files, start=1):
        print(f"{idx}. {name}")

    while True:
        choice = input("Enter number: ")
        try:
            index = int(choice) - 1
        except ValueError:
            index = -1
        if 0 <= index < len(obj_files):
            return obj_files[index]
        print("Invalid selection. Try again.")


# Chargement du mesh du cube
cube = mg.loadObj(select_obj_file())


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
            elif key.lower() == 'o':
                state = mg.toggle_ambient_occlusion()
                print("Ambient occlusion:", "on" if state else "off")
            elif key.lower() == 'p':
                state = mg.toggle_specular()
                print("Specular lighting:", "on" if state else "off")
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
    obj_file = select_obj_file()
    mesh = mg.loadObj(obj_file)

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

            # Afficher le mesh sélectionné avec la caméra et la lumière
            mg.putMesh(mesh, cam, lights)

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
