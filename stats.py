import pandas as pd
import numpy as np
import sqlite3
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, OpenURL, TapTool

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
smTeam = ["MIL"]
allTeams = awTeam + adTeam + mhTeam + tmTeam + smTeam

# Get all games in the dataframe - actuall a view with winner and loser already computed
conn = sqlite3.connect("gameday.db")
df = pd.read_sql_query("select datetime(start_time, 'start of day') as gamedate, home_name_abbrev, home_team_name, home_team_runs, away_name_abbrev, away_team_name, away_team_runs, winner_abbrev, loser_abbrev, game_data_directory from games_winner", conn, parse_dates=['gamedate'])

# Limit the data frame to just teams we are interested in. Could be done in SQL for better performance,
# but doing it in Python in case we want to look at all data later.
df = df.loc[((df['home_name_abbrev'].isin(allTeams)) & ((df['away_name_abbrev'].isin(allTeams)))), ['gamedate', 'home_name_abbrev', 'away_name_abbrev', 'home_team_runs', 'away_team_runs', 'winner_abbrev', 'loser_abbrev', 'game_data_directory']]
# Create a column using just the info we need from the 'game_data_directory' column to make a URl to mlb.com
df['gameURL'] = df['game_data_directory'].str.split("/").str[7]

# More effecient to look through these once, but since there is a limited number of teams
# the dataframe size is small, and this is likely run once a day, we'll call it this way.
# Hopefully improves code readability too.
df[['awWins', 'awTotal']] = df.apply(computeGame, teamList=awTeam, allTeams=allTeams, axis=1)
df[['adWins', 'adTotal']] = df.apply(computeGame, teamList=adTeam, allTeams=allTeams, axis=1)
df[['mhWins', 'mhTotal']] = df.apply(computeGame, teamList=mhTeam, allTeams=allTeams, axis=1)
df[['tmWins', 'tmTotal']] = df.apply(computeGame, teamList=tmTeam, allTeams=allTeams, axis=1)
df[['smWins', 'smTotal']] = df.apply(computeGame, teamList=smTeam, allTeams=allTeams, axis=1)
df['awWinPct'] = df['awWins'].cumsum() / df['awTotal'].cumsum()
df['adWinPct'] = df['adWins'].cumsum() / df['adTotal'].cumsum()
df['mhWinPct'] = df['mhWins'].cumsum() / df['mhTotal'].cumsum()
df['tmWinPct'] = df['tmWins'].cumsum() / df['tmTotal'].cumsum()
df['smWinPct'] = df['smWins'].cumsum() / df['smTotal'].cumsum()

# Print statement for testing - gets DF when two teams play each other
#print(df)
#print(df.loc[((df['home_name_abbrev'].isin(allTeams)) & ((df['away_name_abbrev'].isin(allTeams)))), ['gamedate', 'home_name_abbrev', 'away_name_abbrev', 'home_team_runs', 'away_team_runs', 'awWins', 'awWinPct', 'adWins', 'adWinPct', 'mhWins', 'mhWinPct', 'tmWins', 'tmWinPct']])

# Start the graph
output_file("bet.html")
source=ColumnDataSource(data=df)
hover = HoverTool(
    tooltips = [
        ('Date', '@gamedate{%F}'),
        ('Result', '@home_name_abbrev(@home_team_runs) - @away_name_abbrev(@away_team_runs)'),
        ('Win %', '$y')
    ],
    formatters = {
        'gamedate': 'datetime'
    }
)

p = figure(title="Baseball Bet", x_axis_label='Game Date', x_axis_type='datetime', y_axis_label='Win %', tools=[hover, "tap"])
p.line(x='gamedate', y='awWinPct', legend="A. Williams (" + '' .join(awTeam) + ')', line_width=2, source=source, color='Green')
p.circle(x='gamedate', y='awWinPct', size=4, source=source, color='Green')
p.line(x='gamedate', y='adWinPct', legend="A. Dumat (" + '' .join(adTeam) + ')', line_width=2, source=source, color='Red')
p.circle(x='gamedate', y='adWinPct', size=4, source=source, color='Red')
p.line(x='gamedate', y='mhWinPct', legend="M. Harris (" + '' .join(mhTeam) + ')', line_width=2, source=source, color='Black')
p.circle(x='gamedate', y='mhWinPct', size=4, source=source, color='Black')
p.line(x='gamedate', y='tmWinPct', legend="T. Milsaps (" + '' .join(tmTeam) + ')', line_width=2, source=source, color='Orange')
p.circle(x='gamedate', y='tmWinPct', size=4, source=source, color='Orange')
p.line(x='gamedate', y='smWinPct', legend="S. Milsaps (" + '' .join(smTeam) + ')', line_width=2, source=source, color='Blue')
p.circle(x='gamedate', y='smWinPct', size=4, source=source, color='Blue')
url="https://www.mlb.com/gameday/@gameURL"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)
# Create the graph
show(p)
