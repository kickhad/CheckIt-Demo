from flask_sqlalchemy import BaseQuery
from sqlalchemy import BIGINT, BigInteger, Boolean, DECIMAL, Float, INTEGER, Integer
from sqlalchemy.orm import column_property, synonym

from app1.extensions import db


class FilteredTotalPlan(BaseQuery):
    def filtered(self, val=None):
        return self.filter(TotalPlan.csc == 1)


class FilteredPdpFcst(BaseQuery):
    def filtered(self, val=None):
        return self.filter(PdpFcst.recent == 1)


class FilteredEDI830(BaseQuery):
    def filtered(self, val):
        return self.filter(EDI830.txdate == val)


class Material(db.Model):
    __tablename__ = 'IT_LOC_CANADA_PLANNING_LCL_L_PRODUCT'
    material = db.Column('MATERIAL_ID', db.Integer, primary_key=True)
    eanupc = db.Column('EANUPC', db.BigInteger)
    article = db.Column('ARTL_NUM', db.BigInteger)
    busgrp_id = db.Column('GL_BUSGRP_ID', db.Integer)
    busgrp_ldesc = db.Column('GL_BUSGRP_LDESC', db.String(40, 'SQL_Latin1_General_CP1_CI_AS'))
    desc = db.Column('MATERIAL_DESC', db.String(51, 'SQL_Latin1_General_CP1_CI_AS'))
    active = db.Column('ACTIVE', db.SMALLINT)
    pctr_text = db.Column('GL_PCTR_TEXT', db.String(72, 'SQL_Latin1_General_CP1_CI_AS'))
    pctr_id = db.Column('GL_PCTR_ID', db.Integer)
    upc_desc = db.Column('UPC_DESC', db.String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    unit_factor = db.Column('UNIT_FACTOR', db.Numeric(18, 3), nullable=False)


class PdpFcst(db.Model):
    # __bind_key__ = 'db002'
    __tablename__ = 'IT_LOC_CANADA_PLANNING_LCL_F_PDP'
    posted_week = db.Column('POST_CAL_WK_ID', BigInteger, primary_key=True)
    dcid = db.Column('DC_ID', BigInteger, primary_key=True)
    article = db.Column('ARTL_NUM', BigInteger)
    firm_qty = db.Column('FIRM_QTY', Integer)
    est_qty = db.Column('EST_QTY', Integer)
    dno = db.Column('DNO_FLAG', Boolean)
    hbc = db.Column('HBC_FLAG', Integer)
    MY_WEEK = db.Column('MY_WEEK_ID', BigInteger)
    recent = db.Column('IS_CURRENT', Boolean)
    query_class = FilteredPdpFcst


class TotalPlan(db.Model):
    __tablename__ = 'IT_LOC_CANADA_PLANIT_LCL_F_TOTPLAN'
    # __bind_key__ = 'db002'
    MY_WEEK = db.Column('MY_WEEK_ID', Integer, primary_key=True)
    material = db.Column('MATERIAL_ID', BigInteger)
    promo_sls_adj_base = db.Column('x_Z1006', Float)
    xlift = db.Column('x_Z1007', Float)
    cof_qty = db.Column('COF_QTY', DECIMAL)
    sls_tot_base = db.Column('x_Z1009', Float)
    # TODO add in LFT column
    cy_act_vol = db.Column('ZCYACT', Float)
    # cof_amt = db.Column('COF_AMT', DECIMAL)
    sls_qty = column_property(sls_tot_base + xlift)
    sls = synonym('sls_qty')
    csc = db.Column('CSC', Boolean)
    query_class = FilteredTotalPlan


class EDI830(db.Model):
    __tablename__ = 'IT_LOC_CANADA_EDI_LCL_F_EDI830'
    txdate = db.Column('TX_DATE', BIGINT, primary_key=True)
    dcid = db.Column('DC_ID', INTEGER, primary_key=True)
    eanupc = db.Column('EANUPC', BIGINT, primary_key=True)
    MY_WEEK = db.Column('MY_WEEK_ID', INTEGER, primary_key=True)
    qty = db.Column('QTY', INTEGER)
    query_class = FilteredEDI830


class time_lkp(db.Model):
    __tablename__ = 'IT_LOCACCT_LCL_TIME_LKP',
    MY_WEEK = db.Column('MY_WEEK_ID', db.BigInteger, primary_key=True)
    scj_month = db.Column('scj_month_id', db.BigInteger)
    lcl_week = db.Column('LCL_WEEK', db.BigInteger)


class config_settings(db.Model):
    __tablename__ = 'IT_LOC_CANADA_PLANNING_CONFIG'
    kwarg = db.Column('KEYWORD', db.String(50, 'SQL_Latin1_General_CP1_CI_AS'),
                      nullable=False, primary_key=True)
    kwval = db.Column('VALUE', db.String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    dtype = db.Column('DTYPE', db.String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    

           

    # class Material: # upc = db.Column('UPC_ID', db.BigInteger)
    # db.Column('MAT_GRP1_ID', db.String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    # db.Column('GL_CAT_ID', db.Integer)
    # db.Column('MAT_GRP1_DESC', db.String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    # db.Column('GL_SEG_ID', db.Integer),
    # db.Column('GL_CAT_LDESC', db.String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    # db.Column('GL_SUBSEG_ID', db.Integer),
    # db.Column('GL_SUBSEG_LDESC', db.String(40, 'SQL_Latin1_General_CP1_CI_AS')),
