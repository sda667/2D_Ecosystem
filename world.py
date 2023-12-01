import numpy as np
from abc import ABC, abstractmethod

class Case(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
    
    @property
    def case_type(self) -> str:
        return self.name
    
class CaseForest(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "FOREST"

    def case_type(self) -> str:
        return self.name

class World():
    def __init__(self, x_size: int, y_size: int) -> None:
        x, y = np.arange(0, x_size, 1), np.arange(0, y_size, 1)
        grid_x, grid_y = np.meshgrid(x, y)
        self.grid = np.zeros_like(grid_x, dtype=Case)  #Manipuler grid avec grid[(x, y)]
        self.i_size, self.j_size = x_size, y_size

    @property
    def getGrid(self):
        return self.grid
    
    def create_world(self):
        for i in range(self.i_size):
            for j in range(self.j_size):
                self.setCase(i, j, "FOREST")
            

    def setCase(self, x: int, y: int, type: str):
        if type == "FOREST":
            self.grid[(x,y)] = CaseForest()


        

