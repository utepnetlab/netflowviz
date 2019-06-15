#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 10:52:37 2019

@author: Carlos Alcantara
"""

import pandas as pd
from math import nan
import country
import organization
import drilldownHist
import sys

def countryDriver(filename, src, dst, outputFileName):
    df = pd.read_csv(filename)
    df = df.replace(nan,'unknown')
    Csrcval = src
    Cdstval = dst

    dfcountry = df[(df['src_continent'] == Csrcval) & (df['dst_continent'] == Cdstval)]

    c_ind = list(dfcountry['src_country'].unique())
    c_col = list(dfcountry['dst_country'].unique())
    c_dfFlows = pd.DataFrame(index = c_ind, columns = c_col, data = 0)
    dftest = dfcountry.groupby(['src_country','dst_country']).size()
    for x in dftest.index.values.tolist():
        c_dftemp = dfcountry[(dfcountry['src_country'] == x[0]) & (dfcountry['dst_country'] == x[1])]
        c_dfFlows.at[[x[0]],[x[1]]] = len(c_dftemp)

    #   rename column
    c_dfFlows.columns.name = Cdstval

    #   create df to be visualized
    dfViz = pd.DataFrame(c_dfFlows.stack(), columns=['value']).reset_index()
    dfViz.columns=['src_country','dst_country','value']
    
    if ( len(dfViz.index) == 1 ):
        print('skip to org level')
        orgDriver(filename, c_ind[0], c_col[0], outputFileName)
    else:
        print('normal country level')
        country.main(filename, src, dst, outputFileName)
        
        
        
def orgDriver(filename, src, dst, outputFileName):
    df = pd.read_csv(filename)
    df = df.replace(nan,'unknown')


    ###########################################################################################
    #####################################   CREATE DF   #######################################


    Csrcval = src
    Cdstval = dst

    dfcountry = df[(df['src_country'] == Csrcval) & (df['dst_country'] == Cdstval)]

    c_ind = list(dfcountry['src_org'].unique())
    c_col = list(dfcountry['dst_org'].unique())
    c_dfFlows = pd.DataFrame(index = c_ind, columns = c_col, data = 0)
    dftest = dfcountry.groupby(['src_org','dst_org']).size()
    for x in dftest.index.values.tolist():
        c_dftemp = dfcountry[(dfcountry['src_org'] == x[0]) & (dfcountry['dst_org'] == x[1])]
        c_dfFlows.at[[x[0]],[x[1]]] = len(c_dftemp)

    #   rename column
    c_dfFlows.columns.name = Cdstval

    #   create df to be visualized
    dfViz = pd.DataFrame(c_dfFlows.stack(), columns=['value']).reset_index()
    dfViz.columns=['src_org','dst_org','value']
    
    if ( len(dfViz.index) == 1 ):
        print('skip to hist level')
        drilldownHist.main(filename, c_ind[0], c_col[0], outputFileName)
    else:
        print('continue to org level')
        organization.main(filename, src, dst, outputFileName)

csvfile = sys.argv[1]
src = sys.argv[2]
dst = sys.argv[3]
outfile = sys.argv[4]

if (outfile == 'views/country.ejs'):
    countryDriver(csvfile, src, dst, outfile)
elif (outfile == 'views/org.ejs'):
    orgDriver(csvfile, src, dst, outfile)
else:
    drilldownHist.main(csvfile, src, dst, outfile)