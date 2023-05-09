# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

from urllib.parse import urlparse, parse_qs
import dash
from dbUtil import DBgetCommonNamesAllOrto
import mysql.connector
import dash_bootstrap_components as dbc
from dash import dcc, callback, html
from dash import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import dash_mantine_components as dmc
from pathlib import Path
import configparser

dash.register_page(__name__,
                   path='/search_results_tabCommon',
                   title='Search Results Common',
                   name='Search Results Common',
                   location="error")

CONTENT_STYLE = {
    "padding": "2rem 1rem",
}

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "padding": "2rem 1rem",
    "border-right": "2px solid whitesmoke"
}

def layout(lang_ID=None, Num=None):

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
    if lang_ID != '1':
        lang_ID = 1

    areThereResults = False
    commonSp = ''
    if Num == '1':
        areThereResults = True
        commonSp = 'Budding yeast, worm, fruit fly and mouse'
    if Num == '2':
        areThereResults = True
        commonSp = 'Budding yeast, worm and fruit fly'
    if Num == '3':
        areThereResults = True
        commonSp = 'Budding yeast, worm and mouse'
    if Num == '4':
        areThereResults = True
        commonSp = 'Budding yeast, fruit fly and mouse'
    if Num == '5':
        areThereResults = True
        commonSp = 'Worm, fruit fly and mouse'
    if Num == '6':
        areThereResults = True
        commonSp = 'Budding yeast and worm'
    if Num == '7':
        areThereResults = True
        commonSp = 'Budding yeast and fruit fly'
    if Num == '8':
        areThereResults = True
        commonSp = 'Budding yeast and mouse'
    if Num == '9':
        areThereResults = True
        commonSp = 'Worm and fruit fly'
    if Num == '10':
        areThereResults = True
        commonSp = 'Worm and mouse'
    if Num == '11':
        areThereResults = True
        commonSp = 'Fruit fly and mouse'

    if areThereResults==False:
        return html.Div([
            dbc.Alert("No results found", color="warning"),
            html.Br(),
            dcc.Link(f'Go back to search options', href=f'/search?lang_ID={lang_ID}')])
    else:
        return html.Div([
            dbc.Row([
                ### MENU
                dbc.Col([

                    html.Div([
                        html.A([html.Img(src="/assets/images/Logo.png", style={'width': '98%'})]),
                        html.Hr(),
                        html.P('Cross species comparison of oxidation changes during aging',
                               style={"margin-left": "1rem"}),
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
                                         href='http://topf-lab.org/',
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
                        html.H1(children=[
                            html.Span('Results for Common Proteins Search ', style={'color': '#3d3d3d'}), ], ),
                        html.H4(
                            children=[
                                html.Span('Table contaning proteins found oxidized accross species ',
                                          style={'color': '#3d3d3d'}), ], ),
                        html.Hr(),
                        dmc.Breadcrumbs(
                            children=[
                                dcc.Link(
                                    [html.I(className="bi bi-house"), html.Span('Home', style={"margin-left": "7px"})],
                                    href=f'/?lang_ID={lang_ID}', target='_blank'),
                                dcc.Link([html.I(className="bi bi-search-heart"),
                                          html.Span('Search Page', style={"margin-left": "7px"})],
                                         href=f'/search?lang_ID={lang_ID}', target='_blank'),
                                dcc.Link([html.Span('Common Proteins Search')],
                                         href=f'/search_multipleProteins?lang_ID={lang_ID}'),
                                dcc.Link([html.Span('Common Proteins Search')],
                                         href=f'/search_results_tabCommon?lang_ID={lang_ID}&Num={Num}'
                                         ),
                            ],
                        ),
                        html.Br(),

                        dmc.Stepper(
                            active=3,
                            color="green",
                            radius="lg",
                            size="sm",
                            children=[
                                dmc.StepperStep(label="First step", description="Choose the type of search"),
                                dmc.StepperStep(label="Second step", description="Type the annotation"),
                                dmc.StepperStep(label="Third step",
                                                description="Choose the specific protein from result table",
                                                loading=True),
                                dmc.StepperStep(label="Fourth step", description="Enjoy the cross-species comparison!"),
                            ],
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.Row([dbc.Col([
                            html.Br(),
                            dbc.Alert([
                                html.P([html.I(className="bi bi-info-square-fill"),
                                        html.Span(['To see the oxidation state of the chosen protein and the '
                                                   'orthologs, click on the UniProt ID link of chosen protein. ',
                                                   html.Hr(),
                                                   'The table can be sorted using arrows next to the column names. '
                                                   'The table can be filtered by typing in the empty box under the column names '
                                                   'and clicking ENTER. To remove the filter, clear the box and click '
                                                   'ENTER once more.'],
                                                  style={"margin-left": "7px"})],
                                       className="alert-heading"),
                            ], color='dark', id="alert-auto-common", is_open=True, dismissable=True),
                        ], xs=11, sm=11, md=11, lg=10, xl=10),
                        ]),
                        html.Br(),

                        dbc.Row([dbc.Col([
                            html.H4(
                                children=[html.Span('Common proteins between species: ', style={'color': '#3d3d3d'}),
                                          html.Span(f'{commonSp}',
                                                    style={'color': '#FF5147', 'font-size': '0.9em'})], ),
                            html.Br(),
                            html.Br(),

                            html.Div([dmc.LoadingOverlay
                                      (dmc.Grid(id='gridAlignment-common',
                                                children=[(html.P('Loading table ...',
                                                                  style={'margin-left': 'auto', 'margin-right': 'auto',
                                                                         'margin-top': '15px', 'color': '#0096FF',
                                                                         'height': '90px'}))], gutter="lg"),
                                       exitTransitionDuration=1000, overlayColor='grey',
                                       overlayOpacity=0, loaderProps={'variant': 'dots'},
                                       ),
                                      html.Br(), html.Hr(), html.Br(), ]
                                     ),
                            dcc.Location(id='url-multi2', refresh=False),
                            dcc.Interval(id='interval-component2', interval=1 * 1000, n_intervals=0, max_intervals=1),

                        ], xs=11, sm=11, md=11, lg=9, xl=9),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.Br(),
                                dbc.Button(children=[html.I(className="bi bi-download"),
                                                     html.Span("Download Table", style={"margin-left": "15px"})],
                                           color="info", className="d-flex align-items-center",
                                           id='btn-download-common', n_clicks=0),
                                dcc.Download(id="download-common"),
                                dcc.Location(id='url-function', refresh=False),

                            ], xs=10, sm=10, md=10, lg=10, xl=10),
                        ]),

                    ])
                ], xs=9, sm=9, md=9, lg=9, xl=9)
            ])
        ])


@callback(
    Output('download-common', 'data'),
    Input('tbl-common-multi', 'data'),
    Input('btn-download-common', 'n_clicks'),
    Input('url-multi2', 'href'),
    prevent_initial_call=True,
)
def update_search_button(data, n_clicks, href):
    if n_clicks == 0:
        return ''
    else:
        parsed_url = urlparse(href)
        getParams = parse_qs(parsed_url.query)
        Num = ''
        uni = getParams.get('Num')
        if not uni:
            Num = ''
        else:
            Num = uni[0]

        dataFrame = pd.DataFrame(data)
        dataFrame2 = dataFrame.drop(columns='UniProt Link1')
        dataFrame3 = dataFrame2.drop(columns='UniProt Link2')

        if Num == '1':
            dataFrame3 = dataFrame3.drop(columns='UniProt Link3')
            dataFrame3 = dataFrame3.drop(columns='UniProt Link4')
        if Num == '2' or Num == '3' or Num == '4' or Num == '5':
            dataFrame3 = dataFrame3.drop(columns='UniProt Link3')
        return dcc.send_data_frame(dataFrame3.to_csv, "OxiAge_CommonProteins_Table.txt", sep=';')


@callback(
    Output('gridAlignment-common', 'children'),
    Input('interval-component2', 'n_intervals'),
    Input('url-multi2', 'href'),
    prevent_initial_call=True,
)
def update_common_table(n_intervals, href):

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

    parsed_url = urlparse(href)
    getParams = parse_qs(parsed_url.query)
    Num = ''
    uni = getParams.get('Num')
    if not uni:
        Num = ''
    else:
        Num = uni[0]

    path = Path(__file__).parent / "../assets/tables/OxiAge_CommonProteins.xlsx"

    commonSp = ''
    intersect=''
    org1=''
    org2=''
    org3=''
    if Num == '1':
        commonSp = 'Budding yeast, worm, fruit fly and mouse'
        intersect = pd.read_excel(path, sheet_name="SGD_WB_FB_MGI")
        uniYeast = []
        geneYeast = []
        for y in intersect['UniProt Org1']:
            uniProtNamesFromDBOrtoYeast = DBgetCommonNamesAllOrto(mydb, y)
            uniYeast.append(uniProtNamesFromDBOrtoYeast[0][0])
            geneYeast.append(uniProtNamesFromDBOrtoYeast[0][1])
        uniWorm = []
        geneWorm = []
        for w in intersect['UniProt Org2']:
            uniProtNamesFromDBOrtoWorm = DBgetCommonNamesAllOrto(mydb, w)
            uniWorm.append(uniProtNamesFromDBOrtoWorm[0][0])
            geneWorm.append(uniProtNamesFromDBOrtoWorm[0][1])
        uniFly = []
        geneFly = []
        for f in intersect['UniProt Org3']:
            uniProtNamesFromDBOrtoFly = DBgetCommonNamesAllOrto(mydb, f)
            uniFly.append(uniProtNamesFromDBOrtoFly[0][0])
            geneFly.append(uniProtNamesFromDBOrtoFly[0][1])
        uniMouse = []
        geneMouse = []
        for m in intersect['UniProt Org4']:
            uniProtNamesFromDBOrtoMouse = DBgetCommonNamesAllOrto(mydb, m)
            uniMouse.append(uniProtNamesFromDBOrtoMouse[0][0])
            geneMouse.append(uniProtNamesFromDBOrtoMouse[0][1])

        dataTable = {'Uni org1': uniYeast, 'Gene org1': geneYeast,
                     'Uni org2': uniWorm, 'Gene org2': geneWorm,
                     'Uni org3': uniFly, 'Gene org3': geneFly,
                     'Uni org4': uniMouse, 'Gene org4': geneMouse,}
        df = pd.DataFrame(dataTable)
        df['UniProt Link1'] = df['Uni org1'].apply(
            lambda Ly: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={Ly}' target='_blank'>{Ly}</a>")
        df['UniProt Link2'] = df['Uni org2'].apply(
            lambda Lw: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={Lw}' target='_blank'>{Lw}</a>")
        df['UniProt Link3'] = df['Uni org3'].apply(
            lambda Lf: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={Lf}' target='_blank'>{Lf}</a>")
        df['UniProt Link4'] = df['Uni org4'].apply(
            lambda Lm: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={Lm}' target='_blank'>{Lm}</a>")

        return [
            dash_table.DataTable(export_columns='all',
                                 data=df.to_dict('records'),
                                 columns=[
                                     {'id': 'UniProt Link1', 'name': [" Budding yeast", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org1', 'name': [" Budding yeast", " Gene name"]},

                                     {'id': 'UniProt Link2', 'name': [" Nematode (worm)", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org2', 'name': [" Nematode (worm)", " Gene name"]},

                                     {'id': 'UniProt Link3', 'name': [" Fruit fly", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org3', 'name': [" Fruit fly", " Gene name"]},

                                     {'id': 'UniProt Link4', 'name': [" Mouse", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org4', 'name': [" Mouse", " Gene name"]},
                                 ],
                                 markdown_options={"html": True},
                                 merge_duplicate_headers=True,
                                 style_as_list_view=False,
                                 page_size=20,
                                 style_cell={'font-family': 'sans-serif'},
                                 style_cell_conditional=[
                                     {'if': {'column_id': ['Gene org1', 'Gene org2', 'Gene org3', 'Gene org4']},
                                      'height': 'auto', 'width': 'auto',
                                      'textAlign': 'left', },
                                     {'if': {'column_id': ['UniProt Link1', 'UniProt Link2', 'UniProt Link3', 'UniProt Link4']},
                                      'height': 'auto', 'width': 'auto',
                                      'textAlign': 'left', },
                                 ],
                                 sort_action="native",
                                 filter_action="native",
                                 filter_options={'case': 'insensitive'},
                                 page_current=0,
                                 id='tbl-common-multi',
                                 tooltip_data=[{'UniProt Link1':
                                     {
                                         'value': 'Click here to search for the data on oxidation of chosen protein'.format(
                                             str(row['UniProt Link1'])),
                                         'type': 'markdown', }
                                 } for row in df.to_dict('records')],
                                 css=[{'selector': '.dash-table-tooltip',
                                       'rule': 'background-color: whitesmoke; font-family: Helvetica; color: black; '
                                               'text-align: center', },
                                      ],
                                 tooltip_delay=0,
                                 tooltip_duration=None, )
        ]


    if Num == '2' or Num == '3' or Num == '4' or Num == '5':
        if Num == "2":
            commonSp = 'Budding yeast, worm and fruit fly'
            org1 = 'Budding yeast'
            org2 = 'Nematode (worm)'
            org3 = 'Fruit fly'
            intersect = pd.read_excel(path, sheet_name="SGD_WB_FB")
        if Num == "3":
            commonSp = 'Budding yeast, worm and mouse'
            intersect = pd.read_excel(path, sheet_name="SGD_WB_MGI")
            org1 = 'Budding yeast'
            org2 = 'Nematode (worm)'
            org3 = 'Mouse'
        if Num == "4":
            commonSp = 'Budding yeast, fruit fly and mouse'
            intersect = pd.read_excel(path, sheet_name="SGD_FB_MGI")
            org1 = 'Budding yeast'
            org2 = 'Fruit fly'
            org3 = 'Mouse'
        if Num == "5":
            commonSp = 'Nematode (worm), fruit fly and mouse'
            intersect = pd.read_excel(path, sheet_name="WB_FB_MGI")
            org1 = 'Nematode (worm)'
            org2 = 'Fruit fly'
            org3 = 'Mouse'

        uniOrg1 = []
        geneOrg1 = []
        for or1 in intersect['UniProt Org1']:
            uniProtNamesFromDBOrtoOr1 = DBgetCommonNamesAllOrto(mydb, or1)
            uniOrg1.append(uniProtNamesFromDBOrtoOr1[0][0])
            geneOrg1.append(uniProtNamesFromDBOrtoOr1[0][1])
        uniOrg2 = []
        geneOrg2 = []
        for or2 in intersect['UniProt Org2']:
            uniProtNamesFromDBOrtoOr2 = DBgetCommonNamesAllOrto(mydb, or2)
            uniOrg2.append(uniProtNamesFromDBOrtoOr2[0][0])
            geneOrg2.append(uniProtNamesFromDBOrtoOr2[0][1])
        uniOrg3 = []
        geneOrg3 = []
        for or3 in intersect['UniProt Org3']:
            uniProtNamesFromDBOrtoOr3 = DBgetCommonNamesAllOrto(mydb, or3)
            uniOrg3.append(uniProtNamesFromDBOrtoOr3[0][0])
            geneOrg3.append(uniProtNamesFromDBOrtoOr3[0][1])

        dataTable = {'Uni org1': uniOrg1, 'Gene org1': geneOrg1,
                     'Uni org2': uniOrg2, 'Gene org2': geneOrg2,
                     'Uni org3': uniOrg3, 'Gene org3': geneOrg3,}
        df = pd.DataFrame(dataTable)
        df['UniProt Link1'] = df['Uni org1'].apply(
            lambda L1: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={L1}' target='_blank'>{L1}</a>")
        df['UniProt Link2'] = df['Uni org2'].apply(
            lambda L2: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={L2}' target='_blank'>{L2}</a>")
        df['UniProt Link3'] = df['Uni org3'].apply(
            lambda L3: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={L3}' target='_blank'>{L3}</a>")

        return [
            dash_table.DataTable(export_columns='all',
                                 data=df.to_dict('records'),
                                 columns=[
                                     {'id': 'UniProt Link1', 'name': [f" {org1}", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org1', 'name': [f" {org1}", " Gene name"]},

                                     {'id': 'UniProt Link2', 'name': [f" {org2}", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org2', 'name': [f" {org2}", " Gene name"]},

                                     {'id': 'UniProt Link3', 'name': [f" {org3}", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org3', 'name': [f" {org3}", " Gene name"]},
                                 ],
                                 markdown_options={"html": True},
                                 merge_duplicate_headers=True,
                                 style_as_list_view=False,
                                 page_size=20,
                                 style_cell={'font-family': 'sans-serif'},
                                 style_cell_conditional=[
                                     {'if': {'column_id': ['Gene org1', 'Gene org2', 'Gene org4']},
                                      'height': 'auto', 'width': 'auto',
                                      'textAlign': 'left', },
                                     {'if': {'column_id': ['UniProt Link1', 'UniProt Link2', 'UniProt Link3']},
                                      'height': 'auto', 'width': 'auto',
                                      'textAlign': 'left', },
                                 ],
                                 sort_action="native",
                                 filter_action="native",
                                 page_current=0,
                                 id='tbl-common-multi',
                                 tooltip_data=[{'UniProt Link1':
                                     {
                                         'value': 'Click here to search for the data on oxidation of chosen protein'.format(
                                             str(row['UniProt Link1'])),
                                         'type': 'markdown', }
                                 } for row in df.to_dict('records')],
                                 css=[{'selector': '.dash-table-tooltip',
                                       'rule': 'background-color: whitesmoke; font-family: Helvetica; color: black; '
                                               'text-align: center', },
                                      ],
                                 tooltip_delay=0,
                                 tooltip_duration=None, )
        ]
    else:
        if Num == "6":
            commonSp = 'Budding yeast and worm'
            org1 = 'Budding yeast'
            org2 = 'Nematode (worm)'
            intersect = pd.read_excel(path, sheet_name="SGD_WB")
        if Num == "7":
            commonSp = 'Budding yeast and worm'
            intersect = pd.read_excel(path, sheet_name="SGD_FB")
            org1 = 'Budding yeast'
            org2 = 'Fruit fly'
        if Num == "8":
            commonSp = 'Budding yeast and mouse'
            intersect = pd.read_excel(path, sheet_name="SGD_MGI")
            org1 = 'Budding yeast'
            org2 = 'Mouse'
        if Num == "9":
            commonSp = 'Worm and fruit fly'
            intersect = pd.read_excel(path, sheet_name="WB_FB")
            org1 = 'Nematode (worm)'
            org2 = 'Fruit fly'
        if Num == "10":
            commonSp = 'Worm and mouse'
            intersect = pd.read_excel(path, sheet_name="WB_MGI")
            org1 = 'Nematode (worm)'
            org2 = 'Mouse'
        if Num == "11":
            commonSp = 'Fruit fly and mouse'
            intersect = pd.read_excel(path, sheet_name="FB_MGI")
            org1 = 'Fruit fly'
            org2 = 'Mouse'

        uniOrg1 = []
        geneOrg1 = []
        for or1 in intersect['UniProt Org1']:
            uniProtNamesFromDBOrtoOr1 = DBgetCommonNamesAllOrto(mydb, or1)
            uniOrg1.append(uniProtNamesFromDBOrtoOr1[0][0])
            geneOrg1.append(uniProtNamesFromDBOrtoOr1[0][1])
        uniOrg2 = []
        geneOrg2 = []
        for or2 in intersect['UniProt Org2']:
            uniProtNamesFromDBOrtoOr2 = DBgetCommonNamesAllOrto(mydb, or2)
            uniOrg2.append(uniProtNamesFromDBOrtoOr2[0][0])
            geneOrg2.append(uniProtNamesFromDBOrtoOr2[0][1])

        dataTable = {'Uni org1': uniOrg1, 'Gene org1': geneOrg1,
                     'Uni org2': uniOrg2, 'Gene org2': geneOrg2,}
        df = pd.DataFrame(dataTable)
        df['UniProt Link1'] = df['Uni org1'].apply(
            lambda L1: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={L1}' target='_blank'>{L1}</a>")
        df['UniProt Link2'] = df['Uni org2'].apply(
            lambda L2: f"↘️ <a href='/search_results_final?lang_ID=1&UniProt={L2}' target='_blank'>{L2}</a>")

        return [
            dash_table.DataTable(export_columns='all',
                                 data=df.to_dict('records'),
                                 columns=[
                                     {'id': 'UniProt Link1', 'name': [f" {org1}", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org1', 'name': [f" {org1}", " Gene name"]},
                                     {'id': 'UniProt Link2', 'name': [f" {org2}", " UniProt ID"],
                                      'presentation': 'markdown'},
                                     {'id': 'Gene org2', 'name': [f" {org2}", " Gene name"]},
                                 ],
                                 markdown_options={"html": True},
                                 merge_duplicate_headers=True,
                                 style_as_list_view=False,
                                 page_size=20,
                                 style_cell={'font-family': 'sans-serif'},
                                 style_cell_conditional=[
                                     {'if': {'column_id': ['Gene org1', 'Gene org2']},
                                      'height': 'auto', 'width': 'auto',
                                      'textAlign': 'left', },
                                     {'if': {'column_id': ['UniProt Link1', 'UniProt Link2']},
                                      'height': 'auto', 'width': 'auto',
                                      'textAlign': 'left', },
                                 ],
                                 sort_action="native",
                                 filter_action="native",
                                 page_current=0,
                                 id='tbl-common-multi',
                                 tooltip_data=[{'UniProt Link1':
                                     {
                                         'value': 'Click here to search for the data on oxidation of chosen protein'.format(
                                             str(row['UniProt Link1'])),
                                         'type': 'markdown', }
                                 } for row in df.to_dict('records')],
                                 css=[{'selector': '.dash-table-tooltip',
                                       'rule': 'background-color: whitesmoke; font-family: Helvetica; color: black; '
                                               'text-align: center', },
                                      ],
                                 tooltip_delay=0,
                                 tooltip_duration=None, )
        ]