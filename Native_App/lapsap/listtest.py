import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QStackedWidget, QWidget
from PyQt5.QtCore import *
import sqlite3
import datetime
import random, string

class ReportList(QMainWindow):
    def __init__(self):
        super(ReportList,self).__init__()
        loadUi("reportlist.ui",self)
        user = "patrick cain"

        self.reportTable.setColumnWidth(0,75)
        self.reportTable.setColumnWidth(1,100)
        self.reportTable.setColumnWidth(2,100)
        self.reportTable.setColumnWidth(3,75)
        self.reportTable.setColumnWidth(4,80)
        self.reportTable.setHorizontalHeaderLabels(["Report ID", "Area", "Reason", "Date", "Status"])
        stylesheet = "::section{Background-color:rgba(255,255,255,150)}"
        self.reportTable.horizontalHeader().setStyleSheet(stylesheet)   
        self.loaddata(user)

    def loaddata(self,user):
        con = sqlite3.connect("db/traffic_db.db")
        cur = con.cursor()
        query = 'SELECT * FROM report WHERE Name =\''+user+"\'"

        tablerow = 0
        for row in cur.execute(query):
            self.reportTable.setRowCount(tablerow+1)
            self.reportTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[2]))
            self.reportTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.reportTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.reportTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[5]))
            self.reportTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[7]))

            tablerow += 1


app = QApplication(sys.argv)
welcome = ReportList()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(450)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")