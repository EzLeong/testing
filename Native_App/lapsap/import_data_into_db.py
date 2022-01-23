import sqlite3

con = sqlite3.connect("db/traffic_db.db")
cur = con.cursor()

# query = '''CREATE TABLE TRAFFIC_DATA(
#     Area TEXT,
#     time TEXT,
#     rate INT 
# )'''

# cur.execute(query)
# con.commit()
import random, string
x=[]
y=[]
for i in range (0,10):
    a = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    cur.execute('INSERT INTO vehicle_id (id,emergency_status) VALUES (?,?)',(a,False))
    con.commit()
    # x.append(a)
    # y.append(False)
# print(x)
# print(y)

# x = ['12am','1am','2am','3am','4am','5am','6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm','11pm']
# y = [5,3,0,0,0,0,6,59,86,82,48,31,35,40,35,35,38,61,89,88,54,25,15,10]

# for i in range(0,len):
#     cur.execute('INSERT INTO traffic_data (time,rate) VALUES (?,?)',(x[i],y[i]))
#     con.commit()

con.close()