import mysql.connector as mc
mydb=mc.connect(host="localhost",user="python",password="lenovog500s",database="python")
print(bool(mydb))
mycursor=mydb.cursor(buffered=True)
ms="insert into ece values(%s,%s,%s)"
#kl=[("Vijay",32,78),("Ajith",45,78),("Dhanush",56,78),("Rajini",14,46)]
#mycursor.executemany(ms,kl)
mycursor.execute("select * from ece")
ls=mycursor.fetchall()
print("One",mycursor.fetchone())
print("ls",ls)
mydb.commit()
for i in mycursor:
    print(i)


