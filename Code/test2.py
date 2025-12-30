import csv

with open("games_details.csv","r") as f:
	cur = csv.reader(f)
	for i in cur:
		print(i)