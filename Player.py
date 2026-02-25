from Entity import Entity
import pygame
from Skill import Fireball, Heal, Mana
from Node import Node
from Audio import Audio
import random

class Player(Entity):
    """This is a class to manage player"""
    # Constant for this class
    FIRST_IMAGE = 0
    MID_IMAGE = 1
    LAST_IMAGE = 2
    def __init__(self, hp: int, steps: int):
        """Initialize player with their core component"""
        super().__init__(hp)
        self.steps = steps
        self.skills : list = []
        self.max_hp = hp
        self.max_steps = steps
        self.player_current_image  = None
        self.player_images = []
        self.audio = Audio()

        # Loading battle image for the player
        for i in range (1,4):
            path = pygame.image.load(f"image/battle/player/player_battle{i}.png")
            self.player_images.append(path)

        self.skills = [Fireball(), Mana(), Heal()] # Player's skill

    def hp_status(self):
        """This method will change the player battle image based on the hp"""
        if self.hp < (0.3 * self.max_hp):
            self.player_current_image = self.player_images[self.LAST_IMAGE]
        elif self.hp < (0.65 * self.max_hp):
            self.player_current_image = self.player_images[self.MID_IMAGE]
        else:
            self.player_current_image = self.player_images[self.FIRST_IMAGE]

    def move (self, destination_node: Node, all_nodes: list):
        """Movement method for the player"""
        self.steps -= (self.current_node.weight + destination_node.weight)
        self.current_node = destination_node
        self.node_effect(destination_node, all_nodes) # If player step special node
        if self.steps < 0:
            self.steps = 0

    def is_alive(self) -> bool:
        """Method to check if player is still alive"""
        if self.hp <= 0 or self.steps <= 0:
            return False
        return True
    
    def node_effect(self, destination_node, all_node: list):
        """Executing each special node effect if the player is in that node"""
        if destination_node.is_blessing: # Blessing node
            heal_amount = int(0.1 * self.max_hp)
            self.audio.blessing_sound.play(0)
            self.hp += heal_amount
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            
            stamina_amount = int(0.1 * self.max_steps)
            self.steps += stamina_amount
            if self.steps > self.max_steps:
                self.steps = self.max_steps
            
            destination_node.is_blessing = False
        
        if destination_node.is_acidic: # Acid node
            damage_amount = int(0.1 * self.max_hp)
            self.audio.acidic_sound.play(0)
            self.hp -= damage_amount
            if self.hp < 0:
                self.hp = 0
            
            stamina_amount = int(0.1 * self.max_steps)
            self.steps -= stamina_amount
            if self.steps < 0:
                self.steps = 0

        if destination_node.is_teleport: # Teleport node
            teleport_done = False
            teleport_node = []
            for node in all_node:
                if node.is_teleport:
                    teleport_node.append(node)
            while not teleport_done:
                for node in teleport_node:
                    random_teleport = random.randint(0, 3)
                    if node.is_teleport and (random_teleport == 1):
                        self.current_node = node
                        teleport_done = True
                        break