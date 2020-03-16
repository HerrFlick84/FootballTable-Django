import requests
def getresponse(reqpath):
    resp = requests.get(reqpath)
    return resp 
toobtain=getresponse('https://api.football-data.org/v2/competitions')
dictionarry =toobtain.json()
print(toobtain)