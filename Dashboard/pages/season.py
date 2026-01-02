from dash import html, dcc, register_page, callback, Output, Input, State
import pandas as pd

teams_df = pd.read_csv("data/team.csv")
team_lookup = dict(zip(teams_df['TEAM_ID'], teams_df['ABBREVIATION']))

register_page(__name__, path_template="/seasons/<season_id>")


def create_game_box(row):
        home_abbr = team_lookup.get(row['HOME_TEAM_ID'], "N/A")
        away_abbr = team_lookup.get(row['VISITOR_TEAM_ID'], "N/A")
        pts_h = row['PTS_home']
        pts_a = row['PTS_away']
        gameid = str(row['GAME_ID'])[3:]
        
        if pts_h > pts_a:
            winner = home_abbr
            score_text = f"{int(pts_h)} - {int(pts_a)}"
        else:
            winner = away_abbr
            score_text = f"{int(pts_a)} - {int(pts_h)}"

        return dcc.Link(
            href=f"/game/{row['GAME_ID']}",
            className="game-card-link",
            children=[
                html.Div(className="game-box", children=[
                    html.Div(gameid, className="vertical-id"),
                    html.Div(className="game-matchup-container", children=[

                        html.Img(src=f"/assets/{home_abbr}.png", className="team-icon-small"),
                        html.Span(f"{home_abbr}", className="team-name"),
                        html.Span(" VS ", className="vs-text"),
                        html.Span(f"{away_abbr}", className="team-name"),
                        html.Img(src=f"/assets/{away_abbr}.png", className="team-icon-small"),
                    ]),
                    html.Div([
                        html.Span("WON: ", className="label"),
                        html.Span(winner, className="winner-name")
                    ], className="game-winner"),
                    html.P(row['GAME_DATE_EST']),
                    html.Div(score_text, className="game-score")
                ])
            ]
        )


def layout(season_id=None):
    if not season_id:
        return html.Div("No season selected.", style={'color': 'white'})

    try:
        all_years = list(range(2003, 2022)) 
        other_seasons = [s for s in all_years if str(s) != str(season_id)]
        mai_df = pd.read_csv(f"data/game2/g{season_id}.csv")
        mai_df = mai_df.sort_values(by='GAME_ID', ascending=False)
        total_games = len(mai_df)
    except Exception as e:
        return html.Div(f"Error loading data for season {season_id}: {e}", style={'color': 'red'})

    return html.Div(className="season-page", children=[
        # --- THE MISSING REDIRECT COMPONENT ---
        dcc.Location(id='season-url-redirect', refresh=True),
        dcc.Store(id='current-season-id', data=season_id),
        html.Div(className="nav-header", children=[
            dcc.Link("← BACK TO SEASONS", href="/seasons", className="back-button"),
            html.Span(f"NBA / SEASON / {season_id}-{int(season_id)+1}", className="breadcrumb")
        ]),

        html.H1(f"MAIN SEASON {season_id}-{str(int(season_id)+1)[2:]} DATA", className="season-title"),
        html.Hr(className="premium-divider"),

        html.Div(className="season-content-wrapper", children=[
            # SIDEBAR
            html.Div(className="season-sidebar", children=[
                html.H3("SELECT SEASON"),
                dcc.Dropdown(
                    id='season-selector',
                    options=[{'label': f"Season {s}-{s+1}", 'value': str(s)} for s in other_seasons],
                    # Change value to None or a placeholder to force a change
                    placeholder="Switch Year...",
                    clearable=False,
                    className="custom-dropdown"
                ),
                html.Hr(style={'margin': '20px 0', 'opacity': '0.1'}),
                html.H3("OVERVIEW"),
                html.Div(className="stat-box", children=[
                    html.Label("TOTAL MAIN SEASON GAMES"),
                    html.P(str(total_games)) 
                ])
            ]),

            # GRID
            html.Div(className="game-display-area", children=[
                html.Div(className="search-container", children=[
                    html.H3("GAME LIST", style={'margin': '0'}),
                    dcc.Input(
                        id="game-search-input",
                        type="text",
                        placeholder="Search Team (e.g. PHI) or Game ID...",
                        className="game-search-bar",
                        debounce=False # This makes it filter as you type
                    ),
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '20px'}),
                html.Div(id="games-grid-container",className="games-grid", children=[
                    create_game_box(row) for _, row in mai_df.iterrows()
                ]),
            ])
        ])
    ])


@callback(
    Output('season-url-redirect', 'pathname'),
    Input('season-selector', 'value'),
    prevent_initial_call=True
)
def update_season_url(selected_year):
    return f"/seasons/{selected_year}" if selected_year else dash.no_update

# CALLBACK 2: Search (Fixed Inputs)
@callback(
    Output("games-grid-container", "children"),
    Input("game-search-input", "value"),
    State("current-season-id", "data") # Use State so typing doesn't trigger unless input changes
)
def filter_games(search_value, current_season):
    df = pd.read_csv(f"data/game2/g{current_season}.csv")
    
    # Sort the data immediately after loading
    df = df.sort_values(by='GAME_ID', ascending=False)
    
    if not search_value:
        return [create_game_box(row) for _, row in df.iterrows()]
    
    search_value = search_value.upper()
    df['h_abbr'] = df['HOME_TEAM_ID'].map(team_lookup)
    df['a_abbr'] = df['VISITOR_TEAM_ID'].map(team_lookup)
    
    filtered_df = df[
        df['h_abbr'].str.contains(search_value, na=False) |
        df['a_abbr'].str.contains(search_value, na=False) |
        df['GAME_ID'].astype(str).str.contains(search_value, na=False)
    ]

    if filtered_df.empty:
        return html.Div("No matches found.", style={'color': 'gray', 'padding': '20px'})

    return [create_game_box(row) for _, row in filtered_df.iterrows()]