import numpy as np
import time
from abc import ABC, abstractmethod

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

class World():
    def __init__(self, x_size: int, y_size: int) -> None:
        # initialise the grid
        x, y = np.arange(0, x_size, 1), np.arange(0, y_size, 1)
        grid_x, grid_y = np.meshgrid(x, y)
        self.grid = np.zeros_like(grid_x, dtype=Case)  #Manipuler grid avec grid[(x, y)]
        self.i_size, self.j_size = x_size, y_size

    @property
    def getGrid(self):
        return self.grid
    
    def create_world(self, background, foreground):
        # create the grid depending of background file
        with open(background) as file:
            data = file.readlines()  
            print(data[29][59])  
            print(len(data), len(data[0]))
            for i in range(self.i_size):
                for j in range(self.j_size):
                    print(len(data), len(data[0]))
                    #print(i, j, data[i][j])
                    self.setCase(i, j, data[j][i])
        

    def setCase(self, x: int, y: int, type: str):
        if type == "S":
            self.grid[(x,y)] = CaseSea()
        elif type == "C":
            self.grid[(x,y)] = CaseCoral()


        

