import pandas as pd
import numpy as np
import sqlite3

# Compute each participants win total for the game based on their MLB team   
def computeGame(game, teamList, allTeams):
    wins = 0            # total wins for teamList
    gamesPlayed = 0     # total games for teamList
    if game['winner_abbrev'] in teamList and game['loser_abbrev'] in allTeams:
        wins = 1
        gamesPlayed = 1
    if game['loser_abbrev'] in teamList and game['winner_abbrev'] in allTeams:
    # Add to total games
        gamesPlayed += 1
    return pd.Series([wins, gamesPlayed])
            
# Define MLB teams for each participant    
#awTeam = ["CHC", "ATL"]
#adTeam = ["CIN", "FLA"]
#mhTeam = ["STL", "NYM"]
#tmTeam = ["PIT", "PHI"]
awTeam = ["CHC"]
adTeam = ["CIN"]
mhTeam = ["STL"]
tmTeam = ["PIT"]
allTeams = awTeam + adTeam + mhTeam + tmTeam

# Get all games in the dataframe - actuall a view with winner and loser already computed
conn = sqlite3.connect("gameday.db")
df = pd.read_sql_query("select datetime(start_time, 'start of day') as gamedate, home_name_abbrev, home_team_name, home_team_runs, away_name_abbrev, away_team_name, away_team_runs, winner_abbrev, loser_abbrev from games_winner", conn)

# More effecient to look through these once, but since there is a limited number of teams
# the dataframe size is small, and this is likely run once a day, we'll call it this way.
# Probably improves code readability also.
df[['awWins', 'awTotal']] = df.apply(computeGame, teamList=awTeam, allTeams=allTeams, axis=1)
df[['adWins', 'adTotal']] = df.apply(computeGame, teamList=adTeam, allTeams=allTeams, axis=1)
df[['mhWins', 'mhTotal']] = df.apply(computeGame, teamList=mhTeam, allTeams=allTeams, axis=1)
df[['tmWins', 'tmTotal']] = df.apply(computeGame, teamList=tmTeam, allTeams=allTeams, axis=1)
df['awWinPct'] = df['awWins'].cumsum() / df['awTotal'].cumsum()
df['adWinPct'] = df['adWins'].cumsum() / df['adTotal'].cumsum()
df['mhWinPct'] = df['mhWins'].cumsum() / df['tmTotal'].cumsum()
df['tmWinPct'] = df['tmWins'].cumsum() / df['mhTotal'].cumsum()



# Testing print statement - gets DF when two opponents play each other
#print(df.loc[((df['home_name_abbrev'].isin(allTeams)) & ((df['away_name_abbrev'].isin(allTeams)))), ['gamedate', 'home_name_abbrev', 'away_name_abbrev', 'home_team_runs', 'away_team_runs', 'awResult', 'adResult', 'mhResult', 'tmResult', 'awSum']])
print(df.loc[((df['home_name_abbrev'].isin(allTeams)) & ((df['away_name_abbrev'].isin(allTeams)))), ['gamedate', 'home_name_abbrev', 'away_name_abbrev', 'home_team_runs', 'away_team_runs', 'awWins', 'awWinPct', 'adWins', 'adWinPct', 'mhWins', 'mhWinPct', 'tmWins', 'tmWinPct']])

#print(list(df))
# Make DF for each participant. We'll compute each seperately
#aaronDF = df.loc[((df['home_name_abbrev'].isin(aaronTeam)) | ((df['away_name_abbrev'].isin(aaronTeam))))]
#deweyDF = df.loc[((df['home_name_abbrev'].isin(deweyTeam)) | ((df['away_name_abbrev'].isin(deweyTeam))))]
#mattDF = df.loc[((df['home_name_abbrev'].isin(mattTeam)) | ((df['away_name_abbrev'].isin(mattTeam))))]
#aaronDF = computeWinner(aaronDF, aaronTeam, 'aaronResult')
#aaronDF['aaronPct'] = aaronDF['aaronResult'].rolling(1000).mean()
#print(aaronDF)
#computeWinner(deweyDF, deweyTeam, 'deweyResult')
#computeWinner(mattDF, mattTeam, 'mattResult')
#mergeDF = aaronDF.append([deweyDF, mattDF])
#print(mergeDF)

# Find Cubs wins
#cubWin = df.loc[((df['home_name_abbrev']=='CHC') & (df['home_team_runs'].gt(df['away_team_runs']))) | ((df['away_name_abbrev']=='CHC') & (df['away_team_runs'].gt(df['home_team_runs'])))]
#aaronWin = df.loc[((df['home_name_abbrev'].isin(aaronTeam)) & (df['home_team_runs'].gt(df['away_team_runs']))) | ((df['away_name_abbrev'].isin(aaronTeam)) & (df['away_team_runs'].gt(df['home_team_runs'])))]
#print (aaronWin.to_string())

#df['aaronPct'] = df['aaronResult'].rolling(1000).mean()

#aaronGame = df.loc[(df['home_name_abbrev'].isin(aaronTeam)) | (df['away_name_abbrev'].isin(aaronTeam))]
#print(aaronGame)
#print(df)