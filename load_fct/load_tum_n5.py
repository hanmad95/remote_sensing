# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

#============================================================================
# Read the csv data | ch4 data in ppm
#============================================================================


def load_tum_n5_ch4(path_to_file):
     
    #META Information about the measurement stations 
    stations = {"center":(48.150712,11.569149), "north":(48.250000,11.548000),"east":(48.148000,11.730000),"south":(48.04200,11.60800),"west":(48.12100,11.425000)}
    
    #Read the CSV file 
    df = pd.read_csv(path_to_file)
    headers = list(df)
    
    #Drop the xco2 data columns
    for col_name in headers:
        if str("xco2") in col_name:
            headers.remove(col_name)
            df = df.drop(col_name,axis=1)
    
    return df,stations
