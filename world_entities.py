from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
        self.type = 0
        self.age = 0
        self.age_span = (0, 1)
        self.sex = ("FEMALE", "MALE")
        self.zone = ("Near Beach", "Mid Ocean", "Far Ocean")
        self.life_style = "individual"
        self.hunger = 0
        self.last_movement = (0, 0)
        self.depth = ("Surface Sea", "Sea", "Deep Sea")

    @property
    def entity_name(self) -> str:
        return self.name

    def set_entity_name(self, name: str) -> None:
        self.name = name

    @property
    def entity_type(self) -> int:
        return self.type

    def set_entity_type(self, type: int) -> None:
        self.type = type

    @property
    def entity_age(self) -> int:
        return self.age

    def set_entity_age(self, age: int) -> None:
        self.age = age

    @property
    def entity_hunger(self) -> int:
        return self.hunger

    def set_entity_hunger(self, hunger: int) -> None:
        self.hunger = hunger
    @property
    def entity_sex(self) -> str:
        return self.sex

    def set_entity_sex(self, sex: str):
        self.sex = sex
    @property
    def entity_life_style(self) -> str:
        return self.life_style

    def set_entity_life_style(self, life_style: str):
        self.life_style = life_style

    @property
    def entity_age_span(self) -> str:
        return self.age_span

    def set_entity_age_span(self, max_age: tuple):
        self.age_span = max_age

    @property
    def entity_zone(self) -> str:
        return self.zone

    def set_entity_zone(self, zone: tuple):
        self.zone = zone

    def get_last_movement(self) -> int:
        return self.last_movement

    def set_last_movement(self, dx: int, dy: int) -> None:
        self.last_movement = (dx, dy)

    @property
    def entity_depth(self):
        return self.depth

    def set_entity_depth(self, depth: tuple) -> None:
        self.depth = depth


class Plankton(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.set_entity_name("Plankton")
        # lower the type, the lower the creature are in the food chain.
        self.set_entity_type(0)
        self.set_entity_zone("Sea")


class Crab(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.set_entity_name("Crab")
        self.set_entity_type(1)
        self.set_entity_age_span((3, 5))
        self.set_entity_depth("Deep Sea")
        self.set_entity_zone("Near Beach")


class Medusa(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.set_entity_name("Medusa")
        self.set_entity_type(1)
        self.set_entity_age_span((1, 3))
        self.set_entity_depth("Surface Sea")
        self.set_entity_zone(("Near Beach", "Mid Ocean"))


class Fish(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.set_entity_name("Fish")
        self.set_entity_type(1)
        self.set_entity_age_span((2, 5))
        self.set_entity_zone(("Near Beach", "Mid Ocean"))
        self.set_entity_depth(("Surface Sea", "Sea"))


class Shark(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.set_entity_name("Shark")
        self.set_entity_type(3)
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_age_span((20, 30))
        self.set_entity_zone(("Near Beach", "Mid Ocean", "Far Ocean"))


class Orca(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.set_entity_name("Orca")
        # super predator , it can eat all creature
        self.set_entity_type(4)
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_life_style("Group")
        self.set_entity_age_span((50, 90))
        self.set_entity_zone(("Near Beach", "Mid Ocean", "Far Ocean"))

