import pypyodbc 
import pandas as pd
import os
import requests
import json
import sqlalchemy as sa
import pyodbc
from datetime import datetime

server = 'BDN011\SQLEXPRESS'
database = 'FootballResults'


df=pd.DataFrame(columns=['ID','CompetitionID','CompetitionName','Date','HomeTeamID','HomeTeamName','HomeTeamScore','HomeTeamScoreHT','AwayTeamID','AwayTeamName','AwayTeamScore','AwayTeamScoreHT'])
engine = sa.create_engine('mssql+pyodbc://@' + server + '/' + database + '?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server')
#root_dir = 'C:\\Users\\TomaszHyla\\source\\repos\\Expenses report\\ExpensesReport\\dataresults'
headers = {
  'X-Auth-Token': 'adfc68b0479c470d94cb1c0ff2c0f9eb'
}
for file in [2002,2014,2021]:#Leagues ID
    #filename= os.path.join(directory, file)
    rqststr  = "https://api.football-data.org/v2/competitions/"+str(file)+"/matches"
    response = requests.request("GET", rqststr, headers=headers).content.decode('utf8')
    #resp = requests.get(rqststr,)
    #home = response.json()
    #home=open(filename,encoding="utf-8")
    home=json.loads(response)
    CompetitionID= home['competition']['id'] 
    CompetitionName= home['competition']['name']
    #read details and store in pandas dataframe
        
    for game in home["matches"]:
        Date=datetime.strptime(game['utcDate'],"%Y-%m-%dT%H:%M:%SZ")
        ID=game['id']
        HomeTeamID = game['homeTeam']['id']
        HomeTeamName = game['homeTeam']['name']
        AwayTeamID = game['awayTeam']['id']
        AwayTeamName = game['awayTeam']['name']
        HomeTeamScore= game['score']['fullTime']['homeTeam']
        AwayTeamScore= game['score']['fullTime']['awayTeam']
        HomeTeamScoreHT= game['score']['halfTime']['homeTeam']
        AwayTeamScoreHT= game['score']['halfTime']['awayTeam']
        df = df.append({'ID': ID,'CompetitionID':CompetitionID,'CompetitionName':CompetitionName,'Date':Date,'HomeTeamID':HomeTeamID,'HomeTeamName':HomeTeamName,'HomeTeamScore':HomeTeamScore,'HomeTeamScoreHT':HomeTeamScoreHT,'AwayTeamID':AwayTeamID,'AwayTeamName':AwayTeamName,'AwayTeamScore':AwayTeamScore,'AwayTeamScoreHT':AwayTeamScoreHT}, ignore_index=True)
#Bulk load datafram to table
df.to_sql('Results',engine,if_exists="replace",index=False)

