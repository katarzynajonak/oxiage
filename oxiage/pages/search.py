# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

dash.register_page(__name__,
                   path='/search',
                   title='Search',
                   name='Search',
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
        ###MENU
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
                html.H1(children=[html.Span('Search Page ', style={'color': '#3d3d3d'}), ], ),
                html.H3(children=[
                    html.Span('Choose the type of search that interests You ', style={'color': '#3d3d3d'}), ], ),
                html.Hr(),
                dmc.Breadcrumbs(
                    children=[
                        dcc.Link([html.I(className="bi bi-house"), html.Span('Home', style={"margin-left": "7px"})],
                                 href=f'/?lang_ID={lang_ID}'),
                        dcc.Link([html.I(className="bi bi-search-heart"),
                                  html.Span('Search Page', style={"margin-left": "7px"})],
                                 href=f'/search?lang_ID={lang_ID}'),
                    ], ),
                html.Br(),

                dmc.Stepper(
                    active=1,
                    color="green",
                    radius="lg",
                    size="sm",
                    children=[
                        dmc.StepperStep(label="First step", description="Choose the type of search", loading=True),
                        dmc.StepperStep(label="Second step", description="Type the protein/s or annotation/s"),
                        dmc.StepperStep(label="Third step",
                                        description="Choose the specific protein from result table"),
                        dmc.StepperStep(label="Fourth step", description="Enjoy the cross-species comparison!"),
                    ],
                ),

                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardImg(src="/assets/images/Search_Single.png", top=True, ),
                            dbc.CardBody([
                                html.H5("Search for Single Protein", className="card-title"),
                                html.P([html.Span(['Click the button below to start searching for the oxidation '
                                                   'pattern of a single chosen protein and its orthologs in '
                                                   'four species: budding yeast, worm, fruit fly, or mouse',
                                                      ],
                                                  className='tooltip2')], className='card-text',
                                       style={'text-align': 'justify'}
                                       ),
                                html.Br(),
                                dbc.Button(children=[html.Span([html.Span("SINGLE PROTEIN SEARCH"),
                                                                html.Span('Click the button',
                                                                          className='tooltiptext2')],
                                                               className='tooltip2')],
                                           color="success", className="d-grid gap-2",
                                           href=f'/search_singleProt?lang_ID={lang_ID}', target='blank',
                                           external_link=True, )
                            ]),
                        ], style={"width": 'auto'}, ),
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardImg(src="/assets/images/Search_Annotation.png", top=True),
                            dbc.CardBody([
                                html.H5("Search for Annotation", className="card-title"),
                                html.P([html.Span(
                                    ['Click the button below to start searching for the oxidation pattern of '
                                     'multiple proteins localized in a defined cellular compartment, involved in '
                                     'a particular biological process or enabling a chosen molecular function',],
                                    className='tooltip2')], className='card-text', style={'text-align': 'justify'}),
                                dbc.Button(children=[html.Span([html.Span("ANNOTATION SEARCH"),
                                                                html.Span('Click the button',
                                                                          className='tooltiptext2')],
                                                               className='tooltip2')],
                                           color="info", className="d-grid gap-2",
                                           href=f'/search_Annotation?lang_ID={lang_ID}', target='blank',
                                           external_link=True, )
                            ]),
                        ], style={"width": 'auto%'}, ),
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardImg(src="/assets/images/Search_Common.png", top=True),
                            dbc.CardBody([
                                html.H5("Search for Common Proteins", className="card-title"),
                                html.P([html.Span(['Click the button below to start searching for commonly oxidized '
                                                   'proteins in different species during aging',
                                                      ],
                                                  className='tooltip2')], className='card-text',
                                       style={'text-align': 'justify'}),
                                html.Br(),
                                html.Br(),
                                dbc.Button(children=[html.Span([html.Span("COMMON PROTEINS SEARCH"),
                                                                html.Span('Click the button',
                                                                          className='tooltiptext2')],
                                                               className='tooltip2')],
                                           color="warning", className="d-grid gap-2",
                                           href=f'/search_multipleProteins?lang_ID={lang_ID}', target='blank',
                                           external_link=True, )
                            ]),
                        ], style={"width": "auto%"}, ),
                    ]),
                ], style={'width': '90%'}),
            ])
        ], xs=9, sm=9, md=9, lg=9, xl=9)
    ])
    ])