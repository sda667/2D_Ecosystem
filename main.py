import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer

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
        # create a timer to make the game continue and not static
        #self.game_timer = QTimer(self)
        #self.game_timer.timeout.connect(self.game_update)
        #self.game_timer.start(16)

    def game_update(self):
        pass
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

        #Taille de la grille
        self.grid_size = self.config['GridSize']['grid_size_factor']
    def get_pixemap(self, case):
        # return the pixmap of the correspondant type
        if case.case_type == "Sea":
            return self.Sea_pixmap
        elif case.case_type == "Coral":
            return self.Coral_pixmap

    def showWorld(self):
        # create Qlabel to show the world
        grid = self.world.getGrid
        i_size, j_size = grid.shape
        square_size = (self.grid_size//i_size)
        for i in range(i_size):
            for j in range(j_size):
                case = grid[(i, j)]
                label_image = QLabel(self)
                label_image.setGeometry(i*(self.grid_size//i_size)+i, j*((self.grid_size)//i_size)+j, self.grid_size//i_size, self.grid_size//i_size)
                label_image.setPixmap(self.get_pixemap(case))


if __name__ == "__main__":
    #Creating pyQT5 window
    app = QApplication(sys.argv)
    window = mainWindow()
    #show it
    window.showWorld()
    window.show()
    sys.exit(app.exec_())

