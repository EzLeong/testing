import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3
import datetime
import random, string


class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen,self).__init__()
        loadUi("welcomescreen.ui",self)
        self.roaduserb.clicked.connect(self.gotologin)
        self.adminb.clicked.connect(self.gotoelogin)

    def gotoelogin(self):
        elogin = eLoginScreen()
        widget.addWidget(elogin)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print(widget.currentIndex())

    def gotologin(self):
       login = LoginScreen()
       widget.addWidget(login)
       widget.setCurrentIndex(widget.currentIndex()+1)
       print(widget.currentIndex())

#road user interface
class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen,self).__init__()
        loadUi("login.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.signup.clicked.connect(self.gotocreate)
        self.backb.clicked.connect(self.back)

    def back(self):
        widget.removeWidget(self)
        print(widget.currentIndex())

    def gotomenu(self,user):
        menu = MenuScreen(user)
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print(widget.currentIndex())

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print(widget.currentIndex())

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
            if result_pass is not None:
                if result_pass == password:
                    print("Successfully logged in")
                    self.error.setText("")
                    self.usernamefield.clear()
                    self.passwordfield.clear()
                    self.gotomenu(user)
                else:
                    self.error.setText("Invalid username or password") 
            else:
                self.error.setText("Invalid username or password")

class CreateAccScreen(QMainWindow):
    def __init__(self):
        super(CreateAccScreen,self).__init__()
        loadUi("createacc.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordfield_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupb.clicked.connect(self.signup)
        self.backb.clicked.connect(self.back)

    def back(self):
       widget.removeWidget(self)
       print(widget.currentIndex())

    def signup(self):
        user = self.usernamefield.text()
        passw1 = self.passwordfield.text()
        passw2 = self.passwordfield_2.text()
        conn = sqlite3.connect("db/traffic_db.db")
        cur = conn.cursor()
        
        if len(user)==0 or len(passw1)==0 or len(passw2)==0:
             self.error.setText("Please fill in all inputs")

        elif passw1!=passw2:
            self.error.setText("Passwords do not match.")

        else:
            #self.error.setText("")
            user_info = [user, passw1]
            try:
                cur.execute('INSERT INTO login_info (username,password) VALUES (?,?)', user_info)
                conn.commit()
                widget.removeWidget(self)
                print(widget.currentIndex())

            except sqlite3.IntegrityError:
                self.error.setText("Username already exists! Please reenter a new username.")
                
class MenuScreen(QMainWindow):
    def __init__(self, user):
        super(MenuScreen,self).__init__()
        loadUi("menupage.ui",self)
        # self.user = user
        # print(user)
        self.displayname.setText(user)
        self.reportb.clicked.connect(lambda: self.gotoreport(user))
        self.backb.clicked.connect(self.back)
        self.trafficb.clicked.connect(lambda: self.gototraffic(user))

    def gototraffic(self,user):
        traffic = TrafficGraph(user)
        widget.addWidget(traffic)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print(widget.currentIndex())

    def back(self):
       widget.removeWidget(self)
       print(widget.currentIndex())

    def gotoreport(self,user):
        report = ReportScreen(user)
        widget.addWidget(report)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print(widget.currentIndex())
        
class ReportScreen(QMainWindow):
    def __init__(self,user):
        super(ReportScreen,self).__init__()
        loadUi("reportscreen.ui",self)
        self.displayname.setText(user)
        self.breakdown.stateChanged.connect(self.uncheck)
        self.accident.stateChanged.connect(self.uncheck)
        self.potholes.stateChanged.connect(self.uncheck)
        self.others.stateChanged.connect(self.uncheck)
        self.submitb.clicked.connect(lambda: self.check(user))
        self.backb.clicked.connect(self.back)
        self.reportlist.clicked.connect(lambda: self.gotoreportlist(user))

    def gotoreportlist(self, user):
        reportlist = ReportList(user)
        widget.addWidget(reportlist)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def back(self):
       widget.removeWidget(self)
       print(widget.currentIndex())

    def uncheck(self, state):
  
        # checking if state is checked
        if state == Qt.Checked:
            
            # if first check box is selected
            if self.sender() == self.breakdown:
                self.box_chosen = self.breakdown.text()
                print(self.box_chosen)
                # making other check box to uncheck
                self.accident.setChecked(False)
                self.potholes.setChecked(False)
                self.others.setChecked(False)
  
            # if second check box is selected
            elif self.sender() == self.accident:
                self.box_chosen = self.accident.text()
                # making other check box to uncheck
                self.breakdown.setChecked(False)
                self.potholes.setChecked(False)
                self.others.setChecked(False)
  
            # if third check box is selected
            elif self.sender() == self.potholes:
                self.box_chosen = self.potholes.text()
                # making other check box to uncheck
                self.breakdown.setChecked(False)
                self.accident.setChecked(False)
                self.others.setChecked(False)

            elif self.sender() == self.others:
                self.box_chosen = self.others.text()
                # making other check box to uncheck
                self.breakdown.setChecked(False)
                self.accident.setChecked(False)
                self.potholes.setChecked(False)

    def check(self, user):
        area = self.areabox.currentText()
        checkbox_list = [self.breakdown.isChecked(), self.accident.isChecked(), self.potholes.isChecked(), self.others.isChecked()]
        description = self.descriptiontext.toPlainText()
        print(checkbox_list)

        conn = sqlite3.connect("db/traffic_db.db")
        cur = conn.cursor()

        if area == "--Select Area--":
            self.error.setText("Please select an area!")
        elif sum(checkbox_list)==0:
            self.error.setText("Please select a reason for report!")
        else:
            self.error.setText("")
            current = datetime.datetime.now()
            current_date = str(current.day) + "/" + str(current.month) + "/" + str(current.year)
            current_time = str(current.hour) + ":" + str(current.minute)
            report_id =  ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            answer_list = [user, area, report_id, self.box_chosen, description, current_date, current_time, "pending" ]
            cur.execute('INSERT INTO report (Name,Area,Report_ID,Reason,Description,Date,Time,Status) VALUES (?,?,?,?,?,?,?,?)',answer_list)
            conn.commit()
            widget.removeWidget(self)

class ReportList(QMainWindow):
    def __init__(self, user):
        super(ReportList,self).__init__()
        loadUi("reportlist.ui",self)
        self.reportTable.setColumnWidth(0,75)
        self.reportTable.setColumnWidth(1,100)
        self.reportTable.setColumnWidth(2,100)
        self.reportTable.setColumnWidth(3,75)
        self.reportTable.setColumnWidth(4,80)
        self.reportTable.setHorizontalHeaderLabels(["Report ID", "Area", "Reason", "Date", "Status"])
        stylesheet = "::section{Background-color:rgba(255,255,255,150)}"
        self.reportTable.horizontalHeader().setStyleSheet(stylesheet)   
        self.loaddata(user)
        self.backb.clicked.connect(self.back)

    def back(self):
        widget.removeWidget(self)

    def loaddata(self,user):
        con = sqlite3.connect("db/traffic_db.db")
        cur = con.cursor()
        query = 'SELECT * FROM report WHERE Name =\''+user+"\'"

        tablerow = 0
        for row in cur.execute(query):
            self.reportTable.setRowCount(tablerow+1)
            print(row)
            self.reportTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[2]))
            self.reportTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.reportTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.reportTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[5]))
            self.reportTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[7]))

            tablerow += 1

class TrafficGraph(QMainWindow):
    def __init__(self,user):
        super(TrafficGraph,self).__init__()
        loadUi("trafficgraph.ui",self)
        self.backb.clicked.connect(self.back)
        hour = [1,2,3,4,5,6,7,8,9,10]
        perc = [30,32,34,32,33,31,29,32,35,45]
        self.plot(hour, perc)

    def plot(self, x, y):
        self.graphWidget.plot(x, y)

    def back(self):
        widget.removeWidget(self)

#admin interface
class eLoginScreen(QMainWindow):
    def __init__(self):
        super(eLoginScreen,self).__init__()
        loadUi("emergencylogin.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.backb.clicked.connect(self.back)

    def back(self):
        widget.removeWidget(self)

    def gotoemenu(self,user):
        menu = eMenuScreen(user)
        widget.addWidget(menu)
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
            if result_pass is not None:
                if result_pass == password:
                    print("Successfully logged in")
                    self.error.setText("")
                    self.usernamefield.clear()
                    self.passwordfield.clear()
                    self.gotoemenu(user)
                    # menu = eMenuScreen(user)
                    # widget.addWidget(menu)
                    # widget.setCurrentIndex(widget.currentIndex()+1)
                else:
                    self.error.setText("Invalid username or password") 
            else:
                self.error.setText("Invalid username or password")

class eMenuScreen(QMainWindow):
    def __init__(self,user):
        super(eMenuScreen,self).__init__()
        loadUi("emergencymenu.ui",self)
        self.displayname.setText(user)
        self.reportb.clicked.connect(lambda: self.gotoreport(user))
        self.backb.clicked.connect(self.back)
        self.trafficb.clicked.connect(lambda: self.gototraffic(user))
        self.emodeb.clicked.connect(self.gotoemergency)

    def gototraffic(self,user):
        traffic = TrafficGraph(user)
        widget.addWidget(traffic)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def back(self):
       widget.removeWidget(self)

    def gotoreport(self,user):
        report = ReportScreen(user)
        widget.addWidget(report)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoemergency(self):
        em = EmergencyScreen()
        widget.addWidget(em)
        widget.setCurrentIndex(widget.currentIndex()+1)


class EmergencyScreen(QMainWindow):
    def __init__(self):
        super(EmergencyScreen,self).__init__()
        loadUi("emergency.ui",self)
        #self.additemsintobox
        self.backb.clicked.connect(self.back)
        con = sqlite3.connect("db/traffic_db.db")
        cur = con.cursor()
        vehicle_id = [vehicle_id[0] for vehicle_id in cur.execute("SELECT id FROM vehicle_id")]
        con.commit()
        con.close()
        #print(vehicle_id)
        completer = QCompleter(vehicle_id)
        self.vehicleidfield.setCompleter(completer)
        self.onb.clicked.connect(lambda: self.check("ON"))
        self.offb.clicked.connect(lambda: self.check("OFF"))

    def check(self,status):
        v_id = self.vehicleidfield.text()
        con = sqlite3.connect("db/traffic_db.db")
        cur = con.cursor()
        if len(v_id)==0:
            self.error.setText("Please input vehicle id")
        else:
            cur.execute('SELECT * FROM vehicle_id WHERE id =\''+v_id+"\'")
            result = cur.fetchone()
            if result is None:
                self.error.setText("Wrong vehicle id input")
            else:
                eid = result[0]
                estatus = result[1]
                if status=="ON" and estatus==1:
                    self.error.setText("The vehicle selected is already in Emergency Mode")
                elif status=="ON" and estatus==0:
                    print("change status")
                    query='UPDATE vehicle_id SET emergency_status = 1 WHERE id = \''+eid+"\'"
                    cur.execute(query)
                    con.commit()
                    self.error.setText("Successfully turned vehicle "+eid+" to Emergency Mode")
                elif status=="OFF" and estatus==0:
                    self.error.setText("The vehicle selected is already in Normal Mode")
                elif status=="OFF" and estatus==1:
                    print("change status")
                    query='UPDATE vehicle_id SET emergency_status = 0 WHERE id = \''+eid+"\'"
                    cur.execute(query)
                    con.commit()
                    self.error.setText("Successfully turned vehicle "+eid+" to Normal Mode")




    def back(self):
        widget.removeWidget(self)

    





#main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(450)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")