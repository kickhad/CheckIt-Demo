import dash_bootstrap_components as dbc

from app1.dicts import *


def get_new_side_tabs(cache, busgrp_id=None) -> [dbc.Tabs]:
    tab_ids = cache.get(BUSGRP_ID__PCTR_ID_DICT)[busgrp_id]
    tab_labels = cache.get(PCTR_ID__PCTR_TEXT)
    tabs = [dbc.Tab(tab_id=str(i), label=tab_labels[i], tabClassName='side-menu-tab')
            for i
            in tab_ids]
    return tabs
