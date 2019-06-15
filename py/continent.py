#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 13:00:22 2018

@author: Carlos Alcantara
"""
import pandas as pd
from math import nan
from bokeh.models import CustomJS, LinearColorMapper, BasicTicker, ColorBar, Button
from bokeh.plotting import figure
from bokeh.io import save
from bokeh.layouts import column, row
from bokeh.models.widgets import RadioButtonGroup
from bokeh import events
from customPalette import RdBu
import sys

def main(filename, outputFileName):
  df = pd.read_csv(filename)
  df = df.replace(nan,'unknown')

  srcval = 'src_continent'
  dstval = 'dst_continent'
  valuetype = 'Flows'


  ###########################################################################################
  #####################################   CREATE DF   #######################################


  #   create list from df
  ind = list(df[srcval].unique())
  col = list(df[dstval].unique())
  #   create df for all 3 options and fill with zeros
  dfFlows = pd.DataFrame(index = ind, columns = col, data = 0)
  dfPkts = pd.DataFrame(index = ind, columns = col, data = 0)
  dfOcts = pd.DataFrame(index = ind, columns = col, data = 0)
  #   extract data to new df 
  dftest = df.groupby([srcval,dstval]).size()
  for x in dftest.index.values.tolist():
      dftemp = df[(df[srcval] == x[0]) & (df[dstval] == x[1])]
      print(f'Pkts from {x[0]} to {x[1]}')
      dfPkts.at[[x[0]],[x[1]]] = dftemp['dPkts'].sum()
      print(dftemp['dPkts'].sum())
      print(f'Bytes from {x[0]} to {x[1]}')
      dfOcts.at[[x[0]],[x[1]]] = dftemp['dOctets'].sum()
      print(dftemp['dOctets'].sum())
      print(f'Flows from {x[0]} to {x[1]}')
      dfFlows.at[[x[0]],[x[1]]] = len(dftemp)
      print(len(dftemp))
      
  #   rename column
  dfPkts.columns.name = dstval
  dfOcts.columns.name = dstval
  dfFlows.columns.name = dstval

  #   create df to be visualized
  dfViz = pd.DataFrame(dfFlows.stack(), columns=['value']).reset_index()
  dfViz.rename(columns={'level_0':srcval}, inplace=True)
  dfViz2 = pd.DataFrame(dfPkts.stack(), columns=['value']).reset_index()
  dfViz2.rename(columns={'level_0':srcval}, inplace=True)
  dfViz3 = pd.DataFrame(dfOcts.stack(), columns=['value']).reset_index()
  dfViz3.rename(columns={'level_0':srcval}, inplace=True)


  ###########################################################################################
  #####################################  COLOR MAP   ########################################


  colors = RdBu(500)
  mapper = LinearColorMapper(palette=colors, low=dfViz.value.min(), high=dfViz.value.max())
  mapper2 = LinearColorMapper(palette=colors, low=dfViz2.value.min(), high=dfViz2.value.max())
  mapper3 = LinearColorMapper(palette=colors, low=dfViz3.value.min(), high=dfViz3.value.max())


  ###########################################################################################
  #####################################  LIST CHECK   #######################################


  srclist = list(dfViz.src_continent.unique())
  dstlist = list(dfViz.dst_continent.unique())

  if len(srclist) == 1 and len(dstlist) == 1:
        return 1
  else :
    ###########################################################################################
    #######################################   PLOT 1   ########################################


    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom,tap"

    p = figure(title="Interactive Visualization",
           x_range=list(dfViz.src_continent.unique()), y_range=list(dfViz.dst_continent.unique()),
           x_axis_location="above", plot_width=900, plot_height=400,
           tools=TOOLS, toolbar_location='below'
           ,tooltips=[('Source', '@'+srcval), ('Destination', '@'+dstval), (valuetype, '@value')]
           )

    p.title.align = 'center'
    p.grid.grid_line_color = None
    p.axis.axis_line_color = 'white'
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.xaxis.axis_label = 'Source'
    p.yaxis.axis_label = 'Destination'

    heatmap = p.rect(x=srcval, y=dstval, width=1, height=1,
           source=dfViz,
           fill_color={'field': 'value', 'transform': mapper},
           line_color='white')

    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="10pt",
                         ticker=BasicTicker(desired_num_ticks=10),
                         label_standoff=12, border_line_color=None, location=(0, 0))
    color_bar.formatter.use_scientific = False
    p.add_layout(color_bar, 'right')


    ###########################################################################################
    #######################################   PLOT 2   ########################################


    valuetype = 'dPkts'

    p2 = figure(title="Interactive Visualization",
           x_range=list(dfViz2.src_continent.unique()), y_range=list(dfViz2.dst_continent.unique()),
           x_axis_location="above", plot_width=900, plot_height=400,
           tools=TOOLS, toolbar_location='below'
           ,tooltips=[('Source', '@'+srcval), ('Destination', '@'+dstval), (valuetype, '@value')]
           )

    p2.title.align = 'center'
    p2.grid.grid_line_color = None
    p2.axis.axis_line_color = 'white'
    p2.axis.major_tick_line_color = None
    p2.axis.major_label_text_font_size = "10pt"
    p2.axis.major_label_standoff = 0
    p2.xaxis.axis_label = 'Source'
    p2.yaxis.axis_label = 'Destination'

    heatmap2 = p2.rect(x=srcval, y=dstval, width=1, height=1,
           source=dfViz2,
           fill_color={'field': 'value', 'transform': mapper2},
           line_color='white')

    color_bar2 = ColorBar(color_mapper=mapper2, major_label_text_font_size="10pt",
                         ticker=BasicTicker(desired_num_ticks=10),
                         label_standoff=12, border_line_color=None, location=(0, 0))
    color_bar2.formatter.use_scientific = False
    p2.add_layout(color_bar2, 'right')


    ###########################################################################################
    #######################################   PLOT 3   ########################################


    valuetype = 'dOctets'

    p3 = figure(title="Interactive Visualization",
           x_range=list(dfViz3.src_continent.unique()), y_range=list(dfViz3.dst_continent.unique()),
           x_axis_location="above", plot_width=900, plot_height=400,
           tools=TOOLS, toolbar_location='below'
           ,tooltips=[('Source', '@'+srcval), ('Destination', '@'+dstval), (valuetype, '@value')]
           )

    p3.title.align = 'center'
    p3.grid.grid_line_color = None
    p3.axis.axis_line_color = 'white'
    p3.axis.major_tick_line_color = None
    p3.axis.major_label_text_font_size = "10pt"
    p3.axis.major_label_standoff = 0
    p3.xaxis.axis_label = 'Source'
    p3.yaxis.axis_label = 'Destination'

    heatmap3 = p3.rect(x=srcval, y=dstval, width=1, height=1,
           source=dfViz3,
           fill_color={'field': 'value', 'transform': mapper3},
           line_color='white')

    color_bar3 = ColorBar(color_mapper=mapper3, major_label_text_font_size="10pt",
                         ticker=BasicTicker(desired_num_ticks=10),
                         label_standoff=12, border_line_color=None, location=(0, 0))
    color_bar3.formatter.use_scientific = False
    p3.add_layout(color_bar3, 'right')


    ###########################################################################################
    ######################################   BUTTONS   ########################################


    homeButton = Button(label="Back to Homepage")

    col = column(p, p2, p3)

    radioBtn = RadioButtonGroup(labels=["All","Flows", "Packets", "Bytes"], active=0)

    radioCallback = CustomJS(args=dict(plots=[p,p2, p3], col=col, radioBtn=radioBtn), code="""
    const children = []
    if (radioBtn.active == 0) {
         children.push(plots[0])
         children.push(plots[1])
         children.push(plots[2])
    }
    if (radioBtn.active == 1) {
         children.push(plots[0])
    }
    if (radioBtn.active == 2) {
         children.push(plots[1])
    }
    if (radioBtn.active == 3) {
         children.push(plots[2])
    }
    col.children = children
    """)

    radioBtn.js_on_change('active', radioCallback)

    homeButtonCallback = CustomJS(code="""
        window.location.href = "http://engineering.utep.edu:62432";
    """)

    homeButton.js_on_event(events.ButtonClick, homeButtonCallback)
    jsonString = dfViz.to_json(orient='table', index=False)
    callback = CustomJS(args=dict(plots=[p,p2, p3], src=srclist, dst=dstlist, file=filename, dataframe=jsonString),code="""
    // the event that triggered the callback is cb_obj:
        // The event type determines the relevant attributes
        // console.log('Tap event occurred at x-position: ' + cb_obj.x)
        // console.log('Tap event occurred at y-position: ' + cb_obj.y)
        // console.log('Tap event occurred at y-position: ' + parseInt(cb_obj.y))

        console.log('Tap event occurred at x-position: ' + src[parseInt(cb_obj.x)]);
        console.log('Tap event occurred at y-position: ' + dst[parseInt(cb_obj.y)]);
        console.log('Tap event occurred at value:');
        df = JSON.parse(dataframe);
        console.log(df);
        // console.log(df.data[4]);
        
        function findObjectByKey(array, key1, value1, key2, value2) {
            for (var i = 0; i < array.length; i++) {
                // console.log(i);
                // console.log(array[i][key1]+' : '+value1+' VS '+array[i][key2]+' : '+ value2);
                if (array[i][key1] === value1 && array[i][key2] === value2) {
                    return array[i];
                }
            }
            return null;
        }
        var obj = findObjectByKey(df.data, 'src_continent', src[parseInt(cb_obj.x)], 'dst_continent', dst[parseInt(cb_obj.y)]);
        
        console.log(obj.value);
        if (obj.value == 0)
        {
            alert('Selected pair has no communication');
            plots[0].reset.emit();
            plots[1].reset.emit();
            plots[2].reset.emit();
        }
        else
        {
            var form = document.createElement('form');
                form.setAttribute('method', 'post');
                form.setAttribute('action', '/country');
                form.style.display = 'none';
                var fileName = document.createElement("textarea");
                            fileName.type = "textarea";
                            fileName.name = "FileName";
                            fileName.id = "FileName";
                            fileName.value = file;
                            form.appendChild(fileName);
                var sourceVal = document.createElement("textarea");
                            sourceVal.type = "textarea";
                            sourceVal.name = "SrcVal";
                            sourceVal.id = "SrcVal";
                            sourceVal.value = src[parseInt(cb_obj.x)];
                            form.appendChild(sourceVal);
                var destVal = document.createElement("textarea");
                            destVal.type = "textarea";
                            destVal.name = "DestVal";
                            destVal.id = "DestVal";
                            destVal.value = dst[parseInt(cb_obj.y)];
                            form.appendChild(destVal);
                document.body.appendChild(form);
                console.log(fileName.value);
                console.log(sourceVal.value);
                console.log(destVal.value);
                form.submit();
                plots[0].reset.emit();
                plots[1].reset.emit();
                plots[2].reset.emit();
            }
    """)

    p.js_on_event('tap', callback)
    p2.js_on_event('tap', callback)
    p3.js_on_event('tap', callback)
    

    ###########################################################################################
    ######################################   OUTPUT   #########################################


    layout = column(row(homeButton, radioBtn), col)

    save(layout,filename=outputFileName,title='Continent Level')
    return 0
    
main(sys.argv[1],'views/continent.ejs')