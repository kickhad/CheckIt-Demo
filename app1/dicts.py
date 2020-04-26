from collections import namedtuple

import pandas as pd

ITEM_HEADER_COLS = {
        'material': 'SCJ Item', 'eanupc': 'Case UPC', 'desc': 'Product Desc',
}
DASHVIEW_GET_DF_DF_SORT_MAP = {
        'edi' : 0,
        'pdp' : 1,
        'sls' : 2,
        'cof' : 3
}
dict_ean_week_type = {
        'eanupc' : 'int64',
        'MY_WEEK': 'int64',
        'material':'int64'
}
DASH_VIEW_GET_DF_ASTYPE = {
        'value': 'int64', 'eanupc': 'int64',

}
ORDERD_DF_INDEX_LIST = ['eanupc', 'material', 'MY_WEEK', 'variable', 'busgrp_id', 'pctr_id']
ORDERED_DF_VARIABLES = ['EDI', 'PDP', 'SLS', 'LFT', 'COF']
DF_ORDERED_VARIABLES_PD_CAT_DTYPE = pd.CategoricalDtype(
        categories=['EDI', 'PDP', 'SLS', 'COF'], ordered=True)
nt = namedtuple('slicers', ['busgrp_ldesc', 'pctr_text'])
EANUPC_TO_BUSGRP_ID_DICT = 'eanupc_to_busgrp_id'
EANUPC_TO_DESC_DICT = 'EANUPC_TO_DESC_DICT'
EANUPC_TO_PCTR_ID_DICT = 'EANUPC_TO_PCTR_ID_DICT'
BUSGRP_ID__PCTR_ID_DICT = 'BUSGRP_ID__PCTR_ID_DICT'
PCTR_ID__EANUPCS = 'PCTR_ID__EANUPCS'
CACHE__BUSGRP_ID__BUSGRP_LDESC = 'Busgrps'
CACHE__BUSGRPS__PROFIT_CENTRE_DICT = 'BusGrp to Pctr'
CACHE_MAIN_DATAFRAME = 'Main Dataframe'
CACHE__PCTR_ID__PCTR_TEXT = 'Pctr Labels'
CACHE_MATERIALS_DATAFRAME = 'df_materials'
CACHE_EANUPCS_LIST = 'eanupcs'
PCTR_ID__PCTR_TEXT = 'PCTR_ID__PCTR_TEXT'
BUSGRP_ID__BUSGRP_LDESC = 'BUSGRP_ID__BUSGRP_LDESC'
EANUPC__LABEL_TEXT = 'EANUPC__LABEL_TEXT'
CACHE_EANUPC__LABEL_TEXT = 'CACHE_EANUPC__LABEL_TEXT'
