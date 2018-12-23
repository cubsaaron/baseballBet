-- Create a view that will make add columns of the winner/loser of the game
DROP VIEW games_winner;

CREATE VIEW games_winner as
select *,
case
  when home_team_runs > away_team_runs
    then home_name_abbrev
  else away_name_abbrev
end winner_abbrev,
case
  when home_team_runs < away_team_runs
    then home_name_abbrev
  else away_name_abbrev
end loser_abbrev
from games;

COMMIT;