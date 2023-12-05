import typing
from PyQt5 import QtCore
import world as wd
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
import json

class mainWindow(QWidget):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        with open('config.json') as f:
            self.config = json.load(f)
        self.initUI(width, height)

    def initUI(self, width, height):
        #Taille et nom de la fenêtre
        self.setGeometry(100, 100, width, height)
        self.setWindowTitle("2D_simulation")

        #Initialisation des pixmap
        self.forest_pixmap = QPixmap(self.config['TilesPath']['path_forest'])
        self.mountain_pixmap = QPixmap(self.config['TilesPath']['path_mountain'])

        #Taille de la grille
        self.grid_size = self.config['GridSize']['grid_size_factor']


    
    def showWorld(self, world: wd.World):
        grid = world.getGrid
        i_size, j_size = grid.shape
        for i in range(i_size):
            for j in range(j_size):
                case = grid[(i, j)]
                label_image = QLabel(self)
                label_image.setGeometry(i*(self.grid_size//i_size), j*((self.grid_size+j_size)//i_size), self.grid_size//i_size, self.grid_size//i_size)
                if case.case_type == "FOREST":
                    label_image.setPixmap(self.forest_pixmap)
                elif case.case_type == "MOUNTAIN":
                    label_image.setPixmap(self.mountain_pixmap)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow(1280, 720)
    
    world = wd.World(20, 20)
    world.create_world()
    window.showWorld(world)
    window.show()
    
    sys.exit(app.exec_())

