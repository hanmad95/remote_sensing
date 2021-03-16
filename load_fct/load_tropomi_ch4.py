# -*- coding: utf-8 -*-
import os 
from netCDF4 import Dataset
import numpy as np
import pandas as pd 

#============================================================================
# Read the nc data of Tropomi
#============================================================================


def load_product_data(paths_to_files:list, area_of_interest:dict, qthresh:float, dates:str):
    """
    Notes to Inputs: 
        area_of_interest = {"lat_min_area":46,"lat_max_area":55,"lon_min_area":5,"lon_max_area":15}
        qthresh = only data samples above this quality threshold will be considered
    """
    dataframes = []
    sat_lats = []
    sat_lons = []
    grid_shapes = []
    max_ch4_values=[]
    min_ch4_values=[]
    i = 0    
    for path in paths_to_files:
        
        
        nc_file = Dataset(path, mode='r')
        grp = 'PRODUCT' #TROPOMI Structure
        lat = nc_file.groups[grp].variables['latitude'][0][:][:] # latitude of ground pixels
        shape = lat.shape
        lat = lat.reshape((lat.shape[0]*lat.shape[1],1))
        lon = nc_file.groups[grp].variables['longitude'][0][:][:].reshape(lat.shape)# longitude of ground pixels
    
        xch4_column_name = 'methane_mixing_ratio'
        not_cor_xch4_column_name = 'methane_mixing_ratio_not bias_corrected'
        data_quality = 'qa_value'
    
        # get xch4 data and transform it into array
        ch4_data=nc_file.groups[grp].variables[xch4_column_name]
        
        # get qualitiy of datapoints
        quality = nc_file.groups[grp].variables[data_quality]
    
        # get the satellite longitude and latitude for the WGS84 ellipsoid.
        sat_lat = nc_file['/PRODUCT/SUPPORT_DATA/GEOLOCATIONS/'].variables['satellite_latitude'][0]
        sat_lon = nc_file['/PRODUCT/SUPPORT_DATA/GEOLOCATIONS/'].variables['satellite_longitude'][0]
    
        # get the bounds in longitude and latitude for the WGS84 ellipsoid.
        bounds_lat = nc_file['/PRODUCT/SUPPORT_DATA/GEOLOCATIONS/'].variables['latitude_bounds'][0].reshape((lat.shape[0]*lat.shape[1],4))
        bounds_lon = nc_file['/PRODUCT/SUPPORT_DATA/GEOLOCATIONS/'].variables['longitude_bounds'][0].reshape((lat.shape[0]*lat.shape[1],4))
        
        # transform data into array
        dataArray=np.array(ch4_data[0][:][:])
        dataArray[dataArray==ch4_data._FillValue]=np.nan # replace fill value of dataset with nan 
        dataArray=dataArray.reshape(lat.shape)
        
        #transform quality
        qualityArray=np.array(quality[0][:][:]).reshape(lat.shape)
        qualityArray[qualityArray==quality._FillValue]=np.nan
        
        
        temp = np.concatenate((lat,lon,dataArray,qualityArray,bounds_lat,bounds_lon),axis =1)
        df = pd.DataFrame(temp,columns=["lat","lon","tropomi_ch4","quality","bounds_lat_ll","bounds_lat_lr","bounds_lat_ur","bounds_lat_ul","bounds_lon_ll","bounds_lon_lr","bounds_lon_ur","bounds_lon_ul"])
        del temp
                
        # Cut out Area of interest: 
        df = df.loc[df["lat"]>area_of_interest["lat_min_area"]]
        df = df.loc[df["lat"]<area_of_interest["lat_max_area"]]
        df = df.loc[df["lon"]>area_of_interest["lon_min_area"]]
        df = df.loc[df["lon"]<area_of_interest["lon_max_area"]]
        
        possible_samples = df.shape[0]
        
        # Cut out nan Values or fill values
        df = df.dropna(subset=["tropomi_ch4"])
        
        contained_samples = df.shape[0]
        print("Tropomi data from {3} fills {0} out of {1}: {2}%".format(contained_samples,possible_samples,(contained_samples/possible_samples)*100,dates[i]))
        # Assure certain quality
        df = df.loc[df["quality"]>= float(qthresh)]
        
        # Get Min and Max Values
        max_ch4 = np.max(df["tropomi_ch4"])
        min_ch4 = np.min(df["tropomi_ch4"])
        max_ch4_values.append(max_ch4)
        min_ch4_values.append(min_ch4)
        
        #Append on linst
        dataframes.append(df)
        grid_shapes.append(shape)
        sat_lats.append(sat_lat)
        sat_lons.append(sat_lon)
        
        # close nc file
        nc_file.close()
        
        # increase index 
        i +=1
        
    return dataframes,sat_lats,sat_lons,grid_shapes,max_ch4_values,min_ch4_values