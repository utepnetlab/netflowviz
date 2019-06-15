#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 13:00:22 2018

@author: Carlos Alcantara
"""
import pandas as pd
from math import nan , pi
from bokeh.models import CustomJS, LinearColorMapper, BasicTicker, ColorBar, Button
from bokeh.plotting import figure
from bokeh.io import save, output_file
from bokeh.layouts import column, row
#from bokeh.palettes import magma
from bokeh.models.widgets import RadioButtonGroup
from bokeh import events
from customPalette import RdBu
import sys

def main(filename, src, dst, outputFileName):
    df = pd.read_csv(filename)
    df = df.replace(nan,'unknown')
    valuetype = 'Flows'


    ###########################################################################################
    #####################################   CREATE DF   #######################################


    Csrcval = src
    Cdstval = dst

    dfcountry = df[(df['src_country'] == Csrcval) & (df['dst_country'] == Cdstval)]

    c_ind = list(dfcountry['src_org'].unique())
    c_col = list(dfcountry['dst_org'].unique())
    c_dfFlows = pd.DataFrame(index = c_ind, columns = c_col, data = 0)
    c_dfPkts = pd.DataFrame(index = c_ind, columns = c_col, data = 0)
    c_dfOcts = pd.DataFrame(index = c_ind, columns = c_col, data = 0)
    dftest = dfcountry.groupby(['src_org','dst_org']).size()
    for x in dftest.index.values.tolist():
        c_dftemp = dfcountry[(dfcountry['src_org'] == x[0]) & (dfcountry['dst_org'] == x[1])]
        print(f'Pkts from {x[0]} to {x[1]}')
        c_dfPkts.at[[x[0]],[x[1]]] = c_dftemp['dPkts'].sum()
        print(c_dftemp['dPkts'].sum())
        print(f'Bytes from {x[0]} to {x[1]}')
        c_dfOcts.at[[x[0]],[x[1]]] = c_dftemp['dOctets'].sum()
        print(c_dftemp['dOctets'].sum())
        print(f'Flows from {x[0]} to {x[1]}')
        c_dfFlows.at[[x[0]],[x[1]]] = len(c_dftemp)
        print(len(c_dftemp))

    #   rename column
    c_dfPkts.columns.name = Cdstval
    c_dfOcts.columns.name = Cdstval
    c_dfFlows.columns.name = Cdstval

    #   create df to be visualized
    dfViz = pd.DataFrame(c_dfFlows.stack(), columns=['value']).reset_index()
    dfViz.columns=['src_org','dst_org','value']
    dfViz2 = pd.DataFrame(c_dfPkts.stack(), columns=['value']).reset_index()
    dfViz2.columns=['src_org','dst_org','value']
    dfViz3 = pd.DataFrame(c_dfOcts.stack(), columns=['value']).reset_index()
    dfViz3.columns=['src_org','dst_org','value']


    ###########################################################################################
    #####################################  COLOR MAP   ########################################

 
    colors = RdBu(500)
    c_mapper = LinearColorMapper(palette=colors, low=dfViz.value.min(), high=dfViz.value.max())
    c_mapper2 = LinearColorMapper(palette=colors, low=dfViz2.value.min(), high=dfViz2.value.max())
    c_mapper3 = LinearColorMapper(palette=colors, low=dfViz3.value.min(), high=dfViz3.value.max())
        

    ###########################################################################################
    #####################################  LIST CHECK   #######################################


    srclist = list(dfViz.src_org.unique())
    dstlist = list(dfViz.dst_org.unique())

    if len(srclist) == 1 and len(dstlist) == 1:
        return 1
    else :
        ###########################################################################################
        #######################################   PLOT 1   ########################################


        TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom,tap"

        c_p = figure(title="Interactive Visualization",
                   x_range=c_ind, y_range=c_col,
                   x_axis_location="above", plot_width=900, plot_height=800,
                   tools=TOOLS, toolbar_location='below'
                   ,tooltips=[('Source', '@src_org'), ('Destination', '@dst_org'), (valuetype, '@value')]
                   )

        c_p.title.align = 'center'
        c_p.grid.grid_line_color = None
        c_p.axis.axis_line_color = 'white'
        c_p.axis.major_tick_line_color = None
        c_p.axis.major_label_text_font_size = "10pt"
        c_p.axis.major_label_standoff = 0
        c_p.xaxis.axis_label = 'Source'
        c_p.yaxis.axis_label = 'Destination'
        c_p.xaxis.major_label_orientation = pi / 3

        c_heatmap = c_p.rect(x='src_org', y='dst_org', width=1, height=1,
                source=dfViz,
                fill_color={'field': 'value', 'transform': c_mapper},
                line_color='white')

        c_color_bar = ColorBar(color_mapper=c_mapper, major_label_text_font_size="10pt",
                ticker=BasicTicker(desired_num_ticks=10),
                label_standoff=12, border_line_color=None, location=(0, 0))
        c_color_bar.formatter.use_scientific = False
        c_p.add_layout(c_color_bar, 'right')


        ###########################################################################################
        #######################################   PLOT 2   ########################################


        valuetype = 'dPkts'

        c_p2 = figure(title="Interactive Visualization",
                   x_range=c_ind, y_range=c_col,
                   x_axis_location="above", plot_width=900, plot_height=800,
                   tools=TOOLS, toolbar_location='below'
                   ,tooltips=[('Source', '@src_org'), ('Destination', '@dst_org'), (valuetype, '@value')]
                   )

        c_p2.title.align = 'center'
        c_p2.grid.grid_line_color = None
        c_p2.axis.axis_line_color = 'white'
        c_p2.axis.major_tick_line_color = None
        c_p2.axis.major_label_text_font_size = "10pt"
        c_p2.axis.major_label_standoff = 0
        c_p2.xaxis.axis_label = 'Source'
        c_p2.yaxis.axis_label = 'Destination'
        c_p2.xaxis.major_label_orientation = pi / 3

        c_heatmap2 = c_p2.rect(x='src_org', y='dst_org', width=1, height=1,
                source=dfViz2,
                fill_color={'field': 'value', 'transform': c_mapper2},
                line_color='white')

        c_color_bar2 = ColorBar(color_mapper=c_mapper2, major_label_text_font_size="10pt",
                ticker=BasicTicker(desired_num_ticks=10),
                label_standoff=12, border_line_color=None, location=(0, 0))
        c_color_bar2.formatter.use_scientific = False
        c_p2.add_layout(c_color_bar2, 'right')
        

        ###########################################################################################
        #######################################   PLOT 3   ########################################


        valuetype = 'dOctets'

        c_p3 = figure(title="Interactive Visualization",
                   x_range=c_ind, y_range=c_col,
                   x_axis_location="above", plot_width=900, plot_height=800,
                   tools=TOOLS, toolbar_location='below'
                   ,tooltips=[('Source', '@src_org'), ('Destination', '@dst_org'), (valuetype, '@value')]
                   )

        c_p3.title.align = 'center'
        c_p3.grid.grid_line_color = None
        c_p3.axis.axis_line_color = 'white'
        c_p3.axis.major_tick_line_color = None
        c_p3.axis.major_label_text_font_size = "10pt"
        c_p3.axis.major_label_standoff = 0
        c_p3.xaxis.axis_label = 'Source'
        c_p3.yaxis.axis_label = 'Destination'
        c_p3.xaxis.major_label_orientation = pi / 3

        c_heatmap3 = c_p3.rect(x='src_org', y='dst_org', width=1, height=1,
                source=dfViz3,
                fill_color={'field': 'value', 'transform': c_mapper3},
                line_color='white')

        c_color_bar3 = ColorBar(color_mapper=c_mapper2, major_label_text_font_size="10pt",
                ticker=BasicTicker(desired_num_ticks=10),
                label_standoff=12, border_line_color=None, location=(0, 0))
        c_color_bar3.formatter.use_scientific = False
        c_p3.add_layout(c_color_bar3, 'right')
        

        ###########################################################################################
        ######################################   BUTTONS   ########################################


        homeButton = Button(label="Back to Homepage")

        col = column(c_p, c_p2, c_p3)

        radioBtn = RadioButtonGroup(labels=["All","Flows", "Packets", "Bytes"], active=0, width=300)

        radioCallback = CustomJS(args=dict(plots=[c_p,c_p2, c_p3], col=col, radioBtn=radioBtn), code="""
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
        callback = CustomJS(args=dict(plots=[c_p,c_p2, c_p3], src=srclist, dst=dstlist, file=filename, dataframe=jsonString),code="""
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
        var obj = findObjectByKey(df.data, 'src_org', src[parseInt(cb_obj.x)], 'dst_org', dst[parseInt(cb_obj.y)]);
        
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
                form.setAttribute('action', '/asHist');
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

        c_p.js_on_event('tap', callback)
        c_p2.js_on_event('tap', callback)
        c_p3.js_on_event('tap', callback)


        ###########################################################################################
        ######################################   OUTPUT   #########################################
        

        output_file("continent_test.ejs")

        layout = column(row(homeButton, radioBtn), col)

        save(layout,filename=outputFileName,title='Organization Level')
        return 0