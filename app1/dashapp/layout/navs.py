import dash_bootstrap_components as dbc
import dash_core_components as dcc

search_bar = dbc.Row(children=[dbc.Col(
        dbc.Input(type="search", id='search-button', placeholder="Search")
        ),
        dbc.Col(dcc.Dropdown(id="search-box"))],
        no_gutters=True,
        className="ml-auto flex-nowrap mt-3 mt-md-0",
        align="right"
        )
search_collapse = dbc.Collapse(search_bar, id="navbar-collapse", is_open=True, navbar=True)

# search_navbar = dbc.Navbar(
#         dbc.Container(
#                 [
#                         # dbc.NavbarBrand("Search", href="#"),
#                         dbc.NavbarToggler(id="navbar-toggler3"),
#                         dbc.Collapse(
#                                 dbc.Row(
#                                         [
#                                                 dbc.Col(
#                                                         dbc.Input(type="search",
#                                                                   placeholder="Search")
#                                                         ),
#                                                 dbc.Col(
#                                                         dbc.Button(
#                                                                 "Search", color="primary",
#                                                                 className="ml-2"
#                                                                 ),
#                                                         # set width of button column to auto 
#                                                         # to allow
#                                                         # search box to take up remaining space.
#                                                         width="auto",
#                                                         ),
#                                                 ],
#                                         no_gutters=True,
#                                         # add a top margin to make things look nice when the 
#                                         # navbar
#                                         # isn't expanded (mt-3) remove the margin on medium or
#                                         # larger screens (mt-md-0) when the navbar is expanded.
#                                         # keep button and search box on same row (flex-nowrap).
#                                         # align everything on the right with left margin (
#                                         # ml-auto).
#                                         className="ml-auto flex-nowrap mt-3 mt-md-0",
#                                         align="center",
#                                         ),
#                                 id="navbar-collapse3",
#                                 navbar=True,is_open=False
#                                 ),
#                         ]
#                 ),
#         className="mb-5",
#         fixed=True
#         )
