import math
import random
from priority_queue import PriorityQueue  # USING priority queue used in project 311

# MOUVEMENTS POSSIBLES (ENUM?)
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3


class controller():
    def __init__(self, world):
        self.world = world
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # DEPLACEMENT IDLE D'UNE ENTITE (STOCHASTIQUE, MARCHE ALEATOIRE A MEMOIRE)
    def move(self, entity, start, end):
        self.world.entities[end] = entity
        self.world.clear_entity(*start)
        entity.set_entity_speed_cooldown(entity.entity_speed)

    def entity_positions_list_update(self, entity_positions, old_position, new_position):
        for i in range(len(entity_positions)):
            if entity_positions[i] == old_position:
                entity_positions[i] = new_position
                return

    def __idle_update(self, x, y, entity_positions):
        entity = self.world.entities[(x, y)]
        name = entity.entity_name
        movement = entity.get_last_movement()
        weight_dict = {
            (-1, 0): [0.1, 0.7, 0.1, 0.1],
            (0, 1): [0.1, 0.1, 0.7, 0.1],
            (1, 0): [0.7, 0.1, 0.1, 0.1],
            (0, -1): [0.1, 0.1, 0.1, 0.7]}

        # Action suivant le dernier mouvement, s'ils est inconnu: aléatoire
        weights = weight_dict.get(movement, [0.25] * 4)
        dx, dy = random.choices(self.directions, weights=weights)[0]
        new_x, new_y = x + dx, y + dy
        while not self.world.inboard((new_x, new_y)):
            dx, dy = random.choices(self.directions, weights=weights)[0]
            new_x, new_y = x + dx, y + dy

        # Déplacement d'entité
        if self.world.normal_movement_condition(new_x, new_y):
            self.move(entity, (x, y), (new_x, new_y))
            self.entity_positions_list_update(entity_positions, (x, y), (new_x, new_y))
            entity.set_last_movement(dx, dy)

    # DEPLACEMENT D'UN PREDATEUR (CHASSE, SE DEPLACE VERS LA PROIE LA PLUS PROCHE, S'IL Y EN A UNE A PORTEE)
    def __predator_update(self, x, y, entity_positions):
        myself = self.world.entities[(x, y)]
        preys = []
        # Liste des proies possibles
        for entity_position in entity_positions:
            if entity_position != (x, y):
                entity = self.world.entities[entity_position]
                if entity.entity_name in myself.prey_set:
                    preys.append(entity_position)

        # Détermine le prédateur le plus proche
        closest_prey = None
        distance = math.inf
        for prey in preys:
            if self.heuristique((x, y), prey) < distance:
                distance = self.heuristique((x, y), prey)
                closest_prey = prey

        # Chemin optimisé vers la proie
        actions = self.astar((x, y), closest_prey)
        if len(actions) != 0:
            action = actions[0]
            dx, dy = self.directions[action]
            new_x, new_y = x + dx, y + dy
            entity = self.world.entities[(x, y)]
            if self.world.predator_condition(new_x, new_y):
                if ((new_x, new_y) == closest_prey):
                    entity.eat(self.world.entities[closest_prey])
                    entity_positions.remove((x, y))
                self.move(entity, (x, y), (new_x, new_y))
                self.entity_positions_list_update(entity_positions, (x, y), (new_x, new_y))
                entity.set_last_movement(dx, dy)

    # S'ENFUIT A L'OPPOSE DU PREDATEUR PROCHE
    def __flee_update(self, x, y, entity_positions):
        myself = self.world.entities[(x, y)]
        enemies = []

        # Tous les prédateurs possibles
        for entity_position in entity_positions:
            if entity_position != (x, y):
                entity = self.world.entities[entity_position]
                if myself.entity_name in entity.prey_set:
                    enemies.append(entity_position)

        # Prédateur le plus proche
        closest_enemy = None
        distance = math.inf
        for enemy in enemies:
            if self.heuristique((x, y), enemy) < distance:
                distance = self.heuristique((x, y), enemy)
                closest_enemy = enemy

        # Détermine la case à atteindre pour s'enfuir
        dx = closest_enemy[0] - x
        dy = closest_enemy[1] - y
        target_position = (x - dx, y - dy)
        if (self.world.predator_condition(*target_position)):
            actions = self.astar((x, y), target_position)
            if len(actions) != 0:
                action = actions[0]
                dx, dy = self.directions[action]
                new_x, new_y = x + dx, y + dy
                entity = self.world.entities[(x, y)]
                if self.world.normal_movement_condition(new_x, new_y):
                    self.move(entity, (x, y), (new_x, new_y))
                    self.entity_positions_list_update(entity_positions, (x, y), (new_x, new_y))
                    entity.set_last_movement(dx, dy)


    # UPDATE DU MOUVEMENT D'UNE ENTITE

    def __update_entity(self, x, y, entity_positions):
        entity = self.world.entities[(x, y)]
        # not implemented yet , the entity think about what to do
        Action = entity.brain((x, y), entity_positions, self.world.entities)
        if Action == "Idle":
            self.__idle_update(x, y, entity_positions)
        elif Action == "Predation":
            self.__predator_update(x, y, entity_positions)
        elif Action == "Flee":
            self.__flee_update(x, y, entity_positions)
        elif Action == "Stay":
            if entity.entity_speed != -1:
                entity.set_entity_speed_cooldown(entity.entity_speed_cooldown - 1)
        elif Action == "Mate":
            self.__mate_update(x, y, entity_positions)

    # UPDATE THE ATTRIBUTS OF A ENTITY AT (X, Y)
    def __status_update(self, x, y, entity_positions):
        entity = self.world.entities[(x, y)]
        entity.set_entity_hunger(entity.entity_hunger + 1)
        entity.set_entity_age(entity.entity_age + 1)
        if entity.entity_name == "Fish" and entity.entity_hunger > 0:
            hunger_recover =  min(self.world.plankton, entity.entity_hunger)
            entity.set_entity_hunger(entity.entity_hunger-hunger_recover)
        if entity.entity_birth > 0:
            entity.set_entity_birth(entity.entity_birth-1)
        if entity.entity_hunger >= 100 or entity.entity_age >= entity.entity_life_span[
            1]:
            self.world.clear_entity(x, y)
            entity_positions.remove((x, y))

        else:
            if entity.entity_age >= entity.entity_life_span[0]:
                if random.choices([0, 1], [0.8, 0.2]) == 1:
                    self.world.clear_entity(x, y)
                    entity_positions.remove((x, y))


    # S'APPROCHER D"UNE CREATURE D"UNE MEME ESPECE ET SE REPRODUIRE
    def __mate_update(self, x, y, entity_positions):
        myself = self.world.entities[(x, y)]
        mates = []

        # Tous les entities de memes especes possibles
        for entity_position in entity_positions:
            if entity_position != (x, y):
                entity = self.world.entities[entity_position]
                if myself.entity_name == entity.entity_name and entity.entity_birth == 0:
                    mates.append(entity_position)

        # le partenaire le plus proche
        closest_mate = None
        distance = math.inf
        for mate in mates:
            if self.heuristique((x, y), mate) < distance:
                distance = self.heuristique((x, y), mate)
                closest_mate = mate
        target_position = closest_mate
        print(myself.entity_name + f" approching position {target_position}")
        actions = self.astar((x, y), target_position)
        if actions == None:
            return
        if len(actions) != 0:
            action = actions[0]
            dx, dy = self.directions[action]
            new_x, new_y = x + dx, y + dy
            entity = self.world.entities[(x, y)]
            if ((new_x, new_y) == closest_mate):
                entity.mate((x, y), self.world.entities[closest_mate], self.world)
            if self.world.normal_movement_condition(new_x, new_y):
                self.move(entity, (x, y), (new_x, new_y))
                self.entity_positions_list_update(entity_positions, (x, y), (new_x, new_y))
                entity.set_last_movement(dx, dy)

    # UPDATE DES ENTITES
    def update_entities(self):
        # Set des positions des entités
        entity_positions = []
        # Récupération des positions des entités
        for i in range(self.world.entities.shape[0]):
            for j in range(self.world.entities.shape[1]):
                if self.world.entities[i, j] != 0:
                    entity_positions.append((i, j))  # Add entity position to the set
        # Update des entités
        for position in entity_positions:
            self.__status_update(*position, entity_positions)
        for position in entity_positions:
            self.__update_entity(*position, entity_positions)  # Update each entity position

    # PLUS COURS CHEMIN AVEC ASTAR
    def astar(self, current_position, target_position):
        stack = PriorityQueue()
        stack.push((current_position, [], 0), self.heuristique(current_position, target_position))
        marked_state = set()
        marked_state.add(current_position)
        while not stack.is_empty():
            smallest_G_H = stack.pop()
            current_position, actions, Greedy = smallest_G_H
            if current_position == target_position:
                return actions
            for next_position, action in self.get_actions(current_position, target_position):
                if next_position in marked_state:
                    continue
                stack.push((next_position, actions + [action], Greedy + 1),
                           Greedy + 1 + self.heuristique(next_position, target_position))
                marked_state.add(next_position)
        return None

    def heuristique(self, position, target_position):
        x_distance = abs(target_position[0] - position[0])
        y_distance = abs(target_position[1] - position[1])
        distance = math.sqrt(math.pow(x_distance, 2) + math.pow(y_distance, 2))
        return distance

    def get_actions(self, position, target_position):
        possible_actions = {UP: (position[0], position[1] + 1), DOWN: (position[0], position[1] - 1),
                            LEFT: (position[0] - 1, position[1]), RIGHT: (position[0] + 1, position[1])}
        real_possible_actions = []
        for direction in possible_actions:
            if self.world.predator_condition(*target_position):
                if possible_actions[direction] == target_position:
                    return [(possible_actions[direction], direction)]
                if self.world.predator_condition(*possible_actions[direction]) and self.world.entities[possible_actions[direction]] == 0:
                    real_possible_actions.append((possible_actions[direction], direction))
        return real_possible_actions
    def plankton_update(self):
        if self.world.sun:
            self.world.plankton = random.choices([0.5, 1, 2, 4], [0.2, 0.5, 0.2, 0.1])[0]
        else:
            self.world.plankton = 0