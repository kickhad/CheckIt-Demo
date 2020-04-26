import logging

import dash_table as dt
from dash_bootstrap_components import Button, Col, Container, NavItem, Navbar, Row, Tab, Tabs
from dash_html_components import A, Div, H1, H2, H3

from app1.dashapp.callbacks.callbacks import VISIBILITY_HIDDEN
from app1.dashapp.layout.navs import search_collapse
from app1.dicts import *

logger = logging.getLogger('view')
header = H1('THIS')


def layout(view):
    """
    Layout with the following hierachy
    
    my-content-window
    :param view: app1.viewmodel.DashView 
    :return: dash.Dash().layout
    """
    df = view.df
    busgrps = view.dicts[BUSGRP_ID__BUSGRP_LDESC]

    this_layout = get_main_layout(
            main_window_col_10=get_main_window(),
            side_menu_col_2=get_side_menu(),
            top_navbar=get_top_navbar(busgrps),
            )
    # bottom_navbar = None

    return this_layout


# def get_bottom_bar():
#     bottom_navbar = Container(Navbar(search_collapse, fixed='bottom'))
#     return bottom_navbar


def get_top_navbar(busgrps):
    navbar = Navbar(id='top-nav-bar', children=[get_tabs_container(busgrps), Button(A(
            'Download to Excel', id='download-link', download='export.csv')),
                                                search_collapse],
                    fixed='top')
    # top_navbar = Col(id='top-navbar-col-12', children=[navbar, search_collapse])
    return navbar


def get_main_window():
    col_10_main_window = Col([get_item_hud(), get_table_container()], width=10,
                             id='my-content-window')
    return col_10_main_window


def get_side_menu():
    side_menu = Tabs(Tab(label='', tab_id='pctr_text'), id='side-menu-tabs',
                     active_tab='pctr_text')
    side_menu_col = Col(id='side-menu-col-2', style=VISIBILITY_HIDDEN, width=2, children=[H3('',
                                                                                             id='side-menu-header'),
                                                                                          side_menu])
    return side_menu_col



def get_table_container():
    table_container = Container(dt.DataTable(id='my-dash-data-table', fill_width=False,
                                             style_as_list_view=True, style_data={
                'whiteSpace': 'normal'
                },
                                             style_table={
                                                     'max-width': '1200px'
                                                     },
                                             style_cell={'color': 'black'}))
    return table_container


def get_main_layout(main_window_col_10, side_menu_col_2, top_navbar, bottom_navbar=None):
    """
    
    :param bottom_navbar: dash_bootstrap_components.Navbar 
    :param main_window_col_10: dash_bootstrap_components. 
    :param side_menu_col_2: dash_bootstrap_components.
    :param top_navbar: dash_bootstrap_components.Navbar
    :return: 
    """
    this_layout = Container([Row(
            Col(
                    [
                            top_navbar,
                            Row([
                                    side_menu_col_2, main_window_col_10
                                    ])
                            # ,bottom_navbar
                            ]

                    )
            )], fluid=True)
    return this_layout


def get_tabs_container(busgrps):
    """
    
    :param busgrps: main menu tabs 
    :return: Tab(id=str(busgrp_id)
    """
    tabs = [Tab(label=val, tab_id=str(key)) for key, val in busgrps.items()]
    tabs_container = Tabs(id='busgrp_ldesc-tabs', children=tabs, active_tab=tabs[0])
    return tabs_container


def get_item_hud(hud_title='LCL FORECAST ANALYSIS', hud_1_0='', hud_1_1='') \
        -> Container:
    """
    :param hud_title: str top of HUD
    :param hud_1_0: str Byline Position 1
    :param hud_1_1: str Byline Position 2
    
    :param
    hud_1_2: str
    :return: 
    Container: 'item-hud-container'
        Row
            Container:'item-hud-title-container'
                Col
                    H1: 'hud-title'
        Container: 'item-hud-byline-container'
            Row 
                Navbar: item-hud-bar'
                    NavItem:
                        H2: 'hud-1-0'
                        H2: hud-1-1'
            Row
                Tabs: 'table-tabs-nav'
                    Tab: 'tab-all
    """
    layout = Container(fluid=True, id='item-hud-container', children=
    [
            Row(
                    Container(

                            id='item-hud-title-container',
                            children=[
                                    Col(
                                            H1(id='hud-title', children=hud_title)
                                            )
                                    ]
                            )
                    ),
            Container(
                    id='item-hud-byline-container',
                    style=VISIBILITY_HIDDEN,
                    children=
                    [
                            Row(
                                    [
                                            Navbar(
                                                    id='item-hud-bar',
                                                    children=
                                                    [
                                                            NavItem
                                                                    (
                                                                    H2(hud_1_0, id='hud-1-0')
                                                                    ),
                                                            NavItem(
                                                                    H2(hud_1_1, id='hud-1-1')
                                                                    )
                                                            ]
                                                    )
                                            ]
                                    ),
                            Row(
                                    [
                                            Tabs(
                                                    id='table-tabs-nav',
                                                    children=[
                                                            Tab(tab_id='tab-all', label='All')
                                                            ],
                                                    )
                                            ], id='item-hub-tabs-row'
                                    )
                            ]
                    )
            , Div(id='datasource-1'), Div(id='datasource-2')]
                       )
    return layout
