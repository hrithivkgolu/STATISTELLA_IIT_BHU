from dash import html, dcc, register_page
# import pandas as pd


# df = pd.read_csv("teams.csv")

register_page(__name__, path_template="/teams/<team_id>")

def layout(team_id=None):
    return html.Div(f"Welcome to the page for {team_id}")