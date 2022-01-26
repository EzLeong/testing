import sqlite3
import datetime

current = datetime.datetime.now()
date = str(current.day)+"/" + str(current.month) + "/" + str(current.year)
print(date)
con = sqlite3.connect("db/traffic_db.db")
cur = con.cursor() 
cur.execute('SELECT time,rate FROM traffic_data WHERE Date=\''+date+"\'")
data = cur.fetchall()
#print(data[1][1])
# user = "Weeee"
# cur.execute('SELECT password FROM login_info WHERE username =\''+user+"\'")
print(data)
print(data[0][1])
print(len(data))
date_list=[]
rate_list=[]
for i in range (0,len(data)):
    if data[i][0] == "12am" or data[i][0] == "6am" or data[i][0] == "12pm" or data[i][0] == "6pm" or data[i][0] == "11pm" or i == len(data)-1:
        date_list.append(data[i][0])
    else:
        date_list.append("")
    rate_list.append(data[i][1])

print(date_list)
print(rate_list)
print(len(rate_list))
con.commit()

