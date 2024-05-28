import mysql.connector as mc
mydb=mc.connect(host="localhost",user="python",password="lenovog500s",database="python")
mycursor=mydb.cursor(buffered=True)
#qu="insert into fam values(%s,%s,%s,%s)"
#val=[(3,"Bhuvaneswari",50,94451),(4,"Nayana Sree",15,97898),(5,"Rathinaswamy",72,94441)]
#mycursor.execute("update fam set contact=97109 where id=1")
#a=mycursor.fetchone()
mycursor.execute("select * from fam limit 3")
ls=mycursor.fetchall()
print(mycursor.rowcount)
for i in ls:
    print(i)
mydb.commit()
