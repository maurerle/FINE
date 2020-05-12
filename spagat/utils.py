import geopandas as gpd
import os

import time

import matplotlib.pyplot as plt


def plt_savefig(save_name=None, path=None, fig=None, bbox_inches=None):
    if fig is None:
        fig = plt.gcf()

    if path is not None:
        save_name = os.path.join(path, save_name)
        print(''.format(save_name))

    if save_name is None:
        plt.savefig('test.png', format='png')
    else:
        plt.savefig('{}.png'.format(save_name), format='png',
                    bbox_inches="tight", dpi=200)


def timer(func):
    def f(*args, **kwargs):
        before = time.perf_counter()  # maybe exchange with time.process_time()
        rv = func(*args, **kwargs)
        after = time.perf_counter()
        print('elapsed time for {.__name__}: {:.2f} minutes'.format(func, (after - before)/60))
        return rv
    return f


def create_dir(directory):
    '''Creates a new directory, if it doesn't exist yet.'''
    if not os.path.exists(directory):

        os.makedirs(directory)


def create_gdf(df, geometries, crs, filepath=None):
    gdf = gpd.GeoDataFrame(df, geometry=geometries)
    gdf.crs = {'init': f'epsg:{crs}'}  # TODO: check whether this works correctly

    if filepath is not None:
        gdf.to_file(filepath)

    return gdf
