import numpy as np
from abc import ABC
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
class Case(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
    
    @property
    def case_type(self) -> str:
        return self.name
    
class CaseSea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sea"

    @property
    def case_type(self) -> str:
        return self.name
    
class CaseCoral(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Coral"

    @property
    def case_type(self) -> str:
        return self.name
class Predator(ABC):
    def __init__(self, position) -> None:
        super().__init__()
        self.name = "NONE"
        self.type = "Predator"
        self.position = position

    @property
    def Creature_type(self) -> str:
        return self.type

    @property
    def get_creature(self) -> str:
        return self.name

    @property
    def get_position(self) -> tuple:
        return self.position
class Shark(Predator):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.name = "Shark"
    def setposition(self,position):
        self.position = position
class World():
    def __init__(self, x_size: int, y_size: int) -> None:
        # initialise the grid
        x, y = np.arange(0, x_size, 1), np.arange(0, y_size, 1)
        grid_x, grid_y = np.meshgrid(x, y)
        self.grid = np.zeros_like(grid_x, dtype=Case)  #Manipuler grid avec grid[(x, y)]
        self.i_size, self.j_size = x_size, y_size
        self.creatures = []

    @property
    def getGrid(self):
        return self.grid
    
    def create_world(self, background, foreground):
        # create the grid depending of background file
        with open(background) as file:
            data = file.readlines()
            for i in range(self.i_size):
                for j in range(self.j_size):
                    self.setCase(i, j, data[i][j])
        self.get_creature(foreground)
    def get_creature(self,foreground):
        with open(foreground) as file:
            data = file.readlines()
            for creature in data:
                creature_data = creature.split()
                creature_name = creature_data[0]
                creature_position = (int(creature_data[1]), int(creature_data[2]))
                self.setCreature(creature_name, creature_position)
    def setCreature(self,name, position):
        if name == "Shark":
            self.creatures.append(Shark(position))

    def setCase(self, x: int, y: int, type: str):
        if type == "S":
            self.grid[(x,y)] = CaseSea()
        elif type == "C":
            self.grid[(x,y)] = CaseCoral()


        

