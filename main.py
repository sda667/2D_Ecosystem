import typing
from PyQt5 import QtCore
import world as wd
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap

class mainWindow(QWidget):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.initUI(width, height)

    def initUI(self, width, height):
        #Taille et nom de la fenêtre
        self.setGeometry(100, 100, width, height)
        self.setWindowTitle("2D_simulation")

        #Initialisation des pixmap
        self.forest_pixmap = QPixmap('forest_image.jpg')
        self.mountain_pixmap = QPixmap('mountain_image.jpg')

        self.label_image = QLabel(self)
        self.label_image.setGeometry(0, 0, 50, 50)

        image_path = 'forest_image.jpg'
        self.pixmap = QPixmap(image_path)
        self.pixmop = QPixmap('mountain_image.jpg')
        self.label_image.setPixmap(self.pixmap)
        self.label_image.setPixmap(self.mountain_pixmap)

    def afficher_image_aux_coordonnees(self, image_path, x, y, largeur, hauteur):
        # Charger l'image depuis un fichier PNG
        pixmap = QPixmap(image_path)

        # Redimensionner l'image si nécessaire
        pixmap = pixmap.scaled(largeur, hauteur)

        # Afficher l'image dans le QLabel aux coordonnées spécifiées
        self.label_image.setGeometry(x, y, largeur, hauteur)
        self.label_image.setPixmap(pixmap)
        self.label_image.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow(1280, 720)
    #window.afficher_image_aux_coordonnees("forest_image.png", 50, 50, 50, 50)
    window.show()
    
    sys.exit(app.exec_())