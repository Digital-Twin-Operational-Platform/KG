class BaseNode:
    equivalence = ["produce", "manufacture", "aftermath"]

    def __init__(self, name, label=None):
        # Set up node properties dynamically based on identified_by attribute
        self.nodeProperties = {self.identified_by: name}
        #self.identified_by = name
        if label is not None:
            #self.label = label
            self.nodeProperties = {self.identified_by: name, self.label: label}
            self.nodeProperties["label"] = label
        self.node = None  # Placeholder for a Node instance, if needed

    def create_node(self, tx):
        # Use a transaction to create a node in the database
        if "label" not in self.nodeProperties:
            query = f"CREATE (p:{self.nodeType} {{{self.identified_by}: ${self.identified_by}}}) RETURN p"
        else:
            query = f"CREATE (p:{self.nodeType} {{{self.identified_by}: ${self.identified_by}, label: ${self.label}}}) RETURN p"
        result = tx.run(query, **self.nodeProperties)
        self.node = result.single()[0]
        return self.node


class BaseRelationship:
    def __init__(self, start_node, end_node, relationship_type, properties=None):
        self.start_node = start_node
        self.end_node = end_node
        self.properties = properties if properties else {}
        self.type = relationship_type

    def create_relationship(self, tx):
        if self.start_node.node is None or self.end_node.node is None:
            raise ValueError("Both nodes must be created before creating a relationship.")
        

        # Construct a Cypher query to create a relationship with properties
        if "label" not in self.end_node.nodeProperties:
            prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
            query = (
                f"MATCH (a:{self.start_node.nodeType} {{{self.start_node.identified_by}: $start_name}}) "
                f"OPTIONAL MATCH (b:{self.end_node.nodeType} {{{self.end_node.identified_by}: $end_name}}) "
                f"WITH a, b "
                f"WHERE b IS NOT NULL "
                f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
                f"RETURN r"
            )

            parameters = {
                "start_name": self.start_node.nodeProperties[self.start_node.identified_by],
                "end_name": self.end_node.nodeProperties[self.end_node.identified_by],
                **self.properties
            }
        else:
            prop_string = ', '.join([f'{k}: ${k}' for k in self.properties])
            query = (
                f"MATCH (a:{self.start_node.nodeType} {{{self.start_node.identified_by}: $start_name}}) "
                f"OPTIONAL MATCH (b:{self.end_node.nodeType} {{{self.end_node.identified_by}: $end_name, label: $label}}) "
                f"WITH a, b "
                f"WHERE b IS NOT NULL "
                f"CREATE (a)-[r:{self.type} {{{prop_string}}}]->(b) "
                f"RETURN r"
            )

            parameters = {
                "start_name": self.start_node.nodeProperties[self.start_node.identified_by],
                "end_name": self.end_node.nodeProperties[self.end_node.identified_by],
                "label": self.end_node.nodeProperties["label"],
                **self.properties
            }
        result = tx.run(query, parameters)
        return result.single()[0]
