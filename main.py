from display import GridDisplay
import pygame as pg
import json
from world import *
import time
import threading
from Controller import controller


# MAIN TEST
def main(cell_size=15, x_size = 60, y_size=120) -> None:
    # Taille de la fenêtre
    screen_size = (y_size*cell_size, x_size*cell_size)
    # Initialisation du monde
    monde = World(x_size, y_size)
    monde.generate_world("World data/entities.txt")

    
    grid_display = GridDisplay(monde, cell_size=cell_size, screen_size=screen_size)  # Taille d'une case en pixels
    grid_display.run()

    # Initialisation du contrôleur

    controleur = controller(monde)
    plankton_update_timer = 0
    # Boucle d'action du monde (plus besoin de toucher à l'affichage)
    while True:
        plankton_update_timer+=1
        # TODO change the value to change the time each turn take
        time.sleep(0.2)
        controleur.update_entities()
        if plankton_update_timer%10 == 0 :
            plankton_update_timer%= 10
            controleur.plankton_update()

if __name__ == "__main__":
  main()