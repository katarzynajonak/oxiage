# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

dash.register_page(__name__, location="error")

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
                            dbc.NavLink(
                                children=[html.I(className="bi bi-house"), ' Home'],
                                href=f'/?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(children=[html.I(className="bi bi-search-heart"),
                                                  ' Database search'],
                                        href=f'/search?lang_ID={lang_ID}', active=False, external_link=True,
                                        style={'color': '#FF5147'}),
                            dbc.NavLink(
                                children=[html.I(className="bi bi-download"), ' Downloads'],
                                href=f'/downloads?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(
                                children=[html.I(className="bi bi-chat-quote"), ' Cite us'],
                                href=f'/cite_us?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(children=[html.I(className="bi bi-question-circle"),
                                                  ' Help'],
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
                    html.H1("The requested URL was not found."),
                    dcc.Link('Please click here and go back to the home page.', href='/')
                ])
            ], xs=9, sm=9, md=9, lg=9, xl=9)
        ])
    ])