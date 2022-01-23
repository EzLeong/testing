import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QStackedWidget, QWidget
from PyQt5.QtCore import *
import sqlite3
import datetime
import random, string
import loginpage as l


class WelcomeScreen(QMainWindow):
    def __init__(self,app):
        super(WelcomeScreen,self).__init__()
        loadUi("welcomescreen.ui",self)
        self.login.clicked.connect(self.gotologin)

    def gotologin(self):
       login = l.LoginScreen()
       widget = QtWidgets.QStackedWidget()
       widget.addWidget(login)
       widget.setCurrentIndex(widget.currentIndex()+1)
       print(widget.currentIndex())
       try:
            sys.exit(app.exec_())
       except:
            print("Exiting")