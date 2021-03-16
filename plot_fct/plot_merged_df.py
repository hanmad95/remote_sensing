
# -*- coding: utf-8 -*-
import branca.colormap as cm
import folium 
from folium import plugins
import numpy as np

##============================================================================
# Plot the merged data
#=============================================================================
# Input:
# Dataframe: # ["lat","lon","lat_index","lon_index","cams_reg_ch4","quality","tropomi_ch4","lulc_class"]
# GroupContainer: [group_tropomi_container,group_cams_reg_container, group_lulc_container]
def plot_merged(m,fg,dataframe,lat_bounds,lon_bounds,group_container):
    

    cam_ch4 = dataframe["cams_reg_ch4"].to_numpy()
    trop_ch4 = dataframe["tropomi_ch4"].to_numpy()
    lulc_classes = dataframe["lulc_class"].to_numpy()
    lat_center= dataframe["lat"].to_numpy()
    lon_center = dataframe["lon"].to_numpy()
    lat_index = dataframe["lat_index"].to_numpy(dtype=int)
    lon_index = dataframe["lon_index"].to_numpy(dtype=int)
    
    # Create Colormap for CAMS_REG---------------------------------------------------------
    cam_min_value = np.nanmin(cam_ch4)
    cam_max_value = np.nanmax(cam_ch4)
    cam_colormap = cm.LinearColormap(colors=['green','lightgreen','brown'], index=[cam_min_value,(cam_min_value+cam_max_value)/2,cam_max_value],
                             vmin=cam_min_value,vmax=cam_max_value)
    m.add_child(cam_colormap)
    
    # Create Colormap for Tropomi ---------------------------------------------------------
    trop_min_value = np.nanmin(trop_ch4)
    trop_max_value = np.nanmax(trop_ch4)
    trop_colormap = cm.LinearColormap(colors=['blue','lightblue','red'], index=[trop_min_value,(trop_min_value+trop_max_value)/2,trop_max_value],
                             vmin=trop_min_value,vmax=trop_max_value)
    m.add_child(trop_colormap)
    
    
    # Create Colormap for Tropomi ---------------------------------------------------------
    lulc_min_value = np.nanmin(lulc_classes)
    lulc_max_value = np.nanmax(lulc_classes)
    lulc_colormap = cm.LinearColormap(colors=['green','lightgreen','brown'], index=[lulc_min_value,(lulc_min_value+lulc_max_value)/2,lulc_max_value],
                             vmin=lulc_min_value,vmax=lulc_max_value)
    m.add_child(lulc_colormap)
    
    
    #============================================================================
    # Plot the filtered ch4 values onto the map
    #============================================================================
    # Draw the points    
    for k in range(cam_ch4.shape[0]):
    
        # Create Parallelograms
        upper_left=(lat_bounds[lat_index[k]-1,0], lon_bounds[lon_index[k]-1,0])
        upper_right=(lat_bounds[lat_index[k]-1,0], lon_bounds[lon_index[k]-1,1])
        lower_right=(lat_bounds[lat_index[k]-1,1], lon_bounds[lon_index[k]-1,1])
        lower_left=(lat_bounds[lat_index[k]-1,1], lon_bounds[lon_index[k]-1,0])
        edges = [upper_left, upper_right, lower_right, lower_left]
        
        # Add Color for CAMS-REG Data--------------------------------
        cam_color= cam_colormap(cam_ch4[k])  
        # Add the Polygon
        folium.vector_layers.Polygon(locations=edges, color=cam_color, fill_color=cam_color,fill=False,fill_opacity=0.8).add_to(group_container[1][0])
        
        # Add Color for Tropomi Data--------------------------------
        
        if not np.isnan(trop_ch4[k]):
            trop_color= trop_colormap(trop_ch4[k])  
            # Add the Polygon
            folium.vector_layers.Polygon(locations=edges, color=trop_color, fill_color=trop_color,fill=False,fill_opacity=0.8).add_to(group_container[0][0])
            
        # Add Color for LULC--------------------------------
        lulc_color= lulc_colormap(lulc_classes[k])  
        # Add the Polygon
        folium.vector_layers.Polygon(locations=edges, color=lulc_color, fill_color=lulc_color,fill=False,fill_opacity=0.8).add_to(group_container[2][0])
        
        # Mark the centers points 
        folium.CircleMarker([lat_center[k], lon_center[k]],radius=1,color='black',fill=True,fill_opacity=0.3).add_to(group_container[1][1])
        
    return m,trop_colormap



# Dataframe: ["lat","lon","tropomi_ch4","quality", "cams_reg_ch4","lulc_class"]
# GroupContainer: [group_tropomi_container,group_cams_reg_container, group_lulc_container]
def plot_merged_to_trop(m,fg,dataframe,cur_tum_n5_df,group_container):
    

    cam_ch4 = dataframe["cams_reg_ch4"].to_numpy()
    trop_ch4 = dataframe["tropomi_ch4"].to_numpy()
    lulc_classes = dataframe["lulc_class"].to_numpy()
    lat_center= dataframe["lat"].to_numpy()
    lon_center = dataframe["lon"].to_numpy()

    # Check CH4 range of TUM N5------------------------------------------------    
    tum_ch4 = cur_tum_n5_df.iloc[[0][:]].to_numpy()
    tum_ch4 = tum_ch4[0,1:]*1000
    tum_ch4_values = []
    # Ignore the zero values
    k = 0
    for vals in tum_ch4:
        if vals != 0:
            tum_ch4_values.append(vals)
    
    tum_min = min(tum_ch4_values)
    tum_max = max(tum_ch4_values)
    
    # Create Colormap for CAMS_REG---------------------------------------------------------
    cam_min_value = np.nanmin(cam_ch4)
    cam_max_value = np.nanmax(cam_ch4)
    cam_colormap = cm.LinearColormap(colors=['green','lightgreen','brown'], index=[cam_min_value,(cam_min_value+cam_max_value)/2,cam_max_value],
                             vmin=cam_min_value,vmax=cam_max_value)
    m.add_child(cam_colormap)
    
    # Create Colormap for Tropomi ---------------------------------------------------------
    trop_min_value = min(tum_min,np.nanmin(trop_ch4))
    trop_max_value = max(tum_max,np.nanmax(trop_ch4))
    trop_colormap = cm.LinearColormap(colors=['blue','lightblue','red'], index=[trop_min_value,(trop_min_value+trop_max_value)/2,trop_max_value],
                             vmin=trop_min_value,vmax=trop_max_value)
    m.add_child(trop_colormap)
    
    
    # Create Colormap for Tropomi ---------------------------------------------------------
    lulc_min_value = np.nanmin(lulc_classes)
    lulc_max_value = np.nanmax(lulc_classes)
    lulc_colormap = cm.LinearColormap(colors=['green','lightgreen','brown'], index=[lulc_min_value,(lulc_min_value+lulc_max_value)/2,lulc_max_value],
                             vmin=lulc_min_value,vmax=lulc_max_value)
    m.add_child(lulc_colormap)
    
    
    #============================================================================
    # Plot the filtered ch4 values onto the map
    #============================================================================
    # Draw the points    
    for k in range(dataframe.shape[0]):
    
        # Create Parallelograms
        upper_left=(dataframe["bounds_lat_ul"].iloc[k], dataframe["bounds_lon_ul"].iloc[k])
        upper_right=(dataframe["bounds_lat_ur"].iloc[k], dataframe["bounds_lon_ur"].iloc[k])
        lower_right=(dataframe["bounds_lat_lr"].iloc[k], dataframe["bounds_lon_lr"].iloc[k])
        lower_left=(dataframe["bounds_lat_ll"].iloc[k], dataframe["bounds_lon_ll"].iloc[k])
        edges = [upper_left, upper_right, lower_right, lower_left]
        
        # Calculate rotation angle
        lat_dist = abs(lower_left[0] - lower_right[0])
        lon_dist = abs(lower_left[1] - lower_right[1])
        angle = np.arctan(lat_dist/lon_dist)
        missed_area_due_merge = 1
        
        
        # Add Color for CAMS-REG Data--------------------------------
        cam_color= cam_colormap(cam_ch4[k])  
        # Add the Polygon
        folium.vector_layers.Polygon(locations=edges, color=cam_color, fill_color=cam_color,fill=False,fill_opacity=0.8).add_to(group_container[1][0])
        
        # Add Color for Tropomi Data--------------------------------
        
        if not np.isnan(trop_ch4[k]):
            trop_color= trop_colormap(trop_ch4[k])  
            # Add the Polygon
            folium.vector_layers.Polygon(locations=edges, color=trop_color, fill_color=trop_color,fill=False,fill_opacity=0.8).add_to(group_container[0][0])
            
        # Add Color for LULC--------------------------------
        lulc_color= lulc_colormap(lulc_classes[k])  
        # Add the Polygon
        folium.vector_layers.Polygon(locations=edges, color=lulc_color, fill_color=lulc_color,fill=False,fill_opacity=0.8).add_to(group_container[2][0])
        
        # Mark the centers points 
        folium.CircleMarker([lat_center[k], lon_center[k]],radius=1,color='black',fill=True,fill_opacity=0.3).add_to(group_container[0][1])
        
    return m,trop_colormap

def plot_merged_outliers(m,merged_df,labels,color,container):
    
    if merged_df.shape[0] != len(labels):
        print("labels do not fit to input data!")
        
    else:
        # Cut out nan values from merging
        merged_df = merged_df.dropna(subset=["tropomi_ch4"])
        
        lat = merged_df["lat"].to_numpy()
        lon = merged_df["lon"].to_numpy()

        for k in range(merged_df.shape[0]):
            
            if labels[k] == 1 : 
                # Mark Oultier on map
                folium.CircleMarker([lat[k], lon[k]],radius=3,
                color=color,fill=False,fill_opacity=1).add_to(container[0])
                
                
    return m 