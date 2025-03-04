import numpy as np
import matplotlib.pyplot as plt
import glob
#from py2neo import Node, Graph
from neo4j import GraphDatabase
#from neo4j.graph import Node
import json
import re
import csv
import os.path, time
from .Baseclass import BaseNode, BaseRelationship


class Product(BaseNode):
    identified_by = 'product_name'
    nodeType = "product"


class Agent(BaseNode):
    identified_by = 'agent_name'
    nodeType = "agent"


class AgentInput(BaseNode):
    identified_by = 'agentinput_name'
    nodeType = "agentinput"


class AgentOutput(BaseNode):
    identified_by = 'agentoutput_name'
    nodeType = "agentoutput"

class Parameter(BaseNode):
    identified_by = 'parameter_name'
    nodeType = "parameter"

class ParameterValue(BaseNode):
    identified_by = 'parameter_value'
    label = 'label'
    nodeType = "parameter_value"


class ParameterUnit(BaseNode):
    identified_by = 'parameter_unit'
    nodeType = "parameter_unit"


class OutputFile(BaseNode):
    identified_by = 'outputfile_name'
    nodeType = "outputfile"


class FilePath(BaseNode):
    identified_by = 'filepath_name'
    nodeType = "filepath"

#######################################################################
# Geometric    
class Component(BaseNode):
    identified_by = 'component_name'
    nodeType = "component"

class Material(BaseNode):
    identified_by = 'material_name'
    nodeType = "material"

# deleted MaterialProperty & PropertyValue & PropertyUnit 

    
#######################################################################
# ODE -  all same as geometric

#######################################################################
# Mesh -  all same as geometric (Meshing, MeshingInput, MeshingOutput)

#######################################################################
# UQ -  all same as geometric, perhaps redefine the Data (.npy)

#######################################################################
# FEM



class Mesh(BaseNode):
    identified_by = 'mesh_name'
    nodeType = "mesh"


class BoundaryCondition(BaseNode):
    identified_by = 'boundarycondition_name'
    nodeType = "boundarycondition"

class Force(BaseNode):
    identified_by = 'force_name'
    nodeType = "force"



