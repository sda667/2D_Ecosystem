import queue

import pygame

from display import GridDisplay
from world import *
from Controller import Controller
import time
import threading
# MAIN TEST
def main(cell_size=15, x_size=60, y_size=120, seed=time.time()) -> None:
    # Taille de la fenêtre
    screen_size = (y_size * cell_size, x_size * cell_size)
    # Initialisation du monde
    monde = World(x_size, y_size, seed)
    generate_entities("World data/entities.txt")
    monde.generate_world("World data/entities.txt")
    event_queue = queue.Queue()
    grid_display = GridDisplay(monde, cell_size=cell_size, screen_size=screen_size)  # Taille d'une case en pixels
    thread = threading.Thread(target=grid_display.start_display, args=(event_queue,), daemon=True)
    thread.start()
    # Initialisation du contrôleur
    controleur = Controller(monde)
    timer = 0
    while True:
        for event in pygame.event.get():
            event_queue.put(event)
        timer += 1
        # TODO change the value to change the number of turn to update the graph
        if (timer % 10 == 0):
            grid_display.count_current_elements()
            timer %= 10
        # TODO change the value to change the time each turn take
        time.sleep(0.2)
        controleur.update_entities()
        controleur.plankton_update()
        if not thread.is_alive():
            pygame.quit()
            exit()


if __name__ == "__main__":
    main()
