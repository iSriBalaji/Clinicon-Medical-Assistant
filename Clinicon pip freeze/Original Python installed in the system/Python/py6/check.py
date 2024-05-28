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
loc=ab.locations(query='T Nagar',coordinate=[13.0431714,80.2299073])
print(loc)
enty=loc['location_suggestions'][0]['entity_type']
enid=loc['location_suggestions'][0]['entity_id']
loc_det=ab.location_details(enid,enty)
res_ls=loc_det['nearby_res']
print(res_ls)
print(dir(ZomatoAPI))
