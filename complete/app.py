from dash import Dash, html, page_container

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    page_container,

    # --- THE GLOBAL FOOTER ---
    html.Footer(className="global-footer", children=[
        html.Hr(className="footer-divider"),
        html.Div(className="footer-content", children=[

            html.P("Designed & Developed By:", className="footer-label"),
            html.Div(className="footer-names", children=[
                html.Span("Hrithivk Rajbhar"),
                html.Span("Sumit Kumar"),
                html.Span("Tejaswani Kanpur"),
                html.Span("Shivani Parihar"),
            ]),
            html.P("TEAM: QUAD(ISc BHU)", className="footer-label"),
            html.A(
                f"Contact: Hrithivkgo1111@gmail.com", 
                href="mailto:Hrithivkgo1111@gmail.com", 
                className="footer-email"
            )
        ])
    ])
])

if __name__ == "__main__":
    app.run(debug=True)
