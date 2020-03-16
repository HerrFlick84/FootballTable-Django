from django.db import models
class Result(models.Model):
    GameID=              models.CharField(max_length=120)#1
    CompetitionID=   models.CharField(max_length=120)#2
    CompetitionName= models.CharField(max_length=120)#3
    Date=            models.CharField(max_length=120)#4
    HomeTeamID=      models.CharField(max_length=120)#5
    HomeTeamName=    models.CharField(max_length=120)#6
    HomeTeamScore=   models.IntegerField()#7
    HomeTeamScoreHT= models.IntegerField()#8
    AwayTeamID=      models.CharField(max_length=120)#9
    AwayTeamName=    models.CharField(max_length=120)#10
    AwayTeamScore=   models.IntegerField()#11
    AwayTeamScoreHT= models.IntegerField()#12

    #HomeTeamName = models.CharField(max_length=120)
    #HomeTeamScore=models.IntegerField( )