import sqlite3
import datetime

con = sqlite3.connect("App/Database.db")
cur = con.cursor()

# query = '''CREATE TABLE TRAFFIC_DATA(
#     Area TEXT,
#     time TEXT,
#     rate INT 
# )'''

# cur.execute(query)
# con.commit()
import random, string
# x=[]
# y=[]
# for i in range (0,24):
#     #a = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
#     cur.execute('INSERT INTO traffic_data (Date) VALUES (?)',(25))
#     con.commit()
    # x.append(a)
    # y.append(False)
# print(x)
# print(y)
date_list = []
x = ['12am','1am','2am','3am','4am','5am','6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm','11pm']
y = []
y1 = []
y2 = []
current = datetime.datetime.now()

for i in range (0,7):
    days = datetime.timedelta(7-i-1)
    new_date = current - days
    date_str = str(new_date.day)+"/" + str(new_date.month) + "/"+ str(new_date.year)
    date_list.append(date_str)
    rand_traff=[]
    rand_traff1=[]
    rand_traff2=[]
    for b in range (0,24):
        rand_num = random.randint(0,100)
        rand_traff.append(rand_num)
        rand_num1 = random.randint(0,100)
        rand_traff1.append(rand_num1)
        rand_num2 = random.randint(0,100)
        rand_traff2.append(rand_num2)
    y.append(rand_traff)
    y1.append(rand_traff1)
    y2.append(rand_traff2)
    
 
for i in range (0,len(y)):
     print(y[i])
     print(y1[i])
     print(y2[i])

a = 0
for date in date_list:
    for i in range(0,len(x)):
        cur.execute('INSERT INTO traffic_data (Date,time,jalan_templer,jalan_gasing,jalan_pj) VALUES (?,?,?,?,?)',(date,x[i],y[a][i],y1[a][i],y2[a][i]))
        con.commit()
    a+=1

con.close()