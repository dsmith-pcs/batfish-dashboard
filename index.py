from dash import dcc, html
from dash.dependencies import Input, Output
from app import app
from layouts import main_page_layout
import callbacks

app.title = "Batfish Dashboard"
app.layout = main_page_layout


external_css = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
    ]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js"]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=False)
