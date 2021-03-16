import pandas as pd
import numpy as np
from netCDF4 import Dataset

def load_CAMS_data(path_to_file:list, weights:list, area_of_interest:dict):
        # INPUT: area_of_interest = {"lat_min_area":46,"lat_max_area":55,"lon_min_area":5,"lon_max_area":15}

        #============================================================================
        # Load the grid
        #============================================================================
        nc_file = Dataset(path_to_file, mode='r')
        # Load the grid of CAMS REG AP
        lat_grid = np.array(nc_file.variables['latitude'])
        lat_bounds = np.array(nc_file.variables['latitude_bounds'])
        lon_grid = np.array(nc_file.variables['longitude'])
        lon_bounds = np.array(nc_file.variables['longitude_bounds'])

        #============================================================================
        # Load CH4 Data, Remove 0 values
        #============================================================================
        
        # load ch4 data
        ch4 = np.array(nc_file.variables['ch4'])
        ch4 = ch4.reshape(ch4.shape[0],1)
        lat_center = np.array(nc_file.variables['latitude_source']).reshape(ch4.shape)# latitude of necessary ground pixels
        lon_center = np.array(nc_file.variables['longitude_source']).reshape(ch4.shape) # longitude of ground pixels
        lat_index = np.array(nc_file.variables['latitude_index']).reshape(ch4.shape)# index of grid latitude
        lon_index = np.array(nc_file.variables['longitude_index']).reshape(ch4.shape) #  index of grid longitude
        
        # Possible Categories
        cat = np.array(nc_file.variables['emis_cat_code'])
        # load data categories from all data points
        data_cat = np.array(nc_file.variables['emission_category_index']).reshape(ch4.shape)
        
        # Create Dataframe
        df = pd.DataFrame(np.hstack((lat_center,lon_center,lat_index,lon_index,ch4,data_cat)),columns=["lat","lon","lat_index","lon_index","ch4","data_cat"],dtype=float)
        del lat_center,lon_center,lat_index,lon_index,ch4
        
        # Delete zero values and not interested areas
        df = df.loc[df["ch4"]!= 0]
        df = df.loc[df["lat"]>area_of_interest["lat_min_area"]]
        df = df.loc[df["lat"]<area_of_interest["lat_max_area"]]
        df = df.loc[df["lon"]>area_of_interest["lon_min_area"]]
        df = df.loc[df["lon"]<area_of_interest["lon_max_area"]]
           
        # Filter out unique lon lat comibinations into new merged df:
        merged_df = df.loc[:, df.columns != "data_cat"]
        merged_df = merged_df.loc[:, merged_df.columns != "ch4"]
        merged_df = merged_df.drop_duplicates(subset=['lat','lon'], keep='last')
     
        
        # Merge all Categories together
        temp_array = np.zeros((merged_df.shape[0],1))
        for k in range(temp_array.shape[0]):
            temp = df.loc[df["lat"] == merged_df.iloc[k,0]]
            temp = temp.loc[temp["lon"] == merged_df.iloc[k,1]]  
            if temp.shape[0] != 0:
                for l in range(temp.shape[0]):
                    temp_array[k,0] += float(weights[int(temp.iloc[l,5])-1])*float(temp.iloc[l,4])
           
        temp_array = temp_array.reshape(temp_array.shape[0],1)
        merged_array = merged_df.to_numpy()
        merged_array = np.concatenate((merged_array,temp_array), axis=1) #"lat","lon","lat_index","lon_index","datat_cat","ch4"
        del merged_df,temp_array,temp
        
        # convert into dataframe again.
        df = pd.DataFrame(merged_array,columns=["lat","lon","lat_index","lon_index","ch4"])           
        del merged_array
        
         # close nc file
        nc_file.close()
        
        return df,lat_grid,lat_bounds,lon_grid,lon_bounds