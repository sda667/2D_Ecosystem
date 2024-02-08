import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt
import Controller
import world as wd
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
import json

class mainWindow(QWidget):
    def __init__(self) -> None:
        # init Qwidget
        super().__init__()
        # init configuration
        with open('config.json') as f:
            self.config = json.load(f)
        # init data
        self.initUI()
        # create the word modele
        self.world = wd.World(self.world_x_size, self.world_y_size)
        # create world depending of the configuration and world background
        self.world.create_world(self.config['WorldSettings']['world_background'],self.config['WorldSettings']['world_creature'])
        # create a controller
        self.controller = Controller.controller(self.world)
        # create a timer to make the game continue and not static
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.game_update)
        self.game_timer.start(1000)
        self.temp_labels_storage = []
        # draw the background
        self.draw_background()
        self.draw_foreground()

    def game_update(self):
        while (self.temp_labels_storage):
            image = self.temp_labels_storage.pop()
            image.deleteLater()
        self.world.creatures[0].setposition((0, 1))
        self.update()
        self.draw_foreground()
        self.update()
    def initUI(self):
        # getting window settings and world seting
        self.width = self.config['WindowSettings']['window_width']
        self.height = self.config['WindowSettings']['window_height']
        self.world_x_size = self.config["WorldSettings"]['world_x_size']
        self.world_y_size = self.config["WorldSettings"]['world_y_size']


        #Taille et nom de la fenêtre
        self.setGeometry(100, 100, self.width, self.height)
        self.setWindowTitle("2D_simulation")

        #Initialisation des pixmap
        self.Coral_pixmap = QPixmap(self.config['TilesPath']['path_Coral'])
        self.Sea_pixmap = QPixmap(self.config['TilesPath']['path_Sea'])
        self.Shark_pixmap = QPixmap(self.config['Creatures']['Shark'])

        #Taille de la grille
        self.grid_size = self.config['GridSize']['grid_size_factor']
        self.case_size = self.grid_size // self.world_x_size
    def set_pixelmap(self,label, type):
        # return the pixmap of the correspondant type
        if type == "Sea":
            label.setPixmap(self.Sea_pixmap)
        elif type == "Coral":
            label.setPixmap(self.Coral_pixmap)
        elif type == "Shark":
            label.setPixmap(self.Shark_pixmap)
    def draw_foreground(self):
        for creature in self.world.creatures:
            label_image = QLabel(self)
            label_image.setGeometry(creature.get_position[0] * (self.case_size + creature.get_position[0]), creature.get_position[1] * (self.case_size + creature.get_position[1]),
                                    self.case_size, self.case_size)
            self.set_pixelmap(label_image, creature.get_creature)
            self.temp_labels_storage.append(label_image)
            label_image.show()
    def draw_background(self):
        # create Qlabel to show the world
        grid = self.world.getGrid
        i_size, j_size = grid.shape
        square_size = (self.grid_size // i_size)
        for i in range(i_size):
            for j in range(j_size):
                case = grid[(i, j)]
                label_image = QLabel(self)
                label_image.setGeometry(i * (self.grid_size // i_size) + i, j * ((self.grid_size) // i_size) + j,
                                        self.grid_size // i_size, self.grid_size // i_size)
                self.set_pixelmap(label_image, case.case_type)


if __name__ == "__main__":
    #Creating pyQT5 window
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

