from Node import Node
from MazeVisualize import MazeVisualize
import random 
from Player import Player
from Monster import Monster
import pygame

class Maze:
    """This class manage all generation of the nodes and connect each node together"""

    def __init__ (self, maze_grid : list):
        """Initialize the maze"""
        self.grid = maze_grid
        self.nodes = []
        self.start_node = None
        self.exit_nodes : Node = []
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) 
        self.x_axis = [x for x in range(self.cols)]
        self.y_axis = [y for y in range(self.rows)]

    def compute_nodes(self):
        """Calculate and initialize all node based on the 2D array grid"""
        for rows in range(self.rows):
            for cols in range(self.cols):
                new_node = Node(node_id=[rows, cols], weight=self.grid[rows][cols])

                if self.grid[rows][cols] == 0:
                    del new_node
                    continue

                if self.grid[rows][cols] == 1: # value 1 = start node
                    self.start_node = new_node

                elif self.grid[rows][cols] == 11: # value 11 = exit node
                    self.exit_nodes.append(new_node)
                                          
                else:
                    self.nodes.append(new_node)
        
    def set_connections(self):
        """Setting connections between adjecent nodes"""
        # Connection for starting node
        self.start_node.connect_node(self.nodes[0])
        self.nodes[0].connect_node(self.start_node)
        for starting_connection in self.nodes: 
            if starting_connection.node_id[1] == self.start_node.node_id[1] and starting_connection.node_id[0] != self.start_node.node_id[0]:
                self.start_node.connect_node(starting_connection)
                starting_connection.connect_node(self.start_node)
                break

        # Connection between building node
        for node in self.nodes:
            for connection_node in self.nodes:

                if (connection_node.node_id != node.node_id) and (
                    connection_node.node_id [0] >= node.node_id [0]-1 and connection_node.node_id [0] <= node.node_id [0]+1) and (
                    connection_node.node_id [1] >= node.node_id [1]-1 and connection_node.node_id [1] <= node.node_id [1]+1 ):
                    
                    if connection_node in node.get_neighbor():
                        continue
                    node.connect_node(connection_node)
                    connection_node.connect_node(node)
                
        # Connection for the exit node
        for exit_node in self.exit_nodes:
            for node in self.nodes:

                if (exit_node.node_id != node.node_id) and (
                    exit_node.node_id [0] >= node.node_id [0]-1 and exit_node.node_id [0] <= node.node_id [0]+1) and (
                    exit_node.node_id [1] >= node.node_id [1]-1 and exit_node.node_id [1] <= node.node_id [1]+1 ):

                    exit_node.connect_node(node)
                    node.connect_node(exit_node)
        
    def summon_monsters(self, monsters: list):
        """Summon all of the monster randomly to the maze"""
        total_nodes = len(self.nodes)
        last_node_index = 0
        for monster in monsters:
            while True:
                random_node = random.randint(0, total_nodes - 1)
                if last_node_index == random_node:
                    continue
                monster.current_node = self.nodes[random_node]
                last_node_index = random_node
                break

    def special_node_generator(self, stage: int = 0):
        """Generating the special node based on the stage"""
        for node in self.nodes:
            bless_generator = random.randint(0, 24)
            if bless_generator < 2:
                node.is_blessing = True
        for node in self.nodes:
            acidic_generator = random.randint(0, 20)   
            if acidic_generator < 2:
                if node.is_blessing == True:
                    continue
                node.is_acidic = True

        if stage >= 2:
            teleport_counter = 2
            while teleport_counter > 0:
                for node in self.nodes:
                    teleport_generator = random.randint(0, 30)
                    if teleport_generator < 2:
                        if node.is_blessing == True or node.is_acidic == True:
                            continue
                        teleport_counter -= 1
                        node.is_teleport = True

    def generate_maze(self, player : Player = None, monsters : list = None, 
                      screen : pygame.Surface = None, stage: int = None) -> bool:
        """Generating the maze, and visualize the game"""
        visual = MazeVisualize(self.rows, self.cols)
        self.compute_nodes()
        self.set_connections() 
        self.summon_monsters(monsters)
        self.special_node_generator(stage)
        # Determine whether player complete or fail the maze
        return visual.visualize(self.exit_nodes, self.nodes, self.start_node, 
                                self.rows, self.cols, player, monsters, screen)
        

