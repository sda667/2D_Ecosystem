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



class Entity(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
        self.type = 0
        self.age = 0
        self.hunger = 0
    
    @property
    def entity_name(self) -> str:
        return self.name    
    @property
    def entity_type(self) -> int:
        return self.type
    @property
    def entity_age(self) -> int:
        return self.age
    @property
    def entity_hunger(self) -> int:
        return self.hunger

class Plankton(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Plankton"
        # lower the type, the lower the creature are in the food chain.
        self.type = 0
class Crab(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Crab"
        self.type = 1

class Medusa(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Medusa"
        self.type = 1

class Fish(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Fish"
        self.type = 1

class Shark(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Shark"
        self.type = 3

class Orca(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Orca"
        # super predator , it can eat all creature
        self.type = 4

    @property
    def Creature_type(self) -> str:
        return self.type

    @property
    def get_creature(self) -> str:
        return self.name

    @property
    def get_position(self) -> tuple:
        return self.position



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