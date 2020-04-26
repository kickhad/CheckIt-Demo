from app1.dicts import *


def init_cache(cache, view):
    lu = view.dicts
    cache.set(BUSGRP_ID__BUSGRP_LDESC, lu[BUSGRP_ID__BUSGRP_LDESC])
    cache.set(CACHE_EANUPC__LABEL_TEXT, lu[EANUPC__LABEL_TEXT])
    cache.set(BUSGRP_ID__PCTR_ID_DICT, lu[BUSGRP_ID__PCTR_ID_DICT])
    cache.set(CACHE_MAIN_DATAFRAME, view.df)
    cache.set(PCTR_ID__PCTR_TEXT, lu[PCTR_ID__PCTR_TEXT])
    cache.set(CACHE_MATERIALS_DATAFRAME, view.item_data)
    cache.set(CACHE_EANUPCS_LIST, view.eanupcs)
    return cache
