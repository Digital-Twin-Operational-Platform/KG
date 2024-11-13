# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:09:23 2023

@author: me1xs
"""
import numpy as np
#from py2neo import Graph, Node, NodeMatcher
from neo4j import GraphDatabase

################################################################################
from .entity import Product, Agent,  AgentInput, AgentOutput, Parameter, ParameterValue, ParameterUnit, OutputFile, FilePath, Component, Material, Mesh, BoundaryCondition, Force

from .relationship import Component2Component, Product2Agent, Agent2Agent, Agent2AgentInput, AgentInput2Parameter, AgentInput2File, AgentInput2Component, Agent2AgentOutput, AgentOutput2File, OutputFile2OutputFile, OutputFile2FilePath, AgentInput2Data, AgentOutput2Data, Data2Value, AgentOutput2Parameter, Parameter2Parameter
################################################################################
from .relationship import Component2Parameter, Component2Material, Material2Parameter, Parameter2Value, Parameter2Unit, AgentInput2Mesh, AgentInput2Material, AgentInput2BoundaryCondition, AgentInput2Force, Mesh2Outputfile


import time
import glob
import csv
import os.path
import re


            
class Database:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def deleteAll(self):
        with self.driver.session() as session:
            session.execute_write(self._delete_all)

    def _delete_all(self, tx):
        query = "MATCH (n) DETACH DELETE n"
        tx.run(query)
        

    def refresh(self):
        query = "MATCH (n) RETURN n LIMIT 400"
        #tx.run(query)
        with self.driver.session() as session:
            result = session.run(query)
            nodes = [record['n'] for record in result]  # Extract the nodes
            #session.execute_write(result.single()[0])
        time.sleep(10)


    def add_nodes(self, item):
        with self.driver.session() as session:
            return session.execute_write(item.create_node)

    def add_relationships(self, item):
        with self.driver.session() as session:
            return session.execute_write(item.create_relationship)



def list_files_in_folder(folder_path):
    try:
        # List all files in the specified folder
        files = os.listdir(folder_path)
        # Filter out directories
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        files_without_suffix = [os.path.splitext(f)[0] for f in files if os.path.isfile(os.path.join(folder_path, f))]
        return files, files_without_suffix
    except Exception as e:
        return str(e)



class knowledgeGraph:
    def __init__(self):
        self.db = Database("bolt://neo4j:7687", "neo4j", "12345678")
        #self.db = Database("bolt://127.0.0.1:7687", "neo4j", "12345678")   # for testing
        ###############################
        self.db.deleteAll()
        self.product_3storyFloor = Product("Three_story_Floor")
        self.db.add_nodes(self.product_3storyFloor)

        # Add analytical parameters
        self.analy_model = Agent("ODE_MassSpringDamper") 
        self.db.add_nodes(self.analy_model)

        # product -> analytical
        self.db.add_relationships(Product2Agent(self.product_3storyFloor, self.analy_model))

        # analytical -> input
        self.analyticalinput_ = AgentInput("Parameters")
        self.db.add_nodes(self.analyticalinput_)

        self.db.add_relationships(Agent2AgentInput(self.analy_model, self.analyticalinput_))

        # analytical-> parameters
        analy_m, analy_k, analy_c = ["m1", "m2", "m3"], ["k1", "k2", "k3"], ["c1", "c2", "c3"]
        m, k, c = [5.0394, 4.9919, 4.9693], [34958.3691, 43195.1237, 43295.9086], [7.8963, 4.0129, 5.4905]
        unit_ = ["kg", "N/m", "Ns/m"]
        analy_m_unit = ParameterUnit(unit_[0])
        analy_k_unit = ParameterUnit(unit_[1])
        analy_c_unit = ParameterUnit(unit_[2])
        self.db.add_nodes(analy_m_unit)
        self.db.add_nodes(analy_k_unit)
        self.db.add_nodes(analy_c_unit)
        #
        self.analy_m_, self.analy_k_, self.analy_c_ = {}, {}, {}
        for i in range(0, 3):
            self.analy_m_[str(i)] = Parameter(analy_m[i])
            self.analy_k_[str(i)] = Parameter(analy_k[i])
            self.analy_c_[str(i)] = Parameter(analy_c[i])
            self.db.add_nodes(self.analy_m_[str(i)])
            self.db.add_nodes(self.analy_k_[str(i)])
            self.db.add_nodes(self.analy_c_[str(i)])
            self.db.add_relationships(AgentInput2Parameter(self.analyticalinput_, self.analy_m_[str(i)]))
            self.db.add_relationships(AgentInput2Parameter(self.analyticalinput_, self.analy_k_[str(i)]))
            self.db.add_relationships(AgentInput2Parameter(self.analyticalinput_, self.analy_c_[str(i)]))
            analy_m_value = ParameterValue(str(m[i]), label = analy_m[i])
            analy_k_value = ParameterValue(str(k[i]), label = analy_k[i])
            analy_c_value = ParameterValue(str(c[i]), label = analy_c[i])
            self.db.add_nodes(analy_m_value)
            self.db.add_nodes(analy_k_value)
            self.db.add_nodes(analy_c_value)
            #
            self.db.add_relationships(Parameter2Value(self.analy_m_[str(i)], analy_m_value))
            self.db.add_relationships(Parameter2Value(self.analy_k_[str(i)], analy_k_value))
            self.db.add_relationships(Parameter2Value(self.analy_c_[str(i)], analy_c_value))
            #
            self.db.add_relationships(Parameter2Unit(self.analy_m_[str(i)], analy_m_unit))
            self.db.add_relationships(Parameter2Unit(self.analy_k_[str(i)], analy_k_unit))
            self.db.add_relationships(Parameter2Unit(self.analy_c_[str(i)], analy_c_unit))


        ###############
        # Blender geometric
        self.geometric_ = Agent("Geometric")
        self.db.add_nodes(self.geometric_)

        self.db.add_relationships(Product2Agent(self.product_3storyFloor, self.geometric_))
        geometricInput_ = AgentInput("GeoInput")
        self.db.add_nodes(geometricInput_)
        self.db.add_relationships(Agent2AgentInput(self.geometric_, geometricInput_))

        # floor, pillar, block, V, H
        components_ = ["floor", "pillar", "block", "V", "H"]
        directions_ = ["Len_", "Wid_", "Hei_"]
        dimensions_ = np.array([[0.3005, 0.25, 0.0255],   # L_f, B_f, H_f  floor
                       [0.0065, 0.0255, 0.555],           # L_p, B_p, H_p  pillar
                       [0.0125, 0.0255, 0.0255],          # L_b, B_b, H_b  block
                       [0.0065, 0.0255, 0.05-0.0065],     # L_s_V, B_s_V, H_s_V,  V
                       [0.05, 0.0255, 0.0065]])           # L_s_H, B_s_H, H_s_H    H

        L_f, B_f, H_f = dimensions_[0, 0], dimensions_[0, 1], dimensions_[0, 2]
        L_p, B_p, H_p = dimensions_[1, 0], dimensions_[1, 1], dimensions_[1, 2]
        L_b, B_b, H_b = dimensions_[2, 0], dimensions_[2, 1], dimensions_[2, 2]
        L_s_V, B_s_V, H_s_V = dimensions_[3, 0], dimensions_[3, 1], dimensions_[3, 2]
        L_s_H, B_s_H, H_s_H = dimensions_[4, 0], dimensions_[4, 1], dimensions_[4, 2]
        
        parameter_ = {}
        for i in range(0, 5):
            for j in range(0, 3):
                instance_name = f"{directions_[j]} + {components_[i]}"
                parameter_[instance_name] = Parameter(directions_[j] + components_[i])
                parameter_value_ = ParameterValue(dimensions_[i, j], label = directions_[j] + components_[i])
                self.db.add_nodes(parameter_[instance_name])
                self.db.add_nodes(parameter_value_)
                self.db.add_relationships(Parameter2Value(parameter_[instance_name], parameter_value_))

        #############
        type_dim = ["has_length", "has_width", "has_height"]
        # three floors
        for j in range(0, 3):
            # floor
            component_floor = Component("Floor_"+str(j+1))
            self.db.add_nodes(component_floor)
            self.db.add_relationships(AgentInput2Component(geometricInput_, component_floor))
            loc_ = (0, 0, 0.0255/2.0 + (i+1) * (0.555 - 0.0255) / 3.0)
            parameter_loc = Parameter(f"Loc_Floor_{str(j)}")
            parameter_locValue = ParameterValue(str(loc_), f"Loc_Floor_{str(j)}")
            self.db.add_nodes(parameter_loc)
            self.db.add_nodes(parameter_locValue)
            self.db.add_relationships(Parameter2Value(parameter_loc, parameter_locValue))
            self.db.add_relationships(Component2Parameter(component_floor, parameter_loc, "has_loc"))
            for k in range(0, 3):
                self.db.add_relationships(Component2Parameter(component_floor, parameter_[f"{directions_[k]} + {components_[0]}"], type_dim[k]))


        # four pillars
        for i in range(0, 4):
            component_pillar = Component("Pillar_"+str(i+1))
            self.db.add_nodes(component_pillar)
            self.db.add_relationships(AgentInput2Component(geometricInput_, component_pillar))
            # loc of the four pillars
            if i==0:
                m, n = -1, -1
            elif i==1:
                m, n = -1, 1
            elif i==2:
                m, n = 1, -1
            elif i==3:
                m, n = 1, 1
            loc_ = (m*(L_f + L_p)/2.0, n*(B_f - B_p)/2.0, H_p/2.0)
            parameter_loc = Parameter(f"Loc_Pillar_{str(i)}")
            parameter_locValue = ParameterValue(str(loc_), f"Loc_Pillar_{str(i)}")
            self.db.add_nodes(parameter_loc)
            self.db.add_nodes(parameter_locValue)
            self.db.add_relationships(Parameter2Value(parameter_loc, parameter_locValue))
            self.db.add_relationships(Component2Parameter(component_pillar, parameter_loc, "has_loc"))
            ################
            for k in range(0, 3):
                self.db.add_relationships(Component2Parameter(component_pillar, parameter_[f"{directions_[k]} + {components_[1]}"], type_dim[k]))

            
            
            for j in range(0, 3):
                component_block = Component("Block_" + str(i) + "_" + str(j))
                self.db.add_nodes(component_block)
                self.db.add_relationships(AgentInput2Component(geometricInput_, component_block))
                self.db.add_relationships(Component2Component(component_pillar, component_block, "adjacent"))  # pillar and 3 blocks
                loc_ = (m*(L_f + L_p*2 + L_b)/2.0, n*(B_f - B_p)/2.0, 0.0255/2.0 + (j+1) * (0.555 - 0.0255) / 3.0)   ##
                parameter_loc = Parameter(f"Loc_block_{str(i)}_{str(j)}")
                parameter_locValue = ParameterValue(str(loc_), f"Loc_block_{str(i)}_{str(j)}")
                self.db.add_nodes(parameter_loc)
                self.db.add_nodes(parameter_locValue)
                self.db.add_relationships(Parameter2Value(parameter_loc, parameter_locValue))
                self.db.add_relationships(Component2Parameter(component_block, parameter_loc, "has_loc"))
                for o in range(0, 3):
                    self.db.add_relationships(Component2Parameter(component_block, parameter_[f"{directions_[o]} + {components_[2]}"], type_dim[o]))

            ################
            # the vertical plate
            component_V = Component("V_plate"+str(i+1))
            self.db.add_nodes(component_V)
            self.db.add_relationships(AgentInput2Component(geometricInput_, component_V))
            #
            loc_ = (m*(L_f + L_p*2 + L_s_V)/2.0, n*(B_f - B_p)/2.0, (0.05 - 0.0065)/2.0)
            parameter_loc = Parameter(f"Loc_V_{str(i)}")
            parameter_locValue = ParameterValue(str(loc_), f"Loc_V_{str(i)}")
            self.db.add_nodes(parameter_loc)
            self.db.add_nodes(parameter_locValue)
            self.db.add_relationships(Parameter2Value(parameter_loc, parameter_locValue))
            self.db.add_relationships(Component2Parameter(component_V, parameter_loc, "has_loc"))
            #
            for k in range(0, 3):
                self.db.add_relationships(Component2Parameter(component_V, parameter_[f"{directions_[k]} + {components_[3]}"], type_dim[k]))
            # the horizontal plate
            component_H = Component("H_plate"+str(i+1))
            self.db.add_nodes(component_H)
            self.db.add_relationships(AgentInput2Component(geometricInput_, component_H))
            #
            loc_ = (m*(L_f + L_p*2 + L_s_H)/2.0, n*(B_f - B_p)/2.0,  -0.0065/2.0)
            parameter_loc = Parameter(f"Loc_H_{str(i)}")
            parameter_locValue = ParameterValue(str(loc_), f"Loc_H_{str(i)}")
            self.db.add_nodes(parameter_loc)
            self.db.add_nodes(parameter_locValue)
            self.db.add_relationships(Parameter2Value(parameter_loc, parameter_locValue))
            self.db.add_relationships(Component2Parameter(component_H, parameter_loc, "has_loc"))
            for k in range(0, 3):
                self.db.add_relationships(Component2Parameter(component_H, parameter_[f"{directions_[k]} + {components_[4]}"], type_dim[k]))


        ############
        # STL to MSH
        gmsh_ = Agent("Meshing")
        self.db.add_nodes(gmsh_)

        
        self.db.add_relationships(Product2Agent(self.product_3storyFloor, gmsh_))
        #
        self.gmshinput_ = AgentInput("Gmsh_input")
        self.db.add_nodes(self.gmshinput_)
        self.db.add_relationships(Agent2AgentInput(gmsh_, self.gmshinput_))
        #
        self.gmshoutput_ = AgentOutput("Gmsh_output")
        self.db.add_nodes(self.gmshoutput_)
        self.db.add_relationships(Agent2AgentOutput(gmsh_, self.gmshoutput_))

        
        #
        # angle_surface_ = Parameter("angle_surface_dection")
        # mesh_size = Parameter("mesh_size")
        # geoTolBoolean_ = Parameter("Geometry_tolerance_boolean")
        # curveAngle_ = Parameter("curve_angle")
        parameters_ = ["angle_surface_dection", "mesh_size", "Geometry_tolerance_boolean", "curve_angle"]
        values_ = [40, 0.02, 1e-4, 180]
        for i in range(0, len(parameters_)):
            para_ = Parameter(parameters_[i])
            value_ = ParameterValue(str(values_[i]), parameters_[i])
            self.db.add_nodes(para_)
            self.db.add_nodes(value_)
            self.db.add_relationships(AgentInput2Parameter(self.gmshinput_, para_))
            self.db.add_relationships(Parameter2Value(para_, value_))


        #############
        # Material
        material_aluminum = Material("al6082")
        self.db.add_nodes(material_aluminum)

        
        ####
        aluminum_density = Parameter("density")
        aluminum_youngsmodulus = Parameter("youngsmodulus")
        aluminum_possionsratio = Parameter("possionsratio")
        self.db.add_nodes(aluminum_density)
        self.db.add_nodes(aluminum_youngsmodulus)
        self.db.add_nodes(aluminum_possionsratio)
        ####
        aluminum_density_value = ParameterValue("2700", label = "density")
        aluminum_density_unit = ParameterUnit("kg/m3")
        self.db.add_nodes(aluminum_density_value)
        self.db.add_nodes(aluminum_density_unit)
        ####
        aluminum_E_value = ParameterValue("70e9", label = "youngsmodulus")
        aluminum_E_unit = ParameterUnit("N/m2")
        self.db.add_nodes(aluminum_E_value)
        self.db.add_nodes(aluminum_E_unit)
        ####
        aluminum_mu_value = ParameterValue("0.3", label = "possionsratio")
        aluminum_mu_unit = ParameterUnit("-")
        self.db.add_nodes(aluminum_mu_value)
        self.db.add_nodes(aluminum_mu_unit)
        #########
        self.db.add_relationships(Parameter2Value(aluminum_density, aluminum_density_value))
        self.db.add_relationships(Parameter2Unit(aluminum_density, aluminum_density_unit))
        #
        self.db.add_relationships(Parameter2Value(aluminum_youngsmodulus, aluminum_E_value))
        self.db.add_relationships(Parameter2Unit(aluminum_youngsmodulus, aluminum_E_unit))
        #
        self.db.add_relationships(Parameter2Value(aluminum_possionsratio, aluminum_mu_value))
        self.db.add_relationships(Parameter2Unit(aluminum_possionsratio, aluminum_mu_unit))
        ####
        self.db.add_relationships(Material2Parameter(material_aluminum, aluminum_density))
        self.db.add_relationships(Material2Parameter(material_aluminum, aluminum_youngsmodulus))
        self.db.add_relationships(Material2Parameter(material_aluminum, aluminum_possionsratio))

        #############
        # FEM
        data_path_ = "./digitaltwin/Data/FEM/"
        fem_ = Agent("FEM")
        self.db.add_nodes(fem_)
        self.db.add_relationships(Product2Agent(self.product_3storyFloor, fem_))

        fem_modal = Agent("ModalAnalysis")
        self.db.add_nodes(fem_modal)
        self.db.add_relationships(Agent2Agent(fem_, fem_modal, "has_subagent"))
        #
        fem_steadystate = Agent("SteadyState")
        self.db.add_nodes(fem_steadystate)
        self.db.add_relationships(Agent2Agent(fem_, fem_steadystate, "has_subagent"))
        #
        fem_modal_input_ = AgentInput("Modal_Input")
        self.db.add_nodes(fem_modal_input_)
        self.db.add_relationships(Agent2AgentInput(fem_modal, fem_modal_input_))
        #
        fem_steady_input_ = AgentInput("Steady_Input")
        self.db.add_nodes(fem_steady_input_)
        self.db.add_relationships(Agent2AgentInput(fem_steadystate, fem_steady_input_))

        self.mesh_ = Mesh("Mesh")  # , data_path_)   ! Maybe change this
        self.db.add_nodes(self.mesh_)
        self.db.add_relationships(AgentInput2Mesh(fem_modal_input_, self.mesh_))
        self.db.add_relationships(AgentInput2Mesh(fem_steady_input_, self.mesh_))
        #
        self.db.add_relationships(AgentInput2Material(fem_modal_input_, material_aluminum))
        self.db.add_relationships(AgentInput2Material(fem_steady_input_, material_aluminum))
        #
        # modal analysis parameters
        num_freqs = Parameter("NoEigen")
        self.db.add_nodes(num_freqs)
        self.db.add_relationships(AgentInput2Parameter(fem_modal_input_, num_freqs))
        num_ = ParameterValue("12", label="number_of_eigen_values")
        self.db.add_nodes(num_)
        self.db.add_relationships(Parameter2Value(num_freqs, num_))
        #
        # modal analysis output
        eigen_freqs = AgentOutput("EigenFreqs")
        self.db.add_nodes(eigen_freqs)
        self.db.add_relationships(Agent2AgentOutput(fem_modal, eigen_freqs))
        eigen_vectors = AgentOutput("EigenVecs")
        self.db.add_nodes(eigen_vectors)
        self.db.add_relationships(Agent2AgentOutput(fem_modal, eigen_vectors))
        # Steady-state
        bc_ = BoundaryCondition("BoundaryCondition")  # , data_path_)
        self.db.add_nodes(bc_)
        self.db.add_relationships(AgentInput2BoundaryCondition(fem_steady_input_, bc_))
        force_ = Force("Impluse") #, data_path_)
        self.db.add_nodes(force_)
        self.db.add_relationships(AgentInput2Force(fem_steady_input_, force_))
        #
        fem_disp = AgentOutput("FEM_Disp")
        self.db.add_nodes(fem_disp)
        self.db.add_relationships(Agent2AgentOutput(fem_steadystate, fem_disp))


        #####################################################################
        # Bayesian UQ
        bayesianUQ_ = Agent("Bayesian_UQ")
        self.db.add_nodes(bayesianUQ_)
        self.db.add_relationships(Product2Agent(self.product_3storyFloor, bayesianUQ_))
        #
        self.bayesianinput_ = AgentInput("Bayesian_input")
        self.db.add_nodes(self.bayesianinput_)
        self.db.add_relationships(Agent2AgentInput(bayesianUQ_, self.bayesianinput_))
        #
        self.bayesianoutput_ = AgentOutput("Bayesian_output")
        self.db.add_nodes(self.bayesianoutput_)
        self.db.add_relationships(Agent2AgentOutput(bayesianUQ_, self.bayesianoutput_))

        #
        noise = Parameter("Noise")
        self.db.add_nodes(noise)
        self.db.add_relationships(AgentInput2Parameter(self.bayesianinput_, noise))
        #
        tt_UQ = Parameter("tt_UQ")
        self.db.add_nodes(tt_UQ)
        self.db.add_relationships(AgentInput2Parameter(self.bayesianinput_, tt_UQ))
        #
        xx_UQ = Parameter("xx_UQ")
        self.db.add_nodes(xx_UQ)
        self.db.add_relationships(AgentInput2Parameter(self.bayesianinput_, xx_UQ))
        

        #
        for i in range(0, 3):
            #
            k = Parameter("Prior_k"+str(i))
            self.db.add_nodes(k)
            self.db.add_relationships(AgentInput2Parameter(self.bayesianinput_, k))
            #
            prior = Parameter("UniformPrior_k"+str(i))
            self.db.add_nodes(prior)
            self.db.add_relationships(Parameter2Parameter(k, prior, "has_prior"))
            #parameter_locValue = ParameterValue(str(loc_), f"Loc_Pillar_{str(i)}") # lower to value

            #
            
            #self.db.add_relationships(AgentInput2Parameter(self.bayesianinput_, prior))
            #
            lower = Parameter("Lower_k"+str(i))
            self.db.add_nodes(lower)
            self.db.add_relationships(Parameter2Parameter(prior, lower, "has_lower_bounds"))
            lower_Prior_Value = ParameterValue(str(30000), f"Low_Prior_k{str(i)}") # lower to value
            self.db.add_nodes(lower_Prior_Value)
            self.db.add_relationships(Parameter2Value(lower, lower_Prior_Value))
            #
            upper = Parameter("Upper_k"+str(i))
            self.db.add_nodes(upper)
            self.db.add_relationships(Parameter2Parameter(prior, upper, "has_upper_bounds"))
            upper_Prior_Value = ParameterValue(str(50000), f"Upper_Prior_k{str(i)}") # upper to value
            self.db.add_nodes(upper_Prior_Value)
            self.db.add_relationships(Parameter2Value(upper, upper_Prior_Value))

            # Output
            # Connect to the k1, k2, k3 from the ODE model as the ground truth values
            self.db.add_relationships(AgentOutput2Parameter(self.bayesianoutput_, self.analy_k_[str(i)]))
            # Postprior
            postprior = Parameter("Postprior_k"+str(i))
            self.db.add_nodes(postprior)
            self.db.add_relationships(AgentOutput2Parameter(self.bayesianoutput_, postprior))
            #
            distribution = Parameter("Distribution_k"+str(i))
            self.db.add_nodes(distribution)
            self.db.add_relationships(Parameter2Parameter(postprior, distribution, "has_distribution"))
            #
            postprior_Value = ParameterValue(str(np.linspace(30000, 50000, 100)), f"postprior_k{str(i)}") # lower to value
            self.db.add_nodes(postprior_Value)
            self.db.add_relationships(Parameter2Value(distribution, postprior_Value))

        
            

        


    
    def ODE(self):
        #db = Database("bolt://localhost:7687", "neo4j", "12345678")
        # analytical output
        analyoutput_ = AgentOutput("Results")
        self.db.add_nodes(analyoutput_)
        self.db.add_relationships(Agent2AgentOutput(self.analy_model, analyoutput_))
        ######
        #folder_path = "../Data/ODE/"
        folder_path = "./digitaltwin/Data/ODE/"
        files, files_without_suffix  = list_files_in_folder(folder_path)
        for file_, file_without_suffix_ in zip(files, files_without_suffix):  
            analyoutputdata_ = Parameter(file_without_suffix_)
            self.db.add_nodes(analyoutputdata_)
            self.db.add_relationships(AgentOutput2Parameter(analyoutput_, analyoutputdata_))
            data_value_ = np.load(folder_path + file_)
            #print(data_value_)
            value_ = ParameterValue(str(data_value_), label = str(analyoutputdata_))
            self.db.add_nodes(value_)
            self.db.add_relationships(Parameter2Value(analyoutputdata_, value_))

        # refresh
        #self.db.refresh()

    def Geometric(self):
         geometricoutput_ = AgentOutput("Output")
         self.db.add_nodes(geometricoutput_)
         self.db.add_relationships(Agent2AgentOutput(self.geometric_, geometricoutput_))
         #####
         self.stlFile_ = OutputFile("STL")
         self.db.add_nodes(self.stlFile_)
         self.db.add_relationships(AgentOutput2File(geometricoutput_, self.stlFile_))
         #stlFilePath_ = FilePath("Three_story_floor.stl")
         #self.db.add_filepath(FilePath(stlFilePath_))
         #self.db.add_outputfile2filepath(OutputFile2FilePath(self.stlFile_, stlFilePath_))
         # refresh
         self.db.refresh()

    def Gmsh_(self):
        self.gmshoutputFile_ = OutputFile("MSH")
        self.db.add_nodes(self.gmshoutputFile_)
        self.db.add_relationships(OutputFile2OutputFile(self.stlFile_, self.gmshoutputFile_, "Transform_Msh"))
        self.db.add_relationships(AgentInput2File(self.gmshinput_, self.stlFile_))
        self.db.add_relationships(AgentOutput2File(self.gmshoutput_, self.gmshoutputFile_))
        #mshFilePath_ = FilePath('./digitaltwin/Data/Gmsh/Floor_msh/Three_story_floor.msh')
        #self.db.add_filepath(FilePath(mshFilePath_))
        #self.db.add_outputfile2filepath(OutputFile2FilePath(self.gmshoutput_, mshFilePath_))

    def Gmsh2XDMF(self):
        self.xdmfoutput_ = OutputFile("XDMF")
        self.db.add_nodes(self.xdmfoutput_)
        self.db.add_relationships(OutputFile2OutputFile(self.gmshoutputFile_, self.xdmfoutput_, "Tranform_XDMF"))
        xdmf_ = ["Three_Floor_structure.h5", "Three_Floor_structure.xdmf", "Three_Floor_structure_facets.h5", "Three_Floor_structure_facets.xdmf"]
        for i in range(0, 4):
           xdmfFile_ = OutputFile(xdmf_[i])
           self.db.add_nodes(xdmfFile_)
           self.db.add_relationships(OutputFile2OutputFile(self.xdmfoutput_, xdmfFile_, "has_XDMF_file"))
        

    def FEM_(self):
        self.db.add_relationships(AgentOutput2File(self.mesh_, self.xdmfoutput_))

                                
            
kg_ = knowledgeGraph()
kg_.ODE()
kg_.Geometric()
kg_.Gmsh_()
kg_.Gmsh2XDMF()
kg_.FEM_()






                       
