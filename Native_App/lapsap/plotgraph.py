from PyQt5 import QtWidgets, uic, QtGui
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import sqlite3
import os
import csv

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('trafficgraph.ui', self)

        con = sqlite3.connect("db/traffic_db.db")
        cur = con.cursor() 
        cur.execute("select * from traffic_data")
        with open("traffic_data.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)
        
        #dirpath = os.getcwd() + "/traffic_data.csv"
        #print "Data exported Successfully into {}".format(dirpath)

        x = ['12am','','','','','','6am','','','','','','12pm','','','','','','6pm','','','','','11pm']
        xdict = dict(enumerate(x))
        y = [5,3,0,0,0,0,6,59,86,82,48,31,35,40,35,35,38,61,89,88,54,25,15,10]
        xax = self.graphWidget.getAxis('bottom')
        yax = self.graphWidget.getAxis('left')
        xax.setTicks([xdict.items()])

        self.graphWidget.setBackground(QtGui.QColor(0,255,255,0))
        xax.setPen((0,0,0),width=2)
        xax.setTextPen((0,0,0),width=2)
        yax.setPen((0,0,0),width=2)
        yax.setTextPen((0,0,0),width=2)
        pen = pg.mkPen(color=(255,0,0), width=2)
        self.graphWidget.plot(list(xdict.keys()), y, pen=pen, symbol='o',symbolPen=('k'),symbolBrush=((255,255,255)))
        self.graphWidget.showGrid(y=True)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()