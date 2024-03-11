'''
ExoToComsol

Copyright 2024 National Technology & Engineering Solutions of Sandia, LLC (NTESS). 
Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

BSD 3-Clause License
'''
from exodus3 import *
import numpy as np
import re

from src import Node
from src import Element_Tetrahedra
from src import util

#01/10/2023: code plan: one way of doing the comsol to exo roi crop is as below: 

# read in comsol data as before
# based on user inputs on x, y, z lower and upper bounds kind of generate another txt file of COMSOL
# Now just do the same comsol to exo as before with the roi cropped COMSOL txt file


#user inputs:

inputFolderPath = './input_folder/'
outputFolderPath = './output_folder/'

input_comsol_file_name = "forComsolToExoInput.txt"
outputExodusFilename='output_exo_roi_cropped.e'

x_coord_lower_bound = -0.5 
x_coord_upper_bound = 0.5

y_coord_lower_bound = -0.5
y_coord_upper_bound = 0.5
    
z_coord_lower_bound = -0.5 
z_coord_upper_bound = 0.0

bounds = [[x_coord_lower_bound, x_coord_upper_bound], 
          [y_coord_lower_bound, y_coord_upper_bound],
          [z_coord_lower_bound, z_coord_upper_bound]]

#Get exodus file from comsol data
util.comsolToExo_with_ROI(inputFolderPath, input_comsol_file_name, outputFolderPath, outputExodusFilename, bounds) 