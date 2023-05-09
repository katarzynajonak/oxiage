# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

app = Dash(__name__,
           use_pages=True,
           external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.BOOTSTRAP],
           suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=0.5, maximum-scale=1.6, minimum-scale=0.5'}])

application = app.server

app.layout = html.Div([
    dash.page_container
])

if __name__ == '__main__':
    # app.run_server(host='xxx.xxx.x.x')
    app.run_server()
