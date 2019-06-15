"""
Author: Christopher Mendoza
Creates a visual representation of data transfered between autonomous systems.
Version 4.0

"""
import folium
import pandas as pd
from folium.features import CustomIcon
import urllib.request
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import re


def geovizTrafficMatrix(MatrixOrList,GCL = pd.DataFrame(),savefile = 'Map.html',Src = list(range(1000)),Dst = list(range(1000)),csv = ''):  

#Initilize variables and edit some strings in geo info file to make it look nicer    
    plt.ioff()
    targetfile = 'asnum2.csv'
    LoA = MatrixOrList    
    pd.set_option('display.max_colwidth', -1)
    
    ASNums = pd.read_csv(targetfile)
    ASNums['organization'] = ASNums['organization'].str.replace("'","")
    
    if len(GCL) > 0:
        GCL['organization'] = GCL['organization'].str.replace("'","")
    
    tempdf = pd.DataFrame()
    SelfList = []
    ASUnique = []
    DupList = []
    removelist = []
    
    m = folium.Map(location=[29.7176, -95.4188], tiles='OpenStreetMap', zoom_start=5)


#Seperate into the One Location,Bidirection or Unidirectional Lists
    
    mc = 0
    
    for x in range (0,len(LoA)):
        
        if LoA[x - mc].get('asSrc') == LoA[x - mc].get('asDst'):
            if LoA[x - mc] not in SelfList:
                SelfList.append(LoA[x - mc])
                del LoA[x - mc]
                mc = mc + 1
    
        
    
    for x in range(0,len(LoA)):
        
        if LoA[x].get('asSrc') not in DupList:
            DupList.append(LoA[x].get('asSrc'))
            d = {"asNum":int(LoA[x].get('asSrc'))}
            if d not in ASUnique:
                ASUnique.append(d)
        
        if LoA[x].get('asDst') not in DupList:
            DupList.append(LoA[x].get('asDst'))
            d = {"asNum":int(LoA[x].get('asDst'))}
            if LoA[x].get('asDst') not in ASUnique:
                ASUnique.append(d)
     

    for x in SelfList:
        for y in range (0,len(ASUnique)):
            if int(x.get('asSrc')) == ASUnique[y]['asNum']:
                removelist.append(y)
    
    removelist = set(removelist)        
    removelist = sorted(removelist, reverse=True)            
    
    for x in removelist:
        del ASUnique[x]
        
        
            
#Make Markers for all non self-talkers

    for x in ASUnique:
        
        tempdf = pd.DataFrame()    
        
        if len(GCL) > 0:
            tempdf = GCL[(GCL.asNum == int(x.get('asNum')))].reset_index()
        
        if (len(tempdf) == 0):
            tempdf = ASNums[(ASNums.asNum == int(x.get('asNum')))].reset_index()
        
        if len(tempdf) > 0:
            temp = tempdf.loc[0]
            
            
            asnum = temp.asNum
            
            icon_image = 'http://engsrvdb00.utep.edu/amis/images/as_images/%s.png' % asnum
            
            x['latitude'] = temp.latitude
            x['longitude'] = temp.longitude
            x['Logo'] = '<img src="' + icon_image + '" height="50" width="50">'
            x['Organization'] = temp.organization
    
    
    if len(ASUnique) > 0:
        qq = pd.DataFrame(ASUnique)
        qq['asNum'] = qq['asNum'].astype(int)
        MarkerLat =  qq['latitude'].unique()
        MarkerLong = qq['longitude'].unique() 
        
        for lat in MarkerLat:
            for lng in MarkerLong:
                dff = pd.DataFrame()
                dff = qq[(qq['latitude'] == lat) & (qq['longitude'] == lng)].reset_index(drop = True)
                
                
                if len(dff) == 1:
                    asnum = dff['asNum'][0]
                    icon_image = 'http://engsrvdb00.utep.edu/amis/images/as_images/%s.png' % asnum
                    
                    
                    
                    
                    
                    html = dff.to_html(escape = False).replace('<td>','<td align = "center">').replace('<thead>','<thead align = "center">').replace('border="1"','border="5"').replace('<tr style="text-align: right;">','<tr style="text-align: center;">')
                    

                    
                    location = [lat,lng]
                    iframe = folium.IFrame(html=html, width=450, height = 110)
                    popup = folium.Popup(iframe, max_width=2650)  
                    
                    
                    
                    try:
                        urllib.request.urlretrieve(icon_image)
                        
                    
                        icon = CustomIcon(
                                icon_image,
                                icon_size=(40, 40),
                                popup_anchor=(0, -20),
                                )
                        
                        
                        m1 = folium.Marker(
                        location=location,
                        popup=popup,
                        icon = icon
                        )
                
                    except urllib.error.HTTPError:
                        m1 = folium.Marker(
                        location=location,
                        popup=popup
                        )
                    m.add_child(m1)
                
                
                if len(dff) > 1:
                    
                    ipix = 75*len(dff)
                    ipix = min(ipix,600)
                                        
                    html = dff.to_html(escape = False).replace('<td>','<td align = "center">').replace('<thead>','<thead align = "center">').replace('border="1"','border="5"').replace('<tr style="text-align: right;">','<tr style="text-align: center;">')
                    

                    
                    location = [lat,lng]
                    iframe = folium.IFrame(html=html, width=450, height = ipix)
                    popup = folium.Popup(iframe, max_width=2650)  
                    
                    
                    
                    for p in range(0,len(dff)):
                        asnum = dff['asNum'][p]
                        icon_image = 'http://engsrvdb00.utep.edu/amis/images/as_images/%s.png' % asnum
                        try:
                            urllib.request.urlretrieve(icon_image)
                            
                        
                            icon = CustomIcon(
                                    icon_image,
                                    icon_size=(40, 40),
                                    popup_anchor=(0, -20),
                                    )
                            
                            m1 = folium.Marker(
                                    location=location,
                                    popup=popup,
                                    icon = icon
                                    )
                            break
                    
                        except urllib.error.HTTPError:
                            if p == len(dff) - 1:
                                m1 = folium.Marker(
                                        location=location,
                                        popup=popup
                                        )
                    
                    
                    
                    
                    m.add_child(m1) 
    
    
    
    
    
    
    
    
    
    
    
#Make Markers for all the Self-Talkers    
    
    for x in SelfList:
        
        tempdf = pd.DataFrame()
            
        if len(GCL) > 0:
            tempdf = GCL[(GCL.asNum == int(x.get('asSrc')))].reset_index()
    
        if (len(tempdf) == 0):
            tempdf = ASNums[(ASNums.asNum == int(x.get('asSrc')))].reset_index()
        
        if len(tempdf) > 0:
            temp = tempdf.loc[0]
            
            asnum = temp.asNum
            
            icon_image = 'http://engsrvdb00.utep.edu/amis/images/as_images/%s.png' % asnum
            
            
            x['latitude'] = temp.latitude
            x['longitude'] = temp.longitude
            #x['Logo'] = '<img src="' + icon_image + '" height="50" width="50">'
            x['Organization'] = temp.organization
            x['packets'] = int(x.get('packets'))
            x['bytes'] = int(x.get('bytes'))
            
        

    if len(SelfList) > 0:
        qq = pd.DataFrame(SelfList)
        qq['asSrc'] = qq['asSrc'].astype(int)
        qq['asDst'] = qq['asDst'].astype(int)
        MarkerLat =  qq['latitude'].unique()
        MarkerLong = qq['longitude'].unique() 
        
        for lat in MarkerLat:
            for lng in MarkerLong:
                dff = pd.DataFrame()
                dff = qq[(qq['latitude'] == lat) & (qq['longitude'] == lng)].reset_index(drop = True)
                dff = dff.drop(['id'],axis=1)
                
                if len(dff) == 1:
                    asnum = dff['asSrc'][0]
                    icon_image = 'http://engsrvdb00.utep.edu/amis/images/as_images/%s.png' % asnum
                    
                    
                    
                    
                    
                    html = dff.to_html(escape = False).replace('<td>','<td align = "center">').replace('<thead>','<thead align = "center">').replace('border="1"','border="5"').replace('<tr style="text-align: right;">','<tr style="text-align: center;">')
                    location = [lat,lng]
                    iframe = folium.IFrame(html=html, width=1000, height = 110)
                    popup = folium.Popup(iframe, max_width=2650)  
                    
                    
                    
                    try:
                        urllib.request.urlretrieve(icon_image)
                        
                    
                        icon = CustomIcon(
                                icon_image,
                                icon_size=(40, 40),
                                popup_anchor=(0, -20),
                                )
                        
                        
                        m1 = folium.Marker(
                        location=location,
                        popup=popup,
                        icon = icon
                        )
                
                    except urllib.error.HTTPError:
                        m1 = folium.Marker(
                        location=location,
                        popup=popup
                        )
                        
                    m.add_child(m1)
                
                if len(dff) > 1:
                    
                    ipix = 75*len(dff) + 200
                    ipix = min(ipix,600)
                    
                    if 'App' in dff.columns:
                        h = MakeHist(dff)
                    
                    if len(dff) > 3:
                        dff = dff.sort_values(by=['bytes'],ascending = False).reset_index(drop=True)
                        dff = dff.iloc[0:3]
                    
                    html = dff.to_html(escape = False).replace('<td>','<td align = "center">').replace('<thead>','<thead align = "center">').replace('border="1"','border="5"').replace('<tr style="text-align: right;">','<tr style="text-align: center;">')
                    html = h + html
                    h = ''
                    
                    
                    location = [lat,lng]
                    iframe = folium.IFrame(html=html, width=1000, height = ipix)
                    popup = folium.Popup(iframe, max_width=2650)
                    
                    
                    
                    for p in range(0,len(dff)):
                        asnum = dff['asSrc'][p]
                        icon_image = 'http://engsrvdb00.utep.edu/amis/images/as_images/%s.png' % asnum
                        try:
                            urllib.request.urlretrieve(icon_image)
                            
                        
                            icon = CustomIcon(
                                    icon_image,
                                    icon_size=(40, 40),
                                    popup_anchor=(0, -20),
                                    )
                            
                            m1 = folium.Marker(
                                    location=location,
                                    popup=popup,
                                    icon = icon
                                    )
                            break
                    
                        except urllib.error.HTTPError:
                            if p == len(dff) - 1:
                                m1 = folium.Marker(
                                        location=location,
                                        popup=popup
                                        )
                    
                    
                    
                    
                    m.add_child(m1) 

    
#Save map on server to be served to user
    
    if '.ejs' not in savefile:
        savefile = savefile + '.ejs'   
    m.save(savefile)
    jscode = findMarkers(savefile,csv)
    with open(savefile,"a") as f:
        f.write(jscode)
        f.write("<title>Ra Map - %s</title>" % savefile[:-5])
    return 0




























###############################################################################################################################################################
#    
#                       MAP HTML
#  
###############################################################################################################################################################

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
    
    
###############################################################################################################################################################
#    
#                       JSCode
#  
###############################################################################################################################################################

def findMarkers(name,csv):
    with open(name,'r') as f:
        txt = f.read()
    
    fl = "var elements = ["
    
    p1 = re.compile('map_.+ =')
    mapkey = p1.findall(txt)
    mapkey = mapkey[0][0:-2]
    
    p1 = re.compile('marker_.+ =')
    matches = p1.findall(txt)
    for x in matches:
        x = x[0:-2]
        add = f"'{x}',"
        fl = fl + add
    fl = fl[0:-1]    
    fl = fl + '];\n'
    
    jscode = '''
    
    for(var i = 0, len = elements.length; i < len; i++) {
        temp = eval(elements[i])
        temp.on('contextmenu', onClick);
    }
    
    var check = false;
    var l1 = [];
    var l2 = [];
    var chart = '';
    
    function onClick(e) 
    {
    	if (check == false) 
        {
            alert('Selected');
            l1 = this.getLatLng();
            check = true;
        }
        else 
        {
            l2 = this.getLatLng();
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() 
            {
                if (this.readyState == 4 && this.status == 200) 
                {
                    chart = this.responseText;
                    if (chart.length > 0) 
                    {
                        var polyline = L.polyline([[l1.lat,l1.lng],[l2.lat,l2.lng]], {color: 'green'}).addTo(%s);
                        polyline.bindPopup(chart,{maxWidth : 2650});
                    }
                    else 
                    {
                        alert("No Data Found");
                    }
                }
            }
            xhttp.open("POST", "/mapChart", false);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("csv=" + "%s" + "&" + "lat1=" + l1.lat + "&" + "lon1=" + l1.lng + "&" + "lat2=" + l2.lat + "&" + "lon2=" + l2.lng);
            check = false;
            l1 = l2 = [];
        }
    }
    </script>
        ''' %(mapkey, csv)
        
    jscode = '<script>\n' + fl + jscode
    return jscode

