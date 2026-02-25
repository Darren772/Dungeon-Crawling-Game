from email.mime import audio
import pygame
from Node import Node
from Entity import Entity
from Player import Player
from enum import Enum
import Monster
from Monster import Slime
from Fighting import Fighting
import random
from AdditionalVisual import AdditionalVisual
from Audio import Audio

class NodeLevel(Enum):
    """Enum for node types"""
    START = 1
    BUILDING = 2
    EXIT = 3

class AnimationState(Enum):
    """Enum for movement animations"""
    IDLE = 1,
    WALK_EAST = 2,
    WALK_WEST = 3,
    WALK_NORTH = 4,
    WALK_SOUTH = 5,
    WALK_NORTH_EAST = 6,
    WALK_NORTH_WEST = 7,
    WALK_SOUTH_EAST = 8,
    WALK_SOUTH_WEST = 9,
    TRANSFORM = 10

class MonsterType(Enum):
    """Enum for monster types"""
    SLIME = 1,
    DRAGON = 2
    MUSHROOM = 3

class MazeVisualize:
    """This class will visualize the maze"""
    # Constant for this class
    START_END_ADJUST = 10
    START_END_SIZE = 90
    NODE_SIZE = 68
    SCREEN_SIZE = 1000
    DISTACE_SCALE = 110
    PLAYER_RESIZE = 85
    PLAYER_RECENTER = 4
    
    def __init__(self, rows: int = 0, cols: int = 0):
        """Initialize th visual for maze"""
        self.rows = rows
        self.cols = cols
        self.x_recenter : int
        self.y_recenter : int

    def count_recenter(self, rows: int, cols: int):
        """Calculate the grid so it can fit the screen properly"""

        grid_width = (cols - 1) * self.DISTACE_SCALE
        grid_height = (rows - 1) * self.DISTACE_SCALE
        self.x_recenter = ((self.SCREEN_SIZE - grid_width) / 2) - self.START_END_ADJUST * 2 
        self.y_recenter = ((self.SCREEN_SIZE - grid_height) / 2) - self.START_END_ADJUST * 2

    def draw_clicked_node(self, node: Node, screen: pygame.Surface, level: NodeLevel):
        """Create an animation if the cursor is in the same grid with the node"""
        # loading images
        clicked_node = pygame.image.load("image/clicked_node.png").convert_alpha()
        clicked_node = pygame.transform.scale(clicked_node, (self.NODE_SIZE, self.NODE_SIZE))

        clicked_exit_node = pygame.image.load("image/clicked_en.png").convert_alpha()
        clicked_exit_node = pygame.transform.scale(clicked_exit_node, (self.START_END_SIZE, self.START_END_SIZE))

        clicked_start_node = pygame.image.load("image/clicked_sn.png").convert_alpha()
        clicked_start_node = pygame.transform.scale(clicked_start_node, (self.START_END_SIZE, self.START_END_SIZE))
        
        match level: # Create the animation
            case NodeLevel.START:
                screen.blit(clicked_start_node, (node.node_id[1]*self.DISTACE_SCALE - self.START_END_ADJUST + 
                                                 self.x_recenter, node.node_id[0]*self.DISTACE_SCALE - 
                                                 self.START_END_ADJUST + self.y_recenter))
            case NodeLevel.BUILDING:
                screen.blit(clicked_node,( node.node_id[1]*self.DISTACE_SCALE + self.x_recenter, 
                                          node.node_id[0]*self.DISTACE_SCALE + self.y_recenter))
            case NodeLevel.EXIT:
                screen.blit(clicked_exit_node,( node.node_id[1]*self.DISTACE_SCALE - self.START_END_ADJUST + self.x_recenter, 
                                               node.node_id[0]*self.DISTACE_SCALE - self.START_END_ADJUST + self.y_recenter))
                
    def draw_nodes(self, nodes: list, start_node: Node, exit_nodes: list, screen: pygame.Surface, 
                   start_image: pygame.Surface, node_image: pygame.Surface, exit_image: pygame.Surface):
        """Method to draw all of the image based on the grid"""

        screen.blit(start_image, (start_node.node_id[1]*self.DISTACE_SCALE - self.START_END_ADJUST + 
                                  self.x_recenter, start_node.node_id[0]*self.DISTACE_SCALE - self.START_END_ADJUST + self.y_recenter))

        # Loading the special node images
        acid_node = pygame.image.load("image/specialnode/acid/acid_node.png").convert_alpha()
        acid_node = pygame.transform.scale(acid_node, (self.NODE_SIZE, self.NODE_SIZE))

        blessing_node = pygame.image.load("image/specialnode/blessing/blessing_node.png").convert_alpha()
        blessing_node = pygame.transform.scale(blessing_node, (self.NODE_SIZE, self.NODE_SIZE))

        teleport_node = pygame.image.load("image/specialnode/teleport_node.png").convert_alpha()
        teleport_node = pygame.transform.scale(teleport_node, (self.NODE_SIZE, self.NODE_SIZE))

        for building_node in nodes: # Display the node, including the special node
            if building_node.is_blessing:
                screen.blit(blessing_node,( building_node.node_id[1]*self.DISTACE_SCALE + 
                                           self.x_recenter, building_node.node_id[0]*self.DISTACE_SCALE + 
                                           self.y_recenter))
            elif building_node.is_acidic:
                screen.blit(acid_node,( building_node.node_id[1]*self.DISTACE_SCALE + self.x_recenter, 
                                       building_node.node_id[0]*self.DISTACE_SCALE + self.y_recenter))
            elif building_node.is_teleport:
                screen.blit(teleport_node,( building_node.node_id[1]*self.DISTACE_SCALE + self.x_recenter, 
                                           building_node.node_id[0]*self.DISTACE_SCALE + self.y_recenter))
            else:
                screen.blit(node_image,( building_node.node_id[1]*self.DISTACE_SCALE + self.x_recenter, 
                                        building_node.node_id[0]*self.DISTACE_SCALE + self.y_recenter))

        for exit_node in exit_nodes:
            screen.blit(exit_image,( exit_node.node_id[1]*self.DISTACE_SCALE - self.START_END_ADJUST + self.x_recenter, exit_node.node_id[0]*self.DISTACE_SCALE - self.START_END_ADJUST + self.y_recenter))

    def draw_connections(self, nodes: list, screen: pygame.Surface, node_image: pygame.Surface = None, 
                         exit_image: pygame.Surface = None, start_image: pygame.Surface = None):
        """
        Draw a white line connection between nodes, 
        the connection will be based on the connection generated in Maze class
        """
        node_adjuster = [node_image.get_size(), exit_image.get_size(), start_image.get_size()] #adjust the node
        
        iterator = 0

        for node in nodes:
            if iterator == 0:
                size_adjust = node_adjuster[iterator] 
                iterator += 1
            for connection in node.get_neighbor():   
                
                if (connection and node) in node.check_connection():
                    continue

                # Finding the point of each node
                coordinate_one = [node.node_id[1]*self.DISTACE_SCALE + size_adjust[0]/2 + 
                                  self.x_recenter, node.node_id[0]*self.DISTACE_SCALE + size_adjust[1]/2 + 
                                  self.y_recenter]
                coordinate_two = [connection.node_id[1]*self.DISTACE_SCALE + size_adjust[0]/2 + 
                                  self.x_recenter, connection.node_id[0]*self.DISTACE_SCALE + 
                                  size_adjust[1]/2 + self.y_recenter]
                
                pygame.draw.line(screen, (255, 255, 255), (coordinate_one), (coordinate_two), 2)
                
                node.set_connected([connection, node])
                # Finding the point for the weight text
                x_weight_axis = (coordinate_one[0] + coordinate_two[0]) / 2
                y_weight_axis = (coordinate_one[1] + coordinate_two[1]) / 2

                # Creating the weight text
                text_border = pygame.font.SysFont('Arial', 18, bold = True).render(str(connection.weight + node.weight), 
                                                                                   True, (40, 40, 40))
                text_surface = pygame.font.SysFont('Arial', 16 ).render(str(connection.weight + node.weight), 
                                                                        True, (10, 192, 255))
                
                screen.blit(text_border, (x_weight_axis,y_weight_axis))
                screen.blit(text_surface, (x_weight_axis,y_weight_axis))
                            
                pygame.draw.circle(screen, (255, 255, 255) , (node.node_id[1]*self.DISTACE_SCALE + size_adjust[0]/2 + 
                                                              self.x_recenter, node.node_id[0]*self.DISTACE_SCALE + size_adjust[1]/2 + self.y_recenter), 5)
                pygame.draw.circle(screen, (255, 255, 255), (connection.node_id[1]*self.DISTACE_SCALE + size_adjust[0]/2 + 
                                                             self.x_recenter,  connection.node_id[0]*self.DISTACE_SCALE + size_adjust[1]/2 + self.y_recenter), 5)

    def animate_monster(self, monsters, screen, monster_frame_index, monster_type: MonsterType):
        """Animate the monster based on the monster type"""
        match monster_type:
            case MonsterType.SLIME:
                for monster in monsters:
                    if monster.identity == "Slime":
                        screen.blit(monster.frame[monster_frame_index], 
                                    (monster.current_node.node_id[1] * self.DISTACE_SCALE + 
                                     self.x_recenter, monster.current_node.node_id[0] * self.DISTACE_SCALE + self.y_recenter))
            case MonsterType.DRAGON:
                for monster in monsters:
                    if monster.identity == "Dragon":
                        screen.blit(monster.frame[monster_frame_index], 
                                    (monster.current_node.node_id[1] * self.DISTACE_SCALE + 
                                     self.x_recenter, monster.current_node.node_id[0] * self.DISTACE_SCALE + self.y_recenter))
            case MonsterType.MUSHROOM:
                for monster in monsters:
                    if monster.identity == "Mushroom":
                        screen.blit(monster.frame[monster_frame_index], 
                                    (monster.current_node.node_id[1] * self.DISTACE_SCALE + 
                                     self.x_recenter, monster.current_node.node_id[0] * self.DISTACE_SCALE + self.y_recenter))
        
    def load_animations_image(self, path: str, count: int) -> list:
        """Loading all of the animation image based on the path and count"""
        frame = []
        for index in range(1, count):
            image = pygame.image.load(f"{path}{index}.png").convert_alpha()
            image = pygame.transform.scale(image, (self.PLAYER_RESIZE, self.PLAYER_RESIZE))
            frame.append(image)
        return frame

    def animate_player(self, state: AnimationState) -> list:
        """ Animate all of the player state"""
        knight_idle_frame : int
        player_frame : list = []
        match state:
            case AnimationState.IDLE: # Idle state
                knight_idle_frame = 6
                player_frame = self.load_animations_image("image/character/knight", knight_idle_frame)
                return player_frame
            
            # Movement state
            case AnimationState.WALK_EAST:
                knight_walk_east_frame = 3
                player_frame = self.load_animations_image("image/character/movement/right/run", knight_walk_east_frame)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                return player_frame
            
            case AnimationState.WALK_WEST:
                knight_walk_west_frame = 4
                player_frame = self.load_animations_image("image/character/movement/left/run", knight_walk_west_frame)
                return player_frame
            
            case AnimationState.WALK_NORTH:
                knight_walk_north_frame = 4
                player_frame = self.load_animations_image("image/character/movement/top/run", knight_walk_north_frame)
                return player_frame
            
            case AnimationState.WALK_SOUTH:
                knight_walk_south_frame = 4
                player_frame = self.load_animations_image("image/character/movement/down/run", knight_walk_south_frame)
                return player_frame
            
            case AnimationState.WALK_NORTH_EAST:
                knight_walk_north_east_frame = 3
                player_frame = self.load_animations_image("image/character/movement/rt/run", knight_walk_north_east_frame)
                return player_frame
            
            case AnimationState.WALK_NORTH_WEST:
                knight_walk_north_west_frame = 3
                player_frame = self.load_animations_image("image/character/movement/lt/run", knight_walk_north_west_frame)
                return player_frame
            
            case AnimationState.WALK_SOUTH_EAST:
                knight_walk_south_east_frame = 3
                player_frame = self.load_animations_image("image/character/movement/rd/run", knight_walk_south_east_frame)
                return player_frame

            case AnimationState.WALK_SOUTH_WEST:
                knight_walk_south_west_frame = 3
                player_frame = self.load_animations_image("image/character/movement/ld/run", knight_walk_south_west_frame)
                return player_frame

            # Transform state (From idle to move)
            case AnimationState.TRANSFORM:
                knight_transform_frame = 8
                player_frame = self.load_animations_image("image/character/transform/form", knight_transform_frame)
                return player_frame
    
    def animate_monster_move(self, monsters, monster_frame_index, screen, monster_type: MonsterType, animation_in: bool = True):
        """Animating the monster movement based on the monster type"""
        match monster_type:
            case MonsterType.SLIME:
                for monster in monsters:
                    if monster.identity == "Slime":
                        screen.blit(monster.movement_frame[monster_frame_index], 
                                    (monster.current_node.node_id[1] * self.DISTACE_SCALE + 
                                     self.x_recenter, monster.current_node.node_id[0] * self.DISTACE_SCALE + 
                                     self.y_recenter)) 
            case MonsterType.DRAGON:
                for monster in monsters:
                    if monster.identity == "Dragon":
                        screen.blit(monster.movement_frame[monster_frame_index], 
                                    (monster.current_node.node_id[1] * self.DISTACE_SCALE + self.x_recenter, 
                                     monster.current_node.node_id[0] * self.DISTACE_SCALE + self.y_recenter))
            case MonsterType.MUSHROOM:
                for monster in monsters:
                    if monster.identity == "Mushroom":
                        screen.blit(monster.movement_frame[monster_frame_index], 
                                    (monster.current_node.node_id[1] * self.DISTACE_SCALE + 
                                     self.x_recenter, monster.current_node.node_id[0] * self.DISTACE_SCALE + 
                                     self.y_recenter))
        
    def click_screen(self) -> bool:
        """Method to check if player click the screen"""
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Clicked")
                    return True
        return False

    def track_node(self, nodes: list, start_node: Node, exit_nodes: list, screen: pygame.Surface) -> Node | None:
        """
        this method will track the movement of the player mouse, 
        every time player mouse collide with the node it will return the node.
        """
        x_axis, y_axis = pygame.mouse.get_pos()
        coordinates = [x_axis, y_axis]

        # Checking starting node collision
        start_box = pygame.Rect(
            start_node.node_id[1]*self.DISTACE_SCALE - self.START_END_ADJUST + self.x_recenter,
            start_node.node_id[0]*self.DISTACE_SCALE- self.START_END_ADJUST + self.y_recenter, 
            self.START_END_SIZE, self.START_END_SIZE
            )
                    
        if start_box.collidepoint(coordinates):
            self.draw_clicked_node(start_node, screen, NodeLevel.START)

            if self.click_screen():
                return start_node

        # checking normal node collision
        for node in nodes:
            normal_box = pygame.Rect(
                node.node_id[1]*self.DISTACE_SCALE + self.x_recenter,
                node.node_id[0]*self.DISTACE_SCALE + self.y_recenter,
                self.NODE_SIZE, self.NODE_SIZE
                )
            if normal_box.collidepoint(coordinates):
                self.draw_clicked_node(node, screen, NodeLevel.BUILDING)

                if self.click_screen():
                    return node

        # Checking exit node collision
        for exit_node in exit_nodes:
            end_box = pygame.Rect(
                exit_node.node_id[1]*self.DISTACE_SCALE - self.START_END_ADJUST + self.x_recenter,
                exit_node.node_id[0]*self.DISTACE_SCALE - self.START_END_ADJUST + self.y_recenter,
                self.START_END_SIZE, self.START_END_SIZE
                )
            if  end_box.collidepoint(coordinates):
                self.draw_clicked_node(exit_node, screen, NodeLevel.EXIT)

                if self.click_screen():
                    return exit_node
            
        return None
    
    def check_direction(self, directed_node: Node, player: Player) -> list:
        """Check which direction the player will move to"""
        if directed_node is None:
            return None

        if (directed_node.node_id[0] > player.current_node.node_id[0]) and (
            directed_node.node_id[1] == player.current_node.node_id[1]):
            return self.animate_player(AnimationState.WALK_EAST)
        
        elif (directed_node.node_id[0] < player.current_node.node_id[0]) and (
            directed_node.node_id[1] == player.current_node.node_id[1]):
            return self.animate_player(AnimationState.WALK_WEST)

        elif (directed_node.node_id[0] == player.current_node.node_id[0]) and (
            directed_node.node_id[1] < player.current_node.node_id[1]):
            return self.animate_player(AnimationState.WALK_SOUTH)

        elif (directed_node.node_id[0] == player.current_node.node_id[0]) and (
            directed_node.node_id[1] > player.current_node.node_id[1]):
            return self.animate_player(AnimationState.WALK_NORTH)

        elif (directed_node.node_id[0] > player.current_node.node_id[0]) and (
            directed_node.node_id[1] > player.current_node.node_id[1]):
            return self.animate_player(AnimationState.WALK_NORTH_EAST)
        
        elif (directed_node.node_id[0] > player.current_node.node_id[0]) and (
            directed_node.node_id[1] < player.current_node.node_id[1]):
            return self.animate_player(AnimationState.WALK_SOUTH_EAST)

        elif (directed_node.node_id[0] < player.current_node.node_id[0]) and (
            directed_node.node_id[1] > player.current_node.node_id[1]):
            return self.animate_player(AnimationState.WALK_NORTH_WEST)

        elif (directed_node.node_id[0] < player.current_node.node_id[0]) and (
            directed_node.node_id[1] < player.current_node.node_id[1]):
            return self.animate_player(AnimationState.WALK_SOUTH_WEST)

    def move_animation(self, directed_node: Node, player: Player, screen: pygame.Surface, 
                       move_frame: list, nodes, start_node: Node, exit_nodes: Node, 
                       start_image: pygame.Surface, node_image: pygame.Surface, 
                       exit_image: pygame.Surface, monsters: list, audio: Audio):
        """Visualizing the movement animamtion"""
        #initialize the transform frame, and frame counter
        transform_frame = self.animate_player(AnimationState.TRANSFORM)
        frame_index = 0
        monster_frame_index = 0
        last_update_time = pygame.time.get_ticks()
        animation_cooldown = 100

        # Ensure directed noe is available and meet the requirement
        if directed_node is None or move_frame is None:
            return      
        if directed_node not in player.current_node.neighbor_node:
            return
        
        audio.walking_sound.play(0)
        
        background_image = pygame.image.load("image/background.png").convert()
        additional_graphic = AdditionalVisual(screen, player) 
        while True: # loop for the transformation
            
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > animation_cooldown: # maintain the frame for the player and monster
                frame_index += 1
                if frame_index >= len(transform_frame):
                    break

            if current_time - last_update_time > animation_cooldown:
                monster_frame_index += 1
                last_update_time = current_time
                if monster_frame_index >= Slime.TOTAL_FRAME: # all monster have the same frame, so use slime frame
                    break

            screen.blit(background_image, (0, 0))
            additional_graphic.draw_player_status()
            self.draw_nodes(nodes, start_node, exit_nodes, screen, start_image, node_image, exit_image)
            self.draw_connections([start_node] + nodes + exit_nodes, screen, node_image, exit_image, start_image)
            self.animate_monster_move(monsters, monster_frame_index, screen, MonsterType.SLIME, True)
            self.animate_monster_move(monsters, monster_frame_index, screen, MonsterType.DRAGON, True)
            self.animate_monster_move(monsters, monster_frame_index, screen, MonsterType.MUSHROOM, True)
            screen.blit(transform_frame[frame_index], (player.current_node.node_id[1] * self.DISTACE_SCALE - 
                                                       self.PLAYER_RECENTER + self.x_recenter, player.current_node.node_id[0] * 
                                                       self.DISTACE_SCALE - self.PLAYER_RECENTER + self.y_recenter))
            pygame.display.flip() 

        # Counting the player movement so it align with the path from the current node to the destination node
        start_x = player.current_node.node_id[1] * self.DISTACE_SCALE - self.PLAYER_RECENTER + self.x_recenter
        start_y = player.current_node.node_id[0] * self.DISTACE_SCALE - self.PLAYER_RECENTER + self.y_recenter
        end_x = directed_node .node_id[1] * self.DISTACE_SCALE - self.PLAYER_RECENTER + self.x_recenter
        end_y = directed_node .node_id[0] * self.DISTACE_SCALE - self.PLAYER_RECENTER + self.y_recenter 

        speed = 10
        distance_x = end_x - start_x
        distance_y = end_y - start_y

        move_x = speed if distance_x > 0 else -speed if distance_x < 0 else 0
        move_y = speed if distance_y > 0 else -speed if distance_y < 0 else 0

        location_x = start_x
        location_y = start_y

        # Reset the counter
        frame_index = 0
        monster_frame_index = 0
        last_update_time = pygame.time.get_ticks()

        while True: # Loop for the player movement
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > animation_cooldown:
                frame_index += 1
                last_update_time = current_time
                if frame_index >= len(move_frame):
                    frame_index = 0
                    
            if abs(location_x - end_x) <= abs(move_x) and abs(location_y - end_y) <= abs(move_y):
                location_x = end_x
                location_y = end_y 
                break

            screen.blit(background_image, (0, 0))
            additional_graphic.draw_player_status()
            self.draw_nodes(nodes, start_node, exit_nodes, screen, start_image, node_image, exit_image)
            self.draw_connections([start_node] + nodes + exit_nodes, screen, node_image, exit_image, 
                                  start_image)
            screen.blit(move_frame[frame_index], (location_x, location_y))
            self.animate_monster_move(monsters, monster_frame_index, screen, MonsterType.MUSHROOM, True)
            
            # Move the player
            location_x += move_x
            location_y += move_y

            pygame.display.flip() 

    def move_character_check(self, nodes: list, start_node: Node, exit_nodes: list, screen: pygame.Surface, 
                             player: Player, start_image: pygame.Surface, node_image: pygame.Surface, 
                             exit_image: pygame.Surface, monster_frame_index: int, monsters: list, audio: Audio):
        """Handle the movement of the player"""
        # Checking the directed node, and the direction
        directed_node = self.track_node(nodes, start_node, exit_nodes, screen)
        move_frame = self.check_direction(directed_node, player)
        # Animate
        self.move_animation(directed_node, player, screen, move_frame, nodes, start_node, exit_nodes, start_image, node_image, exit_image, monsters, audio)

        # Move the location
        if directed_node is not None:
            if directed_node in player.current_node.get_neighbor():
                player.move(directed_node, nodes)

                for monster in monsters:
                    monster.move(player.current_node)

    def check_battle_encounter(self, player: Player, monsters: list, screen: pygame.Surface,
                                audio: Audio):
         
         battle_mode = Fighting(player, screen) 
         for monster in monsters: # Checking if the player and the monster is in the same node
                if monster.current_node == player.current_node:

                    audio.pause_bgm()
                    audio.encounter_sound.play(0)

                    self.battle_transition(screen) # Start the battle
                    audio.battle_music.play(-1)

                    # player won (True) or lost/quit (False)
                    won = battle_mode.fight(monster)

                    battle_mode.fight(monster)
                    audio.battle_music.fadeout(700)
                    audio.unpause_bgm()

                    if won:
                        monsters.remove(monster) 
                        print(f"{monster.identity} removed from maze.")
                        break
                    else:
                        audio.game_over_sound.play(0)
                        # Game over
                        return False
          
    def battle_transition(self, screen):
        """Method to create small transition when the player and the monster at the same node"""
        fade_screen = pygame.Surface((self.SCREEN_SIZE, self.SCREEN_SIZE))
        fade_screen.fill((0, 0, 0))
        
        font = pygame.font.SysFont("freesansbold", 35, bold = True)
        battle_notification = font.render(f"!!! ENCOUNTER ENEMY !!!", True, (255, 0, 0))
        recenter_notification = battle_notification.get_rect(center=(self.SCREEN_SIZE // 2, 
                                                                     self.SCREEN_SIZE // 2))
        
        maze_copy = screen.copy()

        # Shake effect
        for shakes in range(5):
            shake_offset = (random.randint(-7,7), random.randint(-7,7))
            screen.blit(maze_copy,shake_offset)
            pygame.display.update()
            pygame.time.delay(15)

        # Create a fading effect for the display
        for transparancy in range (0, 255, 5):
            fade_screen.set_alpha(transparancy)
            screen.blit(fade_screen, (0,0))

            if transparancy > 100:
                screen.blit(battle_notification, recenter_notification)

            pygame.display.update()
            pygame.time.delay(25)

    def visualize(self, exit_nodes: list, nodes: list, start_node: Node, rows: int, cols: int, 
                  player : Player, monsters : list, screen: pygame.Surface):
        """Method to visualize the whole maze, Handle all animation"""
        self.count_recenter(rows, cols)
        player.current_node = start_node
        additional_graphic = AdditionalVisual(screen, player)  

        # Loading background and node images
        background_image = pygame.image.load("image/background.png").convert()

        node_image = pygame.image.load("image/node.png").convert_alpha()
        node_image = pygame.transform.scale(node_image, (self.NODE_SIZE, self.NODE_SIZE))
        
        exit_image = pygame.image.load("image/end_node.png").convert_alpha()
        exit_image = pygame.transform.scale(exit_image, (self.START_END_SIZE, self.START_END_SIZE))
        
        start_image = pygame.image.load("image/start_node.png").convert_alpha()
        start_image = pygame.transform.scale(start_image, (self.START_END_SIZE, self.START_END_SIZE))

        player_animation = self.animate_player(AnimationState.IDLE) #animating player idle state

        audio = Audio()
        audio.play_soundtrack() # Playing the soundtrack


        running = True

        time = pygame.time.Clock()
        delta_time = 0.1
        player_frame_index = 0
        monster_frame_index = 0
        last_update_time = pygame.time.get_ticks()
        animation_cooldown_player = 130  
        animation_cooldown_monster = 150  
        audio.unpause_bgm()

        while running: # Main loop
            all_events = pygame.event.get()
            screen.blit(background_image, (0, 0))
            self.draw_nodes(nodes, start_node, exit_nodes, screen, start_image, node_image, exit_image)
            additional_graphic.draw_player_status()
            self.draw_connections([start_node] + nodes + exit_nodes, screen, node_image, exit_image, 
                                  start_image)
            
            if player.current_node in exit_nodes: # check if player is in the exit node, if yes it will pause the game
                audio.pause_bgm()
                audio.win_sound.play(0)
                proceed = additional_graphic.end_stage(all_events)
                pygame.display.flip()
                if proceed:
                    return True  # Signal stage completed
                continue

            menu_active = additional_graphic.settings(all_events) # Check if the pause menu is active
            if menu_active:
                pygame.display.flip()
                continue
            
            self.move_character_check( nodes, start_node, exit_nodes, screen, player, start_image, 
                                      node_image, exit_image, monster_frame_index, monsters, audio)
            current_time = pygame.time.get_ticks()

            # Check battle encounter
            battle_returned_value = self.check_battle_encounter(player, monsters, screen, audio)
            if battle_returned_value is False:
                return False
                    
            if current_time - last_update_time >= animation_cooldown_player: #iterate the player frame for the animation
                player_frame_index += 1
            if player_frame_index >= len(player_animation):
                player_frame_index = 0

            screen.blit(player_animation[player_frame_index], (player.current_node.node_id[1] * 
                                                               self.DISTACE_SCALE - self.PLAYER_RECENTER + 
                                                               self.x_recenter, player.current_node.node_id[0] * 
                                                               self.DISTACE_SCALE - self.PLAYER_RECENTER + self.y_recenter))

            if current_time - last_update_time >= animation_cooldown_monster: #iterate the monster frame for the animation
                monster_frame_index += 1
                last_update_time = current_time
                if monster_frame_index >= Slime.TOTAL_FRAME:
                    monster_frame_index = 0
            
            # Animate mosnter
            self.animate_monster(monsters, screen, monster_frame_index, MonsterType.SLIME)
            self.animate_monster(monsters, screen, monster_frame_index, MonsterType.DRAGON)
            self.animate_monster(monsters, screen, monster_frame_index, MonsterType.MUSHROOM)


            for event in all_events:
                if event.type == pygame.QUIT:
                    running = False 
            
            # Return when player lose(false)
            if player.hp <= 0:
                audio.game_over_sound.play(0)
                return False
            if player.steps <= 0:
                audio.game_over_sound.play(0)
                return False

            pygame.display.flip()
            delta_time = time.tick(60) / 1000.0
            delta_time = max(0.05, min(delta_time, 0.1))

        return player.hp > 0 and player.steps > 0 # Return whether player win(true) or lose (false)