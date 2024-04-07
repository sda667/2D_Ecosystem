import numpy as np
from world_cases import *
from world_entities import *
import random
from world_entities import simulation_value_A

class Mountain_builder:
    type = None
    high = None
    i = None
    j = None

    def build_mountain(self, i, j, matrix):
        self.set_high(random.randint(1,5))
        self.set_mountain_type(random.randint(1,2))
        self.i = i+1-self.high
        self.j = j
        if self.type == "A":
            self.build_type_A(matrix)
        elif self.type == "B":
            self.build_type_B(matrix)

    def build_type_A(self, matrix):
        for i in range(self.high):
            matrix[self.i+i][self.j] = "L"
            for j in range(i):
                matrix[self.i+i][self.j+j] = "L"
                matrix[self.i+i][self.j-j] = "L"


    def build_type_B(self, matrix):
        if self.high == 1:
            matrix[self.i][self.j] = "L"
            return
        else:
            left = random.randint(1, self.high - 1)
            right = random.randint(1, self.high - 1)
            matrix[self.i][self.j] = "L"
            for i in range(1, self.high):
                matrix[self.i + i][self.j] = "L"
                if (self.high - i) == left and left:
                    matrix[self.i + i][self.j - 1] = "L"
                    left -= 1
                if (self.high - i) == right and right:
                    matrix[self.i + i][self.j + 1] = "L"
                    right -=1



    def build_type_C(self, matrix):
        pass
    def set_mountain_type(self, high: int):
        if high == 1:
            self.type = "A"
        elif high == 2:
            self.type = "B"
        elif high == 3:
            self.type = "C"
        else:
            print("error in random parameter given is not accepted")
            exit(1)

    def set_high(self, high: int):
        self.high = high
def generate_entities(entities_file):
    used_position = set()
    with open("World data/entities_setting.txt", 'r') as file, open(entities_file, 'w') as entities:
        for line in file:
            if file != "\n" or file != '':
                values = line.strip(' ').split()
                population = random.randint(int(values[1]),
                                            int(values[2]))  # Random value between the set base population
                for _ in range(population):
                    new_pos = (random.randint(8, 59), random.randint(1, 119))
                    while new_pos in used_position:  # search for new not used position
                        new_pos = (random.randint(8, 59), random.randint(1, 119))
                    used_position.add(new_pos)
                    age = str(random.randint(0, int(values[3])))  # Age under the life span
                    hunger = str(random.randint(0, 30))  # hunger to start with
                    max_age = str(random.randint(int(values[3]), int(values[4])))  # Age of death inside the life span
                    entities.write(values[0] + ' ' + str(new_pos[0]) + ' ' + str(
                        new_pos[1]) + ' ' + age + ' ' + hunger + ' ' + max_age + '\n')


class World:
    """
    Classe du monde comprenant la création et gestions des cases et entités
    """

    def __init__(self, x_size: int, y_size: int, seed) -> None:
        # initialise the grid
        random.seed(seed)
        x, y = np.arange(0, x_size, 1), np.arange(0, y_size, 1)
        grid_x, grid_y = np.meshgrid(x, y)
        self.grid = np.zeros_like(grid_x, dtype=Case)  # Manipuler grid avec grid[(x, y)]
        self.i_size, self.j_size = x_size, y_size
        self.entities = np.zeros_like(grid_x, dtype=Entity)
        self.sun = True  # is the sun present.
        self.plankton = 0  # 0 if the sun is not present and 0 < plankton <= 1 if the sun is present
        self.shark_existence = (5, 15)
        self.fish_existence = (50, 100)
        self.plankton_existence = (250, 300)
        self.medusa_existence = (20, 40)
        self.orcas_existence = (5, 15)
        self.crab_existence = (20, 30)
        self.temperature = 20
        self.light = 5
        self.target: tuple[int, int] = (0, 0)
        self.target_path = None

    # GETTER DE LA GRILLE
    @property
    def get_grid(self):
        return self.grid

    # DEFINIR LE TYPE DE CASE
    def set_case(self, x: int, y: int, type: str):
        if type == "S":
            self.grid[(x, y)] = SurfaceSea()
        elif type == "Sun":
            self.grid[(x, y)] = Sun()
        elif type == "M":
            self.grid[(x, y)] = CaseSea()
        elif type == "C":
            self.grid[(x, y)] = CaseCoral()
        elif type == "D":
            self.grid[(x, y)] = DeepSea()
        elif type == "L":
            self.grid[(x, y)] = Land()
        elif type == "G":
            self.grid[(x, y)] = Graph()
        elif type == ".":
            pass

    # CREATION DES ENTITES
    def create_entities(self, foreground):
        with open(foreground) as file:
            data = file.readlines()
            for entity in data:
                entity_data = entity.split()
                entity_name = entity_data[0]
                self.set_init_entity(entity_name, int(entity_data[2]), int(entity_data[1]), int(entity_data[3])*simulation_value_A,
                                     int(entity_data[4]), int(entity_data[5])*simulation_value_A)

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
        world_matrix[0][self.j_size//2] = "Sun"
        self.generate_random_floor(world_matrix, sky_layers)
        for i in range(self.i_size):
            for j in range(self.j_size):
                self.set_case(j, i, world_matrix[i][j])
        self.create_entities(foreground)
    # RANDOM GENERATE FLOOR
    def generate_random_floor(self, world_matrix, skylayers):
        # longueur des terrains de terre a la surface de la mer
        cote_left_length = random.randint(3, 10)
        # longueur de la pente du cote gauche jusqu a la fin de la pente
        cote_down_height = random.randint(cote_left_length+3, cote_left_length+10)
        # hauteur de la couche sol en dessous de la mer
        height_floor = random.randint(2, 5)
        #  |                                  |here sky
        #  |L--------------------------------L| here land part on the surface of the sea which cote_left_length = 1
        #  |LLLL--------------------------LLLL| here is the length of the end of the pente which cote_down_height = 4
        #  |LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL|
        #  |LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL| here is the height of the floor under the sea which is height_floor = 2
        # make horizontal floor
        for i in range(self.i_size-1,self.i_size-1-height_floor, -1):
            world_matrix[i] = ["L"] * self.j_size
        # make vertical left floor
        for i in range(self.i_size):
            if world_matrix[i][0] != "L" and world_matrix[i][0] != ".":
                for j in range(0, cote_left_length, 1):
                    world_matrix[i][j] = "L"
        # make vertical right floor
        for i in range(self.i_size):
            if world_matrix[i][self.j_size-1] != "L" and world_matrix[i][0] != ".":
                for j in range(self.j_size-1, self.j_size-1 - cote_left_length, -1):
                    world_matrix[i][j] = "L"
        # creation de la pente
        for i in range(skylayers, self.i_size-height_floor):
            point = self.interpolate_points(self.i_size-1-i, cote_left_length, self.i_size - 1-skylayers, cote_down_height, height_floor)
            for j in range(1, int(point) - cote_left_length+1):
                world_matrix[i][cote_left_length-1+j] = "L"
                world_matrix[i][self.j_size - cote_left_length -j] = "L"
        for j in range(cote_down_height+4, self.j_size-cote_down_height-5, 7):
            self.add_mountain(self.i_size-1-height_floor, j, world_matrix)

    # create a mountain at a location
    def add_mountain(self, i, j, matrix):
        builder = Mountain_builder()
        builder.build_mountain(i, j, matrix)

    def interpolate_points(self, y, x1, y1, x2, y2):
        """
        Interpolation linéaire entre deux points.

        Arguments :
        x : float - La valeur de X pour laquelle nous voulons trouver Y.
        x1, y1 : float - Les coordonnées du premier point.
        x2, y2 : float - Les coordonnées du deuxième point.

        Returns :
        float - La valeur de Y interpolée pour la valeur de X donnée.
        """
        value = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
        return value




    # POSE UNE ENTITE SUR UNE CASE
    def set_init_entity(self, name, x, y, age, hunger, max_age):
        if self.isplayable_and_free(x, y):
            if name == "Shark":
                self.entities[x, y] = Shark(age, hunger, max_age)
            elif name == "Fish" or name == "Fish0" or name == "Fish1" or name == "Fish2":
                self.entities[x, y] = Fish(age, hunger, max_age)
            elif name == "Crab":
                self.entities[x, y] = Crab(age, hunger, max_age)
            elif name == "Medusa":
                self.entities[x, y] = Medusa(age, hunger, max_age)
            elif name == "Orca":
                self.entities[x, y] = Orca(age, hunger, max_age)
        else:
            new_pos = (random.randint(8, 59), random.randint(1, 119))
            self.set_init_entity(name, new_pos[1], new_pos[0], age, hunger, max_age)


    def set_entity(self, name, x, y):
        if self.grid[(x, y)] != 0 and self.grid[(x, y)].name != "Coral":
            if name == "Shark":
                self.entities[x, y] = Shark()
            elif name == "Fish" or name == "Fish0" or name == "Fish1" or name == "Fish2":
                self.entities[x, y] = Fish()
            elif name == "Crab":
                self.entities[x, y] = Crab()
            elif name == "Medusa":
                self.entities[x, y] = Medusa()
            elif name == "Orca":
                self.entities[x, y] = Orca()

    def set_entity_child(self, name, x, y):
        self.set_entity(name, x, y)
        entity = self.entities[x, y]
        entity.set_entity_hunger(40)
        entity.set_entity_birth(entity.entity_birth_cooldown)

    # ENLEVE UNE ENTITE D'UNE CASE
    def clear_entity(self, x, y):
        self.entities[(x, y)] = 0

    # VERIFIE SI LA POSITION EST VALIDE
    def inboard(self, position):
        if (0 <= position[0] < self.j_size) and (0 <= position[1] < self.i_size):
            return True
        else:
            return False

    # condition to move in water, cant move in coral and cant not eat or crush another entities
    def isplayable_and_free(self, new_x, new_y):
        return self.isplayable_case(new_x, new_y) and self.entities[new_x, new_y] == 0

    # Conditions to move in water, can t move in coral and be free to eat
    def isplayable_case(self, new_x, new_y):
        return self.inboard((new_x, new_y)) and self.grid[new_x, new_y] != 0 and self.grid[
            new_x, new_y].case_type != "Coral" and self.grid[
            new_x, new_y].case_type != "Land"
