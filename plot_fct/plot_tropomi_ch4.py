import branca.colormap as cm
import folium 
import numpy as np
#============================================================================
# Plot TROPOMI CH4 from one Dataframe
#============================================================================


def plot_tropomi(m,fg,dataframe,grid_shape,min_value,max_value,sat_lat,sat_lon,group_container):
    
    """
    Notes to Inputs: 
        dataframe = ["lat","lon","tropomi_ch4","quality","bounds_lat_ll","bounds_lat_lr","bounds_lat_ur",
                     "bounds_lat_ul","bounds_lon_ll","bounds_lon_lr","bounds_lon_ur","bounds_lon_ul"]
        sat_= location of the satellite trial
        _container = contains the relevant folium layers
    """
    # Create Colormap
    colormap = cm.LinearColormap(colors=['blue','lightblue','red'], index=[min_value,(min_value+max_value)/2,max_value],
                                 vmin=min_value,vmax=max_value)
    m.add_child(colormap)
        
    # Add all sample points
    for k in range(dataframe["tropomi_ch4"].shape[0]):
        
        #overlook the nan values
        if np.isnan(dataframe["tropomi_ch4"].iloc[k]):
            continue
                                        
        # Create  Centers
        folium.CircleMarker([dataframe["lat"].iloc[k], dataframe["lon"].iloc[k]],radius=1,color='b',
                            fill=True,fill_opacity=0.7).add_to(group_container[2])
        # Create Parallelograms
        upper_left=(dataframe["bounds_lat_ul"].iloc[k], dataframe["bounds_lon_ul"].iloc[k])
        upper_right=(dataframe["bounds_lat_ur"].iloc[k], dataframe["bounds_lon_ur"].iloc[k])
        lower_right=(dataframe["bounds_lat_lr"].iloc[k], dataframe["bounds_lon_lr"].iloc[k])
        lower_left=(dataframe["bounds_lat_ll"].iloc[k], dataframe["bounds_lon_ll"].iloc[k])
        edges = [upper_left, upper_right, lower_right, lower_left]
            
        color = colormap(dataframe["tropomi_ch4"].iloc[k])
    
        # Add the Polygon
        folium.vector_layers.Polygon(locations=edges, color=color, fill_color=color,fill=True,fill_opacity=0.7).add_to(group_container[0])
            
    # Plott the Satellite Path
    for k in range(sat_lat.shape[0]):
        
        # Also plott the satellite travelling
        folium.CircleMarker([sat_lat[k], sat_lon[k]],radius=1,color='green',fill=True,fill_opacity=0.8).add_to(group_container[1])
        
    return m