# x = ['12am','1am','2am','3am','4am','5am','6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm','11pm']
# y = [5,3,0,0,0,0,6,59,86,82,48,31,35,40,35,35,38,61,89,88,54,25,15,10]
# z = []

# #z[0]=[x[0]][y[0]]

# for i in range (0,len(x)):
#     col = []
#     a = x[i]
#     b = y[i]
#     # print(a)
#     # print(y[i])
#     col[0] = a
#     col[1] = b
#     z.append(col)

# print(z)



# for i in x:
#     print(x[i])

# checkbox_list = [True, True, False]
# y = checkbox_list.find(True)
# print(y)
import sqlite3

x = testing

def testing(self):
    con = sqlite3.connect("db/traffic_db.db")
    cur = con.cursor()

    #cur.execute("SELECT id FROM vehicle_id")
    vehicle_id = [vehicle_id[0] for vehicle_id in cur.execute("SELECT id FROM vehicle_id")]
    return vehicle_id

print(x)
