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
from stru import App as STRUCTURE
from hybrid import App as newhybrid

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
        self.resize(500, 200)

        self.img = QLabel(self)
        pixmap = QPixmap(resource_path('img.png'))
        pixmap = pixmap.scaled(480, 200, Qt.KeepAspectRatio)
        self.img.setPixmap(pixmap)
        #self.img.resize(300,50)
        
        #self.resize(pixmap.width(),pixmap.height())
        self.img.move(5, 5)

        self.text = QLabel(self)
        self.text.setText('Please select a software to run:')
        self.text.move(40,160)

        self.btn = QPushButton('STRUCTURE', self)
        self.btn.move(230, 155)
        self.btn.clicked.connect(lambda: self.doAction('STRUCTURE'))

        self.btn = QPushButton('NEWHYBRIDS', self)
        self.btn.move(340, 155)
        self.btn.clicked.connect(lambda: self.doAction('newhybrid'))

        self.show()

    def doAction(self, _software):
        if _software == 'STRUCTURE':
            STRUCTURE()
        elif _software == 'newhybrid':
            newhybrid()
   

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())