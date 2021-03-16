# -*- coding: utf-8 -*-
import folium 
import numpy as np

#============================================================================
# Plot wind data
#============================================================================
# Input:
# Dataframe: ["lat","lon","lat_index","lon_index","ch4"]
def plot_wind_data(m,fg,lat,lon,u10,v10,group_container):
    
    color='black'
    scale=100
    #============================================================================
    # Plot the lulc classes
    #============================================================================
    # Draw the points    
    for k in range(lat.shape[0]):
        for i in range(lon.shape[0]):
            
            
            # draw line from center to the direction of wind
            source = [lat[k],lon[i]]
            sink = [lat[k]+u10[k,i]*scale,lon[i]+v10[k,i]*scale]
            line=[source,sink]
            
            # Create  Centers
            folium.CircleMarker([source[0], source[1]],radius=0.5,color=color,
                            fill=True,fill_opacity=0.7).add_to(group_container[0])
            # Create Sinks
            folium.CircleMarker([sink[0], sink[1]],radius=3,color=color,
                            fill=True,fill_opacity=0.7).add_to(group_container[0])
            
            
            folium.PolyLine(line,color=color,fill=True,fill_opacity=1,weight=2.5).add_to(group_container[0])
            
    return m
    
    