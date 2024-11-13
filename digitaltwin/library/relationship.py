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
from .Baseclass import BaseRelationship

class Component2Component(BaseRelationship):
    def __init__(self, component1, component2, properties=None):
        super().__init__(component1, component2, "Component2Component", properties)


class Product2Agent(BaseRelationship):
    def __init__(self, product, agent, properties=None):
        super().__init__(product, agent, "has_agent", properties)

class Agent2Agent(BaseRelationship):
    def __init__(self, agent1, agent2, relationship, properties=None):
        super().__init__(agent1, agent2, relationship, properties)


class Agent2AgentInput(BaseRelationship):
    def __init__(self, agent, agentinput, properties=None):
        super().__init__(agent, agentinput, "has_input", properties)


class AgentInput2Parameter(BaseRelationship):
    def __init__(self, agentinput, parameter, properties=None):
        super().__init__(agentinput, parameter, "has_parameter", properties)


class AgentInput2Component(BaseRelationship):
    def __init__(self, agentinput, component, properties=None):
        super().__init__(agentinput, component, "has_component", properties)


class Agent2AgentOutput(BaseRelationship):
    def __init__(self, agent, agentoutput, properties=None):
        super().__init__(agent, agentoutput, "has_output", properties)

class AgentInput2File(BaseRelationship):
    def __init__(self, agentinput, outputfile, properties=None):
        super().__init__(agentinput, outputfile, "has_file", properties)

class AgentOutput2File(BaseRelationship):
    def __init__(self, agentoutput, outputfile, properties=None):
        super().__init__(agentoutput, outputfile, "has_file", properties)

class AgentOutput2Parameter(BaseRelationship):
    def __init__(self, agentoutput, parameter, properties=None):
        super().__init__(agentoutput, parameter, "has_parameter", properties)

class OutputFile2OutputFile(BaseRelationship):
    def __init__(self, outputfile1, outputfile2, relationship, properties=None):
        super().__init__(outputfile1, outputfile2, relationship, properties)


class Parameter2Parameter(BaseRelationship):
    def __init__(self, parameter1, parameter2, relationship, properties=None):
        super().__init__(parameter1, parameter2, relationship, properties)


class OutputFile2FilePath(BaseRelationship):
    def __init__(self, outputfile, filepath, properties=None):
        super().__init__(outputfile, filepath, "located_at", properties)


class AgentInput2Data(BaseRelationship):
    def __init__(self, agentinput, data, properties=None):
        super().__init__(agentinput, data, "has_data", properties)


class AgentOutput2Data(BaseRelationship):
    def __init__(self, agentoutput, data, properties=None):
        super().__init__(agentoutput, data, "has_data", properties)


class Data2Value(BaseRelationship):
    def __init__(self, data, data_value, properties=None):
        super().__init__(data, data_value, "has_value", properties)
###############################################################################
# Geometric
class Component2Component(BaseRelationship):
    def __init__(self, component1, component2, type_, properties=None):
        super().__init__(component1, component2, type_, properties)


class Component2Parameter(BaseRelationship):
    def __init__(self, component, parameter, type_, properties=None):
        super().__init__(component, parameter, type_, properties)

class Component2Material(BaseRelationship):
    def __init__(self, component, material, properties=None):
        super().__init__(component, material, "has_material",  properties)

class Material2Parameter(BaseRelationship):
    def __init__(self, material, parameter, properties=None):
        super().__init__(material, parameter, "has_parameter",  properties)


class Parameter2Value(BaseRelationship):
    def __init__(self, parameter, parameter_value,  properties=None):
        super().__init__ (parameter,parameter_value, "has_value", properties)


class Parameter2Unit(BaseRelationship):
    def __init__(self, parameter, parameter_unit,  properties=None):
        super().__init__ (parameter, parameter_unit, "has_unit", properties)

###############################################################################
# ODE - same as geometric


###############################################################################
# Gmsh - no extra to be added

###############################################################################
# UQ - no extra to be added

###############################################################################
# FEM
class AgentInput2Mesh(BaseRelationship):
    def __init__(self, agentinput, mesh, properties=None):
        super().__init__(agentinput, mesh, "has_mesh", properties)

class AgentInput2Material(BaseRelationship):
    def __init__(self, agentinput, material, properties=None):
        super().__init__(agentinput, material, "has_material", properties)


class AgentInput2BoundaryCondition(BaseRelationship):
    def __init__(self, agentinput, boundarycondition, properties=None):
        super().__init__(agentinput, boundarycondition, "has_boundarycondition", properties)

class AgentInput2Force(BaseRelationship):
    def __init__(self, agentinput, force, properties=None):
        super().__init__(agentinput, force, "has_force", properties)

class Mesh2Outputfile(BaseRelationship):
    def __init__(self, mesh, outputfile, properties=None):
        super().__init__(mesh, outputfile, "has_XDMF", properties)
