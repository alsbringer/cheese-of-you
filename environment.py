from entities import Player, Cheese, Platforms, Frame
from skill import Skill
from config import WINDOW_HEIGHT, BACKGROUND_IMG

class Environment:
    def __init__(self):
        self.gravity = 1
        self.players: list[Player] = []
        self.platforms: list[Platforms] = []
        self.items: list[Cheese] = []
        self.skills: list[Skill] = []

    # auto
    def register_skills(self):
        for player in self.players:
            if player.skills:
                for skill in player.skills:
                    self.skills.append(skill)
                    # print("skiil", skill.name, "berhasil ditambahkan ke environmen")

    def apply_collision_x(self):
        for platform in self.platforms:
            for item in self.players + self.items:
                if item.rect.colliderect(platform.rect):
                    platform.resonate()
                    if item.velocity_x > 0: 
                        item.velocity_x = 0
                        item.rect.right = platform.rect.left
                    elif item.velocity_x < 0:
                        item.velocity_x = 0
                        item.rect.left = platform.rect.right

    def apply_collision_y(self):
        for platform in self.platforms:
            for item in self.players + self.items:
                if item.rect.colliderect(platform.rect):
                    platform.resonate()
                    if item.velocity_y > 0: 
                        item.velocity_y = 0
                        item.rect.bottom = platform.rect.top
                        if isinstance(item, Player):
                            item.jump_left = 2
                    elif item.velocity_y < 0:
                        item.velocity_y = 0
                        item.rect.top = platform.rect.bottom
                    if isinstance(item, Cheese):
                        item.velocity_x = 0

    def update_platform(self):
        for platform in self.platforms:
            platform.update_color()
            
    def reset_platform(self):
        for platform in self.platforms:
            platform.reset_color()
            platform.calm()
    
    def display_skill(self, display):
        for effect in self.skills:
            if effect.active:
                current_frame = effect.frames[effect.active_index]
                display.blit(current_frame.surface, current_frame.rect)
    
    
    # used
    def register_entity(self, entity):
            if isinstance(entity, Player):
                self.players.append(entity)
            elif isinstance(entity, Cheese):
                self.items.append(entity)
            elif isinstance(entity, Platforms):
                self.platforms.append(entity)
            else: print("object: ", entity, "belum terdaftar di environment")
        
    def apply_gravity(self, ground_height):
        for entity in self.players + self.items:
            if entity.rect.bottom >= WINDOW_HEIGHT:
                entity.velocity_y = 0
                entity.rect.bottom = WINDOW_HEIGHT - ground_height
            else:
                entity.velocity_y += self.gravity
            
    def apply_skill(self):
        for skill in self.skills:
            skill.update_skill()
            
    def update_all(self):
            self.reset_platform()

            for entity in self.players + self.items:
                if entity.allow_update:
                    entity.update_x()
                    self.apply_collision_x()
                        
                    entity.update_y()
                    self.apply_collision_y()
            
                if isinstance(entity, Player): entity.update_carried_item()

            self.update_platform()
                
    def display_all(self,display):
        display.blit(BACKGROUND_IMG, (0,0))
        for entity in self.platforms + self.players + self.items:
            display.blit(entity.surface, (entity.rect.left, entity.rect.top))
        self.display_skill(display)