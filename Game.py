from Maze import *
from Node import Node
from Player import Player  
from Monster import Slime, Dragon, Mushroom
from Skill import Fireball, Mana, Heal
import math
from AdditionalVisual import AdditionalVisual
import pygame

# Game constant
SCREEN_SIZE = 1000
BLACK = (0, 0, 0)
PLAYER_INITIAL_HP = 100
PLAYER_INITIAL_STEPS = 250

def read_maze_data(file_path: str) -> list:
    """Creating maze layout from CSV file"""
    maze_grid = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Monster:"): # Stop at monster part
                    break
            row = list(map(int, line.strip().split(','))) # append the row from csv in form of list
            maze_grid.append(row)
    return maze_grid

def read_monster_data(file_path: str) -> list:
    """ Read monster data from the CSV file"""
    monster_list = []
    check = False
    with open(file_path, 'r') as file:
        for line in file:
            
            # Ensure to read only the monster part from the csv file
            if check == False:
                if not line.startswith("Monster:"):
                    continue
                elif line.startswith("Monster:"):
                    check = True
                    continue
                
            parts = line.strip().split(',')
            monster_type = parts[1]
            hp = int(parts[0])

            # Check monster type
            if monster_type == "Slime":
                monster = Slime(hp)
                monster_list.append(monster)
            elif monster_type == "Dragon":          
                monster = Dragon(hp)
                monster_list.append(monster)
            elif monster_type == "Mushroom":          
                monster = Mushroom(hp)
                monster_list.append(monster)
    return monster_list

if __name__ == "__main__": # main 
    pygame.init()
    screen = pygame.display.set_mode(( SCREEN_SIZE, SCREEN_SIZE))   
    stages = ["stage1.csv", "stage2.csv","stage3.csv","stage4.csv"]
    player = Player(PLAYER_INITIAL_HP, PLAYER_INITIAL_STEPS)  
    graphics = AdditionalVisual(screen, player)

    pygame.display.set_caption("Dungeon Crawling Game")
    icon = pygame.image.load("image/end_node.png")
    pygame.display.set_icon(icon)

    stage_index = 0
    running = True

    while running: # Main loop for the game
        all_events = pygame.event.get()
        
        if graphics.start_menu_active: # Calling main menu
            graphics.start_menu(all_events)
            pygame.display.flip()
            continue

        if stage_index >= len(stages): # checking stage
            #reset all to initial state
            player = Player(hp=PLAYER_INITIAL_HP, steps=PLAYER_INITIAL_STEPS)
            graphics = AdditionalVisual(screen, player)
            graphics.start_menu_active = True
            stage_index = 0
            
            # Clear screen
            screen.fill((0, 0, 0))
            pygame.display.flip()
            continue

        stage_file = stages[stage_index]
        monsters = read_monster_data(stage_file)
        maze_grid = read_maze_data(stage_file)

        maze = Maze(maze_grid)

        # Clear screen 
        screen.fill(BLACK)
        pygame.display.flip()

        # If the player completed the stage, return True
        stage_completed = maze.generate_maze(player, monsters, screen, stage_index)

        if stage_completed:
            # Clear screen 
            screen.fill(BLACK)
            pygame.display.flip()

            # Add buff for the player            
            player.steps +=  math.ceil(0.4 * player.steps)
            if player.steps > player.max_steps:
                player.steps = player.max_steps
            player.hp += math.ceil(0.5 * player.hp)
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            stage_index += 1
            continue

        elif not stage_completed:
            # Player died or ran out of steps
            game_over_result = None
            while game_over_result is None and running:
                events = pygame.event.get()
                game_over_result = graphics.game_over(events)
                pygame.display.flip()
                
                for event in events:
                    if event.type == pygame.QUIT:
                        running = False
                        break
            
            if not running:
                break  # Exit main loop if window closed
                
            if game_over_result == "restart":
                # Clear screen before restart
                screen.fill(BLACK)
                pygame.display.flip()
                
                # Reset all to initial state
                player = Player(hp=PLAYER_INITIAL_HP, steps=PLAYER_INITIAL_STEPS)
                graphics = AdditionalVisual(screen, player)
                graphics.start_menu_active = True
                stage_index = 0

            elif game_over_result == "quit":
                running = False
                break
            

        for event in all_events:
            if event.type == pygame.QUIT:
                running = False 

    pygame.quit()