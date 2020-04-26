import logging

import numpy as np

from app1.dashmodels import Material
from app1.dicts import *
from app1.extensions import helpers as hfx
# import df_loader, nan_floor, apply_dict, nan_upper,  zero_int64, df_scrub
from app1.extensions.helpers import get_lookup_dict, get_lookup_dict_lists
from app1.viewmodel.datalayer import Idatalayer

# x830, xAPO, self.xMaterial, xPDP

data_logger = logging.getLogger('main')

class DashView(object):
    def concat_series(self) -> pd.DataFrame:
        df = pd.concat([self.x830(), self.xAPO(), self.xPDP()])
        return df

    def get_eanupc_to_desc_dict(self):
        return (
                self.df_mats.loc[:, ['desc', 'eanupc', 'material']]
                    .set_index('eanupc')
                    .apply(lambda df: list(df), axis=1)
                    .to_dict()
        )
    
    
    def material__eanupc_dict(self):
        df_mats = self.xMaterial()
        return get_lookup_dict(df_mats, 'material', 'eanupc')


    def eanupc__material_dict(self):
        df_mats = self.xMaterial()
        df_mats = df_mats[df_mats.active]
        return get_lookup_dict(df_mats, 'eanupc', 'material')


    def eanupc__busgrp_id_dict(self):
        df_mats = self.xMaterial()
        df_mats = df_mats[df_mats.active]
        return get_lookup_dict(df_mats, 'eanupc', 'busgrp_id')


    def eanupc__pctr_id_dict(self):
        df_mats = self.xMaterial()
        df_mats = df_mats[df_mats.active]
        return get_lookup_dict(df_mats, 'eanupc', 'pctr_id')


    def _load_df(self):
        df = self.concat_series()
        fxns = [hfx.df_drop_zeros, hfx.df_index_zeros]
        df = hfx.df_scrub(df, fxns)
        df = df[df.value > 0]
        self.dicts[EANUPC_TO_BUSGRP_ID_DICT] = get_lookup_dict(self.df_mats, 'eanupc', 'busgrp_id')
        self.dicts[EANUPC_TO_PCTR_ID_DICT] = get_lookup_dict(self.df_mats, 'eanupc', 'pctr_id')
        df = df.reset_index()
        df['busgrp_id'] = df.eanupc.map(self.dicts[EANUPC_TO_BUSGRP_ID_DICT])
        df['pctr_id'] = df.eanupc.map(self.dicts[EANUPC_TO_PCTR_ID_DICT])
        df.astype(
                {
                        'busgrp_id': 'int64', 'pctr_id': 'int64', 'MY_WEEK'
                :                    'int64'
                        }
                )
        df = df.set_index(['eanupc', 'material', 'MY_WEEK', 'busgrp_id', 'pctr_id', 'variable'])

        self.df = df
        return df


    def meta_refresh(self):
        df = self.df.reset_index()
        df = df[['eanupc', 'value']]
        eanupcs = (
                df.groupby(by=['eanupc'])
                    .sum()
                    .reset_index()
                    .eanupc
                    .tolist()
        )
        # TODO handler for the 0s
        eanupcs = [i for i in eanupcs if i != 0]
        self.eanupcs = eanupcs

        # self._get_dicts()


    def _load_item_data(self):
        df_mats = hfx.df_loader(Material)
        df_mats = df_mats[df_mats.eanupc.isin(self.eanupcs)].copy()
        self.dicts[EANUPC__LABEL_TEXT] = self.get_eanupc_to_desc_dict()
        self.dicts[EANUPC_TO_DESC_DICT] = get_lookup_dict(df_mats, 'eanupc', 'desc')
        self.dicts[BUSGRP_ID__PCTR_ID_DICT] = get_lookup_dict_lists(df_mats, 'busgrp_id', 'pctr_id')
        self.dicts[PCTR_ID__EANUPCS] = get_lookup_dict_lists(df_mats, 'pctr_id', 'eanupc')
        self.dicts[PCTR_ID__PCTR_TEXT] = get_lookup_dict(df_mats, 'pctr_id', 'pctr_text')
        self.dicts[BUSGRP_ID__BUSGRP_LDESC] = get_lookup_dict(df_mats, 'busgrp_id', 'busgrp_ldesc')
        # self.dicts[] = get_lookup_dict(df_mats, )
        self.item_data = df_mats
        return self.item_data


    def _get_multiindex(self):
        df = (
                self.df
                    .reset_index()
                    .drop('variable', axis=1)
                    .drop_duplicates()
                    .set_index(['eanupc', 'material', 'MY_WEEK', 'busgrp_id', 'pctr_id'])
        )
        tups = []
        for x in df.index:
            for var in ORDERED_DF_VARIABLES:
                # tups.append(x + (busgrps[x[0]], pctrs[x[0]],))
                tups.append(x + (var,))
        idx = pd.MultiIndex.from_tuples(tups, names=['eanupc', 'material', 'MY_WEEK',
                                                     'busgrp_id', 'pctr_id', 'variable'])
        return idx


    def _get_df(self):
        idx = self._get_multiindex()
        df = self.df
        df = df[df.value > 0]
        csc_premerge = df.value.sum()
        df = df.reindex(
                # labels=['eanupc', 'material', 'MY_WEEK', 'variable'],
                index=idx,
                fill_value=np.nan)
        # df = hfx.df_index_zeros(df, 'busgrp_id')
        df = df[~df.index.duplicated()]
        csc_postmerge = df.value.sum()
        # self.meta_refresh(df)
        df.value = df.value.apply(hfx.zero_int64)

        if not csc_postmerge == csc_premerge:
            pass
    
        # TODO Needs an upstream week filter        
        self.df = df


    def __init__(self, app=None):
        self.df = pd.DataFrame()
        # self.item_data = pd.DataFrame()
        self.eanupcs = []
        self.dicts = {}
        datalayer = Idatalayer()
        self.x830 = datalayer.x830
        self.xAPO = datalayer.xAPO
        self.xMaterial = datalayer.xMaterial
        self.xPDP = datalayer.xPDP
        self.df_mats = self.xMaterial()
        self._load_df()
        self.meta_refresh()
        self._load_item_data()
        self._get_df()


    def ItemLabels(self):
        return self.dicts[EANUPC_TO_DESC_DICT]
