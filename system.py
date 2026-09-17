from entities import Player, Cheese, Platforms, Frame
from skill import Skill
from assets.config import WINDOW_HEIGHT, BACKGROUND_IMG

class System:
    def __init__(self):
        self.players: list[Player] = []
        self.platforms: list[Platforms] = []
        self.items: list[Cheese] = []
        self.skills: list[Skill] = []

    def register_entity(self, entity):
        if isinstance(entity, Player):
            self.players.append(entity)
        elif isinstance(entity, Cheese):
            self.items.append(entity)
        elif isinstance(entity, Platforms):
            self.platforms.append(entity)
    
    def register_skills(self):
            for player in self.players:
                if player.skills:
                    for skill in player.skills:
                        self.skills.append(skill)
    

class Environment(System):
    def __init__(self):
        super().__init__()
        self.gravity = 1

    def apply_collision_x(self):
        for platform in self.platforms:
            for entity in self.players + self.items:
                if entity.rect.colliderect(platform.rect):
                    platform.resonate()
                    if entity.velocity_x > 0: 
                        entity.velocity_x = 0
                        entity.rect.right = platform.rect.left
                    elif entity.velocity_x < 0:
                        entity.velocity_x = 0
                        entity.rect.left = platform.rect.right

    def apply_collision_y(self):
        for platform in self.platforms:
            for entity in self.players + self.items:
                if entity.rect.colliderect(platform.rect):
                    platform.resonate()
                    if entity.velocity_y > 0: 
                        entity.velocity_y = 0
                        entity.rect.bottom = platform.rect.top
                        if isinstance(entity, Player):
                            entity.jump_left = 2
                    elif entity.velocity_y < 0:
                        entity.velocity_y = 0
                        entity.rect.top = platform.rect.bottom
                    if isinstance(entity, Cheese):
                        entity.velocity_x = 0

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
    
    def apply_gravity(self, ground_height):
        ground = WINDOW_HEIGHT - ground_height
        for entity in self.players + self.items:
            if entity.rect.bottom >= ground and entity.velocity_y > 0:
                entity.velocity_y = 0
                entity.rect.bottom = ground
                if isinstance(entity, Player):
                    entity.jump_left = 2
            else:
                entity.velocity_y += self.gravity
            
    def apply_skill(self):
        for skill in self.skills:
            skill.update_skill()
            if skill.active:
                for entity in self.players + self.platforms + self.items:
                    if skill.frames[skill.active_index].rect.colliderect(entity.rect) and entity not in skill.hit and entity != skill.user:
                        entity.take_damage(skill.damage)
                        skill.set_hit(entity)
            
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
        
        