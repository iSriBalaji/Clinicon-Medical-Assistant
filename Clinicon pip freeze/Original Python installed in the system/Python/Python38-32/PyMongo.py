import pymongo
from pymongo import MongoClient
#Accessing the Cluster through link
cluster=MongoClient("mongodb+srv://iSriBalaji:lenovog500s@cluster0-nlgba.mongodb.net/test?retryWrites=true&w=majority")
#Accessing the Database
db=cluster["Mypython"]
#Accessing the Particular Database
col=db["Fam"]

#You can see that everything was like JSON   ex: like db[key]


#inserting single value into collections
# val=dict(_id=1,Name="Sri Balaji",Age=20,Contact=9789968131)
# col.insert_one(val)

#inserting multiple values to collections at a time
# val1=dict(_id=2,Name="Muruganandam",Age=54,Contact=9444278976)
# val2=dict(_id=3,Name="Nayana Sree",Age=15,Contact=9789856712)
# val3=dict(_id=4,Name="Bhuvaneswari",Age=48,Contact=9445175326)
# val4=dict(_id=5,Name="Rathinaswamy",Age=72,Contact=9444101850)
# col.insert_many([val1,val2,val3,val4])


#Finding a value in collections
# fi=col.find({"Name":"Sri Balaji"})
# for i in fi:          #f1 is iterable
#     print(i["Contact"])

#To find one value use col.find_one({"_id"=1})


# To select every value from the collection
fi=col.find({})
for i in fi:
    print(i)


# # To delete a single value
# col.delete_one({"_id":5})

# To delete many values
# col.delete_many({"_id":2},{"_id":4})   #doubt

#To update a value
col.update_one({"_id":1},{"$set":{"Name":"Baju"}})
# To set new value same
col.update_one({"_id":1},{"$set":{"Fav":"Data Science"}})

#To update many:
# use update_many()


count=col.count_documents({})
print(count)