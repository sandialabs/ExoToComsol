'''
ExoToComsol

Copyright 2024 National Technology & Engineering Solutions of Sandia, LLC (NTESS). 
Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

BSD 3-Clause License
'''
import numpy as np
import re

def get_nodal_coords(lines_with_nodal_coords):
    """
    Gets nodal coordinates from text

    Returns lists for x, y and z coordinates
    """ 
    
    x_coords = []
    y_coords = []
    z_coords = []
    
    for line in lines_with_nodal_coords: 
                 
        numbers_in_line = re.split(r"\s+",line)
        
        x_coords.append(float(numbers_in_line[0]))
        y_coords.append(float(numbers_in_line[1]))        
        z_coords.append(float(numbers_in_line[2]))
                
    return x_coords, y_coords, z_coords


def get_coords_aft_roi_cropping(nodes_list_roi_cropped): 

    """
    Gets coordinates of nodes inside user-defined region-of-interest

    Returs arrays of x, y and z coordinates
    
    """
    
    x_coords_roi_cropped = []
    y_coords_roi_cropped = [] 
    z_coords_roi_cropped = []
    
    for node in nodes_list_roi_cropped: 
        x_coords_roi_cropped.append(node.x_coord)
        y_coords_roi_cropped.append(node.y_coord)
        z_coords_roi_cropped.append(node.z_coord)
    
    return x_coords_roi_cropped, y_coords_roi_cropped, z_coords_roi_cropped


def get_nodal_sim_data(lines_with_nodal_sim_data): 

    """
    Gets nodal simulation data

    Returns list of nodal simulation data
    """
    
    nodal_sim_data = []

    
    for line in lines_with_nodal_sim_data: 
        
        nodal_temp = float(line)
        
        if nodal_temp == 0.0:
            print("Error")
        
        nodal_sim_data.append(nodal_temp)
         
        # numbers_in_line = re.findall('-?\d+\.\d+', line)
        
        # if(float(numbers_in_line[0]) == 0): 
        #     print("error")
        # else:
        #     nodal_sim_data.append(float(numbers_in_line[0]))

        
    return nodal_sim_data 

def get_nodal_sim_data_roi_cropped(nodes_list_roi_cropped): 

    """
    Gets nodal simulation data over the user-defined region-of-interest

    Returns list of nodal simulation data
    """
    nodal_sim_data_roi_cropped = []
    
    for node in nodes_list_roi_cropped: 
        nodal_sim_data_roi_cropped.append(node.temp)
        
    return nodal_sim_data_roi_cropped 

def get_node_id_array(numNodes): 

    """
    Gets array of node ids from number of nodes and without using node object

    Returns list of node ids
    """
    
    node_id_array = np.arange(1, numNodes+1)
    
    return list(node_id_array)

def create_nodes_list_from_coords(nodal_coords_tuple, nodal_temps_list): 
    
    """
    Creates list of node objects from nodal coordinates and nodal simulation data

    Returns list of node objects
    """
    nodes_list = []
    
    num_nodes = len(nodal_coords_tuple[0])
    
    for i in range(0, num_nodes):
        node = Node(node_id = i+1, #1-based node ids
                    x_coord = nodal_coords_tuple[0][i], 
                    y_coord = nodal_coords_tuple[1][i], 
                    z_coord = nodal_coords_tuple[2][i], \
                    temp = nodal_temps_list[i])
        nodes_list.append(node)
    
    return nodes_list

def get_nodes_list_roi_cropped(x_coord_lower_bound, x_coord_upper_bound , y_coord_lower_bound, y_coord_upper_bound, z_coord_lower_bound , z_coord_upper_bound, nodes_list): 
    
    """
    Gets list of nodes in the user-defined region-of-interest (ROI)

    Returns list of nodes in the ROI
    """
    nodes_list_roi_cropped = []
    node_ids_roi_cropped = []
    
    for node in nodes_list: 
        
        if (node.x_coord >= x_coord_lower_bound and node.x_coord <= x_coord_upper_bound): 
            if (node.y_coord >= y_coord_lower_bound and node.y_coord <= y_coord_upper_bound): 
                if (node.z_coord >= z_coord_lower_bound and node.z_coord <= z_coord_upper_bound): 
            
                    nodes_list_roi_cropped.append(node)
                    
                    node_ids_roi_cropped.append(node.node_id)
                    
                else: 
                    print (f"user specified region of interest (roi) does not contain node with id {node.node_id}")
            
    
    return nodes_list_roi_cropped, node_ids_roi_cropped

def get_new_node_id_after_roi_cropped(nodes_list_roi_cropped):
    
    """
    Gets new node ids after nodes are identifed inside ROI

    Note: new node ids are needed since for COMSOL sectwise format to work node ids must start from 1 and end at the number of nodes

    Returns: none
    """
    #update the node_id_roi_cropped property values for the nodes in nodes_list_roi_cropped    
    #make a list of node_ids of nodes in roi, then order this list (let's call this 'ids_of_nodes_in_roi_ordered')
    #node.node_id_roi_cropped will be equal to the index of the node_id in the array 'ids_of_nodes_in_roi_ordered'
    
    ids_of_nodes_in_roi = []
    
    for node in nodes_list_roi_cropped: 
        ids_of_nodes_in_roi.append(node.node_id)
            
    ids_of_nodes_in_roi.sort()    
    ids_of_nodes_in_roi_ordered = ids_of_nodes_in_roi
    
    for node in nodes_list_roi_cropped: 
        node.node_id_roi_cropped = ids_of_nodes_in_roi_ordered.index(node.node_id) + 1
    
class Node: 

    """
    Definition for Node object
    """

    def __init__(self, node_id = 0, x_coord = 0, y_coord = 0, z_coord = 0, temp = 0):
        
        self.node_id = node_id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord
        
        self.temp = temp
        
        self.node_id_roi_cropped = node_id

        


    

                       
