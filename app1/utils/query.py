class MSSQL:
    def __init__(self):
        
        self.string="""
select
    Team, 
    count(*) GamesPlayed, 
    count(case when HomeTeamScore > AwayTeamScore then 1 end) wins, 
    count(case when AwayTeamScore > HomeTeamScore then 1 end) lost, 
    count(case when HomeTeamScore = AwayTeamScore then 1 end) draws,
    sum(HomeTeamScore) goalsfor, 
    sum(AwayTeamScore) goalsagainst, 
   
    sum(
          case when HomeTeamScore > AwayTeamScore then 3 else 0 end 
        + case when HomeTeamScore = AwayTeamScore then 1 else 0 end
    ) score 
from (
    select HomeTeamName team, HomeTeamScore, AwayTeamScore, CompetitionID,Date,HomeTeamName,AwayTeamName from app1_result 
  union all
    select AwayTeamName, AwayTeamScore, HomeTeamScore, CompetitionID,Date,HomeTeamName,AwayTeamName from app1_result
) a 
where competitionID = CompetitionIDGoesHere and Date < DateGoesHere 
group by team
order by score desc;"""
        #self.defineparams(self,HT,Home,tabledate,competionID)
    def defineparams(self,HT,Home,tabledate,competionID):
        if HT:
            self.string=self.string.replace("HomeTeamScore","HomeTeamScoreHT")
            self.string=self.string.replace("AwayTeamScore","AwayTeamScoreHT")
        if Home !=0:
            if Home == 1:
               self.string=self.string.replace("where","where HomeTeamName=team and ") 
            else:
               self.string=self.string.replace("where HomeTeamName=team and ","where AwayTeamName=team and ") 
        self.string=self.string.replace('DateGoesHere',str(tabledate)[:10].replace('-',''))
        self.string=self.string.replace('CompetitionIDGoesHere',str(competionID)) 
            