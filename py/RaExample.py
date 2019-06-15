#Ra usage example
#By: Christopher Mendoza
#Use pydoc

from Ra import Ra
import pandas as pd
import time
import numpy as np

start = time.time()

def testLogo(self):
    self.df['src_logo'] = '<img src="' + "http://engsrvdb00.utep.edu/amis/images/as_images/" + df['src_as'].astype(str) + ".png" + '" height="50" width="50">'
    self.df['dst_logo'] = '<img src="' + "http://engsrvdb00.utep.edu/amis/images/as_images/" + df['dst_as'].astype(str) + ".png" + '" height="50" width="50">'

def lineColor(self,df):
    if max(df['dPkts']) > 10:
        return 'red'
    
def zooba(self,df):
    if min(df['dPkts'] < 2):
        return 'blue'
    else:
        return 'black'

#df = pd.read_csv('ampath-i2.csv',index_col = 0)
df = pd.read_csv('~/Desktop/uky_20180930_1700_1h.csv',index_col = 0)
df['src_as'] = df['src_as'].astype(int)
df['dst_as'] = df['dst_as'].astype(int)
df = df.dropna().reset_index(drop=True)
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
Ra.lineFunction = zooba
ra = Ra(df)
ra.savefile = 'TestMap'
#ra.focus("dst_country == 'United States'")
#ra.logoCheck = False
ra.getMarkerLogos = True
ra.aggregate('country')
ra.popupWidth['marker'] = 700
ra.popupLen = 5
ra.plotX = 'app'
ra.plotY = 'dOctets'
ra.sortvar = 'dOctets'
#ra.plotHue = 'app'
ra.plotType = 'bar'
#ra.plotEstimator = sum
#ra.markerInfo = ['as','org','lat','long','region','country','continent','logo']
ra.markerInfo = ['as','org','lat','long','region','country','continent']
ra.dfAddLogos()
ra.createMap()
ra.saveMap()

print('Executed in ' + str(round(time.time() - start,2)) + ' Seconds')