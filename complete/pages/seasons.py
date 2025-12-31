from dash import html, dcc, register_page
import plotly.express as px
import pandas as pd

register_page(__name__, path="/seasons")

pre = pd.read_csv("data/game1/MHL1.csv")

p = px.line(pre, x='Year', y=["Mean","Highest","Lowest"], 
              title='NBA Scoring Trends Play-In Tournament (2003-2021) Total Game Points',
              markers=True,
              template="plotly_dark") # Assuming a dark dashboard theme

p.update_layout(
    xaxis=dict(tickmode='linear', tickangle=45),
    margin=dict(l=40, r=40, t=60, b=40),
    paper_bgcolor='rgba(0,0,0,0)', # Transparent background to match your CSS
    plot_bgcolor='rgba(0,0,0,0)'
)
main = pd.read_csv("data/game2/MHL2.csv")

m = px.line(main, x='Year', y=["Mean","Highest","Lowest"], 
              title='NBA Scoring Trends Main Game Season (2003-2021) Total Game Points',
              markers=True,
              template="plotly_dark") # Assuming a dark dashboard theme

m.update_layout(
    xaxis=dict(tickmode='linear', tickangle=45),
    margin=dict(l=40, r=40, t=60, b=40),
    paper_bgcolor='rgba(0,0,0,0)', # Transparent background to match your CSS
    plot_bgcolor='rgba(0,0,0,0)'
)


years = list(range(2003, 2023))
layout = html.Div(
    className="seasons-page",
    children=[
        html.Div(className="nav-header", children=[
            # Link back to the absolute home page
            dcc.Link("← BACK TO HOME", href="/", className="back-button"),
            html.Span("NBA / SEASONS", className="breadcrumb")
        ]),
        html.H1("NBA SEASONS", className="teams-title", style={'textAlign': 'center'}),
        
        html.Div(className="graph-container", children=[
            dcc.Graph(
                id='seasons-trend-graph',
                figure=p,
                config={'displayModeBar': False} # Keeps the UI clean
            )
        ], style={'padding': '20px'}),
        html.Div(className="graph-container", children=[
            dcc.Graph(
                id='seasons-trend-graph',
                figure=m,
                config={'displayModeBar': False} # Keeps the UI clean
            )
        ], style={'padding': '20px'}),
        html.Div(className="text",children=[
        	html.P("The trend of the Total Scoring in a game shows that we are expected to see more points in the further games, but its not a big jump as viewer may think"),
        	html.P("And one more observation we can have is that there are more points being scored in Main Season then Pre or Play-In Season"),
        	html.H2("Go In Details Below", className="Limit-header")
        	]),
        html.Div(
		    className="season-grid",
		    children=[
			    dcc.Link(
			        f"{year}-{str(year+1)[2:]}", 
			        href=f"/seasons/{year}",
			        className="season-button"
			    ) for year in years
			]
		)
    ]
)