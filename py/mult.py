import pandas as pd
import matplotlib.pyplot as plt
import sys

dataFilename = 'C:/inetpub/wwwroot/amis/netflowviz/csv/'+sys.argv[1]
field = sys.argv[2]
vizType = sys.argv[3]
outputFilename = 'tempPlot.svg'

# Load NetFlow data file
netflowData = pd.read_csv(dataFilename)

# Reduce the NetFlow data frame using the SQL query
if (sqlfilter != '') and ( (sqlfilter[:6] == 'SELECT') or (sqlfilter[:6] == 'select')):
    print('Applying SQL filter')
    netflowData = pds.sqldf(sqlfilter, globals())

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
    
# Output to a file, pyplot derives type from extension of file name
plt.savefig(outputFilename)

exit(0)
