#Ra usage example
#By: Christopher Mendoza

from Ra import Ra
from math import nan
import pandas as pd
import time
import numpy as np
import sys
import json

tempString = sys.argv[1]
command = json.loads(tempString)

start = time.time()

conditionalColoring = f"max(df['{command['columnName']}']) {command['condition']} {command['conditionalValue']}"

def testLogo(self):
    self.df['src_logo'] = self.df.apply(lambda row: '<img src="' + f"http://engsrvdb00.utep.edu/amis/images/as_images/{int(row['src_as'])}.png" + '" height="50" width="50">',axis=1)
    self.df['dst_logo'] = self.df.apply(lambda row: '<img src="' + f"http://engsrvdb00.utep.edu/amis/images/as_images/{int(row['dst_as'])}.png" + '" height="50" width="50">',axis=1)

def lineColor(self,df):
    if eval(conditionalColoring):
        self.lineColor = command['conditionalColor']
    else:
        self.lineColor = command['defaultColor']

df = pd.read_csv('C:/inetpub/wwwroot/amis/netflowviz/csv/' + command['file'],index_col = 0)
df = df.dropna()
df = df.replace(nan,'unknown')
mI = df.columns.tolist()
newMI = []
for x in range(0,len(mI)):
    if 'src_' not in mI[x]:
        mI[x] = mI[x].replace('src','src_')
    if 'dst_' not in mI[x]:
        mI[x] = mI[x].replace('dst','dst_')
    newMI.append(mI[x])
df.columns = newMI
Ra.dfAddLogos = testLogo
if command['colorFilter'] == 'true':
    Ra.lineOptions = lineColor
else :
    Ra.lineColor = command['defaultColor']
ra = Ra(df)
ra.savefile = 'C:/inetpub/wwwroot/amis/netflowviz/views/tempMap.ejs'
if command['filter'] != '':
	ra.focus(command['filter'])
#ra.logoCheck = False
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
#ra.plotEstimator = np.mean
ra.markerInfo = ['as','org','lat','long','region','country','continent','logo']
# ra.markerInfo = ['as','org','lat','long','region','country','continent']
ra.dfAddLogos()
ra.createMap()
ra.saveMap()

# print('Executed in ' + str(round(time.time() - start,2)) + ' Seconds')