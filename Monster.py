from Entity import Entity
from abc import ABC, abstractmethod
import pygame
import random
from Skill import SlimeSkill, DragonSkill, MushroomSkill
from Node import Node

class Monster(Entity, ABC):
    """Abstract class for all monster types"""
    def __init__ (self, hp: int):
        """INitialise monster with their main component"""
        super().__init__(hp)
        self.max_hp = hp
    
    @abstractmethod
    def move(self, destination_node):
        """Abstract method for the movement of each monster"""
        pass

    @abstractmethod
    def battle(self, player : Entity):
        """Abstreact method of how each monster fight"""
        pass

    def decide_action(self, player: Entity, high: int, medium: int, low: int) -> str:
        """Method for the monster's decision making during the battle, will be inherited by child classes"""
        utility_attack = high
        utility_special = medium
        utility_hp = low

        hp_percentage = (self.hp / self.max_hp) * 100

        # Decision making calculation for the monster
        if hp_percentage < self.UTILITY_HIGH and not self.skill.special_skill_used:
            utility_special += self.UTILITY_HIGH

            if utility_attack < utility_hp:
                utility_hp -= self.UTILITY_HIGH
                if utility_hp < 0:
                    utility_hp = 0
            else:
                utility_attack -= self.UTILITY_HIGH
                if utility_attack < 0:
                    utility_attack = 0

        
        if player.hp < self.UTILITY_HIGH:
            utility_attack += self.UTILITY_MED

            if utility_attack < utility_special:
                utility_special -= self.UTILITY_MED
                if utility_special < 0:
                    utility_special = 0
            else:
                utility_attack -= self.UTILITY_MED
                if utility_attack < 0:
                    utility_attack = 0


        if self.hp < 60:
            utility_hp += self.UTILITY_MED

            if utility_attack < utility_special:
                utility_special -= self.UTILITY_MED
                if utility_special < 0:
                    utility_special = 0
            else:
                utility_attack -= self.UTILITY_MED
                if utility_attack < 0:
                    utility_attack = 0

        # Final decision for the monster
        decision = random.randint(1, utility_attack + utility_special + utility_hp)
        if decision <= utility_hp:
            return "heal"
        elif (decision <= utility_hp + utility_special) and not self.skill.special_skill_used :
            return "special_skill"
        else:
            return "attack"


class Slime(Monster):
    """ Slime monster class, which is the child class of monster class."""

    # Constant for this class
    SLIME_SIZE = (70, 70)
    BATTLE_SLIME_SIZE = (120, 120)
    TOTAL_FRAME = 4
    # Utility thresholds
    UTILITY_HIGH = 60
    UTILITY_MED = 30
    UTILITY_LOW = 10
    
    def __init__ (self, hp: int):
        """Initialize slime with the sprites and skill"""
        super().__init__(hp)
        self.frame = []
        self.movement_frame = []
        self.identity = "Slime"
        self.skill = SlimeSkill()
        self.is_immune = False
        self.reflect = False
        self.duration_counter = 0
        
        # Load idle sprites
        for i in range (1,5):
            path = pygame.image.load(f"image/slime/slime{i}.png")
            img = pygame.transform.scale(path, self.SLIME_SIZE)
            self.frame.append(img)

        #Load movement sprites
        for i in range (1,5):
            move_path = pygame.image.load(f"image/slime/teleport/slimetp{i}.png")
            move_img = pygame.transform.scale(move_path, self.SLIME_SIZE)
            self.movement_frame.append(move_img)
        
        # Load battle sprites
        path = pygame.image.load(f"image/battle/slime/slime.png")
        self.battle_image = pygame.transform.scale(path, self.BATTLE_SLIME_SIZE)

        # Load description image
        path = pygame.image.load(f"image/battle/description/slime.png")
        self.description_image = pygame.transform.scale(path, (250, 310))

    def move(self, player_node):
        """Move slime toward player using Dijkstra's shortest path algorithm."""

        # Setting start and target
        start_node = self.current_node
        target_node = player_node

        if start_node == target_node: # end the loop if at the same node
            return
        
        # Dijkstra algorithm implementation
        distances = {start_node: 0}
        parents = {start_node: None}

        unvisited = [start_node]
        visited = []

        while True:
            # Checking unvisited node
            current_node = unvisited[0]
            for node in unvisited:
                if distances[node] < distances[current_node]:
                    current_node = node
            
            unvisited.remove(current_node)
            visited.append(current_node)

            if current_node == target_node: # Calculate distance
                break
            
            # Checking the neighboring node
            for neighbor in current_node.get_neighbor(): 
                if neighbor in visited:
                    continue
                
                new_dist = distances[current_node] + neighbor.weight
                
                if neighbor not in distances or new_dist < distances[neighbor]: # If node efficient append
                    distances[neighbor] = new_dist
                    parents[neighbor] = current_node
                    if neighbor not in unvisited:
                        unvisited.append(neighbor)

        # Building the path from the destination back to start
        path = []
        current = target_node
        while current is not None and current in parents:
            if current == start_node: 
                break
            path.append(current)
            current = parents[current]
        self.current_node = path[-1] #Move the monster

    def battle(self, player : Entity) -> str:
        """Method for the monster's decision making during the battle"""
        return self.decide_action(player, self.UTILITY_HIGH, self.UTILITY_MED, self.UTILITY_LOW)
        
class Dragon(Monster):
    """ Dragon monster class, which is the child class of monster class."""
    # Constant for this class
    DRAGON_SIZE = (90, 90)
    BATTLE_DRAGON_SIZE = (350, 350)
    TOTAL_FRAME = 4
    # Utility thresholds
    UTILITY_HIGH = 80
    UTILITY_MED = 50
    UTILITY_LOW = 10
    
    def __init__(self, hp: int):
        """Initialize dragon with the sprites and skill"""
        super().__init__(hp)
        self.frame = []
        self.movement_frame = []
        self.identity = "Dragon"
        self.skill = DragonSkill()
        self.is_immune = False
        self.reflect = False
        self.duration_counter = 0
        
        # Load idle sprites
        for i in range(1, 5):
            path = pygame.image.load(f"image/dragon/dragon{i}.png")
            img = pygame.transform.scale(path, self.DRAGON_SIZE)
            self.frame.append(img)
        
        #Load movement sprites
        for i in range(0, 4):
            move_path = pygame.image.load(f"image/dragon/teleport/dragon{i}.png")
            move_img = pygame.transform.scale(move_path, self.DRAGON_SIZE)
            self.movement_frame.append(move_img)

        # Load battle sprites
        path = pygame.image.load(f"image/battle/dragon/dragon.png")
        self.battle_image = pygame.transform.scale(path, self.BATTLE_DRAGON_SIZE)

        # Load description image
        path = pygame.image.load(f"image/battle/description/dragon.png")
        self.description_image = pygame.transform.scale(path, (250, 310))
    
    def get_heuristic(self, node: Node, target_node: Node) -> int: # counting estimated cost
        """Method to calculate the heuristic of 2 node"""
        distance_x = abs(node.node_id[0] - target_node.node_id[0])
        distance_y = abs(node.node_id[1] - target_node.node_id[1])
        return distance_x + distance_y

    def move(self, player_node):
        """Move dragon toward player using A* algorithm."""
        starting_node = self.current_node
        target_node = player_node

        if starting_node == target_node:
            return
        # A* algorithm implementation
        score_now = {starting_node: 0} #starting node value
        #estimated cost from start to target
        score_estimated = {starting_node: self.get_heuristic(starting_node, target_node)} 

        mapped = {starting_node: None} #mapped nodes

        unvisited = [starting_node] #unvisited nodes
        visited = [] #visited nodes

        while True:
            # finding the best score node
            best_node = None
            best_score = float('inf')

            for node in unvisited:
                score = score_estimated.get(node, float('inf'))
                if score < best_score:
                    best_score = score
                    best_node = node
            current_node = best_node
            
            if current_node == target_node: # end the loop if at the same node
                break

            unvisited.remove(current_node)
            visited.append(current_node)

            # Chekcing neighbour
            for neighbor in current_node.get_neighbor():
                if neighbor in visited:
                    continue
                
                cost_calculation = score_now[current_node] + neighbor.weight # calculating distance

                if neighbor not in score_now or cost_calculation < score_now[neighbor]: # check if node efficient
                    mapped[neighbor] = current_node
                    score_now[neighbor] = cost_calculation
                    # Estimating cost (calculate the heuristic)
                    score_estimated[neighbor] = cost_calculation + self.get_heuristic(neighbor, target_node)

                    if neighbor not in unvisited:
                        unvisited.append(neighbor)
        # Build path from target back to start
        path = []
        current = target_node
        while (current in mapped) and (current is not None):
            if current == starting_node: 
                break
            path.append(current)
            current = mapped[current]
        
        self.current_node = path[-1]

    def battle(self, player : Entity) -> str:
        """Method for the monster's decision making during the battle"""
        return self.decide_action(player, self.UTILITY_HIGH, self.UTILITY_MED, self.UTILITY_LOW)
        
class Mushroom(Monster):
    """ Mushroom monster class, which is the child class of monster class."""
    # Constant for this class
    MUSHROOM_SIZE = (65, 65)
    BATTLE_MUSHROOM_SIZE = (200, 200)
    TOTAL_FRAME = 4
    # Utility thresholds
    UTILITY_HIGH = 70
    UTILITY_MED = 60
    UTILITY_LOW = 10
    
    def __init__(self, hp: int):
        """Initialize mushroom with the sprites and skill"""
        super().__init__(hp)
        self.frame = []
        self.movement_frame = []
        self.identity = "Mushroom"
        self.skill = MushroomSkill()
        self.is_immune = False
        self.reflect = False
        self.duration_counter = 0
        
        # Load idle Sprite
        for i in range(1, 5):
            path = pygame.image.load(f"image/mushroom/mushroom{i}.png")
            img = pygame.transform.scale(path, self.MUSHROOM_SIZE)
            self.frame.append(img)

        self.movement_frame = self.frame # idle sprite the same as movement sprite
        
        # Load battle sprite
        path = pygame.image.load(f"image/battle/mushroom/mushroom.png")
        self.battle_image = pygame.transform.scale(path, self.BATTLE_MUSHROOM_SIZE)

        # Load description image
        path = pygame.image.load(f"image/battle/description/mushroom.png")
        self.description_image = pygame.transform.scale(path, (250, 310))
    


    def move(self, player_node):
        """This monster cannot move, so there is no movement algortihm"""
        pass

    def battle(self, player : Entity) -> str:
        """Method for the monster's decision making during the battle"""
        return self.decide_action(player, self.UTILITY_HIGH, self.UTILITY_MED, self.UTILITY_LOW)
