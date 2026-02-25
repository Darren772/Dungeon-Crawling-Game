import Node
from Node import Node
from abc import ABC, abstractmethod

class Entity(ABC):
    """"Abstract class, which is the base of all entities in the game"""
    def __init__(self, hp: int):
        """Initialize the core part of the entities"""
        self.hp: int = hp
        self.current_node: Node = None
        self.image_path: list = []

    def is_alive(self) -> bool:
        """check if entity is alive"""
        return self.hp > 0
    
    @abstractmethod
    def move(self, destination_node: Node):
        """Abstract method for entity to move"""
        pass



