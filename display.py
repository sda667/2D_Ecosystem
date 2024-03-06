import pygame as pg
import json
from world import *
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

    # CHARGER LES CHEMINS DES IMAGES DES ENTITES (DEPUIS LA CONFIGURATION)
    def __load_entities(self) -> None:
        entities = {}
        for entity_type, path in self.config["EntityPath"].items():
            entities[entity_type] = pg.image.load(path).convert_alpha()
        return entities

    def set_colorkey_with_tolerance(self, image, colorkey, tolerance):
        # Convert the image to use an alpha channel
        image = image.convert_alpha()

        # Get the width and height of the image
        width, height = image.get_size()

        # Iterate over each pixel in the image
        for y in range(height):
            for x in range(width):
                # Get the color of the current pixel
                current_color = image.get_at((x, y))

                # If the current color is white, set the alpha value to 0 (fully transparent)
                if current_color == colorkey:
                    image.set_at((x, y), (0, 0, 0, 0))  # Set alpha to 0 (fully transparent)
                else:
                    # Calculate the difference between the current color and the color key
                    color_diff = abs(current_color[0] - colorkey[0]) + \
                                 abs(current_color[1] - colorkey[1]) + \
                                 abs(current_color[2] - colorkey[2])

                    # If the difference is within the tolerance level, set the alpha value to 0 (fully transparent)
                    if color_diff <= tolerance:
                        current_color[3] = 0  # Set alpha to 0 (fully transparent)

                        # Update the pixel with the modified color
                        image.set_at((x, y), current_color)

        # Set the color key to None since we're using alpha transparency
        image.set_colorkey(None)

        return image
    # AFFICHER LES CASES
    def __draw_tiles(self):
        for i in range(self.world.grid.shape[0]):
            for j in range(self.world.grid.shape[1]):
                if self.world.grid[i, j] != 0:
                    if self.world.grid[i, j].case_type == "Sun":
                        if self.world.sun:
                            tile_image = pg.image.load("image/Sun.jpg").convert()
                            tile_image = self.set_colorkey_with_tolerance(tile_image, (255, 255, 255), 50)
                            resized_image = pg.transform.scale(tile_image, (self.cell_size * 3, self.cell_size * 3))
                            cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size,
                                                self.cell_size)
                            self.screen.blit(resized_image, cell_rect)
                            if self.world.light > 2:
                                if self.world.light <= 4:
                                    tile_image = pg.image.load("image/Sun_type_1.jpg").convert()
                                    tile_image = self.set_colorkey_with_tolerance(tile_image, (255, 255, 255), 50)
                                    resized_image = pg.transform.scale(tile_image,
                                                                       (self.cell_size * 3, self.cell_size * 3))
                                    cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size,
                                                        self.cell_size)
                                    self.screen.blit(resized_image, cell_rect)
                                elif self.world.light <=6:

                                    tile_image = pg.image.load("image/Sun_type_2.jpg").convert()
                                    tile_image = self.set_colorkey_with_tolerance(tile_image, (255, 255, 255), 50)
                                    resized_image = pg.transform.scale(tile_image,
                                                                       (self.cell_size * 3, self.cell_size * 3))
                                    cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size,
                                                        self.cell_size)
                                    self.screen.blit(resized_image, cell_rect)
                                elif self.world. light <=8:
                                    tile_image = pg.image.load("image/Sun_type_3.jpg").convert()
                                    tile_image = self.set_colorkey_with_tolerance(tile_image, (255, 255, 255), 50)
                                    resized_image = pg.transform.scale(tile_image,
                                                                       (self.cell_size * 3, self.cell_size * 3))
                                    cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size,
                                                        self.cell_size)
                                    self.screen.blit(resized_image, cell_rect)
                                elif self.world. light <=10:
                                    tile_image = pg.image.load("image/Sun_type_4.jpg").convert()
                                    tile_image = self.set_colorkey_with_tolerance(tile_image, (255, 255, 255), 50)
                                    resized_image = pg.transform.scale(tile_image,
                                                                       (self.cell_size * 3, self.cell_size * 3))
                                    cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size,
                                                        self.cell_size)
                                    self.screen.blit(resized_image, cell_rect)

                        else:
                            tile_image = pg.image.load("image/DeadSun.jpg").convert()
                            tile_image = self.set_colorkey_with_tolerance(tile_image, (255, 255, 255), 50)
                            resized_image = pg.transform.scale(tile_image, (self.cell_size * 3, self.cell_size * 3))
                            cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size,
                                                self.cell_size)
                            self.screen.blit(resized_image, cell_rect)
                    else:
                        # Calcul de l'opacité en fonction de la profondeur
                        depth = j / self.world.grid.shape[1]
                        opacity = int(255 - (depth * 255))  # Calcul de l'opacité en fonction de la profondeur
                        opacity = max(0, min(255, opacity))
                        # Récupération de l'image de la case (et redimensionnement, opacité)
                        tile_type = self.world.grid[i, j].case_type
                        tile_image = self.tiles.get(tile_type)
                        resized_image = pg.transform.scale(tile_image, (self.cell_size, self.cell_size))
                        resized_image.set_alpha(opacity)

                        # Affichage de l'image
                        cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                        self.screen.blit(resized_image, cell_rect)



    # AFFICHER LA GRILLE
    def __draw_grid(self) -> None:
        
        # Affichage de l'arrière-plan
        background_image = pg.image.load("image/Ocean.png").convert()
        resized_image = pg.transform.scale(background_image,
                                           (self.screen_size[0] // 5, self.screen_size[1] // 5))  # Resize the image
        
        # Répéter l'image en boucle sur le haut de l'écran
        for x in range(0, self.screen_size[0], resized_image.get_width()):
            self.screen.blit(resized_image, (x, 0))
        self.screen.blit(resized_image, (0, 0))

        # Affichage des cases
        self.__draw_tiles()

    # AFFICHER LA BARRE DE FAIM
    def __draw_hunger_bar(self, entity, i, j):
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

    # AFFICHER UNE ENTITE
    def __draw_entity(self, i, j):
        entity = self.world.entities[i, j]
        entity_type = entity.entity_name
        entity_image = self.entities.get(entity_type)
        flipped = pg.transform.flip(entity_image, True, False)
                    # Check if the entity moved to the right
        if entity.last_movement == (1, 0):
            image = flipped
        else:
            image = entity_image
        image.set_colorkey((255, 255, 255))
                    # Affichage de l'image
        cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
        self.screen.blit(image, cell_rect)

                    # Affichage de la barre de faim
        self.__draw_hunger_bar(entity, i, j)

    # AFFICHER LES ENTITES
    def __draw_entities(self) -> None:
        for i in range(self.world.entities.shape[0]):
            for j in range(self.world.entities.shape[1]):
                if self.world.entities[i, j]:
                    self.__draw_entity(i, j)
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
        light_text = font.render(f"Light: {self.world.light},        <-W   X->", True, (0, 0, 0))
        light_rect = light_text.get_rect(topleft=(50, 125))
        self.screen.blit(light_text,
                         light_rect)  # Ajoutez cette ligne pour afficher la température sur l'écran


    # AFFICHER LA GRILLE EN BOUCLE
    def start_display(self, event_queue) -> None:
        controllerUI = ControllerUI(self.world)
        mainloop = True
        running = True
        while running:
            while not event_queue.empty():
                # If the queue is not empty, get the event
                event = event_queue.get()
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
                self.screen.fill((0, 0, 0))  # Wipe the screen
                self.__draw_grid()
                self.__draw_entities()
                pg.display.flip()
                self.clock.tick(10)  # 10 FPS
            else:
                self.__draw_ui()
                pg.display.flip()
                self.clock.tick(10)  # 10 FPS
