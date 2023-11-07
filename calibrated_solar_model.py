import numpy as np
import scipy

from astropy.io import ascii
from astropy.table import Table 
from scipy.optimize import least_squares

import fileinput
import os
import sys

# Solar parameters
L_sun = 1.0
R_sun = 1.0
zx_sun = 0.0245 # Surface Z/X fraction


def replace(filename, input_expression, output_expression):
	for line in fileinput.input(filename, inplace = 1):
		if input_expression in line:
			line = line.replace(input_expression, output_expression)
		sys.stdout.write(line)


def no_diffusion(new):
	replace('inlist_project', 'new_Y = 0.27', 'new_Y = '+str(new[0]))
	replace('inlist_project', 'new_Z = 0.018', 'new_Z = '+str(new[1]))
	replace('inlist_project', 'mixing_length_alpha = 1.83', 'mixing_length_alpha = '+str(new[2]))
	os.system('./rn')
	replace('inlist_project', 'new_Y = '+str(new[0]), 'new_Y = 0.27')
	replace('inlist_project', 'new_Z = '+str(new[1]), 'new_Z = 0.018')
	replace('inlist_project', 'mixing_length_alpha = '+str(new[2]), 'mixing_length_alpha = 1.83')
	history = Table(ascii.read('SolarModel_NoDiff_'+str(zx_sun)+'/history.data', header_start = 4))
	L_star = 10**history['log_L'][-1] # Stellar luminosity
	R_star = 10**history['log_R'][-1] # Stellar radius
	zx_star = 10**history['log_surf_cell_z'][-1]/10**history['log_surface_h1'][-1] # Surface Z/X fraction
	return np.array([np.abs(L_star-L_sun), np.abs(R_star-R_sun), np.abs(zx_star-zx_sun)]) # Should be ~10e-[7/8/9]


def diffusion(new):
	replace('inlist_project', 'new_Y = 0.27', 'new_Y = '+str(new[0]))
	replace('inlist_project', 'new_Z = 0.018', 'new_Z = '+str(new[1]))
	replace('inlist_project', 'mixing_length_alpha = 1.83', 'mixing_length_alpha = '+str(new[2]))
	os.system('./rn')
	replace('inlist_project', 'new_Y = '+str(new[0]), 'new_Y = 0.27')
	replace('inlist_project', 'new_Z = '+str(new[1]), 'new_Z = 0.018')
	replace('inlist_project', 'mixing_length_alpha = '+str(new[2]), 'mixing_length_alpha = 1.83')
	history = Table(ascii.read('SolarModel_Diff_'+str(zx_sun)+'/history.data', header_start = 4))
	L_star = 10**history['log_L'][-1]
	R_star = 10**history['log_R'][-1]
	zx_star = 10**history['log_surf_cell_z'][-1]/10**history['log_surface_h1'][-1] 
	return np.array([np.abs(L_star-L_sun), np.abs(R_star-R_sun), np.abs(zx_star-zx_sun)]) 

initial_Y = 0.27
initial_Z = 0.018
mixing_length_alpha = 1.83
initial = np.array([initial_Y, initial_Z, mixing_length_alpha])
p = least_squares(diffusion, initial, bounds = ([0.20, 0.01, 1.0], [0.30, 0.03, 3.0])) 
print(p)
