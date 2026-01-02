from dash import html, register_page

register_page(__name__, path="/")

layout = html.Div(
    className="home-wrapper",
    children=[

        # Full-width image
        html.Img(
            src="/assets/HOME.jpeg",
            className="full-bg-image"
        ),

        # Overlay content
        html.Div(
            className="overlay",

            children=[
                html.H1("WELCOME TO NBA"),

                html.A(
                    href="/teams",
                    className="card left",
                    children=[
                        html.P("TEAMS"),
                        html.Img(src="/assets/teams.png")
                    ]
                ),

                html.A(
                    href="/seasons",
                    className="card right",
                    children=[
                        html.P("SEASONS"),
                        html.Img(src="/assets/seasons.png")
                    ]
                ),
            ]
        )
    ]
)
