import mysql.connector
mydb=mysql.connector.connect(host="localhost", user="root", passwd="lenovog500s",database="datab")
print(mydb)
if(mydb):
    print("yes")
else:
    print("no")

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE datab")
mycursor.execute("SHOW DATABASES")

mycursor.execute("SHOW TABLES")
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE kkl(id INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(255), Address VARCHAR(255), Rating FLOAT(2), Vote INT(255), Area VARCHAR(255), TypeOfRestaurant VARCHAR(255),Contact VARCHAR(255), Cuisines VARCHAR(255))")

print("----------------")
sql = "INSERT INTO kkl (Name,Address,Rating,Vote,Area,TypeOfRestaurant,Contact,Cuisines) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
val=('Balaji','Mangadu','7.58','34544324','hello yugyuf tydtrse rsrstrdtdc','Dining','hello','Norhihti')
'''val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]'''
print("donnnnneeeeeeee")
mycursor.execute(sql,val)
mydb.commit()

print(mycursor.rowcount, "record inserted.")
print("1 record inserted, ID:", mycursor.lastrowid)
mycursor.execute("SELECT * FROM kkl")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
