import logging

logger = logging.getLogger('dataops')

import numpy as np
import pandas as pd
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.attributes import InstrumentedAttribute


def df_scrub(df: pd.DataFrame, funcs: list) -> pd.DataFrame:
    for fxn in funcs:
        df = fxn(df)

    return df


def df_drop_zeros(df: pd.DataFrame, col: str = 'value') -> pd.DataFrame:
    df = df[df[col] > 0]
    return df


def df_index_zeros(df: pd.DataFrame, col: str = 'eanupc') -> pd.DataFrame:
    dd = df.copy()
    dd = dd.reset_index()
    dd = dd.set_index('value')
    droplist = list(dd[dd[col] == 0].itertuples(index=False, name=None))
    df = df.astype('float')
    df = df.drop(droplist)
    logger.debug('Remove ids @ 0 Droplist = {}'.format(droplist[:10]))
    df.value = df.value.apply(zero_floor)
    return df


def zero_int64(val):
    try:
        return np.int64(val)
    except ValueError:
        return 0


def df_remap(modob):
    mapper = {}
    for x in dir(modob):
        db_fld = getattr(modob, x)
        if type(db_fld) == InstrumentedAttribute:
            mapper[db_fld.property.expression.description] = x
    return mapper


def df_loader(qry, params=None):
    tst = getattr(qry, 'query_class')
    if tst == BaseQuery:
        df = pd.read_sql(qry.query.statement, qry.query.session.bind)
    else:
        df = pd.read_sql(qry.query.filtered(params).statement, qry.query.session.bind)
    df = df.rename(columns=df_remap(qry))
    return df.copy(deep=True)


def list_to_chunks(my_list, n):
    return [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n)]


def rank_coef(val: float, static_range: list) -> int:
    static_range.append(val)
    static_range.sort()
    return static_range.index(val)


def coef_var_from_col_idxs(values, coef_range):
    pop_n = []
    try:
        chunks = list_to_chunks(values, 5)
        for x in chunks:
            [pop_n.append(i) for i in [x[0], x[1] + x[3], x[4]]]
        ser = pd.Series(pop_n)
        return rank_coef(ser.std() / ser.mean(), coef_range)
    except:
        return 0


def nan_floor(val):
    try:
        return np.int64(val)
    except Exception as ex:
        # logging.debug('nan_floor error val in : %s' % val)
        return np.nan


def zero_floor(val):
    try:
        return np.int64(val)
    except Exception as ex:
        # logging.debug('nan_floor error val in : %s' % val)
        return 0


def get_lookup_dict(df_mats, key_id, value_id) -> dict:
    return (
            df_mats[[key_id, value_id]]
                .drop_duplicates()
                .set_index(key_id)
                .to_dict()[value_id]
    )


def get_lookup_dict_lists(df_mats, key_id, value_id) -> dict:
    return (
            df_mats[[key_id, value_id]]
                .drop_duplicates()
                .groupby(by=key_id)
                .agg(lambda df: list(df))
                .to_dict()[value_id]
    )
