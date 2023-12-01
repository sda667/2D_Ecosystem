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


    
    def showWorld(self, world: wd.World):
        grid = world.getGrid
        i_size, j_size = grid.shape
        for i in range(i_size):
            for j in range(j_size):
                case = grid[(i, j)]
                print(case.case_type)
                label_image = QLabel(self)
                label_image.setGeometry(i*50, j*50, 50, 50)
                label_image.setPixmap(self.forest_pixmap)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow(1280, 720)
    window.show()
    world = wd.World(10, 10)
    world.create_world()
    window.showWorld(world)

    
    sys.exit(app.exec_())