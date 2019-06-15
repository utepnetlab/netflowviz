'''
Multivariate NetFlow Visualizations using seaborn pairplot to compare all possible
combinations of pairs as individual scatterplots
Version 1.0.0
Author: Carlos Alcantara
'''

import pandas as pd
import pandasql as pds
import seaborn as sns
import sys
import os

# Resolve relative path for csv data files
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileName = os.path.join(fileDir, 'csv\\'+sys.argv[1])

sqloption = sys.argv[2]
if sqloption == 'true':
    sqlfilter = sys.argv[3]
    # Array of variables to be used
    arg = sys.argv[4:]
else:
    sqlfilter = ' '
    # Array of variables to be used
    arg = sys.argv[3:]

if 'netflowData ' not in sqlfilter:
    pos = sqlfilter.find('FROM')
    if pos == -1:
        pos = sqlfilter.find('from')
        if pos == -1:
            # SQL format not supported
            sqlfilter = ''
    if pos > -1:
        # found FROM, now find WHERE
        pos2 = sqlfilter.find('WHERE')
        if pos2 == -1:
            pos2 = sqlfilter.find('where')
            if pos2 == -1:
                # SQL format not supported
                sqlfilter = ''
        if pos2 > -1:
            # found FROM and WHERE, create new SQL query with netflowData as the table name
            sqlfilter = sqlfilter[:pos+4] + ' netflowData ' + sqlfilter[pos2:]

netflowData = pd.read_csv(fileName)

# Reduce the NetFlow data frame using the SQL query
if (sqlfilter != '') and ( (sqlfilter[:6] == 'SELECT') or (sqlfilter[:6] == 'select')):
    print('Applying SQL filter')
    netflowData = pds.sqldf(sqlfilter, globals())

sns.set(style="ticks", color_codes=True)
sns_plot = sns.pairplot(netflowData, vars=arg)
sns_plot.fig.suptitle("Scatter Plot Matrix for "+fileName.split("\\")[-1], y=1.08)
sns_plot.savefig("images/scatterplot.svg")
