import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import seaborn as sns
#from bokeh.palettes import all_palettes
#import bokeh.palettes.rdbu as RdBu
#import numpy as np
import pandas as pd

def makeSimplePalette(num):
    # Python code to create colors 
    def Create(r,b,g,n1,n2,n3,cnt): 
        ColorArray = []
        for x in range(cnt):
            r = r+n1
            b = b+n2 # no more than 3
            g = g+n3
            a = ('#%02X%02X%02X' % (r,b,g))
            ColorArray.append(a)       
        return ColorArray,r,b,g
     
    ColorArray0 = []
    r0=1
    b0=1
    g0=10
    n1=1
    n2=1
    n3=2
    cnt=50
    ColorArray0,r0,b0,g0 = Create(r0,b0,g0,n1,n2,n3,cnt)       
    #print(ColorArray1)    
    
    ColorArray1 = []
    r1=5
    b1=5
    g1=100
    n1=1
    n2=1
    n3=1
    cnt=150
    ColorArray1,r1,b1,g1 = Create(r1,b1,g1,n1,n2,n3,cnt)       
    #print(ColorArray1)
    
    ColorArray2 = []
    r2=r1
    b2=b1
    g2=g1
    n1=1
    n2=1
    n3=0
    cnt=100
    ColorArray2,r2,b2,g2 = Create(r2,b2,g2,n1,n2,n3,cnt) 
    #print(ColorArray2)
    
    ColorArray3 = []
    r3=r2
    b3=b2
    g3=g2
    n1=0
    n2=-1
    n3=-1
    cnt=100
    ColorArray3,r3,b3,g3 = Create(r3,b3,g3,n1,n2,n3,cnt) 
    #print(ColorArray3)
    
    ColorArray4 = []
    r4=r3
    b4=b3
    g4=g3
    n1=0
    n2=-1
    n3=-1
    cnt = 150
    ColorArray4,r4,b4,g4 = Create(r4,b4,g4,n1,n2,n3,cnt) 
    #print(ColorArray4)
    
    # Python code to remove duplicate elements 
    def Remove(duplicate): 
        final_list = [] 
        for num in duplicate: 
            if num not in final_list: 
                final_list.append(num) 
        return final_list 
          
    # Driver Code 
    duplicate = ColorArray1
    RandVal1 = Remove(duplicate)
    duplicate = ColorArray2
    RandVal2 = Remove(duplicate)
    duplicate = ColorArray3
    RandVal3 = Remove(duplicate)
    duplicate = ColorArray4
    RandVal4 = Remove(duplicate)
    
    #print(len(RandVal1))
    #print(len(MiddleArray))
    sns.set()
    colors = RandVal1 + RandVal2 + RandVal3 + RandVal4
#    print(colors)
#    cmap = ListedColormap(sns.color_palette(colors).as_hex(), N=num)
#    cmap = sns.palplot(sns.hls_palette(10))
    return colors

# Call Function to get cmap

cmaps = makeSimplePalette(500)

def RdBu(value):
    array = makeSimplePalette(value)
    return array

 
#Data = pd.read_csv("temp.csv", index_col = 0)
#x = Data['duration']
#maxVal = max(x)
#minVal = min(x)
##print(maxVal)
##print(minVal)
#fig, ax = plt.subplots(figsize=(100, 1)) # specify size
##plt.savefig("custom_cmap.png")
#fig.subplots_adjust(bottom=0.5, right=0.2) # adjust's size by dividing it
#
##cmap = mpl.cm.husl
#norm = mpl.colors.Normalize(vmin=minVal, vmax=maxVal)
#
#cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmaps,
#                                norm=norm,
#                                orientation='horizontal')
#cb1.set_label('Some Units')
#fig.show()

    