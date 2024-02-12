import numpy as np
from abc import ABC, abstractmethod
from world_cases import *
from world_entities import *

class World():
    def __init__(self, x_size: int, y_size: int) -> None:
        # initialise the grid
        x, y = np.arange(0, x_size, 1), np.arange(0, y_size, 1)
        grid_x, grid_y = np.meshgrid(x, y)
        self.grid = np.zeros_like(grid_x, dtype=Case)  #Manipuler grid avec grid[(x, y)]
        self.i_size, self.j_size = x_size, y_size
        self.entities = np.zeros_like(grid_x, dtype=Entity)

    @property
    def get_grid(self):
        return self.grid

    def set_case(self, x: int, y: int, type: str):
        if type == "S":
            self.grid[(x,y)] = CaseSea()
        elif type == "C":
            self.grid[(x,y)] = CaseCoral()
        elif type == "D":
            self.grid[(x,y)] = DeepSea()
    
    def create_world(self, background, foreground):
        # create the grid depending of background file
        with open(background) as file:
            data = file.readlines()
            for j, line in enumerate(data):
                for i, case_type in enumerate(line):
                    self.set_case(i, j, case_type)
        self.get_entity(foreground)
    def get_entity(self,foreground):
        with open(foreground) as file:
            data = file.readlines()
            for entity in data:
                entity_data = entity.split()
                entity_name = entity_data[0]
                self.set_Entity(entity_name, int(entity_data[1]), int(entity_data[2]))
    def set_Entity(self,name, x, y):
        if name == "Shark":
            self.entities[x, y] = Shark()
    def clear_entity(self, x, y):
        self.entities[(x, y)] = 0
    