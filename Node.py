class Node:
    """This class will handle the node and its attribute"""
    connected_nodes:list = []  
    def __init__(self, node_id: list = [0,0], weight: int = 0):
        """Initializing the node"""
        self.node_id = node_id
        self.weight = weight
        self.neighbor_node: list = []  # node
        self.is_blessing = False 
        self.is_acidic = False
        self.is_mystery = False
        self.is_teleport = False

    def connect_node(self, connection_node):
        """Method to connect one node to the other node, and append it to neighboring node"""
        self.neighbor_node.append(connection_node)

    def get_neighbor(self):
        """Method to return neighboring node"""
        return self.neighbor_node
    
    def check_connection(self):
        """Method to check the connected node"""
        return self.connected_nodes
    
    def set_connected(self, node : list):
        """Method to set a node status to connected by adding it to "connected_node"""
        if node not in self.connected_nodes:
            self.connected_nodes.append(node)
    
