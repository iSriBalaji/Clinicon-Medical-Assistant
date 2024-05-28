import requests
def getInternetStatus():
    try:
        r = requests.get("https://www.google.com/",timeout=3)
        return("Connected")
    except e:
        return(e)


a = getInternetStatus()
print(a)
