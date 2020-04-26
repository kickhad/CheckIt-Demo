from app1.dashmodels import EDI830, Material, PdpFcst, ProductIdCrossRef, TotalPlan
from app1.extensions.helpers import df_loader, get_lookup_dict, nan_floor, zero_int64

SERIES_INDEX_PREMELT = ['eanupc', 'material', 'MY_WEEK']
SERIES_INDEX_MELTED = ['eanupc', 'material', 'MY_WEEK', 'variable']


class Idatalayer(object):
    def eanupc_830__material_dict(self):
        df = df_loader(ProductIdCrossRef)
        df = df[(df.active == 1) & df.unit_factor == 1]
        ean830_dict = get_lookup_dict(df, 'eanupc_830', 'material')
        return ean830_dict

    def article__material_dict(self):
        df = df_loader(ProductIdCrossRef)
        df = df[(df.active == 1)]
        df = df.dropna(axis=0, subset=['article'])
        article_dict = get_lookup_dict(df, 'article', 'material')
        return article_dict

    def eanupc_830__unit_factor(self):
        df = df_loader(ProductIdCrossRef)
        df = df[(df.active == 1) & df.unit_factor == 1]
        ean830_dict_unit_factor = get_lookup_dict(df, 'eanupc_830', 'unit_factor')
        return ean830_dict_unit_factor

    def filter_df_daterange(self, df):
        df = df.loc[df.MY_WEEK.between(self.CURRENT_MY_WEEK, self.CURRENT_END_WEEK)]
        return df

    def material__eanupc_dict(self):
        df_mats = df_loader(Material)
        return get_lookup_dict(df_mats, 'material', 'eanupc')


    def eanupc__material_dict(self):
        df_mats = df_loader(Material)
        return get_lookup_dict(df_mats, 'eanupc', 'material')

    def __init__(self):
        from flask import current_app
        settings = current_app.config['SETTINGS']
        self.CURRENT_MY_WEEK = settings['CURRENT_MY_WEEK']
        self.TIMESTAMP_RECENT_EDI_TX = settings['TIMESTAMP_RECENT_EDI_TX']
        self.CURRENT_END_WEEK = settings['CURRENT_END_WEEK']


    def xAPO(self):
        dfapo = (
                df_loader(TotalPlan)
                    .pipe(self.filter_df_daterange)
        )
        dfapo.material = dfapo.material.astype('int64')
        dfapo['eanupc'] = dfapo.material.map(self.material__eanupc_dict())
        dfapo.eanupc = dfapo.eanupc.apply(zero_int64)

        dfapo = dfapo.rename(columns={
                'anon_1': 'SLS', 'dp_adj_base': 'COF'
                })
        dfapo.SLS = dfapo.SLS.apply(nan_floor)
        dfapo.COF = dfapo.COF.apply(nan_floor)
        cols = ['eanupc', 'material', 'MY_WEEK', 'SLS', 'COF']
        dfapo = (
                dfapo[cols]
                    .groupby(SERIES_INDEX_PREMELT)
                    .agg(sum)
                    .reset_index()
                    .melt(id_vars=SERIES_INDEX_PREMELT, value_vars=["SLS", "COF"])
                    .set_index(SERIES_INDEX_MELTED)

        )
        return dfapo


    def x830(self):

        df = (
                df_loader(EDI830, self.TIMESTAMP_RECENT_EDI_TX)
                    .pipe(self.filter_df_daterange)
                    .assign(material=lambda df: df.eanupc_830.map(self.eanupc_830__material_dict()))
                    .assign(unit_factor=lambda df: df.eanupc_830.map(
                        self.eanupc_830__unit_factor()))
                    .assign(EDI=lambda df: df.qty * df.unit_factor)
                    .assign(eanupc=lambda df: df.eanupc_830)
                    .dropna(subset=['material'], axis=0)
        )

        df = (


                df[['eanupc', 'material', 'MY_WEEK', 'EDI']]
                    .groupby(['eanupc', 'material', 'MY_WEEK'])
                    .sum()
                    .reset_index()
                    .astype({
                        'eanupc':   'int64',
                        'MY_WEEK': 'int64',
                        'material': 'int64',
                        })

        )

        df = (
                df.melt(id_vars=['eanupc', 'material', 'MY_WEEK'], value_vars=['EDI'])

                    .set_index(SERIES_INDEX_MELTED)
                    .astype({'value': 'int64'})
                    .loc[lambda df: df.value > 0]

        )
        return df


    def xPDP(self):
        dfpdp = (
                df_loader(PdpFcst)
                    .pipe(self.filter_df_daterange)
        )
        dfpdp = dfpdp.loc[:, ['article', 'firm_qty', 'est_qty', 'MY_WEEK']]
        dfpdp['PDP'] = dfpdp.firm_qty + dfpdp.est_qty
        dfpdp['eanupc'] = dfpdp.article.map(self.article__material_dict())
        dfpdp['material'] = dfpdp.eanupc.map(self.eanupc__material_dict())
        dfpdp = (
                dfpdp[["eanupc", "MY_WEEK", 'material', "PDP"]]
                    .groupby(SERIES_INDEX_PREMELT).agg(sum)
                    .reset_index()
                    .melt(id_vars=SERIES_INDEX_PREMELT, value_vars=["PDP"])
                    .set_index(SERIES_INDEX_MELTED)
                    .loc[lambda df: df.value > 0]

        )
        return dfpdp


    def xMaterial(self):
        df = df_loader(Material)
        return df

