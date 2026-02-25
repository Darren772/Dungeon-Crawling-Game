import pygame
from Player import Player
import sys
from Monster import Monster

class AdditionalVisual:
    """ This class will store some visual extension that will be use by the other visual class"""
    #constant variable
    SETTING_SIZE = 100
    SCREEN_SIZE = 1000
    MENU_SIZE = 100
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, screen: pygame.Surface, player: Player):
        """Initialize properties for the additional features"""
        self.screen = screen
        self.player = player
        self.menu = False
        self.start_menu_active = True
        self.flip_on = True

        # Buttons template
        self.rule_button = pygame.Rect(350, 400, 300, 50)
        self.back_button = pygame.Rect(350, 470, 300, 50)
        self.quit_button = pygame.Rect(350, 540, 300, 50)
        self.proceed_button = pygame.Rect(350, 400, 300, 50)

    def draw_player_status(self):
        """This method will draw player status on the screen"""
        # HP bar display and calculation
        max_hp = self.player.max_hp
        player_current_hp = self.player.hp
        player_hp_scale = max_hp + (player_current_hp - max_hp)
        player_hp_bar = (200/max_hp) * player_hp_scale

        hp_bar_border =pygame.Rect(0, 0, 204, 24)
        pygame.draw.rect(self.screen, self.BLACK, hp_bar_border)

        hp_shell = pygame.Rect(2, 2, 200, 20)
        pygame.draw.rect(self.screen, self.WHITE, hp_shell)

        hp_bar = pygame.Rect(2, 2, player_hp_bar, 20)
        pygame.draw.rect(self.screen, (255, 0, 0), hp_bar)

        text_hp = pygame.font.SysFont('Arial', 15, bold = True).render(f"HP: {player_current_hp}/{max_hp}", 
                                                                       True, self.BLACK)
        self.screen.blit(text_hp, (10, 2))

        # Stamina bar display and calculation
        max_stamina = self.player.max_steps
        player_current_stamina= self.player.steps
        player_stamina_scale = max_stamina + (player_current_stamina - max_stamina)
        player_stamina_bar = (150/max_stamina) * player_stamina_scale

        stamina_bar_border =pygame.Rect(0, 25, 154, 24)
        pygame.draw.rect(self.screen, self.BLACK, stamina_bar_border)

        stamina_shell = pygame.Rect(2, 27, 150, 20)
        pygame.draw.rect(self.screen, self.WHITE, stamina_shell)

        stamina_bar = pygame.Rect(2, 27, player_stamina_bar, 20)
        pygame.draw.rect(self.screen, (100, 100, 255), stamina_bar)

        text_hp = pygame.font.SysFont('Arial', 15, bold = True).render(f"STAMINA: {player_current_stamina}/{max_stamina}", 
                                                                       True, self.BLACK)
        self.screen.blit(text_hp, (10, 27))  
    
    def draw_monster_status(self, monster: Monster):
        """This method will draw monster status on the screen"""
        monster_height = monster.battle_image.get_height() # To find adjustment for the HP bar position

        max_hp = monster.max_hp
        monster_current_hp = monster.hp
        monster_hp_scale = max_hp + (monster_current_hp - max_hp)
        monster_hp_bar = (200/max_hp) * monster_hp_scale

        hp_bar_border =pygame.Rect(600, monster_height + 250, 204, 24)
        pygame.draw.rect(self.screen, self.BLACK, hp_bar_border)

        hp_shell = pygame.Rect(602, monster_height + 252, 200, 20)
        pygame.draw.rect(self.screen, self.WHITE, hp_shell)

        hp_bar = pygame.Rect(602, monster_height + 252, monster_hp_bar, 20)
        pygame.draw.rect(self.screen, (255, 0, 0), hp_bar)

        text_hp = pygame.font.SysFont('Arial', 15, bold = True).render(f"HP: {monster_current_hp}/{max_hp}", 
                                                                       True, self.BLACK)
        self.screen.blit(text_hp, (604, monster_height + 254))
        
    def draw_clicked_setting(self):
        """This method will create a highlight when the cursor is pointed to setting"""
        setting_image = pygame.image.load("image/selected_setting.png").convert_alpha()
        setting_image = pygame.transform.scale(setting_image, (self.SETTING_SIZE, self.SETTING_SIZE))
        self.screen.blit(setting_image, (850,40))
    
    def setting_menu(self, events):
        """ Creating a setting menu display that will help the user"""
        # Creating the transparent layer
        overlay = pygame.Surface((self.SCREEN_SIZE, self.SCREEN_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        menu_display = pygame.Rect(300, 350, 400, 300)

        # Creating the display
        pygame.draw.rect(self.screen, (200, 200, 200), menu_display, border_radius = 10)
        pygame.draw.rect(self.screen, (50, 50, 50), self.rule_button, border_radius = 5)
        pygame.draw.rect(self.screen, (50, 50, 50), self.back_button, border_radius = 5)
        pygame.draw.rect(self.screen, (160, 0, 0), self.quit_button, border_radius = 5)

        font = pygame.font.SysFont('Arial', 20, bold=True)
        
        rules_text = font.render("RULES", True, self.WHITE)
        back_text = font.render("BACK", True, self.WHITE)
        quit_text = font.render("QUIT", True, self.WHITE)
        
        rules_rect = rules_text.get_rect(center=self.rule_button.center)
        back_rect = back_text.get_rect(center=self.back_button.center)
        quit_rect = quit_text.get_rect(center=self.quit_button.center)
        
        self.screen.blit(rules_text, rules_rect)
        self.screen.blit(back_text, back_rect)
        self.screen.blit(quit_text, quit_rect)

        # To process the event if the user press one of the button
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu:
                    if self.rule_button.collidepoint(event.pos) :
                        self.rule_menu()
                    if self.back_button.collidepoint(event.pos):
                        self.menu = False 
                    if self.quit_button.collidepoint(event.pos):
                        self.menu = False
                        pygame.quit()
                        sys.exit()

    def settings(self, events):
        """Class where all of the settings method is utilized"""
        setting_image = pygame.image.load("image/setting.png").convert_alpha()
        setting_image = pygame.transform.scale(setting_image, (self.SETTING_SIZE, self.SETTING_SIZE))
        self.screen.blit(setting_image, (850,40))

        # Get mouse location
        x_axis, y_axis = pygame.mouse.get_pos()
        coordinates = [x_axis, y_axis]

        setting_box = pygame.Rect(850, 50, 950, 140)
                    
        if setting_box.collidepoint(coordinates):
            self.draw_clicked_setting()

        # Loop to check if the user click setting button
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if setting_box.collidepoint(event.pos):
                    self.menu = True
                    
        if self.menu:
            self.setting_menu(events)
            return True
        
        return False

    def end_stage(self, events):
        """Display stage completion screen with proceed button to continue"""
        # Creating the transparent layer
        overlay = pygame.Surface((self.SCREEN_SIZE, self.SCREEN_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        menu_display = pygame.Rect(300, 350, 400, 300)
        # Create the display
        pygame.draw.rect(self.screen, (200, 200, 200), menu_display, border_radius = 10)

        pygame.draw.rect(self.screen, (0, 120, 0), self.proceed_button, border_radius = 5)
       
        font = pygame.font.SysFont('Arial', 30, bold=True)
        proceed_font = pygame.font.SysFont('Arial', 20, bold=True)

        proceed_text = proceed_font.render("PROCEED", True, self.WHITE)
        proceed_rect = proceed_text.get_rect(center=self.proceed_button.center)
        self.screen.blit(proceed_text, proceed_rect)
        
        self.screen.blit(font.render("STAGE CLEARED!", True, (20, 200, 30)), (390, 350))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.proceed_button.collidepoint(event.pos):
                    return True
        return False

    def start_menu(self, events):
        """Create display for main start menu with game title and buttons"""
        self.screen.fill((0, 0, 0)) # clear screen
        menu_display = pygame.Rect(300, 330, 400, 300)# Border for the menu

        pygame.draw.rect(self.screen, (50, 50, 50), (295, 325, 410, 310), border_radius = 12)
        pygame.draw.rect(self.screen, (200, 200, 200), menu_display, border_radius = 10)


        font = pygame.font.SysFont('Arial', 30, bold=True)
        btn_font = pygame.font.SysFont('Arial', 20, bold=True)

        text_surface = font.render("Dungeon Crawling Game", True, (0, 0, 0))
        self.screen.blit(text_surface, (350, 360))

        pygame.draw.rect(self.screen, (50, 50, 50), self.rule_button, border_radius = 5)
        pygame.draw.rect(self.screen, (0, 120, 0), self.back_button, border_radius = 5) 
        pygame.draw.rect(self.screen, (160, 0, 0), self.quit_button, border_radius = 5) 

        rules_text = font.render("RULES", True, self.WHITE)
        start_text = btn_font.render("START", True, self.WHITE)
        quit_text = btn_font.render("QUIT", True, self.WHITE)
        
        rules_rect = rules_text.get_rect(center = self.rule_button.center)
        start_rect = start_text.get_rect(center = self.back_button.center)
        quit_rect = quit_text.get_rect(center = self.quit_button.center)
        
        self.screen.blit(rules_text, rules_rect)
        self.screen.blit(start_text, start_rect)
        self.screen.blit(quit_text, quit_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rule_button.collidepoint(event.pos):
                    self.rule_menu()
                if self.back_button.collidepoint(event.pos):
                    self.start_menu_active = False
                if self.quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
    
    def game_over(self, events):
        """Display game over screen with restart and quit option"""
        # Creating the transparent layer
        overlay = pygame.Surface((self.SCREEN_SIZE, self.SCREEN_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        menu_display = pygame.Rect(300, 350, 400, 300)

        # Creating the display
        pygame.draw.rect(self.screen, (200, 200, 200), menu_display, border_radius=10)

        pygame.draw.rect(self.screen, (0, 160, 0), self.proceed_button, border_radius=5)
        pygame.draw.rect(self.screen, (160, 0, 0), self.quit_button, border_radius=5)
       
        font = pygame.font.SysFont('Arial', 30, bold=True)
        quit_font = pygame.font.SysFont('Arial', 20, bold=True)

        proceed_font = pygame.font.SysFont('Arial', 20, bold=True)
        proceed_text = proceed_font.render("PROCEED", True, self.WHITE)

        proceed_rect = proceed_text.get_rect(center = self.proceed_button.center)
        self.screen.blit(proceed_text, proceed_rect)

        quit_text = quit_font.render("QUIT", True, self.WHITE)
        quit_rect = quit_text.get_rect(center = self.quit_button.center)
        self.screen.blit(quit_text, quit_rect)
        self.screen.blit(proceed_text, proceed_rect)
        
        self.screen.blit(font.render("GAME OVER", True, (200, 20, 30)), (427, 360))

        # To process the event if the user press one of the button
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.proceed_button.collidepoint(event.pos):
                    return "restart"
                if self.quit_button.collidepoint(event.pos):
                    return "quit"
                
    def rule_menu(self):
        """This method will show the game rule as a pop up"""
        rule = pygame.image.load(f"image/Rule.png")
        rule_image = rule.get_rect(center = (self.SCREEN_SIZE // 2, self.SCREEN_SIZE // 2))
        menu_on = True
        while menu_on: # Loop for the pop up
            all_event = pygame.event.get()
            self.screen.blit(rule, rule_image)
            pygame.display.flip()
            for event in all_event:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu_on = False
                    