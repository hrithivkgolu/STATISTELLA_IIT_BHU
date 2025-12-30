import pandas as pd


df = pd.read_csv("games_details.csv", low_memory=False)

print(df.nunique())
team = df[df["TEAM_ABBREVIATION"] == "NOK"]
print(team.head(5))