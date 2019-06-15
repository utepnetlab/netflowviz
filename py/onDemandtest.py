import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import sys
import urllib.request
import cProfile

###############################################################################
#                                                                             #
#                       Make Bar Chart using seaborn                          #
#                                                                             #
###############################################################################

def MakeHist(df):
    sns.set(font_scale = 1.25)
    fig, ax = plt.subplots()
    fig = plt.figure()
    ax = sns.barplot('App','bytes',data=df,ci = None,estimator=sum)
    ax.set(ylabel = 'Bytes')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    svg = StringIO()
    fig.savefig(svg, format='svg')
    svgtxt = svg.getvalue()
    svg.close()
    plt.close('all')
    return(svgtxt)    

################################################################################################################
#                                                                                                              #
#                           Create Bar Chart On Demand                                                         #
#                                                                                                              #
################################################################################################################
def test():
    netflow = '/Users/carlosalcantara/nodeJS/netflowviz/csv/converted_virgo_in_201803211405_2hr.csv'
    lat1 = 31.7832
    lon1 = -106.4976
    lat2 = 52.2333
    lon2 = 21.0167

    netflow = pd.read_csv(netflow)

    LoA = []
    html = ''
    h = ''


    for p in range(0,len(netflow)):
        
        temp = {"asSrc":netflow['src_as'][p],"asDst":netflow['dst_as'][p],"bytes":netflow['dOctets'][p],"id":p,"packets":netflow['dPkts'][p],"timeEnd":netflow['first'][p],"timeStart":netflow['last'][p],"App":netflow['app'][p]}
        LoA.append(temp)
        
    targetfile = 'asnum2.csv'
    ASNums = pd.read_csv(targetfile)
    ASNums['organization'] = ASNums['organization'].str.replace("'","")

    for x in LoA:
        tempdf = pd.DataFrame()

        if (len(tempdf) == 0):
            tempdf = ASNums[(ASNums.asNum == int(x.get('asSrc')))].reset_index()
        
        if len(tempdf) > 0:
            temp = tempdf.loc[0]
            
            
            asnum = temp.asNum
            
            icon_image = 'http://engsrvdb00.utep.edu/amis/images/as_images/%s.png' % asnum
            
            x['Srclatitude'] = temp.latitude
            x['Srclongitude'] = temp.longitude
            x['SrcOrganization'] = temp.organization
            
            
        tempdf = pd.DataFrame()

        if (len(tempdf) == 0):
            tempdf = ASNums[(ASNums.asNum == int(x.get('asDst')))].reset_index()
        
        if len(tempdf) > 0:
            temp = tempdf.loc[0]
            
            
            asnum = temp.asNum
            
            icon_image = 'http://engsrvdb00.utep.edu/amis/images/as_images/%s.png' % asnum
            
            x['Dstlatitude'] = temp.latitude
            x['Dstlongitude'] = temp.longitude
            x['DstOrganization'] = temp.organization
        

    if len(LoA) > 0:
        zz = pd.DataFrame(LoA)
        zz['asSrc'] = zz['asSrc'].astype(int)
        zz['asDst'] = zz['asDst'].astype(int)
        dff = pd.DataFrame()
        dff = zz[(((zz['Srclatitude'] == lat1) & (zz['Srclongitude'] == lon1))  &    ((zz['Dstlatitude'] == lat2) & (zz['Dstlongitude'] == lon2)))  |   (((zz['Srclatitude'] == lat2) & (zz['Srclongitude'] == lon2))  &    ((zz['Dstlatitude'] == lat1) & (zz['Dstlongitude'] == lon1)))].reset_index(drop = True)
        if len(dff) > 0:
            
            dff = dff.drop(['id'],axis=1)
            
            if len(dff)>1:
                if 'App' in dff.columns:
                        h = MakeHist(dff)
            
            if len(dff) > 3:
                dff = dff.sort_values(by=['bytes'],ascending = False).reset_index(drop=True)
                dff = dff.iloc[0:3]
                
            html = dff.to_html(escape = False).replace('<td>','<td align = "center">').replace('<thead>','<thead align = "center">').replace('border="1"','border="5"').replace('<tr style="text-align: right;">','<tr style="text-align: center;">')
            html = h + html
            html = html.replace('\n','')

    with open('popup.txt','w') as f:
        f.write(html)  
