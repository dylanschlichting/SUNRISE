import numpy as np
import xarray as xr
import xroms
import glob

#Compute time mean at each grid cell for free surface height that is resampled to 1 W
#to make datastructures more manageable. We are doing the entire model output to make 
#the model conditions closer to how the along-track data are calculated.
years = np.arange(1994, 2017)
dsh = []
dsz = []

for y in years:
    path = '/d1/shared/TXLA_ROMS/output_20yr_obc/%i/ocean_his_00*.nc' % y
    ds = xroms.xroms.open_netcdf(glob.glob(path), chunks = {'ocean_time':1})
    ds, grid = xroms.xroms.roms_dataset(ds, Vtransform = None)
    ds = ds.resample(ocean_time="1W").mean()
    dsz.append(ds.zeta)
    
zeta = xr.concat(dsz,dim = 'ocean_time')
zetamean = zeta.mean(dim = 'ocean_time')
zetamean.to_netcdf('zeta_20yrmean.nc')