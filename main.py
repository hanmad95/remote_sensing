#============================================================================
# 0. Import Section
#============================================================================
import os
import sys
import folium
import pickle
from folium import plugins
from datetime import datetime, timedelta

# Add Folderpaths 
current_dir = os.path.dirname(os.path.abspath(__file__))
folder_names = ["load_fct","plot_fct"]
for folder in folder_names:
    Funktion_path = current_dir + "\\" + folder
    sys.path.insert(0,Funktion_path)
    
#Loading and Plotting Functions
from load_tropomi_ch4 import load_product_data
from plot_tropomi_ch4 import plot_tropomi
from load_cams_ch4 import load_CAMS_data
from plot_cams_ch4 import plot_cams_data
from plot_lulc import plot_merged_lulc_data
from merge_data import data_merge_down_lulc_only
from merge_data import data_merge_down
from load_wind_data import load_wind
from plot_wind import plot_wind_data


#============================================================================
#  1 Create Map and Layer COntrol
#============================================================================
# Create Map with Zoom at Munich
m = folium.Map(location=[48.137154, 11.576124],zoom_start=10)

#Define Feature Groups:
fg = folium.FeatureGroup(name=' All CH4 Features from 19.09.202)
m.add_child(fg)

# Create Feature SubGroup of TROPOMI
group_tropomi = plugins.FeatureGroupSubGroup(fg,'TROPMI CH4 [mol / m^2]')
m.add_child(group_tropomi)
group_tropomi_trail = plugins.FeatureGroupSubGroup(fg,'Satellite Trail')
m.add_child(group_tropomi_trail)
group_tropomi_centers = plugins.FeatureGroupSubGroup(fg, 'TROPOMI Centerpoints')
m.add_child(group_tropomi_centers)
group_tropomi_container=[group_tropomi,group_tropomi_trail,group_tropomi_centers]

# Subgroup for the CAMS-REG DATA:
group_cams_reg_ch4 = plugins.FeatureGroupSubGroup(fg, 'CAMS_REG CH4 [kg / year]')
m.add_child(group_cams_reg_ch4)
group_cams_reg_centerpoints = plugins.FeatureGroupSubGroup(fg, 'CAMS_REG_Centerpoints')
m.add_child(group_cams_reg_centerpoints)
group_cams_reg_container=[group_cams_reg_ch4, group_cams_reg_centerpoints]

#Add Wind Data
group_wind = plugins.FeatureGroupSubGroup(fg, 'Wind Data')
m.add_child(group_wind)
group_wind_container=[group_wind]

 # Add Layer Control to Map
folium.LayerControl(collapsed=True).add_to(m)


#============================================================================
# 2. Load TROPOMI DATA [mol / m^2]
#============================================================================

# Read all files of directory into programm
directory = os.getcwd() + r"\tropomi" 
filenames = list(filter(lambda x: '.nc' in x , os.listdir(directory)))

dates = []
paths_to_files = []
for files in filenames:
    paths_to_files.append(os.getcwd() + '\\tropomi\\' +  files)
    dates.append(files[20:28])

area_of_interest = {"lat_min_area":47,"lat_max_area":49,"lon_min_area":10.5,"lon_max_area":12.5}
dataframes,sat_lats,sat_lons,grid_shapes,max_ch4_values,min_ch4_values = load_product_data(paths_to_files, area_of_interest,0,dates)
print("TROPOMI DATA LOADED")


##============================================================================
# 3 PLOT TROPOMI DATA
#=============================================================================
# Choose the data that should be inspected 
i =1
# Plot TROPOMI DATA
m = plot_tropomi(m,fg,dataframes[i],grid_shapes[i],min_ch4_values[i],max_ch4_values[i],sat_lats[i],sat_lons[i],group_tropomi_container)
print("TROPOMI DATA PLOTTED")


##============================================================================
# 4 Read CAMS-REG data [kg / year]
#=============================================================================
# Data was from the  2019
current_dir = os.getcwd()
file_name = r'\CAMS-REG-GHG_v4_2_emissions_year2019.nc'
path_to_file = current_dir + r'\cams_reg' + file_name
category_weights=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] # ABCDEF1F2F3F4GHIJKLM #15

cam_df,cam_lat_grid,cam_lat_bounds,cam_lon_grid,cam_lon_bounds = load_CAMS_data(path_to_file, category_weights, area_of_interest)
print("CAMS DATA LOADED")


##============================================================================
# 5  Add CAMS REG data to MAP
#=============================================================================
m = plot_cams_data(m,fg,cam_df,cam_lat_grid,cam_lon_grid,cam_lat_bounds,cam_lon_bounds,group_cams_reg_container)
print("CAMS DATA PLOTTED")


##============================================================================
#  6 Add wind data
#=============================================================================
current_dir = os.getcwd()
file_name = r'\ecmwf_wind_2020_Sept.nc'
path_to_file = current_dir + r'\ecmwf' + file_name
wind_date = datetime(2020,9,19,12,0,0)

# Get Wind Data
lat_wind,lon_wind,time,u10,v10 = load_wind(path_to_file,area_of_interest,wind_date)
# Plot Wind Data
m = plot_wind_data(m,fg,lat_wind,lon_wind,u10,v10,group_wind_container)


##============================================================================
# 7 Save the map
#=============================================================================
# Save Map
name_of_map = r"maps\Map_trop_"+dates[i]+"_wind_" +str(wind_date)[0:10] +".html" 
m.save(name_of_map)
print("MAP Saved")
