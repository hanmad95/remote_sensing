# -*- coding: utf-8 -*-
import branca.colormap as cm
import folium 
from folium import plugins
import numpy as np

#============================================================================
# Plot LULC Data
#============================================================================
# Input:
# Dataframe: ["lat","lon","lat_index","lon_index","ch4"]
def plot_lulc_data(m,fg,lulc,lat,lon,lat_bounds,lon_bounds,group_container):
    
    #Min and max values
    min_value = np.nanmin(lulc)
    max_value = np.nanmax(lulc)    
    
    # Create Colormap
    colormap2 = cm.LinearColormap(colors=['green','lightgreen','brown'], index=[min_value,(min_value+max_value)/2,max_value],
                             vmin=min_value,vmax=max_value)
    m.add_child(colormap2)
    
    #============================================================================
    # Plot the lulc classes
    #============================================================================
    # Draw the points    
    for k in range(lat.shape[0]):
        for i in range(lon.shape[0]):
        
            # Create Parallelograms
            upper_left=(lat_bounds[k,0], lon_bounds[i,0])
            upper_right=(lat_bounds[k,0], lon_bounds[i,1])
            lower_right=(lat_bounds[k,1], lon_bounds[i,1])
            lower_left=(lat_bounds[k,1], lon_bounds[i,0])
            edges = [upper_left, upper_right, lower_right, lower_left]
            
            # Color
            color2 = colormap2(lulc[k,i])  
            # Add the Polygon
            folium.vector_layers.Polygon(locations=edges, color=color2, fill_color=color2,fill=False,fill_opacity=0.8).add_to(group_container[0])
            
            # Mark the centers of polygons
            #folium.CircleMarker([lat_center[k], lon_center[k]],radius=1,color='black',fill=True,fill_opacity=0.3).add_to(group_container[1])
        
    return m
    
# merged dataframe content ["lat","lon","cams_reg_ch4","lulc_class"]
def plot_merged_lulc_data(m,fg,merged_df,lat_bounds,lon_bounds,group_container):
    
    lulc = merged_df["lulc_class"].to_numpy()
    lat_index = merged_df["lat_index"].to_numpy(dtype=int)
    lon_index = merged_df["lon_index"].to_numpy(dtype=int)
    
    #Min and max values
    min_value = np.nanmin(lulc)
    max_value = np.nanmax(lulc)
    # Create Colormap
    colormap2 = cm.LinearColormap(colors=['green','lightgreen','brown'], index=[min_value,(min_value+max_value)/2,max_value],
                             vmin=min_value,vmax=max_value)
    m.add_child(colormap2)
    
    #============================================================================
    # Plot the filtered ch4 values onto the map
    #============================================================================
    # Draw the points    
    for k in range(lulc.shape[0]):
    
        # Create Parallelograms
        upper_left=(lat_bounds[lat_index[k]-1,0], lon_bounds[lon_index[k]-1,0])
        upper_right=(lat_bounds[lat_index[k]-1,0], lon_bounds[lon_index[k]-1,1])
        lower_right=(lat_bounds[lat_index[k]-1,1], lon_bounds[lon_index[k]-1,1])
        lower_left=(lat_bounds[lat_index[k]-1,1], lon_bounds[lon_index[k]-1,0])
        edges = [upper_left, upper_right, lower_right, lower_left]
        
        # Color
        color2 = colormap2(lulc[k])  
        # Add the Polygon
        folium.vector_layers.Polygon(locations=edges, color=color2, fill_color=color2,fill=False,fill_opacity=0.8).add_to(group_container[0])
        

        
    return m
