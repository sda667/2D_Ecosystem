import pygame as pg

class ControllerUI:
    def __init__(self, world):
        self.world = world
    def control_world(self, event_key):
        if event_key == pg.K_a:
            print("temperature -1 ")
            self.world.temperature -= 1
        elif event_key == pg.K_z:
            print("temperature +1 ")
            self.world.temperature += 1
        else:
            pass