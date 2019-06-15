'''
Multivariate NetFlow Visualizations using seaborn jointplot to show  a scatterplot
Version 1.0.0
Author: Carlos Alcantara
'''

import pandas as pd
import pandasql as pds
import seaborn as sns
import sys
import os
import numpy as np

# Resolve relative path for csv data files
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileName = os.path.join(fileDir, 'csv\\'+sys.argv[1])

sqloption = sys.argv[4]
if sqloption == 'true':
    sqlfilter = sys.argv[5]    
else:
    sqlfilter = ' '
# Correct SQL filter if necessary
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

sns.set(style="white", color_codes=True)
sns_plot = sns.jointplot(x=sys.argv[2], y=sys.argv[3], data=netflowData)
sns_plot.fig.suptitle("Bivariate Distribution for "+fileName.split("\\")[-1], y=1.08)
sns_plot.savefig("images/bivariate.svg")