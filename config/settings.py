import numpy as np
import pandas as pd


def get_settings(uri):
    df = pd.read_sql_table('configs', con=uri)
    settings = {}
    for x in df.itertuples():
        val = x.VALUE
        key = x.KEYWORD
        try:
            settings[key] = np.float(val)
            if settings[key].is_integer():
                settings[key] = int(val)
        except:
            settings[key] = val
    return settings


'''
KEYWORD
TIMESTAMP_RECENT_EDI_TX
CURRENT_MY_WEEK
CURRENT_END_WEEK
ABS_VAR_COEF_0_VAL
ABS_VAR_COEF_1_VAL
ABS_VAR_COEF_2_VAL
ABS_VAR_COEF_3_VAL
ABS_VAR_COEF_4_VAL
ABS_VAR_COEF_0_COLOR
ABS_VAR_COEF_1_COLOR
ABS_VAR_COEF_2_COLOR
ABS_VAR_COEF_3_COLOR
ABS_VAR_COEF_4_COLOR
'''
