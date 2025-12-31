from dash import html, dcc, register_page

register_page(__name__, path="/teams")

nba_teams = {
    "Eastern Conference": [
        "ATL E (Atlanta Hawks)","BOS E (Boston Celtics)","BKN E (Brooklyn Nets)","CHA E (Charlotte Hornets)","CHI E (Chicago Bulls)","CLE E (Cleveland Cavaliers)","DET E (Detroit Pistons)","IND E (Indiana Pacers)","MIA E (Miami Heat)","MIL E (Milwaukee Bucks)","NYK E (New York Knicks)","ORL E (Orlando Magic)","PHI E (Philadelphia 76ers)","TOR E (Toronto Raptors)","WAS E (Washington Wizards)"
    ],
    "Western Conference": [
        "DAL W (Dallas Mavericks)","DEN W (Denver Nuggets)","GSW W (Golden State Warriors)","HOU W (Houston Rockets)","LAC W (LA Clippers)","LAL W (Los Angeles Lakers)","MEM W (Memphis Grizzlies)","MIN W (Minnesota Timberwolves)","NOP W (New Orleans Pelicans)","OKC W (Oklahoma City Thunder)","PHX W (Phoenix Suns)","POR W (Portland Trail Blazers)","SAC W (Sacramento Kings)","SAS W (San Antonio Spurs)","UTA W (Utah Jazz)"
    ]
}

layout = html.Div(
    className="teams-page",
    children=[
        html.H1("NBA TEAMS", className="teams-title", style={'textAlign': 'center'}),
        
        # Main container to hold both columns
        html.Div(
            className="conference-container",
            children=[
                # Loop through the dictionary to create two columns
                html.Div(
                    className=f"conference-column {'east-side' if conf == 'Eastern Conference' else 'west-side'}",
                    children=[
                        html.H2(f"{conf}", className="conference-header"),
                        html.Div(
                            className="teams-grid",
                            children=[
                                # WRAP THE CARD IN A LINK
                                dcc.Link(
                                    href=f"/teams/{code.split(' ')[0]}",
                                    style={'textDecoration': 'none'},
                                    children=[
                                        html.Div(
                                            className="team-card",
                                            **{"data-hover": code.split('(')[-1].strip(')')},
                                            children=[
                                                html.Img(
                                                    src=f"/assets/{code.split(' ')[0]}.png",
                                                    alt=code.split(' ')[0],
                                                    className="team-logo"
                                                ),
                                                html.Span(code.split(' ')[0], className="team-label")
                                            ]
                                        )
                                    ]
                                ) for code in teams
                            ]
                        )
                    ]
                ) for conf, teams in nba_teams.items()
            ]
        )
    ]
)