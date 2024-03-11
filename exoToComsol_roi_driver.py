'''
ExoToComsol

Copyright 2024 National Technology & Engineering Solutions of Sandia, LLC (NTESS). 
Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

BSD 3-Clause License
'''
from exodus3 import *
import numpy as np

from src import Node
from src import Element_Tetrahedra
from src import util

#user inputs:
inputFolderPath = './input_folder/' 
outputFolderPath = './output_folder/' 

inputExodusFilename=  'result_heat_conduction_Aria.e' 
output_comsol_file_name = 'forComsolInput_exo_to_comsol_example'
ouptut_file_extension = '.txt'

elem_type = "tetrahedra"

x_coord_lower_bound = -0.5
x_coord_upper_bound = 0.5

y_coord_lower_bound = -0.5
y_coord_upper_bound = 0.5
    
z_coord_lower_bound = -0.5
z_coord_upper_bound = 0.0

bounds = [[x_coord_lower_bound, x_coord_upper_bound], 
          [y_coord_lower_bound, y_coord_upper_bound],
          [z_coord_lower_bound, z_coord_upper_bound]]

#Run exoToComsol_with_ROI() to generate COMSOL file from exodus file with user-defined ROI
util.exoToComsol_with_ROI(inputFolderPath, inputExodusFilename, outputFolderPath, output_comsol_file_name, ouptut_file_extension, elem_type, bounds)