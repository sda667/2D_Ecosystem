class controller():
    def __init__(self,world):
        self.world = world

    def update_entities(self,entity):
        pass
    def update_entity(self, x, y):
        if self.world.entities[(x, y)].entity_name == "Shark":
            self.world.clear_entity(x, y)
            self.world.set_entity("Shark", x+1, y)