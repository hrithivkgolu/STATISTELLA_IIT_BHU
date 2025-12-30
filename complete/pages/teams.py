from dash import html, register_page

register_page(__name__, path="/teams")

# 30 NBA team abbreviations (example set – adjust if needed)
team_codes = [
    "ATL", "BOS", "BKN", "CHA", "CHI", "CLE",
    "DAL", "DEN", "DET", "GSW", "HOU", "IND",
    "LAC", "LAL", "MEM", "MIA", "MIL", "MIN",
    "NOP", "NYK", "OKC", "ORL", "PHI", "PHX",
    "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
]

layout = html.Div(
    className="teams-page",
    children=[

        # Page title
        html.H1("NBA TEAMS", className="teams-title"),

        # Teams grid
        html.Div(
            className="teams-grid",
            children=[
                html.Div(
                    className="team-card",
                    children=[
                        html.Img(
                            src=f"/assets/{code}.png",
                            alt=code
                        ),
                        html.Span(code)
                    ]
                )
                for code in team_codes
            ]
        )
    ]
)
