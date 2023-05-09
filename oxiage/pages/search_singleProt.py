# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
from dash import html, dcc, callback, Input, Output, State
from dbUtil import DBgetGeneAndProteinNames, DBgetOrganismNames
import mysql.connector
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs
import dash_mantine_components as dmc
from pathlib import Path
import configparser

dash.register_page(__name__,
                   path='/search_singleProt',
                   title='Search Single Protein',
                   name='Search Single Protein',
                   location="mainmenu")

CONTENT_STYLE = {
    "padding": "2rem 1rem"
}

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "padding": "2rem 1rem",
    "border-right": "2px solid whitesmoke"
}

STYLE_DROPDOWN = {"width": "100%"}

def layout(lang_ID=None):

    config = configparser.ConfigParser()
    path = Path(__file__).parent / "../../my_config.ini"
    config.read(path)
    config.sections()

    hostName = config['OxiAge']['host'].strip("'")
    userName = config['OxiAge']['user'].strip("'")
    passwordName = config['OxiAge']['password'].strip("'")
    portName = config['OxiAge']['port'].strip("'")
    databaseName = config['OxiAge']['database'].strip("'")

    mydb = mysql.connector.connect(
        host=hostName,
        user=userName,
        password=passwordName,
        port=portName,
        database=databaseName,
        auth_plugin='mysql_native_password'
    )

    organismsFromDB = DBgetOrganismNames(mydb)
    organismList = {}
    iter = 1
    for organism in organismsFromDB:
        organismList[str(iter)] = f'{organism[0]} ({organism[1]})'
        iter += 1

    if lang_ID == None:
        lang_ID = 1
    if lang_ID != 1:
        lang_ID = 1

    return html.Div([
        dbc.Row([
            ### MENU
            dbc.Col([
                html.Div([
                    html.A([html.Img(src="/assets/images/Logo.png", style={'width': '98%'})]),
                    html.Hr(),
                    html.P('Cross species comparison of oxidation changes during aging', style={"margin-left": "1rem"}),
                    html.Br(),
                    html.Br(),

                    dbc.Nav(
                        [
                            dbc.NavLink(children=[html.I(className="bi bi-house"), ' Home'],
                                        href=f'/?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(children=[html.I(className="bi bi-search-heart"), ' Database search'],
                                        href=f'/search?lang_ID={lang_ID}', active=True, external_link=True,
                                        style={'color': 'white'}),
                            dbc.NavLink(children=[html.I(className="bi bi-download"), ' Downloads'],
                                        href=f'/downloads?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(children=[html.I(className="bi bi-chat-quote"), ' Cite us'],
                                        href=f'/cite_us?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(children=[html.I(className="bi bi-question-circle"), ' Help'],
                                        href=f'/help_page?lang_ID={lang_ID}', active=False, external_link=True),
                        ], vertical=True, pills=True, fill=True,
                    ),

                    html.Br(),
                    html.Br(),

                    dbc.Accordion([
                        dbc.AccordionItem([
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Knoefler et al., 2012", style={"margin-left": "15px"})],
                                     href='https://www.sciencedirect.com/science/article/pii/S1097276512005412',
                                     target='_blank'),
                            html.Br(),
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Brandes et al., 2013", style={"margin-left": "15px"})],
                                     href='https://elifesciences.org/articles/306', target='_blank'),
                            html.Br(),
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Menger et al., 2013", style={"margin-left": "15px"})],
                                     href='https://www.sciencedirect.com/science/article/pii/S2211124715005690?via%3Dihub',
                                     target='_blank'),
                            html.Br(),
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Xiao et al., 2020", style={"margin-left": "15px"})],
                                     href='https://www.sciencedirect.com/science/article/pii/S0092867420301562',
                                     target='_blank'),
                            html.Br(),
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Jonak et al., 2023", style={"margin-left": "15px"})],
                                     href='https://www.biorxiv.org/content/10.1101/2023.05.08.539783v1',
                                     target='_blank'),
                        ], title='Resources', ),
                        dbc.AccordionItem([
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Ulrike Topf Lab", style={"margin-left": "15px"})],
                                     href='http://topf-lab.org/', target='_blank'),
                            html.Br(),
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Oximouse", style={"margin-left": "15px"})],
                                     href='https://oximouse.hms.harvard.edu/', target='_blank'),
                            html.Br(),
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("UniProtKB", style={"margin-left": "15px"})],
                                     href='https://www.uniprot.org/', target='_blank'),
                            html.Br(),
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Alliance of Genome Resources",
                                                         style={"margin-left": "15px"})],
                                     href='https://www.alliancegenome.org/', target='_blank'),
                            html.Br(),
                            dcc.Link(children=[html.I(className="bi bi-box-arrow-in-right"),
                                               html.Span("Gene Ontology", style={"margin-left": "15px"})],
                                     href='http://geneontology.org/', target='_blank'),
                        ], title='External Links', ),
                        dbc.AccordionItem([
                            dcc.Link(children=[html.I(className="bi bi-envelope"),
                                               html.Span("OxiAge authors", style={"margin-left": "15px"})],
                                     href='mailto:k.jonak@bb.waw.pl', target='_blank'),
                        ], title='Contact', ),
                    ], start_collapsed=True),
                    html.Br(),
                    html.Br(),
                    dmc.Text("Copyright© by Katarzyna Jonak and Ulrike Topf, 2023",
                             style={"backgroundColor": "white", 'font-size': '80%'}),
                    html.A([html.Img(src="/assets/images/IBB_logo.png", style={'width': '20%'}), ],
                           href='https://ibb.edu.pl/', target='_blank'),
                ], style=SIDEBAR_STYLE),
            ], xs=3, sm=3, md=3, lg=3, xl=3),

            ### CONTENT
            dbc.Col([
                html.Div(style=CONTENT_STYLE, children=[
                    html.H1(children=[html.Span('Single Protein Search ', style={'color': '#3d3d3d'}), ], ),
                    html.H3(
                        children=[
                            html.Span('Choose organism and protein of interest ', style={'color': '#3d3d3d'}), ], ),
                    html.Hr(),
                    dmc.Breadcrumbs(
                        children=[
                            dcc.Link([html.I(className="bi bi-house"), html.Span('Home', style={"margin-left": "7px"})],
                                     href=f'/?lang_ID={lang_ID}', target='_blank'),
                            dcc.Link([html.I(className="bi bi-search-heart"),
                                      html.Span('Search Page', style={"margin-left": "7px"})],
                                     href=f'/search?lang_ID={lang_ID}', target='_blank'),
                            dcc.Link([html.Span('Single Protein Search')],
                                     href=f'/search_singleProt?lang_ID={lang_ID}'),
                        ], ),
                    html.Br(),

                    dmc.Stepper(
                        active=2,
                        color="green",
                        radius="lg",
                        size="sm",
                        children=[
                            dmc.StepperStep(label="First step", description="Choose the type of search"),
                            dmc.StepperStep(label="Second step", description="Type the single protein", loading=True),
                            dmc.StepperStep(label="Third step",
                                            description="Choose the specific protein from result table"),
                            dmc.StepperStep(label="Fourth step", description="Enjoy the cross-species comparison!"),
                        ],
                    ),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Br(),
                            dbc.Alert([
                                html.H5([html.I(className="bi bi-info-square-fill"),
                                         html.Span('How to search for a single protein?', style={"margin-left": "7px"})],
                                        className="alert-heading"),
                                html.Hr(),
                                html.P('Choose a single organism from a dropdown list and type first three letters '
                                       'of gene name or UniProt ID. Possible search options will be displayed. '
                                       'Click the green button below to see the results in a new browser tab.',
                                       style={'text-align': 'justify'}),
                            ], color='dark', id="alert-auto", is_open=True, dismissable=True),
                        ], xs=10, sm=10, md=10, lg=7, xl=7),
                    ]),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.H5('Choose the organism of interest:'),
                            dcc.Dropdown(
                                options=organismList,
                                value='1',
                                id='organism-dropdown',
                                clearable=False, style=STYLE_DROPDOWN),
                            html.Br(),
                            html.Br(),
                            html.H5('Type in the protein of interest (gene name or UniProt ID):'),
                            dcc.Dropdown(id='geneOrprotein-dynamic-dropdown',
                                         clearable=True,
                                         placeholder='Type first three letters of gene name or UniProt ID',
                                         style=STYLE_DROPDOWN),
                            html.Br(),
                            html.Br(),
                            dbc.Button(children=[html.I(className="bi bi-search-heart"), " START THE SEARCH"],
                                       color="success",
                                       className="mt-auto",
                                       id='search-btn', href='/search_results_tab', disabled=True, external_link=True,
                                       target="_blank"),
                            html.Br(),
                            dcc.Location(id='url', refresh=False)
                        ], xs=10, sm=10, md=10, lg=7, xl=7),
                    ]),
                ])
            ], xs=9, sm=9, md=9, lg=9, xl=9)
        ])
    ])


@callback(
    Output("alert-auto", "is_open"),
    [Input("alert-toggle-auto", "n_clicks")],
    [State("alert-auto", "is_open")],
)
def toggle_alert(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output('geneOrprotein-dynamic-dropdown', 'idOrganism'),
    Input('organism-dropdown', 'value')
)
def update_output(value):
    return f'{value}'


@callback(
    Output('search-btn', 'children'),
    Input('search-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def on_Click(n_clicks):
    return html.I(children=[html.I(className="bi bi-search-heart"), "  SEARCH"])


@callback(
    Output('geneOrprotein-dynamic-dropdown', 'options'),
    Output('geneOrprotein-dynamic-dropdown', 'idOrganism2'),
    Output('geneOrprotein-dynamic-dropdown', 'curValue2'),
    Output('search-btn', 'href'),
    Output('search-btn', 'disabled'),
    Input('organism-dropdown', 'value'),
    Input("geneOrprotein-dynamic-dropdown", "search_value"),
    Input("geneOrprotein-dynamic-dropdown", "idOrganism"),
    Input('geneOrprotein-dynamic-dropdown', 'value'),
    Input('url', 'href'),
    Input('geneOrprotein-dynamic-dropdown', 'idOrganism2'),
    Input('geneOrprotein-dynamic-dropdown', 'curValue2'),
    prevent_initial_call=True
)
def update_options(value, search_value, idOrganism, curValue, href, idOrganism2, curValue2):
    parsed_url = urlparse(href)
    getParams = parse_qs(parsed_url.query)
    lang = getParams.get('lang_ID')
    if not lang:
        lang_u = 1
    else:
        lang_u = lang[0]

    if idOrganism != idOrganism2:
        return {}, idOrganism, curValue, f'/search_results_tab?lang_ID={lang_u}&organism_ID={idOrganism}',True

    if curValue != curValue2:
        if not curValue:
            return {}, idOrganism, curValue, f'/search_results_tab?lang_ID={lang_u}&organism_ID={idOrganism}', True
        else:
            return dash.no_update, idOrganism, curValue, f'/search_results_tab?lang_ID={lang_u}&UniGene={curValue}&organism_ID={idOrganism}', False

    if search_value is None:
        raise PreventUpdate
    else:
        if len(search_value) < 3:
            raise PreventUpdate

    config = configparser.ConfigParser()
    path = Path(__file__).parent / "../../my_config.ini"
    config.read(path)
    config.sections()

    hostName = config['OxiAge']['host'].strip("'")
    userName = config['OxiAge']['user'].strip("'")
    passwordName = config['OxiAge']['password'].strip("'")
    portName = config['OxiAge']['port'].strip("'")
    databaseName = config['OxiAge']['database'].strip("'")

    mydb = mysql.connector.connect(
        host=hostName,
        user=userName,
        password=passwordName,
        port=portName,
        database=databaseName,
        auth_plugin='mysql_native_password'
    )

    geneOrProteinFromDB = DBgetGeneAndProteinNames(mydb, idOrganism, search_value.upper())
    geneOrProteinList = {}

    for geneOrProtein in geneOrProteinFromDB:
        geneOrProteinList[str(geneOrProtein[0])] = f'{geneOrProtein[0]}'

    return geneOrProteinList, idOrganism, curValue, f'/search_results_tab?lang_ID={lang_u}&organism_ID={idOrganism}',True