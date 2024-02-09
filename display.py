import pygame as pg
import numpy as np
import json
from world import *
import time

class GridDisplay:
    def __init__(self, grid, cell_size, screen_size=(1920, 1080)) -> None:
        pg.init()
        self.grid = grid
        self.cell_size = cell_size
        self.screen = pg.display.set_mode(screen_size)
        self.screen_size = screen_size
        self.clock = pg.time.Clock()
        self.config = self.load_config("config.json")
        self.tiles = self.load_tiles()
    
    def load_config(self, config_file: str) -> None:
        with open(config_file, "r") as file:
            return json.load(file)
        
    def load_tiles(self) -> None:
        tiles = {}
        for tile_type, path in self.config["TilesPath"].items():
            tiles[tile_type] = pg.image.load(path).convert()
        print(tiles)
        return tiles

    def draw_grid(self) -> None:
        self.screen.fill((255, 255, 255))

        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                tile_type = self.grid[i, j].case_type
                tile_image = self.tiles.get(tile_type)
                resized_image = pg.transform.scale(tile_image, (self.cell_size, self.cell_size))
                cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                self.screen.blit(resized_image, cell_rect)
        pg.display.flip()

    def run(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.draw_grid()
            self.clock.tick(10) # 10 FPS
        pg.quit()







# EXEMPLE TEST DE BOUCLE DE GAMEPLAY

monde = World(60, 60)
monde.create_world("World data/background.txt")
grid_display = GridDisplay(monde.get_grid, cell_size=20)  # Taille d'une case en pixels
clock = pg.time.Clock()

while True:

    monde.set_case(15, 15, "C")
    grid_display.draw_grid()
    monde.set_case(15, 15, "S")
    grid_display.draw_grid()  # Update the display with the modified grid
    clock.tick(10)  # 10 FPS