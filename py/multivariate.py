'''
Multivariate NetFlow Visualizations using seaborn
Version 1.0.0
Author: Carlos Alcantara
'''

import pandas as pd
import pandasql as pds
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Resolve relative path for csv data files
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileName = os.path.join(fileDir, 'csv\\'+sys.argv[1])

# Save visualization options
x = sys.argv[2]
y = sys.argv[3]
z = sys.argv[4]
dotSize = sys.argv[5]
sqlOption = sys.argv[6]
if sqlOption == 'true':
    sqlFilter = sys.argv[7]
else:
    sqlFilter = ' '

# Correct SQL filter if necessary
if 'netflowData ' not in sqlFilter:
    position = sqlFilter.find('FROM')
    if position == -1:
        position = sqlFilter.find('from')
        if position == -1:
            # SQL format not supported
            sqlFilter = ''
    if position > -1:
        # found FROM, now find WHERE
        position2 = sqlFilter.find('WHERE')
        if position2 == -1:
            position2 = sqlFilter.find('where')
            if position2 == -1:
                # SQL format not supported
                sqlFilter = ''
        if position2 > -1:
            # found FROM and WHERE, create new SQL query with netflowData as the table name
            sqlFilter = sqlFilter[:position+4] + ' netflowData ' + sqlFilter[position2:]

sns.set()
netflowData = pd.read_csv(fileName, index_col=0)
# pairData = pairData.iloc[:20]

# Filter the NetFlow data frame using the SQL query
if (sqlFilter != '') and ( (sqlFilter[:6] == 'SELECT') or (sqlFilter[:6] == 'select')):
    netflowData = pds.sqldf(sqlFilter, globals())

# Create Visualization
if dotSize != 'none':
    netflowData.loc[:,dotSize] *= .15

tempFig = plt.figure()

if dotSize == 'none':
    sns.lmplot(x,y,data=netflowData,hue=z,fit_reg=False, height=7, aspect=2)
else:
    sns.lmplot(x,y,data=netflowData,hue=z,fit_reg=False,scatter_kws={'s':netflowData[dotSize]}, height=6, aspect=10)

plt.title('Multivariate Visualization for '+fileName.split("\\")[-1])
plt.xlabel(x)
plt.ylabel(y)
plt.savefig('images/multivariate.svg')
