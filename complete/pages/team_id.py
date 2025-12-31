from dash import html, dcc, register_page, callback, Output, Input
import pandas as pd


df = pd.read_csv("data/team.csv")
df['FULL_NAME'] = df['CITY'] + " " + df['NICKNAME']
team_details = df.set_index('ABBREVIATION').to_dict('index')


register_page(__name__, path_template="/teams/<team_id>")


def layout(team_id=None):
    if team_id not in team_details:
        return html.H1("Team Not Found")
    
    team = team_details[team_id]
    

    return html.Div(className="team-detail-page", children=[
        dcc.Location(id='url-redirect', refresh=True),
        html.Div(className="nav-header", children=[
            dcc.Link("← BACK TO TEAMS", href="/teams", className="back-button"),
            html.Span("NBA / TEAMS / " + team_id, className="breadcrumb")
        ]),
        # --- TOP HEADER SECTION ---
        html.Div(className="detail-header", children=[
            html.Img(src=f"/assets/{team_id}.png", className="big-team-logo"),
            html.Div(className="name-stack", children=[
                html.Div(team['FULL_NAME'], className="detail-full-name"),
                html.Div(team_id, className="detail-abbr")
            ]),
            dcc.Dropdown(
                id='team-selector',
                options=[{'label': row['FULL_NAME'], 'value': abbr} for abbr, row in team_details.items()],
                value=team_id,
                className="detail-dropdown",
                clearable=False
            )
        ]),

        html.Hr(className="custom-divider"),

        # --- TEAM INFO SECTION ---
        html.Div(className="info-section", children=[
            html.P([html.Strong("Nickname: "), team['NICKNAME']]),
            html.P([html.Strong("Manager: "), team['GENERALMANAGER']]),
            html.P([html.Strong("Arena: "), team['ARENA']]),
        ]),

        # --- PLAYER LIST SECTION (NEW) ---
        html.Hr(className="custom-divider"),
        html.H2("TEAM PLAYERS", className="roster-title"),
        dcc.Input(
                id='player-search',
                type='text',
                placeholder='🔍 Search players...',
                className='player-search-bar',
                debounce=False # Search as you type
            ),
        html.Div(id="player-roster-output", className="roster-grid")

    ])

@callback(Output('url-redirect', 'pathname'), Input('team-selector', 'value'), prevent_initial_call=True)
def update_url(selected_team):
    return f"/teams/{selected_team}"

@callback(
    Output('player-roster-output', 'children'),
    [Input('player-search', 'value'),
     Input('team-selector', 'value')] # Uses team-selector to know which team to filter
)
def filter_roster(search_text, team_id):
    try:
        df_players = pd.read_csv("data/final_teams.csv")
    except:
        df_players = pd.DataFrame(columns=['TEAM_ABBR', 'PLAYER_NAME', 'NUMBER', 'POSITION'])
    
    # 1. Filter by current team
    roster = df_players[df_players['ABBREVIATION'] == team_id]
    
    # 2. Filter by search text (case-insensitive)
    if search_text:
        roster = roster[roster['PLAYER_NAME'].str.contains(search_text, case=False, na=False)]
    
    if roster.empty:
        return html.P("No players found.", style={'color': '#888', 'marginTop': '20px'})

    # 3. Generate the cards
    return [
        html.Div(className="player-card", children=[
            html.Div(str(p['PLAYER_NAME']), className="player-name"),
            html.Div(className="player-info", children=[
                html.Div(p['SEASON'], className="player-meta"),
                html.Div(p['PLAYER_ID'], className="player-number")
            ])
        ]) for _, p in roster.iterrows()
    ]