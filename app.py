import dash
from dash import dcc, html, Input, Output, State
import re

# Initialize the Dash app
app = dash.Dash(__name__)

# Define helper functions to parse links from both formats
def parse_hubcloud(text):
    """Parse the HubCloud format text."""
    pattern = r'\[(.*?)\]\s(.+)\s\[(\d+\.\d+\sGB)\]\n\n💾\s(https://hubcloud.art/video/\w+)'
    matches = re.findall(pattern, text)
    return [{"name": match[1], "size": match[2], "link": match[3]} for match in matches]

def parse_gdtot(text):
    """Parse the GDTot format text."""
    pattern = r'(.+)\s-\s(\d+\.\d+\sGB)\n\s(https://new7.gdtot.dad/file/\d+)'
    matches = re.findall(pattern, text)
    return [{"name": match[0], "size": match[1], "link": match[2]} for match in matches]

# Define the layout of the app
app.layout = html.Div([
    html.H1("Link Parser Dashboard"),
    
    html.Label("Choose Link Type:"),
    dcc.Dropdown(
        id="link-type-dropdown",
        options=[
            {"label": "HubCloud", "value": "hubcloud"},
            {"label": "GDTot", "value": "gdtot"},
        ],
        value="hubcloud"
    ),
    
    html.Br(),
    
    html.Label("Enter Links:"),
    dcc.Textarea(
        id="link-input",
        style={"width": "100%", "height": 150},
        placeholder="Paste your links here..."
    ),
    
    html.Br(),
    
    html.Label("Enter IMDB Codes (comma separated):"),
    dcc.Input(
        id="imdb-input",
        type="text",
        style={"width": "100%"},
        placeholder="e.g. tt1234567, tt7654321"
    ),
    
    html.Br(),
    html.Button("Parse Links", id="parse-button"),
    
    html.Br(), html.Br(),
    
    html.Div(id="parsed-links-output"),
    html.Div(id="imdb-output")
])

# Define the callback to parse and display links
@app.callback(
    Output("parsed-links-output", "children"),
    Output("imdb-output", "children"),
    Input("parse-button", "n_clicks"),
    State("link-type-dropdown", "value"),
    State("link-input", "value"),
    State("imdb-input", "value")
)
def update_output(n_clicks, link_type, input_text, imdb_text):
    if not n_clicks or not input_text:
        return "", ""

    # Parse the input based on the selected link type
    parsed_data = []
    if link_type == "hubcloud":
        parsed_data = parse_hubcloud(input_text)
    elif link_type == "gdtot":
        parsed_data = parse_gdtot(input_text)

    # Format the parsed links output
    links_output = ""
    if parsed_data:
        links_output = html.Ul([
            html.Li([
                html.B("File Name: "), item["name"],
                html.Br(),
                html.B("Size: "), item["size"],
                html.Br(),
                html.B("Link: "), html.A(item["link"], href=item["link"], target="_blank"),
                html.Br(), html.Br()
            ]) for item in parsed_data
        ])
    else:
        links_output = "No links found in the input text."

    # Handle IMDB codes
    imdb_output = ""
    if imdb_text:
        imdb_codes = [code.strip() for code in imdb_text.split(",") if code.strip()]
        imdb_output = html.Ul([html.Li(f"IMDB Code: {code}") for code in imdb_codes])

    return links_output, imdb_output

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
