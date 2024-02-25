import numpy as np
from world_cases import *
from world_entities import *
import random


class World:
    """
    Classe du monde comprenant la création et gestions des cases et entités
    """

    def __init__(self, x_size: int, y_size: int) -> None:
        # initialise the grid
        x, y = np.arange(0, x_size, 1), np.arange(0, y_size, 1)
        grid_x, grid_y = np.meshgrid(x, y)
        self.grid = np.zeros_like(grid_x, dtype=Case)  # Manipuler grid avec grid[(x, y)]
        self.i_size, self.j_size = x_size, y_size
        self.entities = np.zeros_like(grid_x, dtype=Entity)
        self.shark_existence = (5, 15)
        self.fish_existence = (100, 150)
        self.plankton_existence = (250, 300)
        self.medusa_existence = (40, 60)
        self.orcas_existence = (5, 10)
        self.crab_existence = (20, 30)
        self.temperature = 20

    # GETTER DE LA GRILLE
    @property
    def get_grid(self):
        return self.grid

    # DEFINIR LE TYPE DE CASE
    def set_case(self, x: int, y: int, type: str):
        if type == "S":
            self.grid[(x, y)] = SurfaceSea()
        elif type == "M":
            self.grid[(x, y)] = CaseSea()
        elif type == "C":
            self.grid[(x, y)] = CaseCoral()
        elif type == "D":
            self.grid[(x, y)] = DeepSea()
        elif type == ".":
            pass

    # CREATION DES ENTITES
    def create_entities(self, foreground):
        with open(foreground) as file:
            data = file.readlines()
            for entity in data:
                entity_data = entity.split()
                entity_name = entity_data[0]
                self.set_entity(entity_name, int(entity_data[1]), int(entity_data[2]))

    # CREER LE MONDE (A PARTIR DE DEUX FICHIERS, UN POUR LE FOND ET UN POUR LE PREMIER PLAN)
    def create_world(self, background, foreground):
        with open(background) as file:
            data = file.readlines()
            for j, line in enumerate(data):
                for i, case_type in enumerate(line):
                    self.set_case(i, j, case_type)
        self.create_entities(foreground)

    # CREE UN MONDE AVEC UN NOMBRE DE COUCHES ALEATOIRES DANS CERTAINES PROPORTIONS DONNEES
    def generate_world(self, foreground):
        sky_proportion = random.randint(9, 13)
        surfacesea_proportion = random.randint(58, 66)
        sea_proportion = random.randint(9, 13)
        sky_layers = round(sky_proportion / 100 * self.i_size)
        surfacesea_layers = round(surfacesea_proportion / 100 * self.i_size)
        sea_layers = round(sea_proportion / 100 * self.i_size)
        deepsea_layers = self.i_size - sky_layers - surfacesea_layers - sea_layers

        line_values = ['.'] * sky_layers + ['S'] * surfacesea_layers + ['M'] * sea_layers + ['D'] * deepsea_layers
        world_matrix = [[value] * self.j_size for value in line_values]

        for i in range(self.i_size):
            for j in range(self.j_size):
                self.set_case(j, i, world_matrix[i][j])
        self.create_entities(foreground)

    # POSE UNE ENTITE SUR UNE CASE
    def set_entity(self, name, x, y):
        if self.grid[(x, y)] != 0 and self.grid[(x, y)].name != "Coral":
            if name == "Shark":
                self.entities[x, y] = Shark()
            elif name == "Fish":
                self.entities[x, y] = Fish()
            elif name == "Crab":
                self.entities[x, y] = Crab()
            elif name == "Plankton":
                self.entities[x, y] = Plankton()
            elif name == "Medusa":
                self.entities[x, y] = Medusa()
            elif name == "Orca":
                self.entities[x, y] = Orca()

    # ENLEVE UNE ENTITE D'UNE CASE
    def clear_entity(self, x, y):
        self.entities[(x, y)] = 0

    # VERIFIE SI LA POSITION EST VALIDE
    def inboard(self, position):
        if (0 <= position[0] < self.i_size) and (0 <= position[1] < self.j_size):
            return True
        else:
            return False

    # condition to move in water, cant move in coral and cant not eat or crush another entities
    def normal_movement_condition(self, new_x, new_y):
        return self.predator_condition(new_x, new_y) and self.entities[new_x, new_y] == 0

    # Conditions to move in water, can t move in coral and be free to eat
    def predator_condition(self, new_x, new_y):
        return self.inboard((new_x, new_y)) and self.grid[new_x, new_y] != 0 and self.grid[new_x, new_y].case_type != "Coral"

