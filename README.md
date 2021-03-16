-------------------------------------------------------------------------------------------------
Remote Sensing Data Visualization
-------------------------------------------------------------------------------------------------

- Description:
  1. The project is about the visualization of Methane data of one day in Munich: 19.09.2020. 
  2. Data sources are CH4 Tropomi data available at: https://s5phub.copernicus.eu/dhus/#/home,
     CAMS-REG CH4 Emission Estimation and ECMWF Wind data.
  3. The visualization should give a nice insight into the methane hotspots and coldspots around Munich
  4. You can see that a lot of coldspots are due to the underlying underground: lakes, forests, wherease the hotspots
     are mainly due to the dense traffic in the city centers.

- How to use the structure:
  1. Adapt the filepaths to the individial netCDF files of Tropomi / EMCWF Wind data / CAMS-REG GHG
  2. Make sure to select the right time for the wind data, it should be as accurate as possible.
  3. Run the main.py file.
