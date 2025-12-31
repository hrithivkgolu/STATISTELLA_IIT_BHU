import pandas as pd

df1 = pd.read_csv("games_details.csv", low_memory=False)


print(df1.shape)

print(df1.shape[0]/df1.shape[0])
# print(df.nunique())
# team = df[df["TEAM_ABBREVIATION"] == "NOK"]
# print(team.head(5))