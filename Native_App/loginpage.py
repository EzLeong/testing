import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QStackedWidget, QWidget
from PyQt5.QtCore import *
import sqlite3
import datetime
import random, string

class LoginScreen(QMainWindow):
    
    def __init__(self):
        super(LoginScreen,self).__init__()
        loadUi("login.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.signup.clicked.connect(self.gotocreate)
        self.backb.clicked.connect(self.gotowelcome)

    def gotowelcome(self):
        welcome = WelcomeScreen()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def loginfunction(self):
        user = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(user)==0 or len(password)==0:
            self.error.setText("Please input all fields")

        else:
            conn = sqlite3.connect("db/traffic_db.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login_info WHERE username =\''+user+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]
            if result_pass == password:
                print("Successfully logged in")
                self.error.setText("")
                menu = MenuScreen(user)
                widget = QtWidgets.QStackedWidget()
                widget.addWidget(menu)
                widget.setCurrentIndex(widget.currentIndex()+1)

            else:
                self.error.setText("Invalid username or password") 