# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import dash
from dash import dcc, callback, Input, Output, State, html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path='/help_page',
                   title='Help page',
                   name='Help',
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
                                        href=f'/downloads?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(children=[html.I(className="bi bi-chat-quote"), ' Cite us'],
                                        href=f'/cite_us?lang_ID={lang_ID}', active=False, external_link=True),
                            dbc.NavLink(children=[html.I(className="bi bi-question-circle"), ' Help'],
                                        href=f'/help_page?lang_ID={lang_ID}', active=True, external_link=True),
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
                    html.H1(children=[html.Span('Help Page of ', style={'color': '#3d3d3d'}),
                                      html.Span('OxiAge Database', style={'color': '#FF5147'})], ),
                    html.Hr(),
                    dmc.Breadcrumbs(
                        children=[
                            dcc.Link([html.I(className="bi bi-house"), html.Span('Home', style={"margin-left": "7px"})],
                                     href=f'/?lang_ID={lang_ID}'),
                            dcc.Link([html.I(className="bi bi-question-circle"),
                                      html.Span('Help Page', style={"margin-left": "7px"})],
                                     href=f'/help_page?lang_ID={lang_ID}'),
                        ], ),
                    html.Br(),
                    html.Br(),
                    dbc.Button(children=[html.I(className="bi bi-book"),
                                         html.Span("What OxiAge Database is about?", style={"margin-left": "15px"})],
                               id="collapse-button1", className="d-flex align-items-center", color="light", n_clicks=0),
                    html.Div(
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([
                                    dmc.Spoiler(showLabel="Show more", hideLabel="Hide", maxHeight=100,
                                                children=[
                                                    html.P(['Many health conditions associated with ', html.B('aging'),
                                                            ' are linked to complex changes in protein homeostasis '
                                                            'that impair human health. Along with the progression '
                                                            'through aging, ', html.B('reactive oxygen species'),
                                                            ' (ROS) within cells increase, causing changes in proteome '
                                                            'modifications and possibly function. Reversible oxidation '
                                                            'of some protein ', html.B('cysteine residues (Cys)'),
                                                            ' have been found as a way to control the activity of '
                                                            'proteins, regulating a myriad of biological processes '
                                                            'during cellular stress and aging.'],
                                                           style={'text-align': 'justify'}),
                                                    html.Br(),
                                                    html.P(['The OxiAge is an interactive web application of ',
                                                            html.B('cross-species database'),
                                                            ' that connects our current knowledge on reversible '
                                                            'proteome oxidation during aging in various eukaryotes. '
                                                            'The OxiAge Database explores changes in the oxidation '
                                                            'landscape of specific cysteine residues across different '
                                                            'species based on mass spectrometry results from '
                                                            'chronologically aged yeast ',
                                                            html.I('Saccharomyces cerevisiae'), ' adult worms ',
                                                            html.I('Caenorhabditis elegans'), ', fruit flies ',
                                                            html.I('Drosophila melanogaster'), ', and mice ',
                                                            html.I('Mus musculus'), ' (for references, see below).'],
                                                           style={'text-align': 'justify'}),
                                                    html.Br(),
                                                    html.P('The OxiAge Database serves as a basis for researchers to '
                                                           'explore evolutionarily conserved redox-sensitive cysteine '
                                                           'residues differently modified at specific stages of aging. '
                                                           , style={'text-align': 'justify'})
                                                ]),
                                ]), style={"maxWidth": "1000px"}
                            ),
                            id="collapse1", is_open=True,
                        ),
                    ),

                    html.Br(),
                    html.Br(),
                    dbc.Button(children=[html.I(className="bi bi-book"),
                                         html.Span("How to search the OxiAge Database?",
                                                   style={"margin-left": "15px"})],
                               id="collapse-button2", className="d-flex align-items-center", color="light", n_clicks=0),
                    html.Div(
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody(
                                    [dmc.Spoiler(showLabel="Show more", hideLabel="Hide", maxHeight=250, children=[
                                        html.B('Searching the OxiAge Database in four easy steps:'),
                                        html.Br(),
                                        html.Br(),
                                        html.B('1) Choose the type of search '),
                                        html.P('The first version of the OxiAge Database allows performing three '
                                               'different types of searches: '),
                                        html.P(['-> ',
                                                html.A('Single Protein Search', href=f'/search_singleProt?',
                                                       style={'color': '#007500'}),
                                                ' allows searching for a specified protein and the orthologs']),
                                        html.P(['-> ',
                                                html.A('Annotation Search', href=f'/search_singleProt?',
                                                       style={'color': '#2E2EFF'}),
                                                ' allows finding redox-sensitive proteins annotated with a specific '
                                                'Gene Ontology term: cellular component, biological process or '
                                                'molecular function']),
                                        html.P(['-> ',
                                                html.A('Common Proteins Search', href=f'/search_singleProt?',
                                                       style={'color': '#da9a01'}),
                                                ' displays proteins found commonly oxidized between at least two '
                                                'specified species ']),
                                        html.Br(),
                                        html.B('2) Choose the organism, protein, or annotation of interest '
                                               '(depending on the type of search)'),
                                        html.P(
                                            ['Searching for a ', html.A('single protein', style={'color': '#007500'}),
                                             ' or ', html.A('annotation', style={'color': '#2E2EFF'}),
                                             ' requires choosing a single organism from a dropdown list and typing '
                                             'the protein or annotation of interest in the second '
                                             'dropdown field. Note that a ',
                                             html.A('single protein search', style={'color': '#007500'}),
                                             ' can be done by either typing the '
                                             'UniProt ID or gene name. Searching for ',
                                             html.A('common proteins', style={'color': '#da9a01'}),
                                             ' requires choosing at least two organisms to compare between '
                                             'using a multiple dropdown field.'],
                                            style={'text-align': 'justify'}),
                                        html.Br(),
                                        html.B('3) Choose a single protein from a result table'),
                                        html.P('Upon completing step (2), a table with list of proteins will '
                                               'be displayed. Upon clicking on a specific UniProt ID the website '
                                               'directs the user to the information on oxidation of chosen '
                                               'protein and the orthologs in other species.',
                                            style={'text-align': 'justify'}),
                                        html.Br(),
                                        html.B(
                                            '4) Enjoy the cross-species comparison!'),
                                        html.Br(), ]),
                                     html.Br(),
                                     dbc.Carousel(items=[
                                         {
                                             "key": "1",
                                             "src": "/assets/images/Help1.png",
                                         },
                                         {
                                             "key": "2",
                                             "src": "/assets/images/Help2.png",
                                         },
                                         {
                                             "key": "3",
                                             "src": "/assets/images/Help3.png",
                                         },

                                         {
                                             "key": "4",
                                             "src": "/assets/images/Help4.png",
                                         },

                                     ], controls=False, indicators=True, interval=2200, variant='dark',
                                         # style={"width": '750px', "hight": "200px"},
                                         style={"width": '95%'},
                                     ), ], ), style={"maxWidth": "1000px"}
                            ),
                            id="collapse2", is_open=True,
                        ),
                    ),

                    html.Br(),
                    html.Br(),
                    dbc.Button(children=[html.I(className="bi bi-book"),
                                         html.Span(
                                             [html.Span("Results of OxiAge Database", style={"margin-left": "15px"}, ),
                                              html.Span('Click to see more', className='tooltiptext2')],
                                             className='tooltip2')],
                               id="collapse-button3", className="d-flex align-items-center", color="light", n_clicks=0),
                    html.Div(
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([
                                    dmc.Spoiler(showLabel="Show more", hideLabel="Hide", maxHeight=200, children=[
                                        html.B('RESULTS TABLE'),
                                        html.Br(),
                                        html.P('The layout of the table depends on the type of search performed.'),
                                        html.P(['For a single protein search, the table displays the UniProt ID, '
                                                'gene name, and organism name of the searched protein and found '
                                                'orthologs. This table can be sorted and downloaded. The download file '
                                                'contains additional information, such as protein amino acid length, '
                                                'number of all cysteine residues within the protein, motifs '
                                                'surrounding the oxidized cysteine residue, and more.', html.Br(),
                                                'IMPORTANT NOTE: The Database contains information on not only the '
                                                'redox-sensitive proteins detected in given aging datasets. It also '
                                                'contains information on proteins that are not detected, '
                                                'but are annotated as being orthologs of genes of proteins found '
                                                'oxidized in at least one organism included in the Database.'],
                                               style={'text-align': 'justify'}),
                                        html.P('For an annotation search, the table displays UniProt IDs '
                                               'and gene names of all proteins found annotated with a chosen '
                                               'Gene Ontology term. The table does not show the orthologs.',
                                            style={'text-align': 'justify'}),
                                        html.P('For a common proteins search, a visual representation of intersections '
                                               'between species is displayed. Pressing the “Search” button directs '
                                               'the user to a table containing UniProt IDs and gene names '
                                               'of evolutionarily conserved and redox-sensitive proteins. '
                                               'If a certain protein has more than one oxidized ortholog, it will be '
                                               'displayed in a new table row.',
                                               style={'text-align': 'justify'}),
                                        html.Br(),
                                        html.Br(), ]),
                                    html.Br(),
                                    dbc.Carousel(items=[
                                        {"key": "1", "src": "/assets/images/HelpA1.png", },
                                        {"key": "2", "src": "/assets/images/HelpA2.png", },
                                        {"key": "3", "src": "/assets/images/HelpA3.png", },
                                        {"key": "4", "src": "/assets/images/HelpA4.png", },
                                        {"key": "5", "src": "/assets/images/HelpA5.png", },
                                        {"key": "6", "src": "/assets/images/HelpA6.png", },
                                        {"key": "7", "src": "/assets/images/HelpA7.png", },
                                        {"key": "8", "src": "/assets/images/HelpA8.png", },
                                    ], controls=False, indicators=True, interval=2200, variant='dark',
                                        style={"width": '95%'},
                                    ),

                                    dmc.Spoiler(showLabel="Show more", hideLabel="Hide", maxHeight=200, children=[
                                        html.Br(),
                                        html.B('OXIDATION RESULTS PAGE'),
                                        html.Br(),
                                        html.B('Tab 1: Alignment & Oxidation'),
                                        html.P('The final result page contains the alignment of redox-sensitive '
                                               'proteins found in the Database with marked cysteine sites detected '
                                               'in any of the dataset used. The alignment is performed between '
                                               'oxidized proteins and the proteins that are products of the gene '
                                               'orthologs found in other species. '
                                               , style={'text-align': 'justify'}),
                                        html.P(['IMPORTANT NOTE: The alignment is performed between proteins of all '
                                               'known orthologs according to ',
                                                html.A('Alliance of Genome Resources',
                                                      href=f'https://www.alliancegenome.org/', target='_blank'),
                                                ' even if they are not detected in any of the used datasets. '
                                                'This allows for prediction of oxidation state in other species.'],
                                               style={'text-align': 'justify'}),
                                        html.P('The description of the cysteine site in a popover includes '
                                               'the positions of the cysteine residue detected in any of the aging '
                                               'experiment. If the cysteine was detected in a peptide along with '
                                               'another cysteine residue, there are multiple positions shown. '
                                               'This enables identification of multiple cysteine residues '
                                               'within one peptide.', style={'text-align': 'justify'}),
                                        html.P('Oxidation graphs display the average % oxidation during different '
                                               'stages of aging for each protein, species, and experiment (for '
                                               'example yeast from Jonak et al. or Brandes et al.). For mice, '
                                               'additional graphs are presented for each tissue separately. '
                                               'As a default only one tissue is presented with an open graph. '
                                               'To see the results for other tissues from Xiao et al. experiment, '
                                               'click on the blue tabs marked with the names of particular tissues. '
                                               'They can be found below the open graphs.',
                                               style={'text-align': 'justify'}),
                                        html.Br(),
                                        html.B('Tab 2: Results Table'),
                                        html.P('Detailed information on oxidation for all proteins and '
                                               'species shown in all the graphs from the “Alignment & Oxidation” tab '
                                               'are displayed in form of a table. The table can be downloaded with '
                                               'more information included, such as cysteine ID (name of the '
                                               'peptide containing UniProt ID of a protein and positions of cysteine '
                                               'sites detected within the peptide), number of biological replicates, '
                                               'detected isoform, type of experiment, and publication information '
                                               '(first author name, journal name, year of publication and doi).',
                                               style={'text-align': 'justify'}),
                                        html.Br(),
                                        html.B('Tab 3: Information on Proteins'),
                                        html.P(
                                            'Contains key information on chosen proteins and orthologs, mostly derived '
                                            'from UniProt Knowledgebase and a direct link to the predicted structure '
                                            'of the protein. Additionally, information about a number of cysteine '
                                            'residues, positions and motifs is available.',
                                            style={'text-align': 'justify'}),
                                        html.Br(),
                                        html.B('Tab 4: External Resources'),
                                        html.P('The tab contains external links to different websites containing more '
                                               'details about the proteins.', style={'text-align': 'justify'}),
                                    ]),
                                    html.Br(),
                                    dbc.Carousel(items=[
                                        {"key": "1", "src": "/assets/images/HelpB1.png", },
                                        {"key": "2", "src": "/assets/images/HelpB2.png", },
                                        {"key": "3", "src": "/assets/images/HelpB3.png", },
                                        {"key": "4", "src": "/assets/images/HelpB4.png", },
                                        {"key": "5", "src": "/assets/images/HelpB5.png", },
                                    ], controls=False, indicators=True, interval=2200, variant='dark',
                                        style={"width": '95%'},
                                    ),
                                ]), style={"maxWidth": "1000px"}
                            ),
                            id="collapse3", is_open=False,
                        ),
                    ),

                    html.Br(),
                    html.Br(),
                    dbc.Button(children=[html.I(className="bi bi-book"),
                                         html.Span([html.Span("Acknowledgments", style={"margin-left": "15px"}, ),
                                                    html.Span('Click to see more', className='tooltiptext2')],
                                                   className='tooltip2')],
                               id="collapse-button4", className="d-flex align-items-center", color="light", n_clicks=0),
                    html.Div(
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([
                                    html.P(['The first version of the OxiAge Database contains information from '
                                            'five different experiments and four different species (to our '
                                            'knowledge, all currently available experiments on oxidized proteome '
                                            'during eukaryotic aging): yeast ', html.I('S. cerevisiae'), ' from ',
                                            html.A('Jonak et al., 2023', href='https://www.biorxiv.org/content/10.1101/2023.05.08.539783v1',
                                                      target='_blank'),
                                            ' and ',
                                            html.A('Brandes et al., 2013',
                                                      href='https://elifesciences.org/articles/306', target='_blank'),
                                            ', worms ', html.I('C. elegans'), ' from ',
                                            html.A('Knoefler et al., 2012',
                                                      href='https://www.sciencedirect.com/science/article/pii/S1097276512005412',
                                                      target='_blank'),
                                            ', fruit flies ', html.I('D. melanogaster'), ' from ',
                                            html.A('Menger et al., 2015',
                                                      href='https://www.sciencedirect.com/science/article/pii/S2211124715005690?via%3Dihub',
                                                      target='_blank'),
                                            ' and mice ', html.I('M. musculus'), ' from ',
                                            html.A('Xiao et al., 2020',
                                                      href='https://www.sciencedirect.com/science/article/pii/S0092867420301562',
                                                      target='_blank'),
                                            ],
                                        style={'text-align': 'justify'}),
                                    html.P(['The database used in the OxiAge project is created using ',
                                            html.A('MySQL 8.0.', href='https://dev.mysql.com/doc/refman/8.0/en/',
                                                   target='_blank'),
                                            '. For backend, we use ',
                                            html.A('Python 3.10', href='https://github.com/python', target='_blank'),
                                            ', ',
                                            html.A('Plotly Dash framework', href='https://github.com/plotly/dash',
                                                   target='_blank'),
                                            '. For graphs display and user interaction we use ',
                                            html.A('Plotly.js', href='https://github.com/plotly/plotly.js/',
                                                   target='_blank'),
                                            ' (', html.A('Dash bootstrap components',
                                                         href='https://github.com/facultyai/dash-bootstrap-components',
                                                         target='_blank'),
                                            ', ', html.A('Dash mantine components',
                                                         href='https://github.com/snehilvj/dash-mantine-components',
                                                         target='_blank'),
                                            ' and ', html.A('Dash core components',
                                                            href='https://github.com/plotly/dash-core-components',
                                                            target='_blank'),
                                            '). Tables are prepared using ',
                                            html.A('pandas library', href='https://github.com/pandas-dev/pandas',
                                                   target='_blank'),
                                            ' and visualized with ',
                                            html.A('Dash table components', href='https://github.com/plotly/dash-table',
                                                   target='_blank'),
                                            '. Connection with MySQL database is established with ',
                                            html.A('MySQL Connector/ Python',
                                                   href='https://github.com/mysql/mysql-connector-python',
                                                   target='_blank'),
                                            '. Venn diagrams are generated using ',
                                            html.A('pyvenn', href='https://github.com/LankyCyril/pyvenn',
                                                   target='_blank'),
                                            ' and ',
                                            html.A('matplotlib', href='https://github.com/matplotlib/matplotlib',
                                                   target='_blank'),
                                            '. '
                                            ],
                                           style={'text-align': 'justify'}),

                                    html.P(['The website uses ',
                                            html.A('Bootswatch', href='https://bootswatch.com/', target='_blank'),
                                            ' for Bootstrap themes and ',
                                            html.A('Bootstrap icon library', href='https://icons.getbootstrap.com/',
                                                   target='_blank'),
                                            '.'
                                            ], style={'text-align': 'justify'}),

                                    html.P(['Sequence alignment is performed using ',
                                            html.A('Biotite', href='https://github.com/biotite-dev/biotite',
                                                   target='_blank'),
                                            ' packages: ',
                                            html.A('align_optimal',
                                                   href='https://www.biotite-python.org/apidoc/biotite.sequence.align.Alignment.html',
                                                   target='_blank'),
                                            ' and ',
                                            html.A('align_multiple',
                                                   href='https://www.biotite-python.org/apidoc/biotite.sequence.align.align_multiple.html',
                                                   target='_blank'),
                                            '.'
                                            ], style={'text-align': 'justify'}),
                                ]), style={"maxWidth": "1000px"}
                            ),
                            id="collapse4", is_open=False,
                        ),
                    ),

                    html.Br(),
                    html.Br(),
                    dbc.Button(children=[html.I(className="bi bi-book"),
                                         html.Span([html.Span("Copyright and Licence", style={"margin-left": "15px"}, ),
                                                    html.Span('Click to see more', className='tooltiptext2')],
                                                   className='tooltip2')],
                               id="collapse-button8", className="d-flex align-items-center", color="light", n_clicks=0),
                    html.Div(
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([
                                    html.P([
                                        'The OxiAge Database web application is developed under ',
                                        html.A('Creative Commons Attribution-ShareAlike 4.0 International License',
                                               href='https://creativecommons.org/licenses/by-sa/4.0/', target='_blank'),
                                        '. Generated images and graphs are under ',
                                        html.A('Creative Commons Attribution-ShareAlike 4.0 International License',
                                               href='https://creativecommons.org/licenses/by-sa/4.0/', target='_blank'),
                                        '.'
                                    ], style={'text-align': 'justify'}),
                                ]), style={"maxWidth": "1000px"}
                            ),
                            id="collapse8", is_open=False,
                        ),
                    ),

                    html.Br(),
                    html.Br(),
                    dbc.Button(children=[html.I(className="bi bi-book"),
                                         html.Span([html.Span("Help Us to improve!", style={"margin-left": "15px"}, ),
                                                    html.Span('Click to see more', className='tooltiptext2')],
                                                   className='tooltip2')],
                               id="collapse-button7", className="d-flex align-items-center", color="light", n_clicks=0),
                    html.Div(
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([
                                    html.P(['If you find it difficult to navigate through the website or find '
                                            'inconsistencies on the website do not hesitate and ',
                                               html.A('write to Us!', href='mailto:k.jonak@bb.waw.pl',
                                                      target='_blank')]),
                                    html.P('We plan to expand the website soon with additional functionalities and '
                                           'published datasets. Thus, any feedback is greatly appreciated! ',
                                        style={'text-align': 'justify'})
                                ]), style={"maxWidth": "1000px"}
                            ),
                            id="collapse7", is_open=False,
                        ),
                    ),

                    html.Br(),
                    html.Br(),
                    dbc.Button(children=[html.I(className="bi bi-book"),
                                         html.Span([html.Span("Help the scientific community",
                                                              style={"margin-left": "15px"}, ),
                                                    html.Span('Click to see more', className='tooltiptext2')],
                                                   className='tooltip2')],
                               id="collapse-button5", className="d-flex align-items-center", color="light", n_clicks=0),
                    html.Div(
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([
                                    html.P('Sharing is one of the key ingredients for scientific advance. '
                                           'Thus, we encourage you to add your experiment to the OxiAge database. ',
                                           style={'text-align': 'justify'}),
                                    html.P([html.A('Write to us', href='mailto:k.jonak@bb.waw.pl', target='_blank'),
                                            ' if you are the author of any research that provides information on '
                                            'age-dependent proteome oxidation and want to share your results '
                                            'on this website.'], style={'text-align': 'justify'})
                                ]), style={"maxWidth": "1000px"}
                            ),
                            id="collapse5", is_open=False,
                        ),
                    ),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dbc.Button(children=[html.I(className="bi bi-emoji-sunglasses"),
                                         html.Span([html.Span("Cookies", style={"margin-left": "15px"}, ),
                                                    html.Span('Click to see more', className='tooltiptext2')],
                                                   className='tooltip2')],
                               id="collapse-button6", className="d-flex align-items-center", color="light", n_clicks=0),
                    html.Div(
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([
                                    html.P('This website uses cookies. They are used for security and improvement '
                                           'and are not intended to track information or identify users. Information '
                                           'may be used only to identify eventual problems with searches.',
                                        style={'text-align': 'justify'}),
                                ]), style={"maxWidth": "1000px"}
                            ),
                            id="collapse6", is_open=False,
                        ),
                    ),
                ]),
            ], xs=9, sm=9, md=9, lg=9, xl=9)
        ])
    ])


for number in [1, 2, 3, 4, 5, 6, 7, 8]:
    @callback(
        Output("collapse{}".format(number), "is_open"),
        [Input("collapse-button{}".format(number), "n_clicks")],
        [State("collapse{}".format(number), "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open