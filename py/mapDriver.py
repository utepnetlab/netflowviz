'''
Geospatial NetFlow Visualization driver file using Ra
Version 1.0.0
Author: Carlos Alcantara
'''

from Ra import Ra
from math import nan
import pandas as pd
import pandasql as pds
import time
import numpy as np
import sys
import json
import os

tempString = sys.argv[1]
command = json.loads(tempString)

# Resolve relative path for csv data files
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileName = os.path.join(fileDir, 'csv\\'+command['file'])

conditionalColoring = f"max(df['{command['columnName']}']) {command['condition']} {command['conditionalValue']}"

# Create custom function to add logo from webserver
def testLogo(self):
    self.df['src_logo'] = self.df.apply(lambda row: '<img src="' + f"http://engsrvdb00.utep.edu/amis/images/as_images/{int(row['src_as'])}.png" + '" height="50" width="50">',axis=1)
    self.df['dst_logo'] = self.df.apply(lambda row: '<img src="' + f"http://engsrvdb00.utep.edu/amis/images/as_images/{int(row['dst_as'])}.png" + '" height="50" width="50">',axis=1)

def lineColor(self,df):
    if eval(conditionalColoring):
        self.lineColor = command['conditionalColor']
    else:
        self.lineColor = command['defaultColor']

if command['filter'] != 'false':
    sqlfilter = command['filter']
    sqlfilter = sqlfilter.replace('_',' ')  
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

# Load NetFlow data file
netflowData = pd.read_csv(fileName)

# Reduce the NetFlow data frame using the SQL query
if (sqlfilter != '') and ( (sqlfilter[:6] == 'SELECT') or (sqlfilter[:6] == 'select')):
    print('Applying SQL filter')
    netflowData = pds.sqldf(sqlfilter, globals())

# Preprocess dataframe for visualization with Ra
df = netflowData
df = df.dropna()
df = df.replace(nan,'unknown')
originalIndex = df.columns.tolist()
newIndex = []
for item in range(0,len(originalIndex)):
    if 'src_' not in originalIndex[item]:
        originalIndex[item] = originalIndex[item].replace('src','src_')
    if 'dst_' not in originalIndex[item]:
        originalIndex[item] = originalIndex[item].replace('dst','dst_')
    newIndex.append(originalIndex[item])
df.columns = newIndex
Ra.dfAddLogos = testLogo
if command['colorFilter'] == 'true':
    Ra.lineOptions = lineColor
else :
    Ra.lineColor = command['defaultColor']
ra = Ra(df)

ra.savefile = os.path.join(fileDir, 'views\\tempMap.ejs')

if command['getMarkerLogos'] == 'true':
	ra.getMarkerLogos = True

if command['aggregate'] != 'none':
	ra.aggregate(command['aggregate'])

ra.popupWidth['marker'] = 700
ra.popupLen = int(command['popupLen'])
ra.plotX = command['plotX']
ra.plotY = command['plotY']
ra.sortvar = command['sortvar']
ra.plotType = command['plotType']
ra.markerInfo = ['as','org','lat','long','region','country','continent','logo']
ra.dfAddLogos()
ra.createMap()
ra.saveMap()