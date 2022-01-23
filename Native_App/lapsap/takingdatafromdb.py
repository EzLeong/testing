import sqlite3

con = sqlite3.connect("db/traffic_db.db")
cur = con.cursor() 
cur.execute("select * from traffic_data")
data = cur.fetchone()
#print(data[1][1])
# user = "Weeee"
# cur.execute('SELECT password FROM login_info WHERE username =\''+user+"\'")
print(data)
