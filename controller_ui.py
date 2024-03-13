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
        if event_key == pg.K_w:
            if self.world.sun:
                if self.world.light != 1:
                    print("light -1 ")
                    self.world.light -= 1
                elif self.world.light == 1:
                    print("unlight sun")
                    self.world.light -= 1
                    self.world.sun = False
        elif event_key == pg.K_x:
            if self.world.sun:
                if self.world.light != 10:
                    print("light +1 ")
                    self.world.light += 1
            else:
                print("relight sun")
                self.world.light += 1
                self.world.sun = True
        if event_key == pg.K_LEFT:
            i = self.world.target[0]
            for j in range(self.world.target[1]-1, -1, -1):
                if self.world.entities[i, j] != 0:
                    self.world.target = (i, j)
                    return

            for i in range(self.world.target[0]-1, -1, -1):
                for j in range(self.world.entities.shape[1]-1, -1, -1):
                    if self.world.entities[i, j] != 0:
                        self.world.target = (i, j)
                        return
        elif event_key == pg.K_RIGHT:
            i = self.world.target[0]
            for j in range(self.world.target[1]+1, self.world.entities.shape[1]):
                if self.world.entities[i, j] != 0:
                    self.world.target = (i, j)
                    return

            for i in range(self.world.target[0]+1, self.world.entities.shape[0]):
                for j in range(self.world.entities.shape[1]):
                    if self.world.entities[i, j] != 0:
                        self.world.target = (i, j)
                        return



        else:
            pass
