from Entity import Entity
import random
import pygame
from Audio import Audio

class Skill:
    """Base class for all battle skills"""
    def __init__(self, value: int, stamina_cost: int, identity: str):
        """Initialize skill the attributes"""
        self.value = value
        self.stamina_cost = stamina_cost
        self.identity = identity
        self.audio = Audio()

    def use(self, action: str, target: Entity, user: Entity):
        """Execute skill action based on action string"""
        if action == 'attack':
            self.attack(user, target)
        elif action == 'heal':
            self.heal(user)
        elif action == 'special_skill':
            self.special_skill(user, target)


class Fireball(Skill):
    """Player's  attack skill that deals fixed damage to target"""
    def __init__(self):
        """Initialize Fireball skill"""
        super().__init__(15, 5, "fireball")
        self.image = pygame.image.load("image/battle/skills/fireball/fireball.png")

    def use(self, user: Entity, target: Entity):
        """Use fireball damage if user has enough stamina"""
        if user.steps >= self.stamina_cost:
            self.audio.fireball_sound.play(0)
            user.steps -= self.stamina_cost
            target.hp -= self.value
            if target.hp < 0:
                target.hp = 0

class Mana(Skill):
    """Restore stamina to user with randomized amount to Player"""
    def __init__(self):
        """Initialize Mana regen skill"""
        value = random.randint(5, 15)
        super().__init__(value, 0, "Mana")
        self.image = pygame.image.load("image/battle/skills/mana/mana.png")

    def use(self, user: Entity, target: Entity):
        """Restore stamina to user"""
        user.steps += self.value
        self.audio.mana_regen_sound.play(0)
        if user.steps > user.max_steps:
            user.steps = user.max_steps

class Heal(Skill):
    """Heal skill that restores HP to user"""
    def __init__(self):
        """Initialize Heal skill"""
        value = random.randint(4, 16)
        super().__init__(value, 11, "heal")
        self.image = pygame.image.load("image/battle/skills/heal/heal.png")

    def use(self, user: Entity, target: Entity):
        """Heal user if Player have enough stamina"""
        if user.steps >= self.stamina_cost:
            self.audio.heal_sound.play(0)
            user.steps -= self.stamina_cost
            user.hp += self.value
            if user.hp > user.max_hp:
                user.hp = user.max_hp

class SlimeSkill(Skill):
    """Monster skill for slime"""
    def __init__(self):
        """Initialize slime skill"""
        self.special_skill_used = False

    def attack(self, user: Entity, target: Entity):
        """Attack random damage on target"""
        damage = random.randint(3, 6)
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0

    def heal(self, user: Entity):
        """Heal user with random amount"""
        heal_amount = random.randint(6, 10)
        user.hp += heal_amount
        if user.hp > user.max_hp:
            user.hp = user.max_hp

    def special_skill(self, user: Entity, target: Entity):
        """Give user immunity and reflect for limited duration."""
        if not self.special_skill_used:
            user.is_immune = True
            user.reflect = True
            user.duration_counter = 2
            self.special_skill_used = True
        

class DragonSkill(Skill):
    """Monster skill dragon"""
    def __init__(self):
        """Initialize dragon skill"""
        self.special_skill_used = False
        self.damage_boost = False

    def attack(self, user: Entity, target: Entity):
        """Deal damage with boost when active(use special skill to activate)."""
        damage = random.randint(5, 17)
        if self.damage_boost:
            damage += random.randint(1, 7)
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0

    def heal(self, user: Entity):
        """Heal dragon with random amount."""
        heal_amount = random.randint(1, 15)
        user.hp += heal_amount
        if user.hp > user.max_hp:
            user.hp = user.max_hp

    def special_skill(self, user: Entity, target: Entity):
        """Enable damage boost, reflect damage, heal if low HP."""
        if not self.special_skill_used:
            user.reflect = True
            user.duration_counter = 2
            self.damage_boost = True
            if user.hp < (0.5 * user.max_hp):
                user.hp += (0.3 * user.max_hp)
            self.special_skill_used = True
        
    
class MushroomSkill(Skill):
    """Monster skill for Mushroom"""
    def __init__(self):
        """Initialize mushroom skill."""
        self.special_skill_used = False
        self.damage_boost = False

    def attack(self, user: Entity, target: Entity):
        """Deal random damage to target."""
        damage = random.randint(3, 12)
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0

    def heal(self, user: Entity):
        """Heal mushroom with random amount."""
        heal_amount = random.randint(1, 15)
        user.hp += heal_amount
        if user.hp > user.max_hp:
            user.hp = user.max_hp

    def special_skill(self, user: Entity, target: Entity):
        """Deal high damage to target and set own HP to 0."""
        if not self.special_skill_used:
            user.reflect = True
            user.duration_counter = 2
            damage = random.randint(5, 30)
            target.hp -= damage
            if target.hp < 0:
                target.hp = 0
            user.hp = 0
            self.special_skill_used = True
        