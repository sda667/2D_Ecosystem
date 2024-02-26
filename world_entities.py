
from abc import ABC
import random
import math

import world



class Entity(ABC):
    """
    Classe abstraite d'entités, utilisée pour créer chaque entité spécifique
    """

    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
        self.type = 0  # Niveau dans la chaine alimentaire (plus grand = plus de nourriture) (à utiliser pour manger)
        self.age = 0
        self.max_age = 0
        self.sex = random.randint(0, 1)  # 0 Female # 1 Male
        self.zone = ("Near Beach", "Mid Ocean", "Far Ocean")
        self.life_style = "individual"
        self.hunger = 0
        self.last_movement = (0, 0)
        self.depth = ("Surface Sea", "Sea", "Deep Sea")
        self.speed = 0  # cooldown after each turn so speed =0 mean no cooldown the entity will move on each turn
        self.speed_cooldown = 0
        self.birth = 0
        self.birth_cooldown = 0
        self.vision = 0
        self.max_pollution = 0
        self.temp = (0, 1)  # Perfect temp for creature
        self.prey_set = set("Plankton")

    def brain(self, myposition: tuple, entities_position: list, world: world) -> str:
        if self.entity_speed_cooldown == 0 and self.entity_speed != -1:
            if self.check_threat(myposition, entities_position, world):
                print(self.entity_name + " want to flee")
                return "Flee"
            # TODO change the number here to change the minimal hunger for predation
            elif (self.entity_hunger >= 50) and (
                    self.check_prey(myposition, entities_position, world)):
                print(self.entity_name + " want to eat")
                return "Predation"
            else:
                # TODO change the number here for self.entity_hunger to change the maximal accepted hunger for birth
                if self.birth == 0 and self.entity_hunger <= 40 and self.mate_check(myposition, entities_position,
                                                                                    world):
                    print(self.entity_name + " want to mate")
                    return "Mate"
                else:
                    return "Idle"
        else:
            return "Stay"

    # check if there is mate that is not myself, same specie , can birth and are close enough to me
    def mate_check(self, myposition, entities_position, world: world):
        entities_matrix = world.entities
        for entity_position in entities_position:
            entity = entities_matrix[entity_position]
            if entity != self and (
                    entity.entity_name == self.entity_name) and entity.entity_birth == 0 and self.heuristique(
                    myposition,
                    entity_position) <= self.entity_vision:
                return True
        return False

    def eat(self, entity):
        # TODO change value next to * to change the number of hunger entity_type give
        # TODO change value next to + to change the default value of hunger
        value = entity.entity_type * 20 + 10
        hunger = self.entity_hunger
        self.set_entity_hunger(hunger - min(hunger, value))

    def mate(self, myposition, mate: "Entity", world):
        # TODO change value for hunger_consumned to change the amount added to hunger to the ourself and mate
        hunger_consummed = 30
        child_future_position = self.enough_space_around_me(myposition, world)
        if child_future_position != None:
            # starting birth cooldown and add hunger to ourself
            self.set_entity_hunger(self.entity_hunger + hunger_consummed)
            self.set_entity_birth(self.entity_birth_cooldown)
            # starting birth cooldown and add hunger to mate
            mate.set_entity_hunger(mate.entity_hunger + hunger_consummed)
            mate.set_entity_birth(mate.entity_birth_cooldown)
            # create a baby
            world.set_entity_child(self.entity_name, *child_future_position)

    def enough_space_around_me(self, myposition, world):
        for i in range(-1, 1, 1):
            for j in range(-1, 1, 1):
                if i != 0 or j != 0:
                    if world.normal_movement_condition(*(myposition[0] + i, myposition[1] + j)):
                        return (myposition[0] + i, myposition[1] + j)
        return None

    def heuristique(self, position, target_position):
        x_distance = abs(target_position[0] - position[0])
        y_distance = abs(target_position[1] - position[1])
        distance = math.sqrt(math.pow(x_distance, 2) + math.pow(y_distance, 2))
        return distance

    # Check if there are threat that can i see and that he can nearly see to prevent flee from a threat that can not see me
    def check_threat(self, myposition, entities_position: list, world: world):
        entities_matrix = world.entities
        for entity_position in entities_position:
            entity = entities_matrix[entity_position]
            if (self.entity_name in entity.prey_set) and self.heuristique(myposition,
                                                                          entity_position) <= min(self.entity_vision,
                                                                                                  entity.entity_vision + 1):
                return True
        return False

    def check_prey(self, myposition, entities_position, world):
        entities_matrix = world.entities
        for entity_position in entities_position:
            entity = entities_matrix[entity_position]
            if (entity.entity_name in self.prey_set) and self.heuristique(myposition,
                                                                          entity_position) <= self.entity_vision:
                return True
        return False

    # GETTER ET SETTERS
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
    def entity_max_age(self) -> int:
        return self.max_age

    def set_entity_max_age(self, max_age: int):
        self.max_age = max_age

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

    @property
    def entity_vision(self) -> int:
        return self.vision

    def set_entity_vision(self, vision: int) -> None:
        self.vision = vision

    @property
    def entity_speed(self) -> int:
        return self.speed

    def set_entity_speed(self, speed: int) -> None:
        self.speed = speed

    @property
    def entity_speed_cooldown(self) -> int:
        return self.speed_cooldown

    def set_entity_speed_cooldown(self, cooldown: int) -> None:
        self.speed_cooldown = cooldown

    def entity_preys(self):
        return self.prey_set

    def set_entity_preys(self, preys: list):
        for i in range(len(preys)):
            self.prey_set.add(preys[i])

    @property
    def entity_birth(self):
        return self.birth

    def set_entity_birth(self, birth):
        self.birth = birth

    @property
    def entity_birth_cooldown(self):
        return self.birth_cooldown

    def set_entity_birth_cooldown(self, birth_cooldown):
        self.birth_cooldown = birth_cooldown


# CLASSES POUR CHAQUE ENTITE SPECIFIQUE
class Plankton(Entity):
    def __init__(self, age=0, hunger=0) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(10)
        self.set_entity_max_age(100)
        self.set_entity_speed(-1)
        self.set_entity_vision(0)

        self.set_entity_name("Plankton")
        self.set_entity_type(0)
        self.set_entity_depth("Surface Sea")
        self.set_entity_zone(("Near Beach", "Mid Ocean"))


class Crab(Entity):
    def __init__(self, age=0, hunger=0, max_age=random.randint(3, 6)) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(10)  # not configured yet
        self.set_entity_max_age(max_age)  # not configured yet
        self.set_entity_speed(0)  # not configured yet
        self.set_entity_vision(0)  # not configured yet

        self.set_entity_name("Crab")
        self.set_entity_type(1)
        self.set_entity_depth("Deep Sea")
        self.set_entity_zone("Near Beach")
        self.set_entity_preys(["Fish2"])


class Medusa(Entity):
    def __init__(self, age=0, hunger=0, max_age=random.randint(2, 4)) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(10)  # not configured yet
        self.set_entity_max_age(max_age)  # not configured yet
        self.set_entity_speed(-1)  # not configured yet
        self.set_entity_vision(0)  # not configured yet

        self.set_entity_name("Medusa")
        self.set_entity_type(1)
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_zone(("Near Beach", "Mid Ocean"))
        self.set_entity_preys(["Fish2", "Plankton"])


class Fish(Entity):
    def __init__(self, age=0, hunger=0, max_age=random.randint(5, 8)) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(0)
        self.set_entity_birth_cooldown(10)  # not configured yet
        self.set_entity_max_age(max_age)  # not configured yet
        self.set_entity_speed(1)  # not configured yet
        self.set_entity_vision(5)  # not configured yet

        self.set_entity_name("Fish" + str(random.randint(0, 2)))
        self.set_entity_type(1)
        self.set_entity_zone(("Near Beach", "Mid Ocean"))
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_preys(["Plankton"])

    def check_prey(self, myposition, entities_position, world):
        if world.plankton != 0 and self.nearsea_check(myposition, world) != myposition:
            return True
        return False

    # Find the nearest place for Fish to eat plankton
    def isnearsea(self, world, check_position):
        # TODO change the value next to check_position[1] to check the definition of nearsea zone
        # nearsea zone is actually the cases that are near to sky , distance to be considered as near is defined below
        # here the nearsea zone are all cases that have a maximal distance of 10 to the sky
        return not world.inboard((check_position[0], check_position[1] - 10)) or world.grid[
            (check_position[0], check_position[1] - 10)] == 0

    def nearsea_check(self, myposition, world: world):
        check_position = myposition
        while (world.grid[check_position] != 0):
            # find the nearsea zone above
            if self.isnearsea(world, check_position):  #
                # check if the position found are free
                if check_position == myposition:
                    return myposition
                if world.normal_movement_condition(*check_position):
                    return check_position
            check_position = (check_position[0], check_position[1] - 1)
        return None


class Shark(Entity):
    def __init__(self, age=0, hunger=0, max_age=random.randint(20, 30)) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(50)
        self.set_entity_max_age(max_age)
        self.set_entity_speed(0)
        self.set_entity_vision(20)

        self.set_entity_name("Shark")
        self.set_entity_type(3)
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_zone(("Near Beach", "Mid Ocean", "Far Ocean"))
        self.set_entity_preys(["Fish0", "Fish1", "Fish2", "Medusa"])


class Orca(Entity):
    def __init__(self, age=0, hunger=0, max_age=random.randint(50, 90)) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(10)  # not configured yet
        self.set_entity_max_age(max_age)
        self.set_entity_speed(0)  # not configured yet
        self.set_entity_vision(30)  # not configured yet

        self.set_entity_name("Orca")
        self.set_entity_type(4)
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_life_style("Group")
        self.set_entity_zone(("Near Beach", "Mid Ocean", "Far Ocean"))
        self.set_entity_preys(["Fish0", "Fish1", "Fish2", "Medusa", "Shark"])
