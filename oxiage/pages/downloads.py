# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, callback, Input, Output, html
from pathlib import Path

dash.register_page(__name__,
                   path='/downloads',
                   title='Downloads',
                   name='Downloads',
                   location="mainmenu")

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

def layout(lang_ID=None):

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
                                        href=f'/search?lang_ID={lang_ID}', active=False, external_link=True,
                                        style={'color': '#FF5147'}),
                            dbc.NavLink(children=[html.I(className="bi bi-download"), ' Downloads'],
                                        href=f'/downloads?lang_ID={lang_ID}', active=True, external_link=True),
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
                    html.H1(children=[html.Span('Download Page of ', style={'color': '#3d3d3d'}),
                                      html.Span('OxiAge Database', style={'color': '#FF5147'})], ),
                    html.Hr(),
                    dmc.Breadcrumbs(
                        children=[
                            dcc.Link([html.I(className="bi bi-house"), html.Span('Home', style={"margin-left": "7px"})],
                                     href=f'/?lang_ID={lang_ID}'),
                            dcc.Link([html.I(className="bi bi-download"),
                                      html.Span('Download', style={"margin-left": "7px"})],
                                     href=f'/downloads?lang_ID={lang_ID}'),
                        ], ),
                    html.Br(),
                    html.Br(),
                    dbc.Alert([
                        html.H5('"Yeast OxiAge" dataset', className="alert-heading"),
                        html.P(['Download the .txt files of the "yeast OxiAge". For more information on the '
                                 'files and the final filtered "yeast OxiAge", see our publication: ',
                                 html.A('Jonak et al., 2023', href='https://www.biorxiv.org/content/10.1101/2023.05.08.539783v1', target='_blank')]),
                        html.Hr(),
                        html.P(['Complete yeast dataset, unfiltered (information after direct preprocessing of '
                                'mass spectrometry results, used for the OxiAge Database):']),
                        dbc.Button(
                            children=[html.I(className="bi bi-download"),
                                      html.Span("Download Complete Dataset", style={"margin-left": "15px"})],
                            color="info", className="d-flex align-items-center",
                            id='btn-download-file1'),
                        dcc.Download(id="download-component-file1"),
                        html.Br(),
                        html.P(['Filtered yeast dataset: "yeast OxiAge":', ]),
                        dbc.Button(
                            children=[html.I(className="bi bi-download"),
                                      html.Span('Download "Yeast OxiAge"', style={"margin-left": "15px"})],
                            color="info", className="d-flex align-items-center",
                            id='btn-download-file2'),
                        dcc.Download(id="download-component-file2"),
                        html.Br(),
                        html.P(['Clusters based on temporal oxidation pattern of peptides from "yeast OxiAge" '
                                'dataset:']),
                        dbc.Button(
                            children=[html.I(className="bi bi-download"),
                                      html.Span("Download Clusters", style={"margin-left": "15px"})],
                            color="info", className="d-flex align-items-center",
                            id='btn-download-file3'),
                        dcc.Download(id="download-component-file3"),

                    ], color='primary'),
                    html.Br(),
                    dbc.Alert([
                        html.H5('Common Proteins', className="alert-heading"),
                        html.P(['Download the .txt files of proteins commonly found as oxidized between four different '
                                'species. This file contains the comparison of the filtered datasets. For more '
                                'information on the files and filtering method performed, see the method section of: ',
                                html.A('Jonak et al., 2023', href='https://www.biorxiv.org/content/10.1101/2023.05.08.539783v1', target='_blank')]),
                        html.Hr(),
                        html.P(['All datasets you can download here were filtered according to the methods provided '
                                'in our publication. From datasets from other studies only peptides that contained a '
                                'valid average value of oxidation in all considered time points were chosen for '
                                'comparison.']),
                        dbc.Button(
                            children=[html.I(className="bi bi-download"),
                                      html.Span("Download Species Comparison", style={"margin-left": "15px"})],
                            color="success", className="d-flex align-items-center",
                            id='btn-download-file4'),
                        dcc.Download(id="download-component-file4"),
                    ], color='success'),
                ]),
            ], xs=9, sm=9, md=9, lg=9, xl=9)
        ])
    ])

@callback(
    Output('download-component-file1', 'data'),
    Input('btn-download-file1', 'n_clicks'),
    prevent_initial_call=True,
)
def update_search_button(n_clicks):
    path = Path(__file__).parent / "../assets/tables/Table1_Oxidation_Per_Peptide.xlsx"
    data = pd.read_excel(path)
    dataFrame = pd.DataFrame(data)
    return dcc.send_data_frame(dataFrame.to_csv, "OxiAge_Complete_Yeast_Jonak2023.txt", sep=';')

@callback(
    Output('download-component-file2', 'data'),
    Input('btn-download-file2', 'n_clicks'),
    prevent_initial_call=True,
)
def update_search_button(n_clicks):
    path = Path(__file__).parent / "../assets/tables/Table2_Yeast_OxiAge.xlsx"
    data = pd.read_excel(path)
    dataFrame = pd.DataFrame(data)
    return dcc.send_data_frame(dataFrame.to_csv, "OxiAge_Filtered_Yeast_Jonak2023.txt", sep=';')

@callback(
    Output('download-component-file3', 'data'),
    Input('btn-download-file3', 'n_clicks'),
    prevent_initial_call=True,
)
def update_search_button(n_clicks):
    path = Path(__file__).parent / "../assets/Table3_Clustering.xlsx"
    data = pd.read_excel(path)
    dataFrame = pd.DataFrame(data)
    return dcc.send_data_frame(dataFrame.to_csv, "OxiAge_Filtered_Yeast_Clusters_Jonak2023.txt", sep=';')

@callback(
    Output('download-component-file4', 'data'),
    Input('btn-download-file4', 'n_clicks'),
    prevent_initial_call=True,
)
def update_search_button(n_clicks):
    path = Path(__file__).parent / "../assets/tables/Table7_Species_Comparison_All_Proteins.xlsx"
    data = pd.read_excel(path)
    dataFrame = pd.DataFrame(data)
    return dcc.send_data_frame(dataFrame.to_csv, "OxiAge_Common_Jonak2023.txt", sep=';')
