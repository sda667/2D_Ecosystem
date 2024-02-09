import pygame as pg
import numpy as np
import json
from world import *
import time
import threading

class GridDisplay:
    """
    Classe permettant d'afficher la grille du monde
    """
    def __init__(self, grid, cell_size, screen_size=(1920, 1080)) -> None:
        pg.init()
        self.grid = grid
        self.cell_size = cell_size
        self.screen = pg.display.set_mode(screen_size)
        self.screen_size = screen_size
        self.clock = pg.time.Clock()
        self.config = self.__load_config("config.json")
        self.tiles = self.__load_tiles()
    
    # CHARGER LA CONFIGURATION (FICHIER JSON)
    def __load_config(self, config_file: str) -> None:
        with open(config_file, "r") as file:
            return json.load(file)
    
    # CHARGER LES CHEMINS DES IMAGES DES CASES (DEPUIS LA CONFIGURATION)
    def __load_tiles(self) -> None:
        tiles = {}
        for tile_type, path in self.config["TilesPath"].items():
            tiles[tile_type] = pg.image.load(path).convert()
        print(tiles)
        return tiles

    # AFFICHER LA GRILLE
    def __draw_grid(self) -> None:
        # Couleur de fond
        self.screen.fill((255, 255, 255))
        # Affichage des cases
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                # Récupération de l'image de la case
                tile_type = self.grid[i, j].case_type
                tile_image = self.tiles.get(tile_type)
                # Redimensionnement de l'image
                resized_image = pg.transform.scale(tile_image, (self.cell_size, self.cell_size))
                # Affichage de l'image
                cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                self.screen.blit(resized_image, cell_rect)
        pg.display.flip()

    # AFFICHER LA GRILLE EN BOUCLE
    def __start_display(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.__draw_grid()
            self.clock.tick(10) # 10 FPS
        pg.quit()

    # LANCER L'AFFICHAGE DANS UN THREAD (METHODE A APPELER DANS LE MAIN)
    def run(self) -> None:
        thread = threading.Thread(target=self.__start_display, daemon=True)
        thread.start()






# EXEMPLE TEST DE BOUCLE DE GAMEPLAY

monde = World(60, 60)
monde.create_world("World data/background.txt")
grid_display = GridDisplay(monde.get_grid, cell_size=20)  # Taille d'une case en pixels
grid_display.run()

while True:

    monde.set_case(15, 15, "C")
    time.sleep(1)
    monde.set_case(15, 15, "S")
    time.sleep(1)