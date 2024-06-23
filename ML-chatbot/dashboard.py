from requests import post
from dash import Dash, dcc, html, callback, State, Output, Input

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H3(
            "ML Chatbot App",
            style={
                "textAlign": "center",
                "color": "#4CAF50",
                "fontFamily": "Arial, sans-serif",
                "marginBottom": "20px"
            }
        ),
        dcc.Textarea(
            id="input-textarea",
            value="",
            placeholder="Type your question here...",
            style={
                "width": "90%",
                "height": "100px",
                "margin": "0 auto",
                "display": "block",
                "padding": "10px",
                "border": "2px solid #4CAF50",
                "borderRadius": "10px",
                "fontFamily": "Arial, sans-serif",
                "fontSize": "16px"
            }
        ),
        html.Br(),
        html.Button(
            "Submit",
            id="input-submit",
            n_clicks=0,
            style={
                "backgroundColor": "#4CAF50",
                "color": "white",
                "border": "none",
                "padding": "10px 20px",
                "textAlign": "center",
                "textDecoration": "none",
                "display": "inline-block",
                "fontSize": "16px",
                "margin": "10px 2px",
                "cursor": "pointer",
                "borderRadius": "10px",
                "fontFamily": "Arial, sans-serif"
            }
        ),
        html.Div(
            id="output-response",
            style={
                "color": "#4CAF50",
                "backgroundColor": "#f0f0f0",
                "padding": "20px",
                "borderRadius": "10px",
                "width": "90%",
                "margin": "20px auto",
                "fontFamily": "Arial, sans-serif",
                "fontSize": "16px"
            }
        )
    ],
    style={
        "backgroundColor": "#ffffff",
        "padding": "20px",
        "fontFamily": "Arial, sans-serif"
    }
)

@callback(
    [Output("input-textarea", "value"),
     Output("output-response", "children")],
    Input("input-submit", "n_clicks"),
    State("input-textarea", "value")
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        result = post(url="http://127.0.0.1:8000", json={"question": value})

        if result.status_code == 200:
            response = result.json()["response"]
        else:
            response = f"Error: {result.status_code}"

        textarea = ""

        message = html.Div([
            html.Div("**Question:** " + value, style={"fontWeight": "bold"}),
            html.Br(),
            html.Div("**Answer:** " + response)
        ])

        return textarea, message
    else:
        return None, None

if __name__ == "__main__":
    app.run(port=5000, debug=True)
