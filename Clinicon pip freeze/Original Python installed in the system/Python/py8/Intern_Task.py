import os
import sys
import json
#Generated API KEY: c8b450d4a3bd8a5941778e61c94d8f81
from zomathon import ZomatoAPI
import mysql.connector
mydb=mysql.connector.connect(host="localhost", user="root", passwd="lenovog500s",database="datab")  #Connecting to already created database
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE datab")
mycursor.execute("CREATE TABLE restaurant(id INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(255), Address VARCHAR(255), Rating FLOAT(2), Vote INT(255), Area VARCHAR(255), TypeOfRestaurant VARCHAR(255), Contact VARCHAR(255),Cuisines VARCHAR(255))")
sql = "INSERT INTO restaurant(Name,Address,Rating,Vote,Area,TypeOfRestaurant,Contact,Cuisines) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
API_KEY = os.environ.get('c8b450d4a3bd8a5941778e61c94d8f81')
print("----------------------------------------------------------------------")
zom = ZomatoAPI(API_KEY)
print()
ab=ZomatoAPI('c8b450d4a3bd8a5941778e61c94d8f81')
loc=ab.locations(query='T Nagar',coordinate=[13.0431714,80.2299073]) #extracting location id and type
enty=loc['location_suggestions'][0]['entity_type']
enid=loc['location_suggestions'][0]['entity_id']
loc_det=ab.location_details(enid,enty)                              #extracting location details
res_ls=loc_det['nearby_res']                                        #extracting restaurant's ID from the corresponding location
for i in res_ls:                                                    
    ls=[]
    res_det=ab.restaurant(i)                                        #extracting restaurant details using their ID
    name=res_det['name']
    ls.append(name)
    address=res_det['location']['address']
    ls.append(address)
    rating=res_det['user_rating']['aggregate_rating']
    ls.append(rating)
    votes=res_det['user_rating']['votes']
    ls.append(votes)
    area=res_det['location']['locality_verbose']
    ls.append(area)
    type_of_res=res_det['establishment'][0]
    ls.append(type_of_res)
    phoneno=res_det['phone_numbers']
    ls.append(phoneno)
    cuisines=res_det['cuisines']
    ls.append(cuisines)
    print("Name: %s"%(name))
    print("Address: %s"%(address))
    print("Rating: %s"%(rating))
    print("Votes: %s"%(votes))
    print("Area: %s"%(area))
    print("Type of Restaurant: %s"%(type_of_res))
    print("PhoneNo: %s"%(phoneno))
    print("Cuisines: %s"%(cuisines))
    print("-------------------------------------------------------------------")
    mycursor.execute(sql,tuple(ls))                                     #inserting data into table
    mydb.commit()
    print("-------------------------------------------------------------------")

