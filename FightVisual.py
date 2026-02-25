from Player import Player
from Monster import Monster
import pygame
from AdditionalVisual import AdditionalVisual
import math
from Skill import Fireball, Mana, Heal

class FightVisual:
    """Handle the visual during the battle phase"""
    # Constant variable for this class
    CARD_WIDTH = 150
    CARD_HEIGHT = 200
    CARD_Y = 700
    MAX_DISTANCE = 150        
    SHRINK_FACTOR = 0.2   
    SLIME_LOCATION = (600, 250)
    
    # Centers for the card
    CENTER_1 = (375, CARD_Y + 100)
    CENTER_2 = (575, CARD_Y + 100)
    CENTER_3 = (775, CARD_Y + 100)
    
    def __init__(self, player: Player, monster: Monster, screen: pygame.Surface):
        """Initialize the visual"""
        self.player = player
        self.monster = monster
        self.screen = screen

    def draw_player(self):
        """Draw player sprite """
        self.player.hp_status()
        self.screen.blit(self.player.player_current_image,(0, 0))

    def draw_monster(self):
        """Draw monster sprite and status"""
        additional_graphic = AdditionalVisual(self.screen, self.player)
        self.screen.blit(self.monster.battle_image, self.SLIME_LOCATION)
        additional_graphic.draw_monster_status(self.monster)
    
    def display_monster_skill(self, skill_name: str, duration: int = 60):
        """Display monster skill"""
        skill_display = {
            "attack": "MONSTER ATTACKS!",
            "special_skill": "MONSTER USE SPECIAL SKILL!",
            "heal": "MONSTER HEALS!"
        }
        
        display_text = skill_display.get(skill_name, "SKILL USED!")
        
        # Creating the transparent layer
        overlay = pygame.Surface((1000, 1000), pygame.SRCALPHA)
        overlay.fill((30, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))
        
        # Render skill text
        font = pygame.font.SysFont('Arial', 50, bold=True)
        text_surface = font.render(display_text, True, (255, 100, 100))
        text_rect = text_surface.get_rect(center = (500, 400))
        self.screen.blit(text_surface, text_rect)

        
    def draw_player_skill(self):
        """Displaying player's skill in a form of card"""

        if isinstance(self.player.skills[0], str): # checking the instance of the skill 
            self.player.skills = [Fireball(), Mana(), Heal()]

        mouse_pos = pygame.mouse.get_pos()

        # Fire skill
        skill_fire = self.player.skills[0]
        distance_fire = math.hypot(mouse_pos[0] - self.CENTER_1[0], mouse_pos[1] - self.CENTER_1[1])

        scale_fire = 1.0 - (self.SHRINK_FACTOR * 
                            (1.0 - (distance_fire/self.MAX_DISTANCE))) if distance_fire < self.MAX_DISTANCE else 1.0
        
        fire_image = pygame.transform.smoothscale(skill_fire.image, 
                                                  (int(self.CARD_WIDTH * scale_fire), 
                                                    int(self.CARD_HEIGHT * scale_fire)))
        
        self.screen.blit(fire_image, fire_image.get_rect(center=self.CENTER_1))

        # Mana regen skill
        skill_mana = self.player.skills[1]
        distance_mana = math.hypot(mouse_pos[0] - self.CENTER_2[0], mouse_pos[1] - self.CENTER_2[1])

        scale_mana = 1.0 - (self.SHRINK_FACTOR * 
                            (1.0 - (distance_mana/self.MAX_DISTANCE))) if distance_mana < self.MAX_DISTANCE else 1.0
        
        slash_image = pygame.transform.smoothscale(skill_mana.image, 
                                                   (int(self.CARD_WIDTH * scale_mana), 
                                                    int(self.CARD_HEIGHT * scale_mana)))
        
        self.screen.blit(slash_image, slash_image.get_rect(center=self.CENTER_2))

        # Heal skill
        skill_heal = self.player.skills[2]
        distance_heal = math.hypot(mouse_pos[0] - self.CENTER_3[0], mouse_pos[1] - self.CENTER_3[1])

        scale_heal = 1.0 - (self.SHRINK_FACTOR * 
                            (1.0 - (distance_heal/self.MAX_DISTANCE))) if distance_heal < self.MAX_DISTANCE else 1.0
        
        heal_image = pygame.transform.smoothscale(skill_heal.image, 
                                                  (int(self.CARD_WIDTH * scale_heal), 
                                                   int(self.CARD_HEIGHT * scale_heal)))
        self.screen.blit(heal_image, heal_image.get_rect(center = self.CENTER_3))
     

    def display_monster_description(self):
        """Display description of monster skill"""
        description = self.monster.description_image
        description_rect = description.get_rect(center=(400, 200))
        self.screen.blit(description, description_rect)

    def visualize(self):
        """Handle all of the visualization and manage some events"""
        additional_graphic = AdditionalVisual(self.screen, self.player)
        background_image = pygame.image.load("image/fightbackground.png").convert()
        self.screen.blit(background_image, (0, 0))
        additional_graphic.draw_player_status()
        self.draw_player()
        self.draw_player_skill()
        self.draw_monster()
        self.display_monster_description()
       

        all_events = pygame.event.get()
        for event in all_events:
            if event.type == pygame.QUIT:
                return "end"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                m_pos = event.pos

                # Card animation zoom in and zoom out
                if math.hypot(m_pos[0]-self.CENTER_1[0], m_pos[1]-self.CENTER_1[1]) < 75:
                    return self.player.skills[0]
                elif math.hypot(m_pos[0]-self.CENTER_2[0], m_pos[1]-self.CENTER_2[1]) < 75:
                    return self.player.skills[1]
                elif math.hypot(m_pos[0]-self.CENTER_3[0], m_pos[1]-self.CENTER_3[1]) < 75:
                    return self.player.skills[2]

            
        pygame.display.flip()
        