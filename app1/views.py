from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpRequest
from . import APIcalsinglel as APIcall
from .models import Result
import os, requests
import sqlalchemy as sa
import json,pandas as pd
from django.db import connection
from datetime import datetime
standings=[]




#from static import start
# Create your views here.
def startpage(request):
    standings=[]
    class country:
        def __init__(self,name,data):
            self.name=name
            self.data=data
    #standings =[ Student( score, gender ) for score, gender in <some-data-source> ]
    root_dir = 'C:\\Users\\TomaszHyla\\source\\repos\\Expenses report\\ExpensesReport\\data'

    for directory, subdirectories, files in os.walk(root_dir):
        for file in files:
            filename= os.path.join(directory, file)
            home=open(filename,encoding="utf-8")
            home=json.load(home)
            home=home["standings"][0]['table']

            standings.append(country(file,home))
             #print(home.read())
    #home = APIcall.getresponse("https://api.football-data.org/v2/competitions")
    #https://api.football-data.org/v2/competitions/2014/standings Spain
    #2021 EPL
    #2002 Bundesliga
    #2014 La liga
    #home=home.read()
    #home=json.load(home)
    #home=home.json()
        
    #home=home['competitions']
    #home= dict(home)
    #home=home['competitions']
    #home = request.get("https://api.football-data.org/v2/competitions")
    #return HttpResponse("z wnetrznosci appki")
    #print(standings)
    for cntr in standings:
        print(cntr.name)
    return render(request,'start.html',{'standings':standings})


def UpdateResults(request):
    # database_name = settings.DATABASES['default']['NAME']
    # database_url = 'sqlite:///{}'.format(database_name)
    # engine = sa.create_engine(database_url, echo=False)
    list=[]
    headers = {
      'X-Auth-Token': 'adfc68b0479c470d94cb1c0ff2c0f9eb'
    }

    for file in [2002,2014,2021]:
        rqststr  = "https://api.football-data.org/v2/competitions/"+str(file)+"/matches"
        response = requests.request("GET", rqststr, headers=headers).content.decode('utf8')

        home=json.loads(response)
        CompetitionID= home['competition']['id'] 
        CompetitionName= home['competition']['name']

        
        for game in home["matches"]:
            
            Date=datetime.strptime(game['utcDate'],"%Y-%m-%dT%H:%M:%SZ")
            Date  = str(Date)[:10].replace('-','')
            GameID=game['id']
            HomeTeamID = game['homeTeam']['id']
            HomeTeamName = game['homeTeam']['name']
            AwayTeamID = game['awayTeam']['id']
            AwayTeamName = game['awayTeam']['name']
            HomeTeamScore= game['score']['fullTime']['homeTeam']
            AwayTeamScore= game['score']['fullTime']['awayTeam']
            HomeTeamScoreHT= game['score']['halfTime']['homeTeam']
            AwayTeamScoreHT= game['score']['halfTime']['awayTeam']

            list.append(Result(GameID= GameID,CompetitionID=CompetitionID,CompetitionName=CompetitionName,Date=Date,HomeTeamID=HomeTeamID,HomeTeamName=HomeTeamName,HomeTeamScore=HomeTeamScore,HomeTeamScoreHT=HomeTeamScoreHT,AwayTeamID=AwayTeamID,AwayTeamName=AwayTeamName,AwayTeamScore=AwayTeamScore,AwayTeamScoreHT=AwayTeamScoreHT))

    Result.objects.bulk_create(list, batch_size=None, ignore_conflicts=True)
    return HttpResponse('Inserted '+str(len(list))+' lines')
    #R.save(True)
    #return HttpResponse(data["HomeTeamName"])
def TeamGames(request):
    #GET data from DB
    TeamID='5'
    games={}
    cursor  = connection.cursor()
    #query = ''' SELECT name FROM sqlite_master WHERE type='table' ORDER BY name ''';
    query = ''' SELECT * FROM app1_result Result where HomeTeamID='''+TeamID + ''' OR AwayTeamID='''+TeamID + ''' ORDER by date desc'''
#    query='''select 
#    Team, 
#    count(*) GamesPlayed, 
#    count(case when HomeTeamScore > AwayTeamScore then 1 end) wins, 
#    count(case when AwayTeamScore > HomeTeamScore then 1 end) lost, 
#    count(case when HomeTeamScore = AwayTeamScore then 1 end) draws, 
#    sum(HomeTeamScore) goalsfor, 
#    sum(AwayTeamScore) goalsagainst, 
#    --sum(goalsfor) - sum(goalsagainst) goal_diff,
#    sum(
#          case when HomeTeamScore > AwayTeamScore then 3 else 0 end 
#        + case when HomeTeamScore = AwayTeamScore then 1 else 0 end
#    ) score 
#from (
#    select HomeTeamName team, HomeTeamScore, AwayTeamScore, CompetitionID from app1_result 
#  union all
#    select AwayTeamName, AwayTeamScore, HomeTeamScore, CompetitionID from app1_result
#) a 
#where competitionID =2014
#group by team
#order by score desc;--, goal_diff desc;'''
    cursor.execute(query)

    resp = cursor.fetchall()
    #prepare data for template
    #columns = [col[0] for col in cursor.description]
    
    for row in resp:
        listed = list(row)
        
        
        if listed[5] == TeamID:
            oponent=listed[10] 
            Score= listed[7]
            oponentScore=listed[11]
            HA= 'H'
        elif listed[9]==TeamID:
            oponent = listed[6]
            Score= listed[11]
            oponentScore=listed[7]
            HA='A'
        games[listed[0]]={
            'oponent':oponent,
            'Score':Score,
            'oponentScore':oponentScore,
            'HA':HA
            }
    return render(request,'TeamResults.html',{'games':games})
def delall(request):
    Result.objects.all().delete()
    return HttpResponse('done')
def Standings(request):
    #GET data from DB
    CompetitionID='2014'
    teams={}
    cursor  = connection.cursor()
    query='''select 
    Team, 
    count(*) GamesPlayed, 
    count(case when HomeTeamScore > AwayTeamScore then 1 end) wins, 
    count(case when AwayTeamScore > HomeTeamScore then 1 end) lost, 
    count(case when HomeTeamScore = AwayTeamScore then 1 end) draws, 
    sum(HomeTeamScore) goalsfor, 
    sum(AwayTeamScore) goalsagainst, 
    --sum(goalsfor) - sum(goalsagainst) goal_diff,
    sum(
          case when HomeTeamScore > AwayTeamScore then 3 else 0 end 
        + case when HomeTeamScore = AwayTeamScore then 1 else 0 end
    ) score 
from (
    select HomeTeamName team, HomeTeamScore, AwayTeamScore, CompetitionID from app1_result 
  union all
    select AwayTeamName, AwayTeamScore, HomeTeamScore, CompetitionID from app1_result
) a 
where competitionID ='''+CompetitionID+''' 
group by team
order by score desc;--, goal_diff desc;'''
    print(query)
    cursor.execute(query)

    resp = cursor.fetchall()
    
    #prepare data for template
    #columns = [col[0] for col in cursor.description]
    i=1
    for row in resp:
        Listed = list(row)
        teams[i]={
            'team':Listed[0],
            'GamesPlayed':Listed[1],
            'wins':Listed[2],
            'lost':Listed[3],
            'draws':Listed[4],
            'goalsfor':Listed[5],
            'goalsagainst':Listed[6],
            'score':Listed[7]
            }
        i+=1
    #return HttpResponse(teams[2])
    return render(request,'TabbedStandings.html',{'teams':teams})
def Boot(request):
    return render(request,'Boot.html')
def Standingssingle(request):
    from .utils import query
    #GET data from DB
    CompetitionID='2014'
    Context = []
    cursor  = connection.cursor()
    query =query.MSSQL()
    j=0
    while j<3:
        #Home Away Total condition

        query.defineparams(False,j,datetime.today(),CompetitionID)
        print(query.string)
        
        cursor.execute(query.string)

        resp = cursor.fetchall()
        #prepare data for template
        #return HttpResponse(query.string)
        i=1
        teams={}
        for row in resp:
            Listed = list(row)
            teams[i]={
                'team':Listed[0],
                'GamesPlayed':Listed[1],
                'wins':Listed[2],
                'lost':Listed[3],
                'draws':Listed[4],
                'goalsfor':Listed[5],
                'goalsagainst':Listed[6],
                'score':Listed[7]
                }
            i+=1
        #print(teams[1]['team']+" " +str(teams[1]['score']))
        Context.append(teams)
        j=j+1
        
    #for key in Context:

        #print(key[1]['score'])
    return render(request,'TabbedStandings.html',{'Context':Context})