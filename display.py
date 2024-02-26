import random

import pygame as pg
import numpy as np
import json
from world import *
import time
import threading
import sys
from controller_ui import ControllerUI


class GridDisplay:
    """
    Classe permettant d'afficher la grille du monde
    """

    def __init__(self, world, cell_size, screen_size=(1920, 1080)) -> None:
        pg.init()
        self.world = world
        self.cell_size = cell_size
        self.screen = pg.display.set_mode(screen_size, pg.RESIZABLE)
        self.screen_size = screen_size
        self.clock = pg.time.Clock()
        self.config = self.__load_config("config.json")
        self.tiles = self.__load_tiles()
        self.entities = self.__load_entities()
        self.prev_entities = np.copy(self.world.entities)  # Copy the entities grid to compare with the next state

    # CHARGER LA CONFIGURATION (FICHIER JSON)
    def __load_config(self, config_file: str) -> None:
        with open(config_file, "r") as file:
            return json.load(file)

    # CHARGER LES CHEMINS DES IMAGES DES CASES (DEPUIS LA CONFIGURATION)
    def __load_tiles(self) -> None:
        tiles = {}
        for tile_type, path in self.config["TilesPath"].items():
            tiles[tile_type] = pg.image.load(path).convert()
        return tiles

    def __load_entities(self) -> None:
        entities = {}
        for entity_type, path in self.config["EntityPath"].items():
            entities[entity_type] = pg.image.load(path).convert_alpha()
        return entities

    # AFFICHER LA GRILLE
    def __draw_grid(self) -> None:
        # Couleur de fond

        background_image = pg.image.load("image/Ocean.png").convert()
        resized_image = pg.transform.scale(background_image,
                                           (self.screen_size[0] // 5, self.screen_size[1] // 5))  # Resize the image
        # Répéter l'image en boucle sur le haut de l'écran
        for x in range(0, self.screen_size[0], resized_image.get_width()):
            self.screen.blit(resized_image, (x, 0))
        self.screen.blit(resized_image, (0, 0))  # Position the image at the top
        # Affichage des cases
        for i in range(self.world.grid.shape[0]):
            for j in range(self.world.grid.shape[1]):
                if self.world.grid[i, j] != 0:
                    # Récupération de l'image de la case
                    tile_type = self.world.grid[i, j].case_type
                    tile_image = self.tiles.get(tile_type)
                    # Redimensionnement de l'image
                    resized_image = pg.transform.scale(tile_image, (self.cell_size, self.cell_size))
                    # Affichage de l'image
                    cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                    self.screen.blit(resized_image, cell_rect)

    # AFFICHER LES ENTITES
    def __draw_entities(self) -> None:
        for i in range(self.world.entities.shape[0]):
            for j in range(self.world.entities.shape[1]):
                # Récupération de l'image de la case
                if self.world.entities[i, j]:
                    entity = self.world.entities[i, j]
                    entity_type = entity.entity_name
                    entity_image = self.entities.get(entity_type)
                    flipped = pg.transform.flip(entity_image, True, False)
                    # Check if the entity moved to the right
                    if entity.last_movement == (1, 0):
                        image = flipped
                    else:
                        image = entity_image
                    # Redimensionnement de l'image
                    # resized_image = pg.transform.scale(image, (self.cell_size * 3, self.cell_size * 3))
                    # MOn enlève le blanc autour de l'image
                    # resized_image.set_colorkey((255, 255, 255))
                    image.set_colorkey((255, 255, 255))
                    # Affichage de l'image
                    cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                    self.screen.blit(image, cell_rect)

                    # Affichage de la barre de faim
                    hunger_bar_width = self.cell_size * 3
                    hunger_bar_height = 5
                    hunger_level = entity.hunger
                    max_hunger = 100
                    hunger_bar_rect = pg.Rect(i * self.cell_size, j * self.cell_size - hunger_bar_height,
                                              hunger_bar_width, hunger_bar_height)
                    pg.draw.rect(self.screen, (0, 255, 0), hunger_bar_rect)  # Fond de la barre de faim
                    hunger_fill_rect = pg.Rect(i * self.cell_size, j * self.cell_size - hunger_bar_height,
                                               hunger_bar_width * hunger_level / max_hunger, hunger_bar_height)
                    pg.draw.rect(self.screen, (255, 0, 0), hunger_fill_rect)  # Remplissage de la barre de faim

        pg.display.flip()

    def __draw_ui(self) -> None:
        self.screen.fill((200, 250, 255))
        font = pg.font.Font(None, 24)
        font_title = pg.font.Font(None, 36)
        font_title.set_bold(True)

        # Titre
        title_text = font_title.render("Paramètres", True, (0, 0, 0))
        title_rect = title_text.get_rect(topleft=(800, 50))
        self.screen.blit(title_text, title_rect)
        # Affichage de la température du monde
        temperature_text = font.render(f"Temperature: {self.world.temperature},        <-A   Z->", True, (0, 0, 0))
        temperature_rect = temperature_text.get_rect(topleft=(50, 100))
        self.screen.blit(temperature_text,
                         temperature_rect)  # Ajoutez cette ligne pour afficher la température sur l'écran

        pg.display.flip()

    # AFFICHER LA GRILLE EN BOUCLE
    def __start_display(self) -> None:
        controllerUI = ControllerUI(self.world)
        mainloop = True
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    mainloop = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    mainloop = True
                elif event.type == pg.KEYDOWN:
                    controllerUI.control_world(event.key)
            if mainloop:
                self.__draw_grid()
                self.__draw_entities()
                self.clock.tick(5)  # 10 FPS
            else:
                self.__draw_ui()
                self.clock.tick(10)  # 10 FPS
        pg.quit()

    # LANCER L'AFFICHAGE DANS UN THREAD (METHODE A APPELER DANS LE MAIN)
    def run(self) -> None:
        thread = threading.Thread(target=self.__start_display, daemon=True)
        thread.start()
