from abc import ABC, abstractmethod
class Entity(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
        self.type = 0
        self.age = 0
        self.hunger = 0
        self.last_movement = (0,0)
        self.depth = ("Surface Sea", "Sea", "Deep Sea")
    
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
    
    def get_last_movement(self) -> int:
        return self.last_movement

    def set_last_movement(self, dx: int, dy: int) -> None:
        self.last_movement = (dx, dy)

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
        self.depth = ("Surface Sea", "Sea")

class Orca(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Orca"
        # super predator , it can eat all creature
        self.type = 4
        self.depth = ("Surface Sea", "Sea", "Deep Sea")

    @property
    def Creature_type(self) -> str:
        return self.type

    @property
    def get_creature(self) -> str:
        return self.name

    @property
    def get_position(self) -> tuple:
        return self.position