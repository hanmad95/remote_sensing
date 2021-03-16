# -*- coding: utf-8 -*-
import branca.colormap as cm
import folium 
from folium import plugins
import numpy as np
#============================================================================
# Plot TROPOMI CH4 from one Dataframe
#============================================================================


def plot_cams_data(m,fg,dataframe,lat_grid,lon_grid,lat_bounds,lon_bounds,group_container):
    """
    Notes to Inputs: 
        dataframe = ["lat","lon","lat_index","lon_index","ch4"]
        _grid = location of grid center points
        _bounds = mark the area of each sample
        _container = contains the relevant folium layers
    """
    
    # Cut out ch4 of dataframe
    ch4 = dataframe["ch4"].to_numpy()
    lat_center= dataframe["lat"].to_numpy()
    lon_center = dataframe["lon"].to_numpy()
    lat_index = dataframe["lat_index"].to_numpy(dtype=int)
    lon_index = dataframe["lon_index"].to_numpy(dtype=int)
    
    #Min and max values
    min_value = np.nanmin(ch4)
    max_value = np.nanmax(ch4)    
            
    # Create Colormap
    colormap2 = cm.LinearColormap(colors=['green','lightgreen','brown'], index=[min_value,(min_value+max_value)/2,max_value],
                             vmin=min_value,vmax=max_value)
    m.add_child(colormap2)
    
    #============================================================================
    # Plot the filtered ch4 values onto the map
    #============================================================================
    # Draw the points    
    for k in range(ch4.shape[0]):
    
        # Create Parallelograms
        upper_left=(lat_bounds[lat_index[k]-1,0], lon_bounds[lon_index[k]-1,0])
        upper_right=(lat_bounds[lat_index[k]-1,0], lon_bounds[lon_index[k]-1,1])
        lower_right=(lat_bounds[lat_index[k]-1,1], lon_bounds[lon_index[k]-1,1])
        lower_left=(lat_bounds[lat_index[k]-1,1], lon_bounds[lon_index[k]-1,0])
        edges = [upper_left, upper_right, lower_right, lower_left]
        
        # Color
        color2 = colormap2(ch4[k])  
        # Add the Polygon
        folium.vector_layers.Polygon(locations=edges, color=color2, fill_color=color2,fill=False,fill_opacity=0.8).add_to(group_container[0])
        
        # Mark the centers of polygons
        folium.CircleMarker([lat_center[k], lon_center[k]],radius=1,color='black',fill=True,fill_opacity=0.3).add_to(group_container[1])
        
    return m
