from queue import Empty
from PyQt5 import QtWidgets, uic, QtGui
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import sqlite3
import os
import datetime

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('trafficgraph.ui', self)
        current_date = datetime.datetime.now()
        date_today = str(current_date.day) + "/" + str(current_date.month) + "/" + str(current_date.year)
        # area = self.areabox.currentIndex()
        self.plotting(date_today)
        self.areabox.currentIndexChanged.connect(lambda: self.selectionchange(current_date))
        self.daysbox.currentIndexChanged.connect(lambda: self.selectionchange(current_date))

    def plotting (self,date):
        con = sqlite3.connect("db/traffic_db.db")
        cur = con.cursor()
        area = self.areabox.currentIndex()
        if area == 1:
            cur.execute('SELECT time,jalan_templer FROM traffic_data WHERE Date=\''+date+"\'")
        elif area == 2:
            cur.execute('SELECT time,jalan_gasing FROM traffic_data WHERE Date=\''+date+"\'")
        elif area == 3:
            cur.execute('SELECT time,jalan_pj FROM traffic_data WHERE Date=\''+date+"\'")
        data = cur.fetchall()
        x=[]
        y=[]
       
        for i in range (0,len(data)):
            if data[i][0] == "12am" or data[i][0] == "6am" or data[i][0] == "12pm" or data[i][0] == "6pm" or data[i][0] == "11pm" or i == len(data)-1:
                x.append(data[i][0])
            else:
                x.append("")
            y.append(data[i][1])
        
        xdict = dict(enumerate(x))
        xax = self.graphWidget.getAxis('bottom')
        yax = self.graphWidget.getAxis('left')
        xax.setTicks([xdict.items()])

        self.graphWidget.setBackground(QtGui.QColor(0,255,255,0))
        xax.setPen((0,0,0),width=2)
        xax.setTextPen((0,0,0),width=2)
        yax.setPen((0,0,0),width=2)
        yax.setTextPen((0,0,0),width=2)
        self.graphWidget.setYRange(0,100)
        pen = pg.mkPen(color=(255,0,0), width=2)
        self.graphWidget.plot(list(xdict.keys()), y, pen=pen, symbol='o',symbolPen=('k'),symbolBrush=((255,255,255)))
        self.graphWidget.showGrid(y=True)
        xdict = dict(enumerate(x))
        xax = self.graphWidget.getAxis('bottom')
        yax = self.graphWidget.getAxis('left')
        xax.setTicks([xdict.items()])

        self.graphWidget.setBackground(QtGui.QColor(0,255,255,0))
        xax.setPen((0,0,0),width=2)
        xax.setTextPen((0,0,0),width=2)
        yax.setPen((0,0,0),width=2)
        yax.setTextPen((0,0,0),width=2)
        self.graphWidget.setYRange(0,100)
        pen = pg.mkPen(color=(255,0,0), width=2)
        self.graphWidget.plot(list(xdict.keys()), y, pen=pen, symbol='o',symbolPen=('k'),symbolBrush=((255,255,255)))
        self.graphWidget.showGrid(y=True)

        if len(y) != 0:
            if self.daysbox.currentIndex() == 0:
                ylast = y[-1]
                self.currenttd.setText("Current Traffic Density:  ")
                self.currenttd2.setText(str(ylast)+"%")
            else:
                self.currenttd.setText("")
                self.currenttd2.setText("")

            yavg = sum(y)/len(y)
            self.avgtd2.setText(str(round(yavg,2))+"%")
            
            ymax = max(y)
            ymaxidx = y.index(ymax)
            if ymaxidx >=12:
                self.peaktd2.setText(str(ymax)+"%"+" at "+str(ymaxidx%12)+"pm")
            else:
                self.peaktd2.setText(str(ymax)+"%"+" at "+str(ymaxidx)+"am")

    def selectionchange(self,current_date):
        selected = self.daysbox.currentIndex()
        print(selected)
        days = datetime.timedelta(selected)
        current = current_date - days
        date = str(current.day) + "/" + str(current.month) + "/" + str(current.year)
        self.graphWidget.clear()
        self.plotting(date)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()