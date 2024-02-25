import math
import random
from priority_queue import PriorityQueue # USING priority queue used in project 311


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
        if self.world.inboard((new_x, new_y)) and self.world.grid[new_x, new_y] != 0 and self.world.entities[
            new_x, new_y] == 0:
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
            if self.world.inboard((new_x, new_y)) and self.world.grid[new_x, new_y] != 0:
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
        actions = self.astar((x, y), target_position)
        if len(actions) != 0:
            action = actions[0]
            dx, dy = self.directions[action]
            new_x, new_y = x + dx, y + dy
            entity = self.world.entities[(x, y)]
            if self.world.inboard((new_x, new_y)) and self.world.grid[new_x, new_y] != 0:
                self.move(entity, (x, y), (new_x, new_y))
                self.entity_positions_list_update(entity_positions, (x, y), (new_x, new_y))
                entity.set_last_movement(dx, dy)


    # UPDATE DU STATUT D'UNE ENTITE
    def __update_entity(self, x, y, entity_positions):
        entity = self.world.entities[(x, y)]
        # not implemented yet , the entity think about what to do
        Action = entity.brain((x, y), entity_positions, self.world.entities)
        if Action == "Idle":
            self.__idle_update(x, y, entity_positions)
        elif Action == "Predation":
            print(entity.entity_name + " is hungry")
            self.__predator_update(x, y, entity_positions)
        elif Action == "Flee":
            print(entity.entity_name + " is fleeing")
            self.__flee_update(x, y, entity_positions)
        elif Action == "Stay":
            if entity.entity_speed != -1:
                entity.set_entity_speed_cooldown(entity.entity_speed_cooldown - 1)


    # UPDATE THE ATTRIBUTS OF A ENTITY AT (X, Y)
    def __status_update(self, x, y, entity_positions):
        entity = self.world.entities[(x, y)]
        entity.set_entity_hunger(entity.entity_hunger + 1)
        entity.set_entity_age(entity.entity_age + 1)
        if entity.entity_hunger >= 100 or entity.entity_age >= entity.entity_life_span[
            1]:  # TODO: Create function for death (percentage to go beyond the life span or before it)
            print("died due to hunger or overage")
            self.world.clear_entity(x, y)
            entity_positions.remove((x, y))

        else:
            if entity.entity_age >= entity.entity_life_span[0]:
                if random.randint(0, 1) == 1:
                    print("died due to old age")
                    self.world.clear_entity(x, y)
                    entity_positions.remove((x, y))


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
            if self.world.inboard(possible_actions[direction]):
                if possible_actions[direction] == target_position:
                    return [(possible_actions[direction], direction)]
                if self.world.entities[possible_actions[direction]] == 0:
                    real_possible_actions.append((possible_actions[direction], direction))
        return real_possible_actions