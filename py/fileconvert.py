import sia
import pandas as pd
import sys


fileName = sys.argv[1]
pathName = '/Users/carlosalcantara/netlab_git/netflowviz/csv/'+fileName
# Convert CSV to pandas dataframe
officeData = pd.read_csv(pathName)

# Annotate NetFlow data
officeData = sia.netflowConvertProtoStr2Num(officeData)
officeData = sia.annotateNetflow(officeData)
officeData = sia.netflowConvertProtoNum2Str(officeData)

# Convert pandas dataframe to CSV
officeData.to_csv('converted_'+fileName+'.csv')