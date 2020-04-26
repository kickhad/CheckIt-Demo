import logging
from urllib import parse
import os
import dash
import numpy as np
from dash import callback_context
from dash.dependencies import Input, State
from dash.dependencies import Output
from dash_bootstrap_components import Tab
from flask import current_app
from flask_caching import Cache

from app1.dashapp.callbacks.caching import init_cache
from app1.dashapp.callbacks.datatable import weekize_column_labels
from app1.dashapp.callbacks.hud import get_hud_title
from app1.dashapp.callbacks.sidetabs import get_new_side_tabs
from app1.dashapp.funcs import slicer
from app1.dicts import *
from app1.extensions.helpers import coef_var_from_col_idxs

logger = logging.getLogger('view')
table_update = namedtuple('table_update_settings', ['data', 'style', 'columns'])
cache = None
VISIBILITY_HIDDEN = {'visibility': 'hidden'}
VISIBILITY_VISIBLE = {'visibility': 'visible'}
TIMEOUT = 90
LONG_TIMEOUT = 120


def register_callbacks(dashapp, view):
    cache = Cache(dashapp.server,
                  config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': os.environ['CACHE_DIR']})
    cache = init_cache(cache, view)

    settings = current_app.config['SETTINGS']
    coef_range = [settings['ABS_VAR_COEF_{}_VAL'.format(i)] for i in range(0, 4)]
    color_dict = {i: settings['ABS_VAR_COEF_{}_COLOR'.format(i)] for i in range(0, 5)}


    @dashapp.callback([Output('side-menu-tabs', 'children'), Output('side-menu-header',
                                                                    'children'),
                       Output('side-menu-col-2', 'style')],
                      [Input('busgrp_ldesc-tabs', 'active_tab')])
    def busgrp_tabs__activetab___side_nav__children(busgrp_str):
        '''
        Callback. Top menu selection updates & its Label 
        :type busgrp_str: str
        :returns list(dash_bootstrap_components.Tab), str
        '''
        try:
            busgrp_id = np.int64(busgrp_str)
            tabs = get_new_side_tabs(cache, busgrp_id=busgrp_id)
            logger.log(10,
                       'SUCCESS! Side Tabs updated successfully for {}'.format(busgrp_str))
            return tabs, 'PROFIT CENTER', VISIBILITY_VISIBLE
        except Exception as ex:
            logger.log(10,
                       'WARNING: Side Tabs update failed. Was this just page loading? : key {} '
                       '\n\t\t '
                       ''.format(
                               busgrp_str, ex))
            raise dash.exceptions.PreventUpdate


    @dashapp.callback([Output('my-dash-data-table', 'data'), Output('my-dash-data-table',
                                                                    'columns'),
                       Output('my-dash-data-table',
                              'style_data_conditional'),
                       Output('item-hud-byline-container', 'style'),

                       Output('hud-title', 'children'),
                       Output('table-tabs-nav', 'children')
                       ],
                      [Input('side-menu-tabs',
                             'active_tab'), Input('table-tabs-nav', 'active_tab')],
                      [State('table-tabs-nav', 'children')])
    def side_nav__active_tab___datatable_data(rows, sku, state):
        try:

            trigger = callback_context.triggered[0]['prop_id']
            if trigger == 'side-menu-tabs.active_tab' or sku == 'all':
                pctr_id = np.int64(rows)
                cols, data = by_pctr_df(get_pctr_df(), pctr_id)
                hud_tabs = get_sku_tabs_by_pctr(cache, pctr_id)
                hud_title = get_hud_title(cache, pctr_id=pctr_id)
                return data, cols, None, VISIBILITY_VISIBLE, hud_title, hud_tabs
            else:
                eanupc = np.int64(sku)
                table = by_sku_df(get_sku_df(), eanupc)
                hud_tabs = state
                hud_title = '\n'.join([str(i) for i in cache.get(CACHE_EANUPC__LABEL_TEXT)[int(
                        sku)]])
                return table.data, table.columns, table.style, VISIBILITY_VISIBLE, hud_title, \
                       hud_tabs


        except Exception as ex:
            raise dash.exceptions.PreventUpdate

    @dashapp.callback(Output('download-link', 'href'), [Input('download-link', 'n-clicks')])
    def download_df(link):

        data = (
                cache.get(CACHE_MAIN_DATAFRAME)
                    .unstack(level='MY_WEEK')
                    .replace(0, np.nan)
                    .reset_index()
                    .pipe(weekize_column_labels)
                    .to_csv(index=False,
                            encoding='utf-8')
        )
        csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + parse.quote(data)
        return csv_string


    # @cache.cached(timeout=LONG_TIMEOUT,key_prefix='by_pctr_df')
    def get_pctr_df():
        df = (
                cache.get(CACHE_MAIN_DATAFRAME)
                    .groupby(level=['MY_WEEK', 'pctr_id', 'variable'])
                    .sum()
        )

        return df

    def get_sku_df():
        df = (
                cache.get(CACHE_MAIN_DATAFRAME)
                    .droplevel(['busgrp_id'], axis=0)
                # .sort_index()
        )
        return df

        # @cache.memoize(timeout=TIMEOUT)

    # noinspection PyRedundantParentheses
    def get_sku_tabs_by_pctr(cache, pctr_id):
        df = (
                cache.get('df_materials')[['material', 'eanupc', 'pctr_id', 'desc']]
                    .loc[lambda df: (df.pctr_id == pctr_id)]
                    .assign(label=lambda df: df.material.astype('str') + '\n' + df.desc)

        )
        tabs = [Tab(tab_id='all', label='All')]
        for label in df.itertuples():
            tabs.append(Tab(tab_id=str(label.eanupc), label=label.label[:25]))

        return tabs


    # @cache.memoize(timeout=TIMEOUT)
    def by_pctr_df(df, pctr_id):
        df = (
                df.pipe(slicer, pctr_id=pctr_id)
                    .copy()
                    .droplevel(level=['pctr_id'])
                    .unstack('MY_WEEK', fill_value=0)
                    .T

        )
        df['tmp'] = df.apply(lambda x: list(x), axis=1)
        df['VAR'] = df.tmp.apply(lambda x: coef_var_from_col_idxs(x, coef_range.copy()))
        df = (
                df.drop('tmp', axis=1)
                    .T
                    .reset_index()
                    .pipe(weekize_column_labels)
        )

        cols = [{'name': x, 'id': x, 'selectable': False} for x in df.columns]
        data = df.to_dict('records')
        return cols, data

    def by_sku_df(df, sku):


        df = (
                df.pipe(slicer, eanupc=sku)
                    .copy()
                    .droplevel(level=['eanupc', 'pctr_id'])
                    .unstack('MY_WEEK', fill_value=0)
                    .T
                    .assign(tmp=lambda df: df.apply(lambda x: list(x), axis=1))
        )
        df['', 'VAR'] = df.tmp.apply(lambda x: coef_var_from_col_idxs(x, coef_range.copy()))
        df = (
                df.drop('tmp', axis=1)
                    .T
                    .reset_index()
                    .pipe(weekize_column_labels)

        )
        cols = [{'name': x, 'id': x, 'selectable': False} for x in df.columns]
        data = df[df.variable != 'VAR'].to_dict('records')
        style = stylize(df[df.variable == 'VAR'], 2, cols)

        return table_update(data=data, style=style, columns=cols)

    def stylize(df, n_header_cols, cols):
        x = n_header_cols
        eids = df.T.iloc[x:, 0].tolist()
        style_dict = {}
        for eid in range(0 + x, len(eids)):
            style_dict[eid] = color_dict[eids[eid]]

        style = [
                {
                        'if':              {'column_id': cols[key]['id'], },
                        'backgroundColor': val
                        } for key, val in style_dict.items()]
        return style

    # @dashapp.callback(Output('nav', 'active'),[Input('search-box', 'value'),
    #                                                   Input('search-button','n-clicks')])
    # def generate_layout(url):
    #     pass 
    #
