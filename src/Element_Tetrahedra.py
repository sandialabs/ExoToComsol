'''
ExoToComsol

Copyright 2024 National Technology & Engineering Solutions of Sandia, LLC (NTESS). 
Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

BSD 3-Clause License
'''
import re
import numpy as np
import src.Node

def get_elem_connectivity(lines_with_element_connectivity): 
    """
    Gets element connectivity information from text

    Returns list of node ids representing element connectivities.
    """    
    elem_conn = []
    
    for line in lines_with_element_connectivity: 
        
        numbers_in_line_str = re.findall('\d+', line)
        for num_str in numbers_in_line_str: 
            elem_conn.append(int(num_str))
    
    return elem_conn


# Creating element ids with the following function for now. Later make node objects for this: 
def get_element_id_array(numElems): 

    """
    Creates element id array without requiring node object

    Returns element id array
    """
    
    elem_id_array = np.arange(1, numElems+1)
    
    return list(elem_id_array)


def get_num_nodes_per_elem(lines_with_element_connectivity): 

    """
    Gets number of nodes per element from input text

    Returns number of nodes per element
    """
    
    for i in range(0,1): 
        numbers_in_line_str = re.findall('\d+', lines_with_element_connectivity[0])

    return len(numbers_in_line_str)

def create_elems_list_from_elem_conn_list(elem_conn_entire_list, num_blk_elems, nodes_list): 

    """
    Creates a list of element object from a list containing node ids in order to show element connectivity. 

    Returns a list of element objects
    """
    
    elems_list = []
    
    for i in range(0, num_blk_elems):
        

        first_index = i*4
        last_index = i*4+3
        
        elem_conn_list_of_one_elem =  elem_conn_entire_list[first_index:last_index+1]
        
        elem = create_elem( elem_conn_list_of_one_elem,  nodes_list)
        
        elems_list.append(elem)

    return elems_list


def create_elem(elem_conn, nodes_list): 

    """
    Creates an element object from a list of node ids for an element, and a list of node objects

    Note: This function assumes that the nodes are ordered in ascending order of node ids in the input list of node objects

    Returns an element object 
    """
    
    nodes_in_elem_in_order = []
    
    for nodal_id in elem_conn: 
        
        #identify the node in the nodes_list mataching this node_id
        #node_filtered_list = list(filter(lambda node: node.node_id == nodal_id, nodes_list))
        
        #nodes_in_elem_in_order.append(node_filtered_list[0])
        
        #node_ids are 1 based
        nodes_in_elem_in_order.append(nodes_list[nodal_id-1])
        
    return Element_Tetrahedra(nodes_in_elem_in_order)

def create_elem_from_unordered_nodes_list(elem_conn, nodes_list): 

    """
    Creates an element object from a list of node ids for an element, and a list of node objects

    Note: This function assumes that the nodes are not ordered in ascending order of node ids in the input list of node objects. 
    This function as currently implemented using filter() is slow for large list of nodes. To remedy this we can first create a list of nodes ordered by node ids. 

    Returns an element object 
    """
    
    nodes_in_elem_in_order = []
    
    for nodal_id in elem_conn: 
        
        #identify the node in the nodes_list mataching this node_id
        node_filtered_list = list(filter(lambda node: node.node_id == nodal_id, nodes_list))
        
        nodes_in_elem_in_order.append(node_filtered_list[0])
        
    return Element_Tetrahedra(nodes_in_elem_in_order)



def get_elems_list_roi_cropped(elems_list, node_ids_roi_cropped): 

    """
    Creates a list of elements falling inside the user-defined region-of-interest of the model. 

    Returns: List of element objects
    """
    
    elems_list_roi_cropped = []
    node_ids_in_roi_cropped_set = set(node_ids_roi_cropped)
    
    for elem in elems_list:         
        node_ids_of_elem_set = set(elem.node_ids_list_in_elem)
        
        if node_ids_of_elem_set.issubset(node_ids_in_roi_cropped_set): 
            elems_list_roi_cropped.append(elem)
                        
        else:
            pass
            #print(f'Element with node ids: {elem.node_ids_list_in_elem} fall outside of roi')
        
    return elems_list_roi_cropped


def get_elem_conn_list_aft_roi_cropping(elems_list_roi_cropped): 

    """
    Gets the element connectivity list which is a list of node ids after a cropping on the full model based on user-defined region-of-interest has been performed. 

    Note: Separte node ids before and after cropping are required to be generated since node ids must always start from 1 for COMSOL sectionwise file format. 
    """

    elem_conn_list_aft_roi_cropping =[]

    for elem in elems_list_roi_cropped: 
        elem_conn_list_aft_roi_cropping += elem.node_ids_list_aft_roi_cropping
        
        
    return elem_conn_list_aft_roi_cropping
                

class Element_Tetrahedra:
    """
    Definition for Tetrahedra element object

    In future we can have base class 'Element' from which Element_Tetrahedra can inherit
    """
                       
    def __init__(self, nodes_in_elem_in_order): 
        
        self.nodes_in_element_in_order = nodes_in_elem_in_order
        
        node_ids_list_in_elem = []
        node_ids_list_aft_roi_cropping = []
        
        for node in nodes_in_elem_in_order: 
            
            node_ids_list_in_elem.append(node.node_id)
            node_ids_list_aft_roi_cropping.append(node.node_id_roi_cropped)
            
            
        self.node_ids_list_in_elem = node_ids_list_in_elem 
        self.node_ids_list_aft_roi_cropping = node_ids_list_aft_roi_cropping
            
