import json
from typing import Any

import pygame as pg
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pygame import Surface

from controller_ui import ControllerUI
from world import *
import matplotlib.pyplot as plt
from colors import *
import os


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
        self.data: list[dict[str, int]] = []
        self.analyze_size = 400
    # CHARGER LA CONFIGURATION (FICHIER JSON)
    def __load_config(self, config_file: str) -> None:
        with open(config_file, "r") as file:
            return json.load(file)

    # CHARGER LES CHEMINS DES IMAGES DES CASES (DEPUIS LA CONFIGURATION)
    def __load_tiles(self) -> dict:
        tiles = {}
        for tile_type, path in self.config["TilesPath"].items():
            tiles[tile_type] = pg.image.load(path).convert()
        return tiles

    # CHARGER LES CHEMINS DES IMAGES DES ENTITES (DEPUIS LA CONFIGURATION)
    def __load_entities(self) -> dict[Any, Surface]:
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
        size = image.get_size()

        cell_rect = pg.Rect(i * self.cell_size+self.cell_size/2-size[0]/2, j * self.cell_size+self.cell_size/2-size[1]/2, self.cell_size, self.cell_size)
        self.screen.blit(image, cell_rect)
        # TODO set to true to show drawing zone and the entity true case
        if False:
            _cell_rect = pg.Rect(i * self.cell_size + self.cell_size / 2 - size[0] / 2,
                                 j * self.cell_size + self.cell_size / 2 - size[1] / 2, size[0], size[1])
            pg.draw.rect(self.screen, RED, _cell_rect, 2)
            true_cell_rect = pg.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
            pg.draw.rect(self.screen, RED, true_cell_rect, 2)
        if (i, j) == self.world.target and self.analyze:
            _cell_rect = pg.Rect(i * self.cell_size + self.cell_size / 2 - size[0] / 2,
                                 j * self.cell_size + self.cell_size / 2 - size[1] / 2, size[0], size[1])
            pg.draw.rect(self.screen, RED, _cell_rect, 2)

        # Affichage de la barre de faim
        self.__draw_hunger_bar(entity, i, j)

    # AFFICHER LES ENTITES
    def __draw_entities(self) -> None:
        for i in range(self.world.entities.shape[0]):
            for j in range(self.world.entities.shape[1]):
                if self.world.entities[i, j]:
                    self.__draw_entity(i, j)



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
        graph_text = font.render(f"Graphe: G", True, (0, 0, 0))
        graph_rect = light_text.get_rect(topleft=(50, 150))
        self.screen.blit(graph_text,
                         graph_rect)  # Ajoutez cette ligne pour afficher la température sur l'écran
        analyse_text = font.render(f"Analyse: A", True, (0, 0, 0))
        analyse_rect = light_text.get_rect(topleft=(50, 175))
        self.screen.blit(analyse_text,
                         analyse_rect)  # Ajoutez cette ligne pour afficher la température sur l'écran
    def __draw_graph(self):
        image = self.make_graph()
        #size =  image.get_size()

        self.screen.blit(image, (0, 490))
    def get_ten_length_list(self, list):
        if list.__len__() == 10:
            return list
        else:
            new_list = [0 for i in range(10 - list.__len__())]
            new_list.extend(list)
            return new_list

    def make_graph(self):
        element_lists: dict[str, list] = self.convertData()
        fig, ax = plt.subplots()
        fig.set_size_inches(400 / fig.dpi, 400 / fig.dpi)
        for element in element_lists:
            test = self.get_ten_length_list(element_lists.get(element))
            ax.plot(range(10), self.get_ten_length_list(element_lists.get(element)), label=element)
        ax.set_xlabel('ticks', color='w')
        ax.set_ylabel('Numbers', color='w')
        ax.set_title('Numbers of creatures', color='w')
        ax.tick_params(axis='x', colors='w')
        ax.tick_params(axis='y', colors='w')
        ax.legend()

        canvas = FigureCanvas(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        #raw_data = renderer.tostring_rgb()
        #size = canvas.get_width_height()
        #surf = pg.image.fromstring(raw_data, size, "RGB")
        fig.patch.set_facecolor('none')
        temp_file = "temp_graph.png"
        fig.savefig(temp_file, transparent=True)
        surf = pg.image.load(temp_file).convert_alpha()
        os.remove(temp_file)
        return surf


    def convertData(self):
        element_lists = dict()
        for data in self.data:
            for key in data:
                element_lists[key] = element_lists.get(key, [])
                element_lists[key].append(data.get(key))
        return element_lists


    def count_current_elements(self):
        List_Entityt = ["Shark", "Fish", "Medusa", "Orca", "Crab"]
        dictionary = dict()
        for i in range(self.world.entities.shape[0]):
            for j in range(self.world.entities.shape[1]):
                if self.world.entities[i, j] != 0:
                    entity: Entity = self.world.entities[i, j]
                    dictionary[entity.__class__.__name__] = dictionary.get(entity.__class__.__name__, 0)+1
        for entity in List_Entityt:
            if not dictionary.get(entity, False):
                dictionary[entity] = 0
        if self.data.__len__() < 10:
            self.data.append(dictionary)
        else:
            while not (self.data.__len__() < 10):
                self.data.pop(0)
            self.data.append(dictionary)

    def check_target(self):
        if not (self.get_target() != 0):
            for i in range(self.world.entities.shape[0]):
                for j in range(self.world.entities.shape[1]):
                    if self.world.entities[i, j] != 0:
                        self.world.target = (i, j)
                        return True
            return False
        else:
            return True


    def get_target(self) -> Entity:
       return self.world.entities[self.world.target]
    def __draw_analyze(self):
        ecard = 20
        text_ecart = 15
        starting_x_position = self.world.grid.shape[0]*self.cell_size-self.analyze_size
        rect = ((self.world.grid.shape[0]*self.cell_size-self.analyze_size), 0, self.analyze_size, self.analyze_size)
        pg.draw.rect(self.screen, MEDIUM_BLUE, rect)
        pg.draw.rect(self.screen, DARKEST_BLUE, rect, 4)
        image = self.entities.get(self.get_target().entity_name)
        image_size = image.get_size()
        image_case = pg.Rect(starting_x_position + self.analyze_size / 2 - image_size[0]/2, self.analyze_size / 4 - image_size[1]/2, image_size[0], image_size[1])
        image_case_bis = pg.Rect(starting_x_position + self.analyze_size / 2 - image_size[0]/2-5, self.analyze_size / 4 - image_size[1]/2-5, image_size[0]+10, image_size[1]+10)
        pg.draw.rect(self.screen, CLAIR_BLUE, image_case_bis)
        pg.draw.rect(self.screen, DARKER_BLUE, image_case_bis, 2)
        self.screen.blit(image, image_case)
        text_case = pg.Rect(starting_x_position+ecard, self.analyze_size/2+ecard, self.analyze_size-ecard*2, self.analyze_size/2-ecard*2)
        pg.draw.rect(self.screen, CLAIR_BLUE, text_case)
        pg.draw.rect(self.screen, DARKER_BLUE, text_case, 2)

        font = pg.font.Font(None, 24)
        text_list = [f"Type : {self.get_target().entity_name}", f"Position: {self.world.target}", f"Age: {self.get_target().age//simulation_value_A}", f"faim: {int(100 - self.get_target().entity_hunger)}", f"Action: {self.get_target().current_action}", f"Movement cooldown: {self.get_target().speed_cooldown}", f"Naissance cooldown: {self.get_target().birth}"]
        for line in range(len(text_list)):
            line_case = pg.Rect(starting_x_position + ecard, self.analyze_size / 2 + ecard + line*text_ecart + 5,
                                self.analyze_size - ecard * 2, self.analyze_size / 2 - ecard * 2)
            text = font.render(text_list[line], True, (0, 0, 0))
            self.screen.blit(text, line_case)


    # AFFICHER LA GRILLE EN BOUCLE
    def start_display(self, event_queue) -> None:
        controllerUI = ControllerUI(self.world)
        mainloop = True
        graph = True
        self.analyze = False
        E_creature = True
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
                elif event.type == pg.KEYDOWN and event.key == pg.K_g:
                    if graph:
                        graph = False
                    else:
                        graph = True
                elif event.type == pg.KEYDOWN and event.key == pg.K_a:
                    self.analyze = not self.analyze
                elif event.type == pg.KEYDOWN:
                    controllerUI.control_world(event.key)
            if mainloop:
                self.screen.fill((0, 0, 0))  # Wipe the screen
                self.__draw_grid()
                self.__draw_entities()
                if graph:
                    self.__draw_graph()
                if self.analyze and E_creature:
                    E_creature = self.check_target()
                    if E_creature:
                        self.__draw_analyze()
                pg.display.flip()
                self.clock.tick(5)  # 10 FPS
            else:
                self.screen.fill((0, 0, 0))  # Wipe the screen
                self.__draw_ui()
                pg.display.flip()
                self.clock.tick(10)  # 10 FPS
