from Ra import netflowVisualization
import pandas as pd
import pandasql as pds
import sys

fileName = sys.argv[1]
pathName = 'C:/inetpub/wwwroot/amis/netflowviz/csv/'

sqloption = sys.argv[2]
if sqloption == 'true':
    sqlfilter = sys.argv[3] # 'select * from netflowData where duration > 1000000'
else:
    sqlfilter = ''

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

netflowData = pd.read_csv(pathName+fileName)

# Reduce the NetFlow data frame using the SQL query
if (sqlfilter != '') and ( (sqlfilter[:6] == 'SELECT') or (sqlfilter[:6] == 'select')):
    print('Applying SQL filter')
    netflowData = pds.sqldf(sqlfilter, globals())
    netflowData.to_csv(pathName + 'filteredCSV.csv')
    fileName = 'filteredCSV.csv'

pathName = pathName + fileName
savefile = 'views/tempMap.ejs'

netflowVisualization(netflowData,savefile,pathName)
