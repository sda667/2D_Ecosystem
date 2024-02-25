import random
from abc import ABC, abstractmethod
import random
import math



class Entity(ABC):
    """
    Classe abstraite d'entités, utilisée pour créer chaque entité spécifique
    """
    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
        self.type = 0  # Niveau dans la chaine alimentaire (plus grand = plus de nourriture) (à utiliser pour manger)
        self.age = 0
        self.life_span = (0, 0)
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


    def brain(self, myposition: tuple, entities_position: list, entities_matrix) -> str:
        if self.entity_speed_cooldown == 0 and self.entity_speed != -1:
            if self.check_threat(myposition, entities_position, entities_matrix):
                print(self.entity_name + " want to flee")
                return "Flee"
            elif (self.entity_hunger >= 50) and (
                    self.check_prey(myposition, entities_position, entities_matrix)):
                print(self.entity_name + " want to eat")
                return "Predation"
            else:
                if  self.birth == 0 and self.entity_hunger <= 40 and self.mate_check(myposition, entities_position, entities_matrix):
                    print(self.entity_name + " want to mate")
                    return "Mate"
                else:
                    return "Idle"
        else:
            return "Stay"
    # check if there is mate that is not myself, same specie , can birth and are close enough to me
    def mate_check(self, myposition, entities_position, entities_matrix):
        for entity_position in entities_position:
            entity = entities_matrix[entity_position]
            if entity != self and (entity.entity_name == self.entity_name) and entity.entity_birth == 0 and self.heuristique(myposition,
                                                                       entity_position) <= self.entity_vision:
                return True
        return False
    def eat(self, entity):
        value = entity.entity_type * 20 + 10
        hunger = self.entity_hunger
        self.set_entity_hunger(hunger - min(hunger, value))

    def mate(self, myposition, mate: "Entity", world):
        hunger_consummed = 30
        child_future_position = self.enough_space_around_me(myposition, world)
        if child_future_position != None:
            self.set_entity_hunger(self.entity_hunger+hunger_consummed)
            self.set_entity_birth(self.entity_birth_cooldown)
            mate.set_entity_birth(mate.entity_birth_cooldown)
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
    def check_threat(self, myposition, entities_position: list, entities_matrix):
        for entity_position in entities_position:
            entity = entities_matrix[entity_position]
            if (self.entity_name in entity.prey_set) and self.heuristique(myposition,
                                                                       entity_position) <= min(self.entity_vision, entity.entity_vision+1):
                return True
        return False


    def check_prey(self, myposition, entities_position, entities_matrix):
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
    def entity_life_span(self) -> tuple:
        return self.life_span

    def set_entity_life_span(self, max_age: tuple):
        self.life_span = max_age

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
        self.set_entity_life_span(100)
        self.set_entity_speed(-1)
        self.set_entity_vision(0)

        self.set_entity_name("Plankton")
        self.set_entity_type(0)
        self.set_entity_depth("Surface Sea")
        self.set_entity_zone(("Near Beach", "Mid Ocean"))


class Crab(Entity):
    def __init__(self, age=0, hunger=0) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(10) # not configured yet
        self.set_entity_life_span((3, 5)) # not configured yet
        self.set_entity_speed(0) # not configured yet
        self.set_entity_vision(0) # not configured yet

        self.set_entity_name("Crab")
        self.set_entity_type(1)
        self.set_entity_depth("Deep Sea")
        self.set_entity_zone("Near Beach")
        self.set_entity_preys(["Fish"])


class Medusa(Entity):
    def __init__(self, age=0, hunger=0) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)


        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(10)  # not configured yet
        self.set_entity_life_span((1, 3))  # not configured yet
        self.set_entity_speed(-1)  # not configured yet
        self.set_entity_vision(0)  # not configured yet

        self.set_entity_name("Medusa")
        self.set_entity_type(1)
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_zone(("Near Beach", "Mid Ocean"))
        self.set_entity_preys(["Fish", "Plankton"])


class Fish(Entity):
    def __init__(self, age=0, hunger=0) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(0)
        self.set_entity_birth_cooldown(10)  # not configured yet
        self.set_entity_life_span((100, 200))  # not configured yet
        self.set_entity_speed(1)  # not configured yet
        self.set_entity_vision(5)  # not configured yet

        self.set_entity_name("Fish")
        self.set_entity_type(1)
        self.set_entity_zone(("Near Beach", "Mid Ocean"))
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_preys(["Plankton"])


class Shark(Entity):
    def __init__(self, age=0, hunger=0) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(50)
        self.set_entity_life_span((300, 500))
        self.set_entity_speed(0)
        self.set_entity_vision(20)

        self.set_entity_name("Shark")
        self.set_entity_type(3)
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_zone(("Near Beach", "Mid Ocean", "Far Ocean"))
        self.set_entity_preys(["Fish", "Medusa"])


class Orca(Entity):
    def __init__(self, age=0, hunger=0) -> None:
        super().__init__()
        self.set_entity_age(age)
        self.set_entity_hunger(hunger)

        self.set_entity_birth(10)
        self.set_entity_birth_cooldown(10)   # not configured yet
        self.set_entity_life_span((400, 500))  # not configured yet
        #self.set_entity_life_span((50, 90))  # not configured yet
        self.set_entity_speed(0)  # not configured yet
        self.set_entity_vision(0)  # not configured yet

        self.set_entity_name("Orca")
        self.set_entity_type(4)
        self.set_entity_depth(("Surface Sea", "Sea"))
        self.set_entity_life_style("Group")
        self.set_entity_zone(("Near Beach", "Mid Ocean", "Far Ocean"))
        self.set_entity_preys(["Fish", "Medusa", "Shark"])