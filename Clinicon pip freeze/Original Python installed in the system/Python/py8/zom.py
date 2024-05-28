import os
import sys
import json
# API KEY: c8b450d4a3bd8a5941778e61c94d8f81
from zomathon import ZomatoAPI

API_KEY = os.environ.get('c8b450d4a3bd8a5941778e61c94d8f81')
#print(type(API_KEY))
print("------------------")
zom = ZomatoAPI(API_KEY)
#print(zom)
print()
ab=ZomatoAPI('c8b450d4a3bd8a5941778e61c94d8f81')
loc=ab.locations(count=4,query='T Nagar',coordinate=[13.0431714,80.2299073])
print(loc)
enty=loc['location_suggestions'][0]['entity_type']
enid=loc['location_suggestions'][0]['entity_id']
loc_det=ab.location_details(enid,enty)
res_ls=loc_det['nearby_res']
print(res_ls)
for i in res_ls:
    res_det=ab.restaurant(i)
    print("Name: %s"%(res_det['name']))
    print("Address: %s"%(res_det['location']['address']))
    print("Rating: %s"%(res_det['user_rating']['aggregate_rating']))
    print("Votes: %s"%(res_det['user_rating']['votes']))
    print("Area: %s"%(res_det['location']['locality_verbose']))
    print("Type of Restaurant: %s"%(res_det['establishment'][0]))
    print("PhoneNo: %s"%(res_det['phone_numbers']))
    print("Cuisines: %s"%(res_det['cuisines']))
    print("------------------------------------------------")
print()
#print(ab.geocode([13.0431714,80.2299073]))
print()
#print(ab.restaurant(18887017))
print()
# For complete help on the module
#help(zom)
