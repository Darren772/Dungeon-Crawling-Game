from Player import Player
from Monster import Monster
from FightVisual import FightVisual
import pygame
import Skill
from AdditionalVisual import AdditionalVisual

class Fighting:
    """This class will manage the fighting system between monster and player"""
    def __init__ (self, player: Player, screen: pygame.Surface):
        """Initialize fighting system, create core component for the fighting system"""
        self.round: int
        self.player = player
        self.screen = screen

    def execute_monster_turn(self, monster: Monster, visual: FightVisual):
        """Execute monster turn"""
        if not monster.is_alive():
            return
        
        decision = monster.battle(self.player)
        visual.display_monster_skill(decision, duration=60)
        pygame.display.flip()
        pygame.time.wait(400)
        monster.skill.use(decision, self.player, monster) # Execute monster's skill
        

    def execute_player_skill(self, skill: Skill, monster: Monster):
        """Execute player skill, while handling special effect of the monster skill"""
        immune_status = monster.is_immune
        reflect_status = monster.reflect

        if immune_status: # handle immunity status
            if monster.duration_counter > 0:
                monster.duration_counter -= 1
            else:
                monster.is_immune = False
        
        if reflect_status: # Handle bounces back damage to player
            skill.use(self.player, self.player)
            if monster.duration_counter > 0:
                monster.duration_counter -= 1
            else:
                monster.reflect = False
        # Apply player's skill
        if not immune_status:
            skill.use(self.player, monster)

    def fight(self, monster: Monster):
        """The main battle loop between player and monster"""
        visual = FightVisual(self.player, monster, self.screen)
        additional_graphic = AdditionalVisual(self.screen, self.player)
        self.battle = True

        while self.battle:
            player_skill = visual.visualize()
            all_events = pygame.event.get()

            if player_skill == "end":
                self.battle = False
                return False

            if player_skill:
                self.execute_player_skill(player_skill, monster)
                
                # Check monster status
                if monster.hp <= 0:
                    self.battle = False
                    return True
                
                self.execute_monster_turn(monster, visual)
                if monster.hp <= 0:
                    self.battle = False
                    return True
            
            # Check player status
            if self.player.hp <= 0:
                self.battle = False
                return False
