import random
class controller():
    def __init__(self,world):
        self.world = world
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    # DEPLACEMENT IDLE D'UNE ENTITE (STOCHASTIQUE)
    def idle_update(self, x, y):
        entity = self.world.entities[(x, y)]
        name = entity.entity_name
        movement = entity.get_last_movement()
        weight_dict = {
            (-1, 0): [0.1, 0.7, 0.1, 0.1],
            (0, 1): [0.1, 0.1, 0.7, 0.1],
            (1, 0): [0.7, 0.1, 0.1, 0.1],
            (0, -1): [0.1, 0.1, 0.1, 0.7]
        }
        #Si le dernier mouvement est inconnu, on prend une direction aléatoire, sinon on prend une direction aléatoire en privilégiant le dernier mouvement
        weights = weight_dict.get(movement, [0.25]*4)
        dx, dy = random.choices(self.directions, weights=weights)[0]
        new_x, new_y = x + dx, y + dy
        # On déplace l'entité
        self.world.clear_entity(x, y)
        self.world.set_entity(name, new_x, new_y)
        # On met à jour le dernier mouvement
        entity.set_last_movement(dx, dy)

    # UPDATE D'UNE ENTITE
    def update_entity(self, x, y):

        #UPDATE QUAND RIEN NE SE PASSE (PAS DE PROIE, PAS DE PREDATEUR, ETC.)
        self.idle_update(x, y)

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

            