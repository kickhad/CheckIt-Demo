# def by_sku_df(cache, eanupc):
#     eanupc = np.int64(eanupc)
#     df = (
# 
#             cache.get(CACHE_MAIN_DATAFRAME)
#                 .pipe(slicer, eanupc=eanupc)
#                 .droplevel(['eanupc', 'pctr_id', 'busgrp_id'], axis=0)
#                 .rename({'value': 'w'})
#                 .unstack('MY_WEEK', fill_value=0)
#                 .reset_index()
#                 .pipe(weekize_column_labels)
# 
# 
#     )
#     labels = ['PDP', 'SLS', 'LFT', 'COF', 'EDI']
#     cols = [{'name': x, 'id': x, 'selectable': False} for x in df.columns]
#     data = df.to_dict('records')
#     return cols, data
# 

def weekize_column_labels(df):
    df.columns = [collapse_col(i) for i in list(df.columns)]
    return df


def collapse_col(col):
    term0 = col[0]
    if term0 == 'value':
        term0 = 'w'
    return term0 + str(col[1])


# def int_zeros_to_empty_string(data):
#     for mydict in data:
#         for key, item in mydict.items():
#             if item == 0:
#                 mydict[key] = ''
#     return data
def id_safe(val):
    return val.replace(' ', '')
