import pytest
import numpy as np 
import xarray as xr 

import spagat.dataset as spd
import spagat.representation as spr
import spagat.grouping as spg

import metis_utils.io_tools as ito


@pytest.mark.skip()
def test_add_region_centroids_and_distances():

    sds = spd.SpagatDataSet()

    # ...

    spr.add_region_centroids(sds)
    spr.add_centroid_distances(sds)


#@pytest.mark.skip()
def test_aggregate_based_on_sub_to_sup_region_id_dict():
    
     #read the xr_dataset and manipulate it to obtain a test xarray dataset
     test_xr_dataset = xr.open_dataset('tests/data/input/sds_xr_dataset.nc4')
     test_xr_dataset = test_xr_dataset.where(test_xr_dataset==1, other=1)
     
     #save the data in the same folder where the shapefile is 
     test_xr_dataset.to_netcdf('tests/data/input/test_xr_dataset.nc4')  

     #get the dictonary output by string_based_clustering function
     test_xr_dataset_dict = spg.string_based_clustering(test_xr_dataset['region_ids'].values)
     
     #get the sds form of the data and shapefile 
     test_sds = spd.SpagatDataSet()
     test_sds.read_sds(sds_folder_path='tests/data/input' , sds_regions_filename='sds_regions.shp', 
                       sds_xr_dataset_filename='test_xr_dataset.nc4')
     
     #run the function 
     test_output_sds = spr.aggregate_based_on_sub_to_sup_region_id_dict(test_sds, test_xr_dataset_dict)
     test_output_xr_dataset = test_output_sds.xr_dataset
     
     #assert functions 
     ##testing aggregate_connections, with mode='bool'
     assert test_output_sds.xr_dataset['AC_cable_incidence'].loc['de', 'es']== 1
     ##testing aggregate_connections, with mode='sum'
     assert test_output_sds.xr_dataset['AC_cable_capacity'].loc['de', 'es'] == 25
     ##testing aggregate_time_series, with mode='sum'
     assert test_output_xr_dataset['e_load'].loc['de', 8].values == 5
     ##testing aggregate_time_series, with mode='weighted mean'
     assert test_output_sds.xr_dataset['wind cf'].loc['de', 6] == 1
     ##testing aggregate_values, with mode='sum'
     assert test_output_sds.xr_dataset['wind capacity'].loc['de'] == 5

     #assert test_output_sds.add_objects 

     #assert add_region_centroids(test_output_sds)

    

    
    


@pytest.mark.skip()
def test_aggregate_geometries():
    pass


#@pytest.mark.skip()
def test_aggregate_time_series():
     
     #import dataset 
     ds = xr.open_dataset('tests/data/input/sds_xr_dataset.nc4')

     #get the dictonary output by string_based_clustering function
     dict_ds = spg.string_based_clustering(ds['region_ids'].values)
    
     #A test_xr_DataArray is created with dummy values, coordinates and dimensions being region_ids and time
     region_ids = ds['region_ids'].values
     time = ds['time'].values

     temp_num = 60*8760 
     xr_DataArray_values = np.ones(temp_num)*5  #create array of 5s
     xr_DataArray_values = np.reshape(xr_DataArray_values, (60,8760))

     test_xr_DataArray = xr.DataArray(xr_DataArray_values, coords=[region_ids,time], dims=['region_ids','time'])
     
     #call the function 
     ##modes have to be changed, xr_weight_array has to be provided in case of weighted mean  
     mode = 'weighted mean'
     xr_weight_array = test_xr_DataArray   #for weighted mean
     time_series_aggregated = spr.aggregate_time_series(test_xr_DataArray, dict_ds, mode=mode, xr_weight_array=xr_weight_array)

     #correct values for mean = 5, weighted mean = 5, sum = 25  for loc[4,'de']
     assert time_series_aggregated.loc[4,'de'].values == 5   


@pytest.mark.skip()
def test_create_grid_shapefile():
    pass
