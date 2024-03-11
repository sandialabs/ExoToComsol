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

inputExodusFilename='input_dummy_exo_12_tetra_elem.e'
output_comsol_file_name = "forComsolInput_from_exo_to_comsol_example.txt"

elem_type = "tetrahedra"

#Run exoToComsol() to generate COMSOL file from exodus file
util.exoToComsol(inputFolderPath, inputExodusFilename, outputFolderPath, output_comsol_file_name, elem_type)
