# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:41:30 2023

@author: me1xs
"""

class Product2FEM():
    def __init__(self, product, fem, properties=None):
        self.product = product
        self.fem = fem
        self.properties = properties if properties else {}
        self.type = "has_fem"
        
    def create_relationship(self, tx):
        if self.product.node is None or self.fem.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.product.nodeType} {{{self.product.identified_by}: $product_name}}), "
            f"(b:{self.fem.nodeType} {{{self.fem.identified_by}: $fem_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "product_name": self.product.nodeProperties[self.product.identified_by],
            "fem_name": self.fem.nodeProperties[self.fem.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEM2Analysis():
    def __init__(self, fem, femanalysis, properties=None):
        self.fem = fem
        self.femanalysis = femanalysis
        self.properties = properties if properties else {}
        self.type = "has_analysis"
        
    def create_relationship(self, tx):
        if self.fem.node is None or self.femanalysis.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.fem.nodeType} {{{self.fem.identified_by}: $fem_name}}), "
            f"(b:{self.femanalysis.nodeType} {{{self.femanalysis.identified_by}: $femanalysis_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "fem_name": self.fem.nodeProperties[self.fem.identified_by],
            "femanalysis_name": self.femanalysis.nodeProperties[self.femanalysis.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEMAnalysis2Input():
    def __init__(self, femanalysis, feminput, properties=None):
        self.femanalysis = femanalysis
        self.feminput = feminput
        self.properties = properties if properties else {}
        self.type = "has_input"
        
    def create_relationship(self, tx):
        if self.femanalysis.node is None or self.feminput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.femanalysis.nodeType} {{{self.femanalysis.identified_by}: $femanalysis_name}}), "
            f"(b:{self.feminput.nodeType} {{{self.feminput.identified_by}: $feminput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "femanalysis_name": self.femanalysis.nodeProperties[self.femanalysis.identified_by],
            "feminput_name": self.feminput.nodeProperties[self.feminput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEMInput2Mesh():
    def __init__(self, feminput, mesh, properties=None):
        self.feminput = feminput
        self.mesh = mesh
        self.properties = properties if properties else {}
        self.type = "has_mesh"
        
    def create_relationship(self, tx):
        if self.feminput.node is None or self.mesh.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.feminput.nodeType} {{{self.feminput.identified_by}: $feminput_name}}), "
            f"(b:{self.mesh.nodeType} {{{self.mesh.identified_by}: $mesh_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "feminput_name": self.feminput.nodeProperties[self.feminput.identified_by],
            "mesh_name": self.mesh.nodeProperties[self.mesh.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEMInput2Material():
    def __init__(self, feminput, material, properties=None):
        self.feminput = feminput
        self.material = material
        self.properties = properties if properties else {}
        self.type = "has_material"
        
    def create_relationship(self, tx):
        if self.feminput.node is None or self.material.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.feminput.nodeType} {{{self.feminput.identified_by}: $feminput_name}}), "
            f"(b:{self.material.nodeType} {{{self.material.identified_by}: $material_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "feminput_name": self.feminput.nodeProperties[self.feminput.identified_by],
            "material_name": self.material.nodeProperties[self.material.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEMInput2Material():
    def __init__(self, feminput, material, properties=None):
        self.feminput = feminput
        self.material = material
        self.properties = properties if properties else {}
        self.type = "has_material"
        
    def create_relationship(self, tx):
        if self.feminput.node is None or self.material.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.feminput.nodeType} {{{self.feminput.identified_by}: $feminput_name}}), "
            f"(b:{self.material.nodeType} {{{self.material.identified_by}: $material_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "feminput_name": self.feminput.nodeProperties[self.feminput.identified_by],
            "material_name": self.material.nodeProperties[self.material.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEMInput2Parameter():
    def __init__(self, feminput, femmodelparameter, properties=None):
        self.feminput = feminput
        self.femmodelparameter = femmodelparameter
        self.properties = properties if properties else {}
        self.type = "has_parameter"
        
    def create_relationship(self, tx):
        if self.feminput.node is None or self.femmodelparameter.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.feminput.nodeType} {{{self.feminput.identified_by}: $feminput_name}}), "
            f"(b:{self.femmodelparameter.nodeType} {{{self.femmodelparameter.identified_by}: $femmodelparameter_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "feminput_name": self.feminput.nodeProperties[self.feminput.identified_by],
            "femmodelparameter_name": self.femmodelparameter.nodeProperties[self.femmodelparameter.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEMModelParameter2Value():
    def __init__(self, femmodelparameter, parametervalue,  properties=None):
        self.femmodelparameter = femmodelparameter
        self.parametervalue = parametervalue
        self.properties = properties if properties else {}
        self.type = "has_value"
        
    def create_relationship(self, tx):
        if self.femmodelparameter.node is None or self.parametervalue.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.femmodelparameter.nodeType} {{{self.femmodelparameter.identified_by}: $femmodelparameter_name}}), "
            f"(b:{self.parametervalue.nodeType} {{{self.parametervalue.identified_by}: $parametervalue_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "femmodelparameter_name": self.femmodelparameter.nodeProperties[self.femmodelparameter.identified_by],
            "parametervalue_name": self.parametervalue.nodeProperties[self.parametervalue.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEMAnalysis2Output():
    def __init__(self, femanalysis, femoutput, properties=None):
        self.femanalysis = femanalysis
        self.femoutput = femoutput
        self.properties = properties if properties else {}
        self.type = "has_output"
        
    def create_relationship(self, tx):
        if self.femanalysis.node is None or self.femoutput.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.femanalysis.nodeType} {{{self.femanalysis.identified_by}: $femanalysis_name}}), "
            f"(b:{self.femoutput.nodeType} {{{self.femoutput.identified_by}: $femoutput_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "femanalysis_name": self.femanalysis.nodeProperties[self.femanalysis.identified_by],
            "femoutput_name": self.femoutput.nodeProperties[self.femoutput.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]

class FEMInput2BounaryCondition():
    def __init__(self, feminput, boundarycondition, properties=None):
        self.feminput = feminput
        self.boundarycondition = boundarycondition
        self.properties = properties if properties else {}
        self.type = "has_boundarycondition"
        
    def create_relationship(self, tx):
        if self.feminput.node is None or self.boundarycondition.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.feminput.nodeType} {{{self.feminput.identified_by}: $feminput_name}}), "
            f"(b:{self.boundarycondition.nodeType} {{{self.boundarycondition.identified_by}: $boundarycondition_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "feminput_name": self.feminput.nodeProperties[self.feminput.identified_by],
            "boundarycondition_name": self.boundarycondition.nodeProperties[self.boundarycondition.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class FEMInput2Force():
    def __init__(self, feminput, force, properties=None):
        self.feminput = feminput
        self.force = force
        self.properties = properties if properties else {}
        self.type = "has_force"
        
    def create_relationship(self, tx):
        if self.feminput.node is None or self.force.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.feminput.nodeType} {{{self.feminput.identified_by}: $feminput_name}}), "
            f"(b:{self.force.nodeType} {{{self.force.identified_by}: $force_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "feminput_name": self.feminput.nodeProperties[self.feminput.identified_by],
            "force_name": self.force.nodeProperties[self.force.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]


class Mesh2Outputfile():
    def __init__(self, mesh, outputfile, properties=None):
        self.mesh = mesh
        self.outputfile = outputfile
        self.properties = properties if properties else {}
        self.type = "has_XDMF"
        
    def create_relationship(self, tx):
        if self.mesh.node is None or self.outputfile.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        # Construct a Cypher query to create a relationship with properties
        prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
        query = (
            f"MATCH (a:{self.mesh.nodeType} {{{self.mesh.identified_by}: $mesh_name}}), "
            f"(b:{self.outputfile.nodeType} {{{self.outputfile.identified_by}: $outputfile_name}}) "
            f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
            f"RETURN r"
        )
        parameters = {
            "mesh_name": self.mesh.nodeProperties[self.mesh.identified_by],
            "outputfile_name": self.outputfile.nodeProperties[self.outputfile.identified_by],
            **self.properties
        }
        result = tx.run(query, parameters)
        return result.single()[0]
