import time
import platform
import sys
import os
from keyboard_library import KeyboardController  # Importer la bibliothèque personnalisée
import moteur_graphique as mg
from lib_math import *
import math

DEBUG = False

NORMAL_ACTIONS = {}
SPECIAL_ACTIONS_WINDOWS = {}
SPECIAL_ACTIONS_UNIX = {}


def move(direction, dt):
    cam.position += direction * 0.01 * dt


def adjust_height(amount, dt):
    cam.position.y += amount * 0.01 * dt


def change_focal(amount):
    cam.focalLenth += amount


def toggle_ao():
    state = mg.toggle_ambient_occlusion()
    print("Ambient occlusion:", "on" if state else "off")


def toggle_specular():
    state = mg.toggle_specular()
    print("Specular lighting:", "on" if state else "off")


def quit_program():
    print("Touche ESC détectée. Fermeture du programme.")
    return False


def adjust_pitch(amount, dt):
    new_pitch = cam.pitch + amount * 0.01 * dt
    cam.pitch = max(min(new_pitch, 1.57), -1.57)


def adjust_yaw(amount, dt):
    cam.yaw += amount * 0.01 * dt


def init_key_mappings():
    global NORMAL_ACTIONS, SPECIAL_ACTIONS_WINDOWS, SPECIAL_ACTIONS_UNIX
    NORMAL_ACTIONS = {
        "z": lambda dt: move(cam.getForwardDirection(), dt),
        "s": lambda dt: move(cam.getForwardDirection() * -1, dt),
        "d": lambda dt: move(cam.getRightDirection(), dt),
        "q": lambda dt: move(cam.getRightDirection() * -1, dt),
        " ": lambda dt: adjust_height(1, dt),
        "c": lambda dt: adjust_height(-1, dt),
        "j": lambda dt: change_focal(0.1),
        "k": lambda dt: change_focal(-0.1),
        "o": lambda dt: toggle_ao(),
        "p": lambda dt: toggle_specular(),
        "\x1b": lambda dt: quit_program(),
        "\x1b\x1b": lambda dt: quit_program(),
    }

    SPECIAL_ACTIONS_WINDOWS = {
        b"\xe0H": lambda dt: adjust_pitch(1, dt),
        b"\xe0P": lambda dt: adjust_pitch(-1, dt),
        b"\xe0K": lambda dt: adjust_yaw(1, dt),
        b"\xe0M": lambda dt: adjust_yaw(-1, dt),
    }

    SPECIAL_ACTIONS_UNIX = {
        "A": lambda dt: adjust_pitch(1, dt),
        "B": lambda dt: adjust_pitch(-1, dt),
        "D": lambda dt: adjust_yaw(1, dt),
        "C": lambda dt: adjust_yaw(-1, dt),
    }

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
    if not key_info:
        return True

    key_type, key = key_info

    if key_type == "normal":
        action = NORMAL_ACTIONS.get(key.lower()) if len(key) == 1 else NORMAL_ACTIONS.get(key)
        if action:
            result = action(dt)
            if result is False:
                return False

    elif key_type == "special":
        if platform.system() == "Windows":
            action = SPECIAL_ACTIONS_WINDOWS.get(key)
        else:
            action = SPECIAL_ACTIONS_UNIX.get(key)
        if action:
            action(dt)

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
    # Chargement du mesh du cube
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

            # Effacer le tampon d'affichage
            mg.clear(' ')

            # Afficher le mesh sélectionné avec la caméra et la lumière
            mg.putMesh(mesh, cam, lights)
            
            # Rafraîchir la console sans sous-processus
            mg.clear_console()

            # Dessiner le frame
            mg.draw()

            #animer la position de la lumière en cercle
            t = animate_lights(t, lights)


            if DEBUG:
                print(
                    mg.color(255, 255, 255)
                    + "time",
                    t,
                    "light",
                    light.position.printco(),
                    "cam",
                    cam.position.printco(),
                    "camdir",
                    (cam.pitch, cam.yaw),
                    "FOV",
                    cam.focalLenth,
                )
            else:
                print()

            # Petite pause pour limiter l'utilisation CPU
            time.sleep(0.033)
    except KeyboardInterrupt:
        print("\nInterruption clavier détectée. Fermeture du programme.")
    finally:
        controller.stop()  # Arrêter le thread du contrôleur clavier

if __name__ == "__main__":
    # Initialisation de la caméra et de la source de lumière
    cam = mg.Camera(vec3(0, 6, 15), 0.0, 3.2)
    light = mg.LightSource(vec3(0, 5, 0))

    sunlight = mg.LightSource(vec3(4, 20, 20), (255, 255, 170),0.8)  # Soleil jaune
    lamp = mg.LightSource(vec3(0, 5, 0), (0, 0, 255),0.4)   # Lampe bleu
    lamp2 = mg.LightSource(vec3(0, 5, 0), (255, 0, 0),0.4)   # Lampe rouge
    sunlight2 = mg.LightSource(vec3(-4, -20, -20), (255, 255, 170),0.0)  # Soleil jaune

    lights = [sunlight, lamp, lamp2, sunlight2]
    init_key_mappings()
    main()
