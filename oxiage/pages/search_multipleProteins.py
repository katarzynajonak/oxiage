# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
from dash import html, dcc, callback, Input, Output
from dbUtil import DBgetOrganismNames, DBgetProteinsGenesNames
import mysql.connector
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs
import dash_mantine_components as dmc
from pathlib import Path
import configparser

dash.register_page(__name__,
                   path='/search_multipleProteins',
                   title='Search Multiple Proteins',
                   name='Search Multiple Proteins',
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

STYLE_DROPDOWN = {"width": "80%"}

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

    if lang_ID == None:
        lang_ID = 1
    if lang_ID != 1:
        lang_ID = 1

    organismsFromDB = DBgetOrganismNames(mydb)
    organismList = {}
    iter = 1
    for organism in organismsFromDB:
        organismList[str(iter)] = f'{organism[0]} ({organism[1]})'
        iter += 1

    genesFromDB = DBgetProteinsGenesNames(mydb)
    geneList = {}
    iter = 1
    for gene in genesFromDB:
        geneList[str(iter)] = f'{gene[0]} ({gene[1]})'
        iter += 1

    if lang_ID == None:
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
                    html.H1(children=[html.Span('Common Proteins Search ', style={'color': '#3d3d3d'}), ], ),
                    html.H3(
                        children=[
                            html.Span('Choose at least two organisms to perform common protein search ',
                                      style={'color': '#3d3d3d'}), ], ),
                    html.Hr(),
                    dmc.Breadcrumbs(
                        children=[
                            dcc.Link([html.I(className="bi bi-house"), html.Span('Home', style={"margin-left": "7px"})],
                                     href=f'/?lang_ID={lang_ID}', target='_blank'),
                            dcc.Link([html.I(className="bi bi-search-heart"),
                                      html.Span('Search Page', style={"margin-left": "7px"})],
                                     href=f'/search?lang_ID={lang_ID}', target='_blank'),
                            dcc.Link([html.Span('Common Proteins Search')],
                                     href=f'/search_multipleProteins?lang_ID={lang_ID}'),
                        ], ),
                    html.Br(),

                    dmc.Stepper(
                        active=2,
                        color="green",
                        radius="lg",
                        size="sm",
                        children=[
                            dmc.StepperStep(label="First step", description="Choose the type of search"),
                            dmc.StepperStep(label="Second step", description="Choose the common species", loading=True),
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
                                         html.Span('How to search for commonly oxidized proteins?', style={"margin-left": "7px"})],
                                        className="alert-heading"),
                                html.Hr(),
                                html.P('Choose at least two organisms to compare between using a multiple dropdown field. '
                                       'A simple visualization of common proteins detected in different datasets will be displayed. '
                                       'Click the green button below to see the results in a new browser tab.',
                                       style={'text-align': 'justify'}),
                            ], color='dark', id="alert-auto", is_open=True, dismissable=True),
                        ], xs=10, sm=10, md=10, lg=9, xl=9),
                    ]),
                    html.Br(),

                    dbc.Row([dbc.Col([
                        html.H5('Choose at least two organisms of interest:'),
                        dcc.Dropdown(options=[{'label': 'Budding yeast (S. cerevisiae)', 'value': 'Yeast'},
                                              {'label': 'Mouse (M. musculus)', 'value': 'Mice'},
                                              {'label': 'Nematode (C. elegans)', 'value': 'Worm'},
                                              {'label': 'Fruit fly (D. melanogaster)', 'value': 'Fly'}],
                                     placeholder=['Choose at least one organism ...'],
                                     id='crossfilter-organisms', multi=True, style=STYLE_DROPDOWN),
                        html.Br(), ]),
                    ]),

                    dbc.Row([dbc.Col([
                        html.Br(),
                        html.Br(),
                        dbc.Placeholder(
                            html.Div(id="loading-placeholder-output", children=[
                                html.Br(),
                                html.Br(),
                                html.Span(
                                    'Please, choose at least two organisms to see the diagram of overlapping proteins'
                                    'found to be redox-sensitive in performed aging experiments',
                                    style={'color': '#bdb9b9'}),
                            ]), className="w-100", animation="wave",
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.Button(children=[html.I(className="bi bi-search-heart"),
                                             html.Span(
                                                 [html.Span("Search for common proteins", style={"margin-left": "7px"}),
                                                  html.Span(
                                                      'Click when You choose at least two organisms to start the search',
                                                      className='tooltiptext2')], className='tooltip2')],
                                   color="success", n_clicks=0, className="mt-auto", id='search-common',
                                   href='/search_multipleProteins', disabled=False, external_link=True,
                                   target="_blank"),
                        dcc.Location(id='url-multi', refresh=False),
                        html.Br(),
                    ], xs=11, sm=11, md=11, lg=9, xl=9),
                    ]),
                    html.Br(),
                ])
            ], xs=9, sm=9, md=9, lg=9, xl=9)
        ])
    ])


@callback(
    Output('search-common', 'children'),
    Input('search-common', 'n_clicks'),
    prevent_initial_call=True,
)
def on_Click(n_clicks):
    return html.I(children=[html.I(className="bi bi-search-heart"), " Search for common proteins"])


@callback(
    [Output("loading-placeholder-output", "children"),
    Output('search-common', 'href')],
    [Input('url-multi', 'href'),
    Input('crossfilter-organisms', 'value')],
    prevent_initial_call=True
)
def load_output(href, value):
    parsed_url = urlparse(href)
    getParams = parse_qs(parsed_url.query)
    lang = getParams.get('lang_ID')
    if not lang:
        lang_u = 1
    else:
        lang_u = lang[0]

    if value is None:
        raise PreventUpdate

    countY = 0
    countM = 0
    countW = 0
    countF = 0
    for i in range(len(value)):
        if value[i] == 'Yeast':
            countY = 1
        if value[i] == 'Mice':
            countM = 2
        if value[i] == 'Worm':
            countW = 3
        if value[i] == 'Fly':
            countF = 4

    num = 0
    imgCommon = ''
    if countY > 0 and countM > 0 and countW > 0 and countF > 0: #YWFM
        num = 1
        imgCommon = "/assets/images/venn/Website_Venn_YWFM.png"
    if countY > 0 and countW > 0 and countF > 0 and countM == 0: #YWF
        num = 2
        imgCommon = "/assets/images/venn/Website_Venn_YWF.png"
    if countY > 0 and countW > 0 and countF == 0 and countM > 0: #YWM
        num = 3
        imgCommon = "/assets/images/venn/Website_Venn_YWM.png"
    if countY > 0 and countW == 0 and countF > 0 and countM > 0: #YFM
        num = 4
        imgCommon = "/assets/images/venn/Website_Venn_YFM.png"
    if countY == 0 and countW > 0 and countF > 0 and countM > 0: #WFM
        num = 5
        imgCommon = "/assets/images/venn/Website_Venn_WFM.png"
    if countY > 0 and countW > 0 and countF == 0 and countM == 0: #YW
        num = 6
        imgCommon = "/assets/images/venn/Website_Venn_YW.png"
    if countY > 0 and countW == 0 and countF > 0 and countM == 0: #YF
        num = 7
        imgCommon = "/assets/images/venn/Website_Venn_YF.png"
    if countY > 0 and countW == 0 and countF == 0 and countM > 0: #YM
        num = 8
        imgCommon = "/assets/images/venn/Website_Venn_YM.png"
    if countY == 0 and countW > 0 and countF > 0 and countM == 0: #WF
        num = 9
        imgCommon = "/assets/images/venn/Website_Venn_WF.png"
    if countY == 0 and countW > 0 and countF == 0 and countM > 0: #WM
        num = 10
        imgCommon = "/assets/images/venn/Website_Venn_WM.png"
    if countY == 0 and countW == 0 and countF > 0 and countM > 0: #FM
        num = 11
        imgCommon = "/assets/images/venn/Website_Venn_FM.png"

    if num > 0 and num < 12:
        return html.A([html.Img(src=f'{imgCommon}', style={
                'width': '90%'})]), f'/search_results_tabCommon?lang_ID={lang_u}&Num={num}'
    else:
        return html.Span('Please, choose at least two organisms to see the diagram of overlapping proteins'
          'found to be redox-sensitive in performed aging experiments', style={'color': '#bdb9b9'}), f'/search'

