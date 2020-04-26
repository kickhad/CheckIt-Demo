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
    #__tablename__ = 'IT_LOC_CANADA_PLANNING_MATERIAL_LKP_CA'
    material = db.Column('MATERIAL_ID', db.Integer, primary_key=True)
    eanupc = db.Column('EANUPC', db.BigInteger)
    article = db.Column('ARTL_NUM', db.BigInteger)
    busgrp_id = db.Column('GL_BUSGRP_ID', db.Integer)
    busgrp_ldesc = db.Column('GL_BUSGRP_LDESC', db.String(40, 'SQL_Latin1_General_CP1_CI_AS'))
    desc = db.Column('MATERIAL_DESC', db.String(51, 'SQL_Latin1_General_CP1_CI_AS'))
    pctr_text = db.Column('GL_PCTR_TEXT', db.String(72, 'SQL_Latin1_General_CP1_CI_AS'))
    pctr_id = db.Column('GL_PCTR_ID', db.Integer)
    upc_desc = db.Column('UPC_DESC', db.String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class PdpFcst(db.Model):
    #__tablename__ = 'IT_LOC_CANADA_PLANNING_LCL_F_PDP'
    posted_week = db.Column('POST_CAL_WK_ID', BigInteger, primary_key=True)
    dcid = db.Column('DC_ID', BigInteger, primary_key=True)
    article = db.Column('ARTL_NUM', BigInteger)
    firm_qty = db.Column('FIRM_QTY', Integer)
    est_qty = db.Column('EST_QTY', Integer)
    lcl_fcst_week = db.Column('FORECAST_WEEK', BigInteger)
    recent = db.Column('IS_CURRENT', Boolean)
    MY_WEEK = db.Column('MY_WEEK_ID', db.Integer)
    query_class = FilteredPdpFcst


class ProductIdCrossRef(db.Model):
    #__tablename__ = 'IT_LOC_CANADA_PLANNING_LCL_L_PRODUCT_ID'
    eanupc = db.Column('EANUPC', db.BigInteger, primary_key=True, nullable=False)
    material = db.Column('MATERIAL_ID', db.BigInteger, primary_key=True, nullable=False)
    article = db.Column('ARTL_NUM', db.BigInteger)
    eanupc_830 = db.Column('EANUPC_830', db.BigInteger)
    unit_factor = db.Column('UNIT_FACTOR', db.Float)
    active = db.Column('ACTIVE', db.SmallInteger)


class TotalPlan(db.Model):
    #__tablename__ = 'IT_LOC_CANADA_PLANIT_LCL_F_TOTPLAN'
    MY_WEEK = db.Column('MY_WEEK_ID', Integer, primary_key=True)
    material = db.Column('MATERIAL_ID', BigInteger)
    promo_sls_adj_base = db.Column('x_Z1006', Float)
    xlift = db.Column('x_Z1007', Float)
    dp_adj_base = db.Column('x_Z1005', DECIMAL)
    sls_tot_base = db.Column('x_Z1009', Float)
    sls_qty = column_property(sls_tot_base + xlift)
    sls = synonym('sls_qty')
    csc = db.Column('CSC', Boolean)
    query_class = FilteredTotalPlan
    
class configs(db.Model):
    kw = db.Column('KEYWORD', db.String(40),primary_key=True)
    val = db.Column('VALUE', db.String(40))
    


class EDI830(db.Model):
    #__tablename__ = 'IT_LOC_CANADA_EDI_LCL_F_EDI830'
    txdate = db.Column('TX_DATE', BIGINT, primary_key=True)
    dcid = db.Column('DC_ID', INTEGER, primary_key=True)
    eanupc_830 = db.Column('EANUPC_830', BIGINT, primary_key=True)
    MY_WEEK = db.Column('MY_WEEK_ID', INTEGER, primary_key=True)
    qty = db.Column('QTY', INTEGER)
    query_class = FilteredEDI830


class time_lkp(db.Model):
    #__tablename__ = 'IT_LOCACCT_LCL_TIME_LKP'
    MY_WEEK = db.Column('MY_WEEK_ID', db.BigInteger, primary_key=True)
    lcl_week = db.Column('LCL_WEEK', db.BigInteger)
    lcl_week_start_date = ('LCL_WEEK_START_DATE', db.BigInteger)
