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
                   path="/cite_us",
                   title='Cite us',
                   name='Cite us',
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
                                        href=f'/downloads?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(children=[html.I(className="bi bi-chat-quote"), ' Cite us'],
                                        href=f'/cite_us?lang_ID={lang_ID}', active=True, external_link=True),
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
                    html.H1(children=[html.Span('Citing the ', style={'color': '#3d3d3d'}),
                                      html.Span('OxiAge Database', style={'color': '#FF5147'})], ),
                    html.Hr(),
                    dmc.Breadcrumbs(
                        children=[
                            dcc.Link([html.I(className="bi bi-house"), html.Span('Home', style={"margin-left": "7px"})],
                                     href=f'/?lang_ID={lang_ID}'),
                            dcc.Link([html.I(className="bi bi-chat-quote"),
                                      html.Span('Cite Us', style={"margin-left": "7px"})],
                                     href=f'/cite_us?lang_ID={lang_ID}'),
                        ], ),
                    html.Br(),
                    html.Br(),
                    dbc.Alert([
                        html.H6('For citing the OxiAge Database:'),
                        html.H5(children=[html.A('Jonak et al., 2023',
                                                 href='https://www.biorxiv.org/content/10.1101/2023.05.08.539783v1',
                                                 target='_blank'), ]),
                        dbc.Toast(html.H6('Jonak, K., Suppanz, I., Bender, J., Chacinska, A., Warsheid, B., & Topf, U. '
                                          '(2023). Analysis of ageing-dependent thiol oxidation reveals early oxidation '
                                          'of proteins involved in core proteostasis functions. bioRxiv 2023.05.08.539783'), style={"width": 700}),
                    ], color='primary'),
                    html.Br(),
                    dbc.Alert([
                        html.H6('Do not forget to cite the original works used in this Database:'),
                        html.Br(),
                        html.H6(children=['If using data from ',
                                          html.Span('C. elegans', style={"font-style": "italic"}),
                                          ', please cite ',
                                          html.A('Knoefler et al., 2012',
                                                 href='https://www.sciencedirect.com/science/article/pii/S1097276512005412',
                                                 target='_blank')], ),
                        dbc.Toast(html.H6(
                            'Knoefler, D., Thamsen, M., Koniczek, M., Niemuth, N. J., Diederich, A. K., & Jakob, U. '
                            '(2012). Quantitative in vivo redox sensors uncover oxidative stress as an early '
                            'event in life. Molecular cell, 47(5), 767-776.'), style={"width": 700}),
                        html.Br(),
                        html.H6(children=['If using data from ',
                                          html.Span('S. cerevisiae', style={"font-style": "italic"}),
                                          ' strain DBY749, please cite ',
                                          html.A('Brandes et al., 2013', href='https://elifesciences.org/articles/306',
                                                 target='_blank')], ),
                        dbc.Toast(html.H6(
                            'Brandes, N., Tienson, H., Lindemann, A., Vitvitsky, V., Reichmann, D., Banerjee, R., '
                            '& Jakob, U. (2013). Time line of redox events in aging postmitotic cells. Elife, '
                            '2, e00306.'), style={"width": 700}),

                        html.Br(),
                        html.H6(children=['If using data from ',
                                          html.Span('S. cerevisiae', style={"font-style": "italic"}),
                                          ' strain YPH499, please cite ',
                                          html.A('Jonak et al., 2023', href='https://www.biorxiv.org/content/10.1101/2023.05.08.539783v1',
                                                 target='_blank')], ),
                        dbc.Toast(html.H6('Jonak, K., Suppanz, I., Bender, J., Chacinska, A., Warsheid, B., & Topf, U. '
                                          '(2023). Analysis of ageing-dependent thiol oxidation reveals early oxidation '
                                          'of proteins involved in core proteostasis functions. bioRxiv 2023.05.08.539783'), style={"width": 700}),

                        html.Br(),
                        html.H6(children=['If using data from ',
                                          html.Span('D. melanogaster', style={"font-style": "italic"}),
                                          ' , please cite ',
                                          html.A('Menger et al., 2013',
                                                 href='https://www.sciencedirect.com/science/article/pii/S2211124715005690?via%3Dihub',
                                                 target='_blank')], ),
                        dbc.Toast(
                            html.H6(
                                'Menger, K. E., James, A. M., Cochemé, H. M., Harbour, M. E., Chouchani, E. T., Ding, S., ... & Murphy, '
                                'M. P. (2015). Fasting, but not aging, dramatically alters the redox status of cysteine '
                                'residues on proteins in Drosophila melanogaster. Cell reports, 11(12), 1856-1865.'),
                            style={"width": 700}),

                        html.Br(),
                        html.H6(children=['If using data on multiple tissues from ',
                                          html.Span('M. musculus', style={"font-style": "italic"}),
                                          ', please cite ',
                                          html.A('Xiao et al., 2020',
                                                 href='https://www.sciencedirect.com/science/article/pii/S0092867420301562',
                                                 target='_blank'), ], ),
                        dbc.Toast(html.H6(
                            'Xiao, H., Jedrychowski, M. P., Schweppe, D. K., Huttlin, E. L., Yu, Q., Heppner, D. E., '
                            '... & Chouchani, E. T. (2020). A quantitative tissue-specific landscape of protein '
                            'redox regulation during aging. Cell, 180(5), 968-983.'), style={"width": 700}),
                    ], color='success'),
                ])
            ], xs=9, sm=9, md=9, lg=9, xl=9)
        ])
    ])



