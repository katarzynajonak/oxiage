# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
from dash import html, dcc, callback
from dbUtil import DBgetUNIProtNames, DBgetProteinInfo, DBgetAlignmentForUniProt, \
    DBgetDataForGraphsForUniProtmydb, DBgetGeneAndProteinNamesFinal
from dbUtil import DBgetGOComponentNames, DBgetGOFunctionNames, DBgetGOProcessNames
import mysql.connector
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from urllib.parse import urlparse, parse_qs
import dash_mantine_components as dmc
import biotite.sequence as seq
import biotite.sequence.align as align
from time import sleep
from pathlib import Path
import configparser
from dash import dash_table


dash.register_page(__name__,
                   path='/search_results_final',
                   title='Search Results Final',
                   name='Search Results Final',
                   location="error")

CONTENT_STYLE = {
    "padding": "2rem 1rem",
    "overflow": "scroll",
    'overflow-y': 'hidden'
}

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "padding": "2rem 1rem",
    "border-right": "2px solid whitesmoke"
}

TABS_STYLES = {'height': '50px'}

TAB_STYLE = {
    'width': '100%',
    'borderTop': '1px solid silver',
    'color': 'darkgrey',
    'padding': '20px 20px',
    'fontSize': 18,
    'font-family': 'system-ui',
    'align-items': 'center',
    'justify-content': 'center'
}

TAB_SELECTED_STYLE = {
    'width': '100%',
    'borderTop': '1px solid silver',
    'color': 'black',
    'padding': '20px 20px',
    'fontSize': 20,
    'font-family': 'system-ui',
    'align-items': 'center',
    'justify-content': 'center'
}

STYLE_GRID = {
    "textAlign": "left",
    'max-width': '310px',
    'overflow': 'hidden',
    'white-space': 'nowrap',
    'line-height': '1.65',
    'padding': '15px'
}

STYLE_GRID_2 = {
    "textAlign": "left",
    'max-width': '800px',
    'overflow': 'scroll',
    'white-space': 'nowrap',
    'overflow-y': 'hidden',
    'padding': '1rem',
}

STYLE_ACCORD = {
    'width': '90%'
}

TAB_STYLE_GRAPH = {
    'width': '60%',
    'backgroundColor': '#2D3033',
    'color': 'white',
    'padding': '20px 20px',
    'fontSize': 18,
    'font-family': 'system-ui',
    'align-items': 'center',
    'justify-content': 'center'
}



def layout(lang_ID=None, UniProt=None):

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

    pd.options.mode.chained_assignment = None  # default='warn'

    if UniProt != None:
        # Step 1: All orthologs
        uniProtNamesList = [UniProt]

        CheckProtNamesFromDB = DBgetGeneAndProteinNamesFinal(mydb, uniProtNamesList[0])

        if len(CheckProtNamesFromDB) > 0:
            areThereResults = True

            OrtologyUniProtNamesFromDB = DBgetUNIProtNames(mydb, uniProtNamesList)
            for uniProtName in OrtologyUniProtNamesFromDB:
                uniProtNamesList.append(uniProtName[0])

            #Step 2: all UniProt information
            proteinInfoFromDB = DBgetProteinInfo(mydb, uniProtNamesList)

            IDProteinList = []
            UniProtKBList = {}
            AlphaFoldList = {}
            RefPdbList = {}
            RefPdbSTRINGList = {}
            AOGRList = {}
            RefOrgDatabase = {}

            for prot in range(len(proteinInfoFromDB)):
                if proteinInfoFromDB[prot][1] == UniProt:
                    chosenUni = proteinInfoFromDB[prot][1]
                    chosenName = proteinInfoFromDB[prot][2]
                    chosenOrg = proteinInfoFromDB[prot][8]
                    chosenLatin = proteinInfoFromDB[prot][9]

            for IDProtein in proteinInfoFromDB:
                IDProteinList.append(IDProtein[0])
                if IDProtein[1]:
                    UniProtKBList[IDProtein[1]] = []
                    UniProtKBList[IDProtein[1]].append(f'https://www.uniprot.org/uniprotkb/{IDProtein[1]}')
                if IDProtein[1]:
                    AlphaFoldList[IDProtein[1]] = []
                    AlphaFoldList[IDProtein[1]].append(f'https://alphafold.ebi.ac.uk/entry/{IDProtein[1]}')
                if IDProtein[5]:
                    tmpString = str(IDProtein[5])
                    tmpString = tmpString[:len(tmpString) - 1]
                    tmpList = []
                    xyz = tmpString.split(",")
                    if IDProtein[5] == 'None':
                        tmpList.append(' ')
                    else:
                        for x in xyz:
                            tmpList.append(f'https://www.ebi.ac.uk/pdbe/entry/pdb/{x}')
                    RefPdbList[IDProtein[1]] = []
                    RefPdbList[IDProtein[1]].append(tmpList)
                if IDProtein[6]:
                    RefPdbSTRINGList[IDProtein[1]] = []
                    if IDProtein[8] == "Budding yeast":
                        RefPdbSTRINGList[IDProtein[1]].append(f'https://string-db.org/network/4932.{IDProtein[6]}')
                    if IDProtein[8] == "Nematode roundworm":
                        RefPdbSTRINGList[IDProtein[1]].append(f'https://string-db.org/network/6239.{IDProtein[6]}')
                    if IDProtein[8] == "Mouse":
                        RefPdbSTRINGList[IDProtein[1]].append(f'https://string-db.org/network/10090.ENSMUS{IDProtein[6]}')
                    if IDProtein[8] == "Fruit fly":
                        RefPdbSTRINGList[IDProtein[1]].append(f'https://string-db.org/network/{IDProtein[6]}')
                if IDProtein[7]:
                    AOGRList[IDProtein[1]] = []
                    AOGRList[IDProtein[1]].append(f'https://www.alliancegenome.org/gene/{IDProtein[7]}')
                    if IDProtein[8] == "Budding yeast":
                        RefOrgDatabase[IDProtein[1]] = []
                        orgY = IDProtein[7].split(':')
                        orgY = orgY[1]
                        RefOrgDatabase[IDProtein[1]].append(f'https://www.yeastgenome.org/locus/{orgY}')
                    if IDProtein[8] == "Nematode roundworm":
                        RefOrgDatabase[IDProtein[1]] = []
                        orgW = IDProtein[7].split(':')
                        orgW = orgW[1]
                        RefOrgDatabase[IDProtein[1]].append(f'https://www.wormbase.org/species/c_elegans/gene/{orgW}')
                    if IDProtein[8] == "Mouse":
                        RefOrgDatabase[IDProtein[1]] = []
                        RefOrgDatabase[IDProtein[1]].append(f'https://www.informatics.jax.org/marker/{IDProtein[7]}')
                    if IDProtein[8] == "Fruit fly":
                        RefOrgDatabase[IDProtein[1]] = []
                        RefOrgDatabase[IDProtein[1]].append(f'https://flybase.org/reports/{IDProtein[7]}')

            GOComponentInfoFromDB = DBgetGOComponentNames(mydb, IDProteinList)
            GOFunctionInfoFromDB = DBgetGOFunctionNames(mydb, IDProteinList)
            GOProcessInfoFromDB = DBgetGOProcessNames(mydb, IDProteinList)

            if(proteinInfoFromDB):
                areThereResults=True

            #Step 3: For each Uniprot, we get info for alignment
            alignmentAndCysteinInfoFromDB = DBgetAlignmentForUniProt(mydb, uniProtNamesList)

            #Step 4: For each Uniprot, we get info for drawing graphs
            dataForGraphsFromDB = DBgetDataForGraphsForUniProtmydb(mydb, uniProtNamesList)

    if areThereResults==True:
        df = pd.DataFrame(proteinInfoFromDB)
        df.columns = ['ID', 'UniProt', 'Gene', 'Protein', 'Information', 'RefPdb', 'RefString', 'OrgDatabase',
                      'Name', 'Latin', 'Short', 'Length', 'CysNo', 'CysPos', 'CysMotifs']
        dfOxi = pd.DataFrame(dataForGraphsFromDB)
        dfOxi.columns = ['Organism', 'Gene name', 'p_ID', 'CysID', 'c_ID', 'Cysteine positions', 'Cysteine order',
                         'Average Oxidation', 'SD Oxidation', 'Number of quantified replicates',
                         'Isoform quantified', 'sample_ID', 'Sample', 'experiment_ID', 'Experiment type',
                         'Strain', 'publication_ID', 'Author', 'Journal', 'Year', 'DOI', 'noForGraph_ID', 'Details',
                         'UniProt ID']

        for siz in range(len(dfOxi['Number of quantified replicates'])):
            if dfOxi['Number of quantified replicates'][siz] == '-':
                if dfOxi['Average Oxidation'][siz] == 'ni' or dfOxi['Average Oxidation'][siz] == 'ND':
                    dfOxi['Number of quantified replicates'][siz] = '0'
                else:
                    if dfOxi['SD Oxidation'][siz] == 'ni':
                        dfOxi['Number of quantified replicates'][siz] = '1'
                    else:
                        dfOxi['Number of quantified replicates'][siz] = '> 1'

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
                        html.H1(children=[html.Span('Results Page ', style={'color': '#3d3d3d'}), ], ),
                        html.Hr(),
                        html.Br(),
                        dmc.Stepper(
                            active=4,
                            color="green",
                            radius="lg",
                            size="sm",
                            children=[
                                dmc.StepperStep(label="First step", description="Choose the type of search"),
                                dmc.StepperStep(label="Second step",
                                                description="Type the proteins / annotations / ..."),
                                dmc.StepperStep(label="Third step",
                                                description="Choose the specific protein from result table"),
                                dmc.StepperStep(label="Fourth step", description="Enjoy the cross-species comparison!"),
                            ],
                        ),
                        html.Br(),
                        html.Br(),
                        html.H3(children=[html.Span(f'{chosenName} ({chosenUni})',
                                                    style={'color': '#FF5147'})]),
                        html.H5([html.Span(f'for {chosenOrg}'),
                                 html.Span(f' ({chosenLatin})', style={'font-style': 'italic'})]),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        ### Tabs setting
                        dmc.Container([
                            dcc.Tabs(id="tabs-with-classes", parent_className='custom-tabs',
                                     className='custom-tabs-container',
                                     children=[
                                         dcc.Tab(label='Alignment & Oxidation',
                                                 children=getTab2(mydb, lang_ID, alignmentAndCysteinInfoFromDB,
                                                                  dataForGraphsFromDB, dfOxi, df),
                                                 style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),

                                         dcc.Tab(label='Results Table',
                                                 children=getTab4(mydb, lang_ID, dfOxi),
                                                 style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),

                                         dcc.Tab(label='Information on Proteins',
                                                 children=getTab1(proteinInfoFromDB, AlphaFoldList,
                                                                  GOComponentInfoFromDB, GOFunctionInfoFromDB,
                                                                  GOProcessInfoFromDB,
                                                                  ),
                                                 style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),

                                         dcc.Tab(label='External Resources',
                                                 children=getTab3(proteinInfoFromDB, UniProtKBList, AlphaFoldList,
                                                                  RefPdbList,
                                                                  RefPdbSTRINGList, AOGRList, RefOrgDatabase),
                                                 style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                                     ])
                        ], fluid=True, style={"marginTop": 10, "marginBottom": 10, 'width': '100%'}),
                        # 'background-color':'#2D3033'

                        dcc.Location(id='url', refresh=False),
                        dcc.Interval(id='interval-component', interval=1 * 1000, n_intervals=0, max_intervals=1),
                        html.Br(),
                        html.Br(),
                    ]),
                ], xs=9, sm=9, md=9, lg=9, xl=9)
            ])
        ])

### Information
def getTab1(proteinInfoFromDB, AlphaFoldList, GOComponentInfoFromDB, GOFunctionInfoFromDB, GOProcessInfoFromDB):
    return [getProteinAccordionTab1(proteinInfoFromDB, AlphaFoldList, GOComponentInfoFromDB, GOFunctionInfoFromDB, GOProcessInfoFromDB)]

### Results Table
def getTab4(mydb, lang_ID, dfOxi):
    return[html.Br(),html.Br(),
           html.P('Table contains results of % oxidation for all data presented in section "Alignment & Oxidation"'),
           html.P('Download or filter the table displayed below', style={'font-size': '0.8em'}),
           html.P('You can sort the table by alphabetical order (names) or by order of increse or decrese in oxidation, ',
                  style={'font-size': '0.8em'}),
           html.Br(),
           dbc.Button(children=[html.I(className="bi bi-download"),
                                html.Span("Download Results Table", style={"margin-left": "15px"})],
                      color="info", className="d-flex align-items-center",
                      id='btn-download-oxi'),
           dcc.Download(id="download-component-oxi"),html.Br(),html.Br(),
    dmc.Grid(children=[dmc.Col(
        dash_table.DataTable(export_columns='all',
                             data=dfOxi.to_dict('records'),
                             columns=[
                                 {'id': 'Organism', 'name': 'Organism',
                                  'presentation': 'markdown'},
                                 {'id': 'Strain', 'name': 'Strain'},
                                 {'id': 'Details', 'name': 'Tissue'},
                                 {'id': 'Gene name', 'name': 'Gene name'},
                                 {'id': 'CysID', 'name': 'CysID'},
                                 {'id': 'Sample', 'name': 'Sample'},
                                 {'id': 'Average Oxidation', 'name': 'Average % Oxidation'},
                                 {'id': 'SD Oxidation', 'name': 'SD'},
                             ],
                             markdown_options={"html": True},
                             merge_duplicate_headers=True,
                             style_as_list_view=False,
                             page_size=20,
                             style_cell={
                                 'padding': '5px',
                                 'font-family': 'sans-serif'},
                             style_cell_conditional=[
                                 {'if': {'column_id': ['Organism']},
                                  "font-style": "italic", },
                                 {'if': {'column_id': ['Organism']},
                                  "font-style": "italic", },
                             ],
                             style_data_conditional=[
                                 {'if': {'filter_query': '{Average Oxidation} = ni',
                                         'column_id': 'Average Oxidation'},
                                  'color': 'tomato'
                                  },
                                 {'if': {'filter_query': '{Average Oxidation} = ND',
                                         'column_id': 'Average Oxidation'},
                                  'color': 'tomato'
                                  },
                                 {'if': {'filter_query': '{SD Oxidation} = ni',
                                         'column_id': 'SD Oxidation'},
                                  'color': 'tomato'
                                  }
                             ],
                             sort_action="native",
                             filter_action="native",
                             filter_options={'case': 'insensitive'},
                             page_current=0,
                             id='tbl-oxi',
                             ), span=10)]),]

### External links
def getTab3(proteinInfoFromDB, UniProtKBList, AlphaFoldList, RefPdbList, RefPdbSTRINGList, AOGRList, RefOrgDatabase):
    tab3Res = [
        getProteinAccordionTab3(proteinInfoFromDB, UniProtKBList, AlphaFoldList, RefPdbList, RefPdbSTRINGList, AOGRList, RefOrgDatabase),
        html.Br()
    ]
    return tab3Res

### Alignment and Oxidation
def getTab2(mydb, lang_ID, alignmentAndCysteinInfoFromDB, dataForGraphsFromDB, dfOxi, df):
    ###### OXIDATION GRAPHS
    uniqueIdExperiment = {}
    for x in dataForGraphsFromDB:
        if not uniqueIdExperiment.get(x[13]):
            uniqueIdExperiment[x[13]] = x[13]
    dataYForExperimentID = {}
    dataXForExperimentID = {}
    for exp in uniqueIdExperiment:
        dataYForExperimentID[exp] = {}
        dataYForChartsByProteinIDandCID = {}
        dataXForExperimentID[exp] = {}
        dataXForChartsByProteinIDandCID = {}
        for x in dataForGraphsFromDB:
            if x[13]==exp:

                if not dataYForChartsByProteinIDandCID.get(x[2]):
                    dataYForChartsByProteinIDandCID[x[2]] = {}
                    # dataYForChartsByProteinIDandCID[x[2]]['Gene'] = x[1]
                if not dataYForChartsByProteinIDandCID[x[2]].get(x[4]):
                    dataYForChartsByProteinIDandCID[x[2]][x[4]] = {}
                    dataYForChartsByProteinIDandCID[x[2]][x[4]]['CysId'] = x[5]
                    # dataYForChartsByProteinIDandCID[x[2]][x[4]]['Gene'] = x[1]
                    dataYForChartsByProteinIDandCID[x[2]][x[4]]['Data'] = []

                if not dataXForChartsByProteinIDandCID.get(x[2]):
                    dataXForChartsByProteinIDandCID[x[2]] = {}
                    # dataXForChartsByProteinIDandCID[x[2]]['Gene'] = x[1]
                if not dataXForChartsByProteinIDandCID[x[2]].get(x[4]):
                    dataXForChartsByProteinIDandCID[x[2]][x[4]] = {}
                    dataXForChartsByProteinIDandCID[x[2]][x[4]]['CysId'] = x[5]
                    # dataXForChartsByProteinIDandCID[x[2]][x[4]]['Gene'] = x[1]
                    dataXForChartsByProteinIDandCID[x[2]][x[4]]['Data'] = []

                if x[7] == 'ni' or x[7] == 'ND':
                    listing = -1
                else:
                    listing = float(x[7])
                dataYForChartsByProteinIDandCID[x[2]][x[4]]['Data'].append(listing)
                dataXForChartsByProteinIDandCID[x[2]][x[4]]['Data'].append(x[12])
        dataYForExperimentID[exp] = dataYForChartsByProteinIDandCID
        dataXForExperimentID[exp] = dataXForChartsByProteinIDandCID

    ################# Prepare the graphs

    # allows to manipulate the order of the graphs shown
    appendChildren = []
    dataYForExperimentIDsorted = []
    dataYForExperimentIDsortedreturn = []
    for sorting in dataYForExperimentID:
        if sorting > 4 and sorting < 15:
            sorting = sorting + 30
        else:
            sorting = sorting
        dataYForExperimentIDsorted.append(sorting)
    dataYForExperimentIDsorted = sorted(dataYForExperimentIDsorted)
    for sorting_return in dataYForExperimentIDsorted:
        if sorting_return > 34 and sorting_return < 45:
            sorting_return = sorting_return - 30
        else:
            sorting_return = sorting_return
        dataYForExperimentIDsortedreturn.append(sorting_return)

    for id_experiment in dataYForExperimentIDsortedreturn: #sorted
    # for id_experiment in dataYForExperimentID: # not sorted
        for id_protein in dataYForExperimentID[id_experiment]:
            # Each new protein
            wartosciXY = []
            for id_cys in dataYForExperimentID[id_experiment][id_protein]:

                wartosciXY.append({'x': dataXForExperimentID[id_experiment][id_protein][id_cys]['Data'],
                                    'y': dataYForExperimentID[id_experiment][id_protein][id_cys]['Data'],
                                    'name': f'Cys: {dataYForExperimentID[id_experiment][id_protein][id_cys]["CysId"]}'
                                    })

            for x in dataForGraphsFromDB:
                if id_experiment == x[13]:
                    if id_protein == x[2]:
                        protein_name = x[1]
                        org_name = x[0]
                        isoform = x[10]
                        experiment = x[14]
                        strain_name = x[15]
                        public_name = x[17]
                        publication = x[18]
                        year = x[19]
                        doi = x[20]
                        tissue_name = x[22]
                        uniprot_name = x[23]

            if id_experiment < 5 or id_experiment == 15:
                forDataFrame = []
                for ind in range(len(dfOxi['experiment_ID'])):
                    if id_experiment == dfOxi['experiment_ID'][ind]:
                        if id_protein == dfOxi['p_ID'][ind]:
                            fod = {'Gene': dfOxi['Gene name'][ind],'CysID': dfOxi['CysID'][ind],
                                'Sample': dfOxi['Sample'][ind],
                                'Average % Oxidation': dfOxi['Average Oxidation'][ind], 'SD': dfOxi['SD Oxidation'][ind],
                                'Replicates': dfOxi['Number of quantified replicates'][ind],
                                'Isoform': dfOxi['Isoform quantified'][ind]}
                            forDataFrame.append(fod)
                fr = pd.DataFrame(forDataFrame)

                appendChildren.append(
                    dmc.Container([
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(responsive=True, figure={
                                'data': wartosciXY,
                                'layout': {
                                    'title': {'text':f'<i>{org_name}</i> {strain_name} <br><br> <b>{protein_name}</b> ({uniprot_name})'},
                                    'yaxis': {'title': '% oxidation', 'showgrid':False, 'linecolor':'#BCCCDC'},
                                    'xaxis': {'showgrid':False, 'linecolor':'#BCCCDC'}, #'gridcolor': 'grey'
                                    'showlegend': True,
                                    'paper_bgcolor':'rgba(0,0,0,0)', #2D3033',
                                    'plot_bgcolor':'rgba(0,0,0,0)',
                                    'font': {'color': 'dimgray'},
                                    # 'font': {'color': 'white'},
                                    'legend':{'tracegroupgap': 0},
                                    "height": 400,
                                    "width": 'auto', 'autotypenumbers':'convert'},
                                }),
                            ]),
                            dbc.Col([
                                dbc.Alert([
                                    html.P(f'Protein name {protein_name} ({uniprot_name})'),
                                    html.P([html.I(f'{org_name}'), f', strain {strain_name}']),
                                    html.P(f'Isoform detected: {isoform}', style={'font-size': '0.8em'}),
                                    html.P(f'Experiment: {experiment}', style={'font-size': '0.8em'}),
                                    html.P([f'from {public_name}', html.I(' et al. '), f'({year}), {publication}'], style={'font-size': '0.8em'}),
                                    html.P([f'See the publication at: ', html.A(f'{doi}', href=doi, target='_blank')], style={'font-size': '0.8em'})
                                ], color='secondary'),
                                html.Br(),
                                dbc.Alert(html.P('Not that -1 on the graph indicates non-valid value '
                                                 '(not quantified (ni) or not detected (ND). Details are found in the '
                                                 'table below'), color="danger", style={'font-size': '0.7em'}),
                            ], width={'size':4})
                        ]),
                        dbc.Row([dbc.Col([
                            dash_table.DataTable(export_columns='all',
                                                 data=fr.to_dict('records'),
                                                 style_as_list_view=False,
                                                 page_size=10,
                                                 style_cell={
                                                     'padding': '5px',
                                                     'font-family': 'sans-serif'},
                                                 style_data_conditional=[
                                                     {'if': {'filter_query': '{Average % Oxidation} = ni',
                                                             'column_id': 'Average % Oxidation'},
                                                      'color': 'tomato'
                                                      },
                                                     {'if': {'filter_query': '{Average % Oxidation} = ND',
                                                             'column_id': 'Average % Oxidation'},
                                                      'color': 'tomato'
                                                      },
                                                     {'if': {'filter_query': '{SD} = ni',
                                                             'column_id': 'SD'},
                                                      'color': 'tomato'
                                                      },
                                                     {'if': {'filter_query': '{Replicates} < 2',
                                                             'column_id': 'Replicates'},
                                                      'color': 'red'
                                                      }
                                                 ],
                                                 sort_action="native",
                                                 page_current=0,
                                                 export_format='xlsx',
                                                 export_headers='display',
                                                 id='tbl-oxi-1',),], width={'size':12}
                        )])
                    ], style={'border':'1px solid silver', 'height':440, "marginTop": 50,
                                   'overflow':'scroll', 'overflow-x': 'hidden', },),)

            if id_experiment == 5:
                forDataFrame = []
                for ind in range(len(dfOxi['experiment_ID'])):
                    if id_experiment == dfOxi['experiment_ID'][ind]:
                        if id_protein == dfOxi['p_ID'][ind]:
                            fod = {'Gene': dfOxi['Gene name'][ind], 'CysID': dfOxi['CysID'][ind],
                                   'Sample': dfOxi['Sample'][ind],
                                   'Average % Oxidation': dfOxi['Average Oxidation'][ind],
                                   'SD': dfOxi['SD Oxidation'][ind],
                                   'Replicates': dfOxi['Number of quantified replicates'][ind],
                                   'Isoform': dfOxi['Isoform quantified'][ind]}
                            forDataFrame.append(fod)
                fr = pd.DataFrame(forDataFrame)

                appendChildren.append(
                    dmc.Container([
                        dbc.Row([
                            dbc.Col(
                                dcc.Graph(responsive=True, figure={
                                'data': wartosciXY,
                                'layout': {
                                    'title': {'text':f'<i>{org_name}</i> {strain_name}, {tissue_name} <br><br> <b>{protein_name}</b> ({uniprot_name})'},
                                    'yaxis': {'title': '% oxidation', 'showgrid':False, 'linecolor':'#BCCCDC'},
                                    'xaxis': {'showgrid':False, 'linecolor':'#BCCCDC'}, #'gridcolor': 'grey'
                                    'showlegend': True,
                                    'paper_bgcolor':'rgba(0,0,0,0)', #2D3033',
                                    'plot_bgcolor':'rgba(0,0,0,0)',
                                    'font': {'color': 'dimgray'},
                                    'legend':{'tracegroupgap': 0},
                                    "height": 400,
                                    "width": 'auto','autotypenumbers':'convert'},
                                }),
                            ),
                            dbc.Col([
                                dbc.Alert([
                                    html.P(f'Protein name {protein_name} ({uniprot_name})'),
                                    html.P([html.I(f'{org_name}'), f', strain {strain_name}, tissue {tissue_name}']),
                                    html.P(f'Isoform detected: {isoform}', style={'font-size': '0.8em'}),
                                    html.P(f'Experiment: {experiment}', style={'font-size': '0.8em'}),
                                    html.P([f'from {public_name}', html.I(' et al. '), f'({year}), {publication}'],
                                           style={'font-size': '0.8em'}),
                                    html.P([f'See the publication at: ', html.A(f'{doi}', href=doi, target='_blank')],
                                           style={'font-size': '0.8em'})
                                ], color='secondary'),
                                html.Br(),
                                dbc.Alert(html.P('Not that -1 on the graph indicates non-valid value '
                                                 '(not quantified (ni) or not detected (ND). Details are found in the '
                                                 'table below'), color="danger", style={'font-size': '0.7em'}),
                            ], width={'size': 4}),
                        ]),
                        dbc.Row([dbc.Col([
                            dash_table.DataTable(export_columns='all',
                                                 data=fr.to_dict('records'),
                                                 style_as_list_view=False,
                                                 page_size=10,
                                                 style_cell={
                                                     'padding': '5px',
                                                     'font-family': 'sans-serif'},
                                                 style_data_conditional=[
                                                     {'if': {'filter_query': '{Average % Oxidation} = ni',
                                                             'column_id': 'Average % Oxidation'},
                                                      'color': 'tomato'
                                                      },
                                                     {'if': {'filter_query': '{Average % Oxidation} = ND',
                                                             'column_id': 'Average % Oxidation'},
                                                      'color': 'tomato'
                                                      },
                                                     {'if': {'filter_query': '{SD} = ni',
                                                             'column_id': 'SD'},
                                                      'color': 'tomato'
                                                      },
                                                     {'if': {'filter_query': '{Replicates} < 2',
                                                             'column_id': 'Replicates'},
                                                      'color': 'red'
                                                      }
                                                 ],
                                                 sort_action="native",
                                                 page_current=0,
                                                 export_format='xlsx',
                                                 export_headers='display',
                                                 id='tbl-oxi-2', ), ], width={'size': 12}
                        )])
                    ], style={'border': '1px solid silver', 'height': 440, "marginTop": 50,
                              'overflow': 'scroll', 'overflow-x': 'hidden'}, ), )
                appendChildren.append(html.Br())
                appendChildren.append(
                    dbc.Alert(html.P('Click the buttons with tissue names on the bottom of the page '
                                     ' to see the results for other mice tissues '), color="info",
                              style={'font-size': '0.8em', 'width':'70%'}),)
                appendChildren.append(html.Br())

            if id_experiment > 5 and id_experiment < 15:
                forDataFrame = []
                for ind in range(len(dfOxi['experiment_ID'])):
                    if id_experiment == dfOxi['experiment_ID'][ind]:
                        if id_protein == dfOxi['p_ID'][ind]:
                            fod = {'Gene': dfOxi['Gene name'][ind], 'CysID': dfOxi['CysID'][ind],
                                   'Sample': dfOxi['Sample'][ind],
                                   'Average % Oxidation': dfOxi['Average Oxidation'][ind],
                                   'SD': dfOxi['SD Oxidation'][ind],
                                   'Replicates': dfOxi['Number of quantified replicates'][ind],
                                   'Isoform': dfOxi['Isoform quantified'][ind]}
                            forDataFrame.append(fod)
                fr = pd.DataFrame(forDataFrame)

                appendChildren.append(dbc.Alert([
                        dmc.Tabs([
                            dmc.TabsList([
                                dmc.Tab(f'{tissue_name} for {protein_name} ({uniprot_name})', value='graph', style={'color':'black'})
                            ]),
                            dmc.TabsPanel([dmc.Container([dbc.Row([dbc.Col([
                                html.Br(),
                                dcc.Graph(figure={
                                    'data': wartosciXY,
                                    'layout': {
                                        'title': {
                                            'text': f'<i>{org_name}</i> {strain_name}, {tissue_name} <br> <b>{protein_name}</b> {uniprot_name}'},
                                        'yaxis': {'title': '% oxidation', 'showgrid': False, 'linecolor': '#BCCCDC'},
                                        'xaxis': {'showgrid': False, 'linecolor': '#BCCCDC'},  # 'gridcolor': 'grey'
                                        'showlegend': True,
                                        'paper_bgcolor': 'white',  # 2D3033',
                                        'plot_bgcolor': 'white',
                                        'font': {'color': 'black'},
                                        'legend': {'tracegroupgap': 0},
                                        "height": 400,
                                        "width": 600, 'autotypenumbers': 'convert'
                                    },
                                })

                            ]),
                                dbc.Col([
                                    dash_table.DataTable(export_columns='all',
                                                         data=fr.to_dict('records'),
                                                         style_as_list_view=False,
                                                         page_size=10,
                                                         style_cell={
                                                             'padding': '5px',
                                                             'font-family': 'sans-serif'},
                                                         style_data_conditional=[
                                                             {'if': {'filter_query': '{Average % Oxidation} = ni',
                                                                     'column_id': 'Average % Oxidation'},
                                                              'color': 'tomato'
                                                              },
                                                             {'if': {'filter_query': '{Average % Oxidation} = ND',
                                                                     'column_id': 'Average % Oxidation'},
                                                              'color': 'tomato'
                                                              },
                                                             {'if': {'filter_query': '{SD} = ni',
                                                                     'column_id': 'SD'},
                                                              'color': 'tomato'
                                                              },
                                                             {'if': {'filter_query': '{Replicates} < 2',
                                                                     'column_id': 'Replicates'},
                                                              'color': 'red'
                                                              }
                                                         ],
                                                         sort_action="native",
                                                         page_current=0,
                                                         export_format='xlsx',
                                                         export_headers='display',
                                                         id='tbl-oxi-3', ), ], width={'size': 4}
                                )
                            ]),
                                dbc.Row([dbc.Col([
                                    html.Br(),
                                    dbc.Alert(html.P('Not that -1 on the graph indicates non-valid value '
                                                     '(not quantified (ni) or not detected (ND). Details are found in the '
                                                     'table below'), color="danger", style={'font-size': '0.7em'}),
                                ])])
                            ], style={"width":{'size':4}, "overflow": "scroll",'overflow-y': 'hidden'})], value='graph')
                        ], orientation='horizontal', allowTabDeactivation=True, variant='pills', color='blue')
               ], color="info"), ) ###here is the last


    if df['Length'].max() > 3000:
        return [
            html.Br(), html.Br(), html.Br(),
            html.Div([dmc.LoadingOverlay
                      (dmc.Grid(id='gridAlignment',
                                children=[(html.P('Loading alignment ... This protein is big, please open only one at a time ...',
                                                  style={'margin-left': 'auto', 'margin-right': 'auto',
                                                         'margin-top': '15px', 'color': '#0096FF', 'height': '90px'}))],
                                gutter="lg"),
                       exitTransitionDuration=1000, overlayColor='grey', overlayOpacity=0,
                       loaderProps={'variant': 'dots'}
                       ),

                      html.Br(), html.Hr(), html.Br(),

                      dmc.Grid([html.P([html.P('Oxidation Graphs'),
                                        html.P(
                                            'See the graphs of % oxidation in aging organisms for Your chosen protein'
                                            ' and the orthologs', style={'font-size': '0.8em'}),
                                        html.P('Graphs for ten different mice tissues are displayed at '
                                               'the bottom of the page upon clicking the appropriate buttons with tissue '
                                               'name', style={'font-size': '0.8em'}),
                                        ])], ),
                      dmc.Grid(children=[
                          dmc.Col(html.Div(appendChildren), span='auto'), ], gutter="xl"),
                      ])
        ]
    else:
        return [
        html.Br(),html.Br(),html.Br(),
        html.Div([dmc.LoadingOverlay
                  (dmc.Grid(id='gridAlignment',
                            children=[(html.P('Loading alignment ...',
                                              style={'margin-left': 'auto','margin-right': 'auto',
                                                     'margin-top':'15px', 'color': '#0096FF', 'height':'90px'}))],
                            gutter="lg"),
                   exitTransitionDuration=1000, overlayColor='grey', overlayOpacity=0,
                   loaderProps={'variant':'dots'}
                   ),

                  html.Br(),html.Hr(), html.Br(),

                  dmc.Grid([html.P([html.P('Oxidation Graphs'),
                                    html.P('See the graphs of % oxidation in aging organisms for Your chosen protein'
                                           ' and the orthologs', style={'font-size': '0.8em'}),
                                    html.P('Graphs for ten different mice tissues are displayed at '
                                           'the bottom of the page upon clicking the appropriate buttons with tissue '
                                           'name', style={'font-size': '0.8em'}),
                                    ])],),
                  dmc.Grid(children=[
                      dmc.Col(html.Div(appendChildren), span='auto'),], gutter="xl"),
                  ])
        ]


def getProteinAccordionTab1(proteinInfoFromDB, AlphaFoldList, GOComponentInfoFromDB, GOFunctionInfoFromDB, GOProcessInfoFromDB):
    accordionItemsList = []

    for IDProtein in proteinInfoFromDB:

        comp=[]
        for x in GOComponentInfoFromDB:
            if x[0] == IDProtein[1]:
                comp.append(f'{x[1]} ({x[2]})')
        comp = ", ".join(comp)

        func=[]
        for y in GOFunctionInfoFromDB:
            if y[0] == IDProtein[1]:
                func.append(f'{y[1]} ({y[2]})')
        func = ", ".join(func)

        proc=[]
        for z in GOProcessInfoFromDB:
            if z[0] == IDProtein[1]:
                proc.append(f'{z[1]} ({z[2]})')
        proc = ", ".join(proc)

        tmpChildren = []

        tmpChildren.append(html.H5(f'{IDProtein[2]} (UniProt: {IDProtein[1]})'))
        tmpChildren.append(html.H6(f'{IDProtein[3]}'))
        tmpChildren.append(html.Br())
        tmpChildren.append(dbc.Toast(html.P(f'{IDProtein[8]} ({IDProtein[9]})'),
                                     header="Organism", style={"width": 'auto'}))
        tmpChildren.append(html.Br())
        tmpChildren.append(dbc.Toast([html.P(f'Predicted structure from AlphaFold available at: '),
                                      dcc.Link(f'{AlphaFoldList[IDProtein[1]][0]}',
                                               href=f'{AlphaFoldList[IDProtein[1]][0]}', target='_blank')],
                                     header="Protein structure", style={"width": 'auto'}))
        tmpChildren.append(html.Br())
        tmpChildren.append(dbc.Toast(html.P(f'{IDProtein[11]}'),
                                     header="Protein length (amino acid)", style={"width": 'auto'}))
        tmpChildren.append(html.Br())
        tmpChildren.append(dbc.Toast(html.P(f'{IDProtein[12]}'),
                                     header="Number of all cysteine residues", style={"width": 'auto'}))
        tmpChildren.append(html.Br())

        dataTableMotifs = {'Cysteine Position': list(IDProtein[13].split(', ')),
                           'Motif +/- 6 AA around the cysteine': list(IDProtein[14].split(', '))}
        dfMotifs = pd.DataFrame(dataTableMotifs)

        tmpChildren.append(dbc.Toast([
            html.P(['Custom analysis: please cite ', html.A('Jonak et al., 2023', target='_blank',
                                                           href='https://http://topf-lab.org/')], style={'font-size': '0.9em'}),

            dash_table.DataTable(export_columns='all',
                                 data=dfMotifs.to_dict('records'),
                                 style_as_list_view=True,
                                 page_size=15,
                                 style_cell_conditional=[
                                     {'if': {'column_id': ['Cysteine Position']},
                                      'height': 'auto', 'width':'content',
                                      'textAlign': 'left', },
                                     {'if': {'column_id': ['Motif +/- 6 AA around the cysteine']},
                                      'height': 'auto', 'width': 'content',
                                      'textAlign': 'left', },
                                 ],
                                 export_format='xlsx',
                                 export_headers='display',
                                 )
        ],
                                     header="List of amino acid sequence surrounding all cysteine residues "
                                            "(+/-6 amino acids)", style={"width": 'auto'}))

        tmpChildren.append(html.Br())
        tmpChildren.append(dbc.Toast(html.P([html.P(f'Localized in: {comp}'),
                                             html.P(f'Involved in: {proc}'),
                                             html.P(f'Enables: {func}')]),
                                     header="Gene Ontology annotation", style={"width": 'auto'}))

        tmpChildren.append(html.Br())
        tmpChildren.append(dbc.Toast(html.P(f'{IDProtein[4]}'),
                                     header="Protein function (from UniProtKB)", style={"width": 'auto'}))

        accordionItemsList.append(dbc.AccordionItem(
                    children=tmpChildren,
                    title=[IDProtein[8], ', ', IDProtein[2], ' (', IDProtein[1], ')'],
        ))


    return dbc.Accordion(
        accordionItemsList,
        id="accordion-always-open",
        always_open=True,
        style=STYLE_ACCORD
    )



def getProteinAccordionTab3(proteinInfoFromDB, UniProtKBList, AlphaFoldList, RefPdbList, RefPdbSTRINGList, AOGRList, RefOrgDatabase):
    accordionItemsList = []

    for IDProtein in proteinInfoFromDB:

        tmpChildren = []
        tmpChildren.append(html.P('Protein information (UniProtKB):'))
        tmpChildren.append(dcc.Link(f'{UniProtKBList[IDProtein[1]][0]}', href=f'{UniProtKBList[IDProtein[1]][0]}', target='_blank'))
        tmpChildren.append(html.Br())
        tmpChildren.append(html.Br())

        tmpChildren.append(html.P('Gene and protein information:'))
        tmpChildren.append(dcc.Link(f'{RefOrgDatabase[IDProtein[1]][0]}', href=f'{RefOrgDatabase[IDProtein[1]][0]}', target='_blank'))
        tmpChildren.append(html.Br())
        tmpChildren.append(html.Br())

        tmpChildren.append(html.P('Orthologies in other species (Alliance of Genome Resources):'))
        tmpChildren.append(dcc.Link(f'{AOGRList[IDProtein[1]][0]}', href=f'{AOGRList[IDProtein[1]][0]}', target='_blank'))
        tmpChildren.append(html.Br())
        tmpChildren.append(html.Br())

        tmpChildren.append(html.P('Predicted 3D protein structure (Alpha Fold):'))
        tmpChildren.append(dcc.Link(f'{AlphaFoldList[IDProtein[1]][0]}', href=f'{AlphaFoldList[IDProtein[1]][0]}', target='_blank'))
        tmpChildren.append(html.Br())
        tmpChildren.append(html.Br())

        tmpChildren.append(html.P('Interaction network (STRING):'))
        tmpChildren.append(dcc.Link(f'{RefPdbSTRINGList[IDProtein[1]][0]}', href=f'{RefPdbSTRINGList[IDProtein[1]][0]}', target='_blank'))
        tmpChildren.append(html.Br())
        tmpChildren.append(html.Br())

        tmpChildren.append(html.P('Solved 3D protein structure (PDB):'))
        if RefPdbList.get(IDProtein[1]):
            for x in RefPdbList[IDProtein[1]][0]:
                x=x.replace(" ", "")
                tmpChildren.append(dcc.Link(x, href=x, target='_blank'))
                tmpChildren.append(html.Br())
        else:
            tmpChildren.append(html.P("Record not found"))
        tmpChildren.append(html.Br())
        accordionItemsList.append(dbc.AccordionItem(children=[
            dmc.Spoiler(tmpChildren, showLabel="Show more", hideLabel="Hide", maxHeight=350),
            ],
            title=[IDProtein[8], ', ', IDProtein[2], ' (', IDProtein[1], ')']
        ))

    return dbc.Accordion(
        accordionItemsList,
        id="accordion-always-open",
        always_open=True,
        style=STYLE_ACCORD
    )


@callback(
    Output('gridAlignment', 'children'),
    Input('interval-component', 'n_intervals'),
    Input('url', 'href'),
    prevent_initial_call=True,
)
def update_alignment_button(n_intervals, href):

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
    UniProt = ''
    uni = getParams.get('UniProt')
    if not uni:
        UniProt = ''
    else:
        UniProt = uni[0]

    uniProtNamesList = [UniProt]
    OrtologyUniProtNamesFromDB = DBgetUNIProtNames(mydb, uniProtNamesList)
    for uniProtName in OrtologyUniProtNamesFromDB:
        uniProtNamesList.append(uniProtName[0])

    alignmentAndCysteinInfoFromDB = DBgetAlignmentForUniProt(mydb, uniProtNamesList)

    alignmentChildren = []
    alignmentChildren2 = []
    CysOrderForProteinID = {}

    for x in alignmentAndCysteinInfoFromDB:
        if (x[6]):
            if not CysOrderForProteinID.get(x[3]):
                CysOrderForProteinID[x[3]] = {}
            splitPositions = x[6].split(", ")
            for sP in splitPositions:
                CysOrderForProteinID[x[3]][sP] = f'Cys {x[5]}'

    sequenUn=[]
    for x2 in alignmentAndCysteinInfoFromDB:
        sequenUn.append(x2[7])

    sequen = pd.unique(sequenUn)

    sequences=[]
    for seq_str in sequen:
        sequencingNam = seq.ProteinSequence(seq_str)
        sequences.append(sequencingNam)

    readyAlign = []
    if len(sequences) == 1:
        readyAlign.append(sequences[0])

    if len(sequences) == 2:
        matrix = align.SubstitutionMatrix.std_protein_matrix()
        alignment = align.align_optimal(sequences[0], sequences[1], matrix, gap_penalty=(-10,-1), terminal_penalty=True)
        xstr = str(alignment[0])
        w = xstr.replace("\n\n", "\n").split("\n")
        sleep(1)
        indexes = int(len(w) / len(sequences))

        allnewSeq = []
        for pr in range(len(sequences)):
            novel = []
            for inxx in range(indexes):
                newSeq = ''.join(w[pr + len(sequences) * inxx])
                novel.append(newSeq)
            allnewSeq.append(novel)

        for nov in range(len(allnewSeq)):
            neews = ''.join(allnewSeq[nov])
            readyAlign.append(neews)

    if len(sequences) > 2:
        matrix = align.SubstitutionMatrix.std_protein_matrix()
        alignment = align.align_multiple(sequences, matrix, gap_penalty=(-10, -1),
                                        terminal_penalty=True)
        xstr = str(alignment[0])
        w = xstr.replace("\n\n", "\n").split("\n")
        sleep(1)
        indexes = int(len(w) / len(sequences))
        allnewSeq = []
        for pr in range(len(sequences)):
            novel = []
            for inxx in range(indexes):
                newSeq = ''.join(w[pr + len(sequences) * inxx])
                novel.append(newSeq)
            allnewSeq.append(novel)

        for nov in range(len(allnewSeq)):
            neews = ''.join(allnewSeq[nov])
            readyAlign.append(neews)

    ########################### Showing the alignment
    uniqes=[]
    uniqes0=[]
    uniqes1 = []
    uniqes3 = []
    uniqes7 = []
    uniqes8 = []
    for x3 in alignmentAndCysteinInfoFromDB:
        uniqes.append(x3)
        # print(x3)
        uniqes0.append(x3[0]) #latin
        uniqes1.append(x3[1]) #gene
        uniqes3.append(x3[3]) #id
        uniqes7.append(x3[7])  # uniprot
        uniqes8.append(x3[8]) #uniprot
    tech = {"Org":uniqes0, "Gene": uniqes1, 'ID': uniqes3, 'UniProt': uniqes8, 'Seq': uniqes7}
    df1 = pd.DataFrame(tech)
    dfUniq = df1.drop_duplicates(subset=("Org", "Seq"))
    dfUniq[5] = readyAlign
    newdfUniq = dfUniq.to_records(index=False).tolist()

    alreadyUsedIds = {}

    for x in newdfUniq:
        cysCount = 0
        inft=[]
        if not alreadyUsedIds.get(x[2]):
            alreadyUsedIds[x[2]] = ' '
            agC = []
            inft.append(x[0])
            inft.append(x[1])
            inft.append(f'({x[3]})')

            inft_org = ' '.join(inft)
            for char in x[5]:
                agC.append(' ')
                if char == 'C':
                    cysCount = cysCount + 1
                    if CysOrderForProteinID.get(x[2]):
                        if CysOrderForProteinID[x[2]].get(str(cysCount)):
                            agC.append(
                                html.Span([html.Span(char, style={'color':'white', 'backgroundColor': "red",
                                                                  'font-family': 'monospace'}),
                                           html.Span(f'{CysOrderForProteinID[x[2]][str(cysCount)]}',
                                                     className='tooltiptext2')], className='tooltip2'))
                        else:
                            agC.append(html.Span(char,style={'color':'orange'}))
                    else:
                        agC.append(html.Span(char,style={'color':'orange'}))
                else:
                    agC.append(char)

            alignmentChildren2.append(html.Div(children=inft_org, style={'font-family': 'monospace'}))
            alignmentChildren.append(html.Div(children=agC, style={'display': 'inline-block', 'font-family': 'monospace'}))
            alignmentChildren.append(html.Br())

    return[

        dmc.Container([
            dbc.Row([
                dbc.Col([html.P([html.P('Multiple Alignment'),
                                 html.P('You can copy the alignment as text with formating',
                                        style={'font-size': '0.8em'}),
                                 html.P(['For more information on alignment algorithm, see ',
                                         html.A('Help Page ', href=f'/help_page', target='_blank')], style={'font-size': '0.8em'})])])
            ]),
            dbc.Row([
                dbc.Col([html.Div(alignmentChildren2)], style=STYLE_GRID),
                dbc.Col([html.Div(alignmentChildren)],
                        style=STYLE_GRID_2)
            ])
        ], fluid=True, style={'width':'95%', 'overflow-x':'hidden', 'overflow-y': 'hidden', },)
    ]



@callback(
    Output('download-component-oxi', 'data'),
    Input('tbl-oxi', 'data'),
    Input('btn-download-oxi', 'n_clicks'),
    prevent_initial_call=True,
)
def update_search_button(data, n_clicks):
    dataFrame = pd.DataFrame(data)
    dataFrame2 = dataFrame.drop(columns='p_ID')
    dataFrame2 = dataFrame2.drop(columns='c_ID')
    dataFrame2 = dataFrame2.drop(columns='sample_ID')
    dataFrame2 = dataFrame2.drop(columns='experiment_ID')
    dataFrame2 = dataFrame2.drop(columns='noForGraph_ID')
    dataFrame2 = dataFrame2.drop(columns='Cysteine order')
    dataFrame2 = dataFrame2.drop(columns='Cysteine positions')
    dataFrame2 = dataFrame2.drop(columns='Experiment type')
    dataFrame2 = dataFrame2.drop(columns='publication_ID')
    dataFrame2 = dataFrame2.drop(columns='Author')
    dataFrame2 = dataFrame2.drop(columns='Journal')
    dataFrame2 = dataFrame2.drop(columns='Year')
    return dcc.send_data_frame(dataFrame2.to_csv, "OxiAge_Oxidation_Table.txt", sep=';')
