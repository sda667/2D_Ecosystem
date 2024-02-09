import numpy as np
from abc import ABC, abstractmethod

class Case(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
    
    @property
    def case_type(self) -> str:
        return self.name

class SurfaceSea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Surface Sea"

class CaseSea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sea"

class DeepSea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Deep Sea"

class Sand(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sand"

class Land(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Land"

class FishingArea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Finshing Area"

class CaseCoral(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Coral"

class Volcano(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Volcano"


class World():
    def __init__(self, x_size: int, y_size: int) -> None:
        # initialise the grid
        x, y = np.arange(0, x_size, 1), np.arange(0, y_size, 1)
        grid_x, grid_y = np.meshgrid(x, y)
        self.grid = np.zeros_like(grid_x, dtype=Case)  #Manipuler grid avec grid[(x, y)]
        self.i_size, self.j_size = x_size, y_size

    @property
    def get_grid(self):
        return self.grid
    
    def set_case(self, x: int, y: int, type: str):
        if type == "S":
            self.grid[(x,y)] = CaseSea()
        elif type == "C":
            self.grid[(x,y)] = CaseCoral()
    
    def create_world(self, background, foreground):
        # create the grid depending of background file
        with open(background) as file:
            data = file.readlines()  
            for j, line in enumerate(data):
                for i, case_type in enumerate(line):
                    self.set_case(i, j, case_type)