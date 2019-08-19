from PyQt5 import QtGui
from PyQt5.QtWidgets import (QWidget, QProgressBar, QPushButton, QApplication, QHBoxLayout, QTextEdit, QMessageBox, QLabel)
from PyQt5.QtCore import QBasicTimer, Qt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
import time
import datetime
import os
import sys
import os
from win_struc import App as STRUCTURE
from win_hybrid import App as newhybrid
import multiprocessing
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App(QWidget):
    
    def __init__(self):
        super().__init__()  
        self.initUI()
        self._init_params()
        

    def _init_params(self):
        pass
  

    def initUI(self):   
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Easy Parallel')
        self.resize(800, 300)

        self.img = QLabel(self)
        pixmap = QPixmap(resource_path('img.png'))
        pixmap = pixmap.scaled(780, 250, Qt.KeepAspectRatio)
        self.img.setPixmap(pixmap)
        #self.resize(pixmap.width(),pixmap.height())
        self.img.move(5, 5)

        #self.setStyleSheet("QLabel {font: 10pt}")
        #self.setStyleSheet("QPushButton {font: 10pt}")

        self.text = QLabel(self)
        self.text.setText('Please select a software to run:')
        self.text.move(20,235)

        self.btn = QPushButton('STRUCTURE', self)
        #self.btn.resize(200,40)
        self.btn.move(390, 230)
        self.btn.clicked.connect(lambda: self.doAction('STRUCTURE'))

        self.btn = QPushButton('NEWHYBRIDS', self)
        #self.btn.resize(200,40)
        self.btn.move(560, 230)
        self.btn.clicked.connect(lambda: self.doAction('newhybrid'))

        self.show()

    def doAction(self, _software):
        if _software == 'STRUCTURE':
            STRUCTURE()
        elif _software == 'newhybrid':
            newhybrid()
   

        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())