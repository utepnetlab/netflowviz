#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 16:35:56 2018

@author: Carlos Alcantara
"""

import pandas as pd
from math import nan
import seaborn as sns
import matplotlib.pyplot as plt

def main(filename, src, dst, outputFileName):
    df = pd.read_csv(filename)
    df = df.replace(nan,'unknown')
    
    
    ###########################################################################################
    #####################################   CREATE DF   #######################################
    
    
    Csrcval = src
    Cdstval = dst
    
    df_org = df[(df['src_org'] == Csrcval) & (df['dst_org'] == Cdstval)]
    
    c_ind = list(df_org['app'].unique())
    c_dfOcts = pd.DataFrame(index = c_ind, columns = ['value'], data = 0)
    dftest = df_org.groupby(['app']).size()
    for x in dftest.index.values.tolist():
        c_dftemp = df_org[(df_org['app'] == x)]
        c_dfOcts.at[x] = c_dftemp['dOctets'].sum()

    ratio = len(c_ind)/30
    if ratio < 1:
        ratio = 1
        
    if len(c_ind) > 1:
        g = sns.catplot(x="app", y="dOctets", data=df_org, kind="bar", ci=None, height=8.27, aspect=ratio)
        plt.title("Traffic from " + src + " to " + dst)
    else :
        g = sns.catplot(x="app", y="dOctets", data=df_org, kind="swarm", height=8.27, aspect=ratio)
        plt.title("Traffic from " + src + " to " + dst)
    g.set_xticklabels(rotation = 45, ha="right")
    g.savefig('public/hist.svg')
    
    if (outputFileName != 'views/hist.ejs'):
        file = open(outputFileName, "w")
        html = '''
            <!--
            Author: Carlos Alcantara
            Index.html page for Data Visualization map creation
            Version 2.0
            -->
            <html>
              <head>
                <title>Drilldown Bottom Level</title>
              </head>
              <body>
                <h1>Netflow Visualization</h1>
                <div>
                  <form action="http://engineering.utep.edu:62432">
                    <button type="submit" value="Back to Main Page"/>
                  </form>
                    <br>
                    <img src="hist.svg">
                </div>
              </body>
              <style type="text/css">
              </style>
              <script>
              </script>
            </html>'''
        file.write(html)
        file.close()