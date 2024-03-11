'''
ExoToComsol

Copyright 2024 National Technology & Engineering Solutions of Sandia, LLC (NTESS). 
Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

BSD 3-Clause License
'''
import re
from exodus3 import *
import numpy as np

from src import Node
from src import Element_Tetrahedra

def exoToComsol(inputFolderPath, inputExodusFilename, outputFolderPath, output_comsol_file_name, elem_type):     

    """
    Outputs COMSOL file in section-wise format from Exodus file

    Returns/writes a text file in section-wise format directly importable in COMSOL for mesh and simulation data
    """

    exo = exodus(inputFolderPath + inputExodusFilename,mode='r',array_type='numpy')
    elem_blk_ids = exo.get_elem_blk_ids()
    time_step_values = exo.get_times()
    num_time_steps = len(time_step_values)

    coord_names = exo.get_coord_names()
    dimension = len(coord_names)

    nodal_coords_tuple = exo.get_coords()
    nodal_variable_names_list = exo.get_node_variable_names()


    nodal_temps_list_at_last_time_step = exo.get_node_variable_values(nodal_variable_names_list[0], num_time_steps)

    nodal_temps_list_at_first_time_step = exo.get_node_variable_values(nodal_variable_names_list[0], 1)


    num_nodes = exo.num_nodes()

    # get the nodal connectivity, number of elements, and number of nodes per element for a single block
    elem_conn, num_blk_elems, num_elem_nodes = exo.get_elem_connectivity(elem_blk_ids[0])



    #import to close exo file otherwise data corruption can occur and difficult to debug
    exo.close()

    # Create node objects with obtained nodal_coords
    # By default we get the nodal value at the last time step
    nodes_list = Node.create_nodes_list_from_coords(nodal_coords_tuple, nodal_temps_list_at_last_time_step)

    #Testing
    #comment out below after testing
    #nodes_list = Node.create_nodes_list_from_coords(nodal_coords_tuple, nodal_temps_list_at_first_time_step)


    elems_list = Element_Tetrahedra.create_elems_list_from_elem_conn_list(elem_conn, num_blk_elems, nodes_list)


    write_sectionwise_file_for_COMSOL_input_full_mesh(outputFolderPath, 
                                                output_comsol_file_name,
                                                dimension, 
                                                num_nodes, 
                                                num_blk_elems, 
                                                nodes_list, 
                                                elem_type,
                                                elems_list)
                                                
def exoToComsol_with_ROI(inputFolderPath, inputExodusFilename, outputFolderPath, output_comsol_file_name, ouptut_file_extension, elem_type, bounds):     
    """
    Outputs COMSOL file of user-defined region-of-interest (ROI) in section-wise format from Exodus file

    Returns/writes a text file in section-wise format directly importable in COMSOL for mesh and simulation data of user-defined region-of-interest (ROI) 
    """    
    exo = exodus(inputFolderPath + inputExodusFilename,mode='r',array_type='numpy')
    elem_blk_ids = exo.get_elem_blk_ids()
    time_step_values = exo.get_times()
    num_time_steps = len(time_step_values)

    coord_names = exo.get_coord_names()
    dimension = len(coord_names)

    nodal_coords_tuple = exo.get_coords()
    nodal_variable_names_list = exo.get_node_variable_names()

    nodal_temps_list_last_time_step = exo.get_node_variable_values(nodal_variable_names_list[0], num_time_steps)

    nodal_temps_list_at_first_time_step = exo.get_node_variable_values(nodal_variable_names_list[0], 1)

    num_nodes = exo.num_nodes()

    # get the nodal connectivity, number of elements, and number of nodes per element for a single block
    elem_conn, num_blk_elems, num_elem_nodes = exo.get_elem_connectivity(elem_blk_ids[0])

    #import to close exo file otherwise data corruption can occur and difficult to debug
    exo.close()

    # Create node objects with obtained nodal_coords
    # By default we get the nodal value at the last time step
    nodes_list = Node.create_nodes_list_from_coords(nodal_coords_tuple, nodal_temps_list_last_time_step)

    #Testing
    #comment out below after testing
    #nodes_list = Node.create_nodes_list_from_coords(nodal_coords_tuple, nodal_temps_list_at_first_time_step)

    nodes_list_roi_cropped, node_ids_roi_cropped = Node.get_nodes_list_roi_cropped(bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1], bounds[2][0], bounds[2][1], nodes_list)

    Node.get_new_node_id_after_roi_cropped(nodes_list_roi_cropped)

    elems_list = Element_Tetrahedra.create_elems_list_from_elem_conn_list(elem_conn, num_blk_elems, nodes_list)
                                                                

    elems_list_roi_cropped = Element_Tetrahedra.get_elems_list_roi_cropped(elems_list, node_ids_roi_cropped) 

    write_sectionwise_file_for_COMSOL_input_full_mesh(outputFolderPath, 
                                                output_comsol_file_name + ouptut_file_extension,
                                                dimension, 
                                                num_nodes, 
                                                num_blk_elems, 
                                                nodes_list, 
                                                elem_type,
                                                elems_list)

    write_sectionwise_file_for_COMSOL_input_roi_cropped_mesh(outputFolderPath, 
                                                output_comsol_file_name+ '_roi_cropped'  + ouptut_file_extension ,
                                                dimension, 
                                                len(nodes_list_roi_cropped), #num_nodes 
                                                len(elems_list_roi_cropped), #num_elems
                                                nodes_list_roi_cropped, 
                                                elem_type,
                                                elems_list_roi_cropped)

def comsolToExo(inputFolderPath, input_comsol_file_name, outputFolderPath, outputExodusFilename): 

    """
    Outputs Exodus file from COMSOL file 

    Returns/writes an Exodus file for SIERRA code
    """

    numDims, numNodes, numElems, x_coords, y_coords, z_coords, num_nodes_per_elem, nodal_sim_data, elem_conn,  numElemBlocks, numAssembly  = read_COMSOL_section_wise_data(inputFolderPath, input_comsol_file_name)

    ex_pars = ex_init_params(num_dim=numDims, num_nodes=numNodes, num_elem=numElems, num_elem_blk=numElemBlocks, num_assembly=numAssembly)

    exo_output = exodus(file= outputFolderPath + outputExodusFilename, mode='w', array_type = 'numpy', init_params = ex_pars)

    exo_output.put_elem_blk_info(elem_blk_id=1, elem_type = 'Tet', num_blk_elems = numElems, num_elem_nodes = num_nodes_per_elem, num_elem_attrs = 0)

    exo_output.put_elem_connectivity(1, elem_conn)

    exo_output.put_node_id_map(Node.get_node_id_array(numNodes))

    exo_output.put_coords(x_coords, y_coords, z_coords)

    exo_output.put_elem_id_map(Element_Tetrahedra.get_element_id_array(numElems))

    #putting simulation data
    exo_output.put_time(step = 1, value = 0)
    exo_output.put_time(step = 2, value = 1)
    exo_output.set_node_variable_number(number = 1)
    exo_output.put_node_variable_name(name = 'temp', index = 1)
    exo_output.put_node_variable_values(name ='temp', step = 2, values = nodal_sim_data)

    exo_output.close()

    print("Exodus file generated from COMSOL data")

def comsolToExo_with_ROI(inputFolderPath, input_comsol_file_name, outputFolderPath, outputExodusFilename, bounds): 

    """
    Outputs Exodus file from COMSOL file for user-defined region-of-interest (ROI) of the FE model

    Returns/writes an Exodus file for SIERRA code
    """
        
    numDims, numNodes, numElems,x_coords, y_coords, z_coords, num_nodes_per_elem, nodal_sim_data, elem_conn, numElemBlocks, numAssembly  = read_COMSOL_section_wise_data(inputFolderPath, input_comsol_file_name)

    nodal_coords_list = []

    nodal_coords_list.append(np.array(x_coords))
    nodal_coords_list.append(np.array(y_coords))
    nodal_coords_list.append(np.array(z_coords))

    nodal_coords_tuple = tuple(nodal_coords_list)

    nodes_list = Node.create_nodes_list_from_coords(nodal_coords_tuple, nodal_sim_data)

    nodes_list_roi_cropped, node_ids_roi_cropped = Node.get_nodes_list_roi_cropped(bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1], bounds[2][0], bounds[2][1], nodes_list)

    Node.get_new_node_id_after_roi_cropped(nodes_list_roi_cropped)

    x_coords_roi_cropped, y_coords_roi_cropped, z_coords_roi_cropped = Node.get_coords_aft_roi_cropping(nodes_list_roi_cropped)

    nodal_sim_data_roi_cropped = Node.get_nodal_sim_data_roi_cropped(nodes_list_roi_cropped)

    elems_list = Element_Tetrahedra.create_elems_list_from_elem_conn_list(elem_conn, numElems, nodes_list)

    elems_list_roi_cropped = Element_Tetrahedra.get_elems_list_roi_cropped(elems_list, node_ids_roi_cropped) 

    elem_conn_aft_roi_cropping = Element_Tetrahedra.get_elem_conn_list_aft_roi_cropping(elems_list_roi_cropped)

    # In the section below we create the exodus file with info obtained from COMSOL file
    num_nodes_aft_roi_cropping = len(nodes_list_roi_cropped)

    num_elems_aft_roi_cropping = len(elems_list_roi_cropped)

    ex_pars = ex_init_params(num_dim=numDims, num_nodes = num_nodes_aft_roi_cropping, num_elem = num_elems_aft_roi_cropping, num_elem_blk = numElemBlocks, num_assembly=numAssembly)

    exo_output = exodus(file= outputFolderPath + outputExodusFilename, mode='w', array_type = 'numpy', init_params = ex_pars)

    exo_output.put_elem_blk_info(elem_blk_id=1, elem_type = 'Tet', num_blk_elems = num_elems_aft_roi_cropping, num_elem_nodes = num_nodes_per_elem, num_elem_attrs = 0)

    exo_output.put_elem_connectivity(1, elem_conn_aft_roi_cropping)

    exo_output.put_node_id_map(Node.get_node_id_array(num_nodes_aft_roi_cropping))

    exo_output.put_coords(x_coords_roi_cropped, y_coords_roi_cropped, z_coords_roi_cropped)

    exo_output.put_elem_id_map(Element_Tetrahedra.get_element_id_array(num_elems_aft_roi_cropping))

    #putting simulation data
    exo_output.put_time(step = 1, value = 0)
    exo_output.put_time(step = 2, value = 1)
    exo_output.set_node_variable_number(number = 1)
    exo_output.put_node_variable_name(name = 'temp', index = 1)
    exo_output.put_node_variable_values(name ='temp', step = 2, values = nodal_sim_data_roi_cropped)

    exo_output.close()
                    
    print("Exodus file generated from COMSOL data")

def write_sectionwise_file_for_COMSOL_input_full_mesh(path, filename, dimension, 
                                            num_nodes, num_blk_elems, 
                                            nodes_list, elem_type,
                                            elems_list): 
    """
    writes COMSOL file in section-wise format for the full FE model

    outputs text file 
    """        

    # Writing to text file
    output_text_file = open(path + filename, "w")
    output_text_file.write(f"% Dimension: {dimension}\n")
    output_text_file.write(f"% Nodes: {num_nodes}\n")
    output_text_file.write(f"% Elements: {num_blk_elems}\n")
    
    # Write nodal coordinates: 
    output_text_file.write("% Coordinates \n")
    for node in nodes_list:
        output_text_file.write(f"{node.x_coord}   {node.y_coord}   {node.z_coord}\n")
    
    # Write element connectivity:
    output_text_file.write(f"% Elements ({elem_type}) \n")
    for elem in elems_list:
        for i in range(0, len(elem.node_ids_list_in_elem )):
            output_text_file.write(f"{elem.node_ids_list_in_elem[i]}\t") 
        output_text_file.write("\n")    
        
    # Write nodal data:    
    output_text_file.write("% Data (T (K)) \n")
    for node in nodes_list:
        output_text_file.write(f"{node.temp} \n")
    
    
    output_text_file.close()
        
def write_sectionwise_file_for_COMSOL_input_roi_cropped_mesh(path, filename, dimension, 
                                            num_nodes, num_blk_elems, 
                                            nodes_list, elem_type,
                                            elems_list): 

    """
    writes COMSOL file in section-wise format for the user-defined region-of-interest (ROI) of the FE model

    outputs text file 
    """                                                

    # Writing to text file
    output_text_file = open(path + filename, "w")
    output_text_file.write(f"% Dimension: {dimension}\n")
    output_text_file.write(f"% Nodes: {num_nodes}\n")
    output_text_file.write(f"% Elements: {num_blk_elems}\n")
    
    # Write nodal coordinates: 
    output_text_file.write("% Coordinates \n")
    for node in nodes_list:
        output_text_file.write(f"{node.x_coord}   {node.y_coord}   {node.z_coord}\n")
    
    # Write element connectivity:
    output_text_file.write(f"% Elements ({elem_type}) \n")
    for elem in elems_list:
        for i in range(0, len(elem.node_ids_list_aft_roi_cropping)):
            output_text_file.write(f"{elem.node_ids_list_aft_roi_cropping[i]}\t") 
        output_text_file.write("\n")    
        
    # Write nodal data:    
    output_text_file.write("% Data (T (K)) \n")
    for node in nodes_list:
        output_text_file.write(f"{node.temp} \n")
    
    
    output_text_file.close()
    
def read_COMSOL_section_wise_data(inputFolderPath, input_comsol_file_name): 
    
    """
    Reads COMSOL file in section-wise format to retrieve FE model information

    Returns FE mesh and simulation data 
    """

    x_coords = []
    y_coords = []
    z_coords = []
    
    elem_conn = []    
    nodal_sim_data = []
            
    # reading from text file
    input_file = open(inputFolderPath + input_comsol_file_name, 'r')
    lines = input_file.readlines()
    
    # hardcoding these values for now: 
    numElemBlocks = 1
    numAssembly = 1
    
    for line_num, line in enumerate(lines): 
        if re.search("Dimension", line):
            numDims_list = re.findall('\d', line)
            
            numDims = int(numDims_list[0])
            
        elif re.search("Nodes", line):
             numNodes_list = re.findall('\d+', line)
             
             numNodes = int(numNodes_list[0])
             
        elif re.search("Elements:", line):
             numElems_list= re.findall('\d+', line)
             
             numElems = int(numElems_list[0])
             
        elif re.search("Coordinates", line): 
             nodal_coords_str = lines[line_num+1:line_num + numNodes + 1]
                     
        elif re.search("Element", line): 
             elem_conn_str = lines[line_num+1:line_num+ numElems + 1]
            
        elif re.search("Data", line): 
             nodal_sim_data_str = lines[line_num+1:line_num+ numNodes + 1]
            
    x_coords, y_coords, z_coords = Node.get_nodal_coords(nodal_coords_str)
    
    num_nodes_per_elem = Element_Tetrahedra.get_num_nodes_per_elem(elem_conn_str)
    
    nodal_sim_data = Node.get_nodal_sim_data(nodal_sim_data_str)
    
    elem_conn = Element_Tetrahedra.get_elem_connectivity(elem_conn_str)
        
    return numDims, numNodes, numElems, x_coords, y_coords, z_coords, num_nodes_per_elem, nodal_sim_data, elem_conn, numElemBlocks, numAssembly  