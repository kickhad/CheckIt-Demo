import logging

import pandas as pd
from dash.exceptions import InvalidIndexException



idx = pd.IndexSlice


y = 1


def slicer(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    slice_args = {}
    for level_name in df.index.names:
        try:
            slice_args[level_name] = kwargs[level_name]
        except:
            slice_args[level_name] = slice(None)

    try:
        df = df.loc[tuple(slice_args.values()), :]

    except KeyError as kerr:
        fn = log_dataframe(df)
        # logger.log(10, 'KEY ERROR: DataFrame dumped to {}'.format(fn))
        raise InvalidIndexException(kerr.args)
            
    except Exception as ex:
        fn = log_dataframe(df)
        # logger.log(10, 'Unknown error. DataFrame dumped to {}'.format(
        #         __name__, fn))

    return df
