# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
from dash import callback, dash_table, dcc, html
from dbUtil import DBgetUNIProtNames, DBgetOrtologyProteinNames, \
    DBgetGeneAndProteinNamesAll
import mysql.connector
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import dash_mantine_components as dmc
from pathlib import Path
import configparser


dash.register_page(__name__,
                   path='/search_results_tab',
                   title='Search Results',
                   name='Search Results',
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

def layout(lang_ID=None, UniGene=None, organism_ID=None):

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

    areThereResults = False

    if UniGene != None and organism_ID != None:
        if organism_ID == '1' or organism_ID == '2' or organism_ID == '3' or organism_ID == '4':
            #Step 1: UniProts for search
            uniProtNamesFromDB = DBgetGeneAndProteinNamesAll(mydb, organism_ID, UniGene)

            uniProtNamesList = []
            idProtNamesList = []
            for uniProtName in uniProtNamesFromDB:
                uniProtNamesList.append(uniProtName[0])
                idProtNamesList.append(uniProtName[1])

            if len(uniProtNamesList) > 0:
                #Step 2: UniProts orthologs
                OrtologyUniProtNamesFromDB = DBgetUNIProtNames(mydb, uniProtNamesList)
                for uniProtName in OrtologyUniProtNamesFromDB:
                    uniProtNamesList.append(uniProtName[0])

                #Step 3: Results put into table
                proteinOrtologyNamesFromDB = DBgetOrtologyProteinNames(mydb, uniProtNamesList)

                orgNames = ''
                for org in proteinOrtologyNamesFromDB:
                    orgNames += f'{org[0]}, '

                if(len(orgNames)>0):
                    orgNames = orgNames[:len(orgNames) - 2]
                    areThereResults=True

                organismName = ''
                if organism_ID == '1':
                    organismName = 'Budding Yeast'
                if organism_ID == '2':
                    organismName = 'Worm'
                if organism_ID == '3':
                    organismName = 'Mouse'
                if organism_ID == '4':
                    organismName = 'Fruit fly'

    if areThereResults==True:
        df = pd.DataFrame(proteinOrtologyNamesFromDB)
        df.columns = ['Organism name', 'Latin name', 'Latin', 'Gene name', 'UniProt ID', 'Protein description',
                      'Protein length (aa)', 'Number of cysteine residues', 'All cysteine positions',
                      'All cysteine motifs', 'PDB ID', 'STRING ID', 'Organismal Database ID']
        df['UniProt ID Link'] = df['UniProt ID'].apply(lambda x:f"↘️ <a href='/search_results_final?lang_ID={lang_ID}&UniProt={x}' target='_blank'>{x}</a>")

    if lang_ID == None:
        lang_ID = 1
    if lang_ID != '1':
        lang_ID = 1

    if areThereResults==False:
        return html.Div([
            dbc.Alert("No result found", color="warning"),
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
                                       html.Span("Alliance of Genome Resources", style={"margin-left": "15px"})],
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
                        html.H1(
                            children=[html.Span('Results for Single Protein Search ', style={'color': '#3d3d3d'}), ], ),
                        html.H4(
                            children=[html.Span('Table contaning Your search and orthologs found in the Database ',
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
                                dcc.Link([html.Span('Single Protein Search')],
                                         href=f'/search_singleProt?lang_ID={lang_ID}'),
                                dcc.Link([html.Span('Single Protein Search')],
                                         href=f'/search_results_tab?lang_ID={lang_ID}&UniGene={UniGene}&organism_ID={organism_ID}'
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
                                dmc.StepperStep(label="Second step", description="Type the single protein"),
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
                            html.H4(children=[html.Span('Your search: ', style={'color': '#3d3d3d'}),
                                              html.Span(f'{organismName}, {UniGene}',
                                                        style={'color': '#FF5147', 'font-size': '0.9em'})], ),
                            html.Br(),
                            html.Br(),
                            dmc.Grid(children=[dmc.Col(
                                dash_table.DataTable(export_columns='all',
                                                     data=df.to_dict('records'),
                                                     columns=[
                                                         {'id': 'UniProt ID Link', 'name': [" UniProt ID"],
                                                          'presentation': 'markdown'},
                                                         {'id': 'Gene name', 'name': [' Gene Name']},
                                                         {'id': 'Organism name', 'name': [' Organism Name']},
                                                         {'id': 'Latin name', 'name': [' ']},
                                                     ],
                                                     markdown_options={"html": True},
                                                     merge_duplicate_headers=True,
                                                     style_as_list_view=True,
                                                     page_size=10,
                                                     style_cell={
                                                         'font-family': 'sans-serif'},
                                                     style_cell_conditional=[
                                                         {'if': {'column_id': ['Organism name']},
                                                          'height': 'auto', 'minWidth': '7px', 'width': '7px',
                                                          'maxWidth': '7px',
                                                          'textAlign': 'left', },
                                                         {'if': {'column_id': ['Latin name']},
                                                          'height': 'auto', 'minWidth': '7px', 'width': '7px',
                                                          'maxWidth': '7px',
                                                          'textAlign': 'left', "font-style": "italic", },
                                                         {'if': {'column_id': ['Gene name']},
                                                          'height': 'auto', 'minWidth': '6px', 'width': '6px',
                                                          'maxWidth': '6px',
                                                          'textAlign': 'left', },
                                                         {'if': {'column_id': ['UniProt ID Link']},
                                                          'height': 'auto', 'minWidth': '6px', 'width': '6px',
                                                          'maxWidth': '6px',
                                                          'textAlign': 'left', },
                                                     ],
                                                     sort_action="native",
                                                     page_current=0,
                                                     id='tbl',
                                                     tooltip_data=[{'UniProt ID Link':
                                                         {'value': 'Click here to search for the '
                                                                   'data on oxidation of chosen protein'.format(
                                                             str(row['UniProt ID Link'])),
                                                             'type': 'markdown', }
                                                     } for row in df.to_dict('records')],
                                                     css=[{'selector': '.dash-table-tooltip',
                                                           'rule': 'background-color: whitesmoke; '
                                                                   'font-family: Helvetica; color: black; text-align: center',
                                                           },
                                                          ],
                                                     tooltip_delay=0,
                                                     tooltip_duration=None,
                                                     ), span=12)]),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dbc.Button(children=[html.I(className="bi bi-download"),
                                                 html.Span("Download Table", style={"margin-left": "15px"})],
                                       color="info", className="d-flex align-items-center",
                                       id='btn-download'),
                            dcc.Download(id="download-component"),
                            dcc.Location(id='url', refresh=False),
                            dcc.Store(id='intermediate-value'),
                        ], xs=11, sm=11, md=11, lg=10, xl=10),

                        ]),
                    ]),
                ], xs=9, sm=9, md=9, lg=9, xl=9)
            ])
        ]),


@callback(
    Output('download-component', 'data'),
    Input('tbl', 'data'),
    Input('btn-download', 'n_clicks'),
    prevent_initial_call=True,
)
def update_search_button(data, n_clicks):
    dataFrame = pd.DataFrame(data)
    dataFrame2 = dataFrame.drop(columns='UniProt ID Link')
    return dcc.send_data_frame(dataFrame2.to_csv, "OxiAge_SingleProteinSearch_Table.txt", sep=';')
