'''
Univariate NetFlow Visualizations using matplotlib
Version 1.0.0
Author: Carlos Alcantara
'''

import pandas as pd
import pandasql as pds
import matplotlib.pyplot as plt
import sys
import os

# Resolve relative path for csv data files
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileName = os.path.join(fileDir, 'csv\\'+sys.argv[1])

# Save visualization options
field = sys.argv[2]
vizType = sys.argv[3]
outputFileName = 'univariate.svg'
sqlOption = sys.argv[4]
if sqlOption == 'true':
    sqlFilter = sys.argv[5]
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

# Load NetFlow data file
netflowData = pd.read_csv(fileName)

# Filter the NetFlow data frame using the SQL query
if (sqlFilter != '') and ( (sqlFilter[:6] == 'SELECT') or (sqlFilter[:6] == 'select')):
    netflowData = pds.sqldf(sqlFilter, globals())

# Render visualization
plt.style.use('ggplot')
if vizType == 'histogram':
    plt.hist(netflowData[field], bins=500, density=True)
    plt.xlabel(field)
    plt.ylabel('Probability')
elif vizType == 'boxplot':
    plt.boxplot(netflowData[field])
    plt.ylabel(field)
elif vizType == 'violinplot':
    plt.violinplot(netflowData[field])
    plt.ylabel(field)
else:
    # invalid viz type
    exit(-1)
    
plt.title('Univariate Visualization for '+fileName.split("\\")[-1])
plt.savefig('images/'+outputFileName)

exit(0)
