import random
class controller():
    def __init__(self,world):
        self.world = world
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    # DEPLACEMENT IDLE D'UNE ENTITE (STOCHASTIQUE)
    def idle_entity(self, x, y):
        entity = self.world.entities[(x, y)]
        if entity.entity_name == "Shark":
            if entity.get_last_movement() == (0, 0):
                dx, dy = random.choice(self.directions)
            else:
                if entity.get_last_movement() == (-1, 0):
                    weights = [0.1, 0.7, 0.1, 0.1]
                
                elif entity.get_last_movement() == (0, 1):
                    weights = [0.1, 0.1, 0.7, 0.1]
                
                elif entity.get_last_movement() == (1, 0):
                    weights = [0.7, 0.1, 0.1, 0.1]

                elif entity.get_last_movement() == (0, -1):
                    weights = [0.1, 0.1, 0.1, 0.7]
                dx, dy = random.choices(self.directions, weights=weights)[0] 
            new_x = x + dx
            new_y = y + dy

            self.world.clear_entity(x, y)
            self.world.set_entity("Shark", new_x, new_y)
            
            entity.set_last_movement(dx, dy)

    # UPDATE D'UNE ENTITE
    def update_entity(self, x, y):
        self.idle_entity(x, y)

    # UPDATE DES ENTITES
    def update_entities(self):
        # Set des positions des entités
        entity_positions = set()  
        # Récupération des positions des entités
        for i in range(self.world.entities.shape[0]):
            for j in range(self.world.entities.shape[1]):
                if self.world.entities[i, j] != 0:
                    entity_positions.add((i, j))  # Add entity position to the set
        # Update des entités
        for position in entity_positions:
            self.update_entity(*position)  # Update each entity position

            