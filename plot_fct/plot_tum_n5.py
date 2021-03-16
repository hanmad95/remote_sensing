# -*- coding: utf-8 -*-
import branca.colormap as cm
import folium 
from folium import plugins
import numpy as np

#============================================================================
# Plot TROPOMI CH4 from one Dataframe
#============================================================================
# Input:
# Dataframe: ['utc-timestamp', 'center_xch4_ppm', 'south_xch4_ppm', 'west_xch4_ppm', 'north_xch4_ppm', 'east_xch4_ppm']
# Stations {"center":(48.150712,11.569149), "north":(48.250000,11.548000),"east":(48.148000,11.730000),"south":(48.04200,11.60800),"west":(48.12100,11.425000)}
def plot_tum_n5_ch4(m,fg,dataframe,stations,trop_colormap,group_container):
    
    # Load values and convert ppm into ppb
    center_ch4 = float(dataframe['center_xch4_ppm'].values[0])*1000
    south_ch4 = float(dataframe['south_xch4_ppm'].values[0])*1000
    west_ch4 = float(dataframe['west_xch4_ppm'].values[0])*1000
    north_ch4 = float(dataframe['north_xch4_ppm'].values[0])*1000
    east_ch4 = float(dataframe['east_xch4_ppm'].values[0])*1000
    values_ch4 = [center_ch4,south_ch4,west_ch4,north_ch4,east_ch4]
    dictionary_keys = ["center","south","west","north","east"]
  
    # Ignore the zero values
    k = 0
    for vals in values_ch4:
        if vals == 0:
            del dictionary_keys[k]
            del values_ch4[k]
        k+=1
  
    #============================================================================
    # Plot the filtered ch4 values onto the map
    #============================================================================
    # Draw the points    
    for index,key in enumerate(dictionary_keys):
        
        lat_center = stations[key][0]
        lon_center = stations[key][1]
        ch4_val = values_ch4[index]
        
        # Color
        color = trop_colormap(ch4_val)  
        
        # Mark the datapoint
        folium.CircleMarker([lat_center, lon_center],radius=3,color=color,fill=True,fill_opacity=0.8).add_to(group_container[0])
        
    return m


