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

#user inputs:

inputFolderPath = './input_folder/'
outputFolderPath = './output_folder/'

input_comsol_file_name = "busbar_box_T_data_sectionwise.txt"
outputExodusFilename ='output_exo_busbar_box.e'

#Generate exodus file from comsol data
util.comsolToExo(inputFolderPath, input_comsol_file_name, outputFolderPath, outputExodusFilename)