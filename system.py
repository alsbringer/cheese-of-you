from entities import Player, Cheese, Platforms, Frame, Entity
from skill import Skill
from assets.config import WINDOW_HEIGHT, BACKGROUND_IMG, WINDOW_WIDTH
from utils import loadImage, setSize_W
from os.path import join
import pygame

class Database:
    def __init__(self):
        self.players: list[Player] = []
        self.platforms: list[Platforms] = []
        self.items: list[Cheese] = []
        self.skills: list[Skill] = []

    def register_entity(self, entity):
        if isinstance(entity, Player):
            self.players.append(entity)
            for skill in entity.skills:
                self.skills.append(skill)
        elif isinstance(entity, Cheese):
            self.items.append(entity)
        elif isinstance(entity, Platforms):
            self.platforms.append(entity)
    
    def register_skills(self):
            for player in self.players:
                if player.skills:
                    for skill in player.skills:
                        self.skills.append(skill)
    
    def get_entities(self):
        return self.players + self.items + self.platforms

class Environment:
    def __init__(self, database : Database, camera : CameraSystem, health : HealthSystem):
        self.health = health
        self.camera = camera
        self.gravity = 1
        self.database = database

    def apply_collision_x(self):
        for platform in self.database.platforms:
            for entity in self.database.players + self.database.items:
                if entity.rect.colliderect(platform.rect):
                    platform.resonate()
                    if entity.velocity_x > 0: 
                        entity.velocity_x = 0
                        entity.rect.right = platform.rect.left
                    elif entity.velocity_x < 0:
                        entity.velocity_x = 0
                        entity.rect.left = platform.rect.right

    def apply_collision_y(self):
        for platform in self.database.platforms:
            for entity in self.database.players + self.database.items:
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
        for platform in self.database.platforms:
            platform.update_color()
            
    def reset_platform(self):
        for platform in self.database.platforms:
            platform.reset_color()
            platform.calm()
        
    
    def apply_gravity(self, ground_height):
        ground = WINDOW_HEIGHT - ground_height
        for entity in self.database.players + self.database.items:
            if entity.rect.bottom >= ground and entity.velocity_y > 0:
                entity.velocity_y = 0
                entity.rect.bottom = ground
                if isinstance(entity, Player):
                    entity.jump_left = 2
            else:
                entity.velocity_y += self.gravity
            
    def apply_skill(self):
        for skill in self.database.skills:
            skill.update_skill()
            if skill.active:
                for entity in self.database.players + self.database.platforms + self.database.items:
                    if skill.frames[skill.active_index].rect.colliderect(entity.rect) and entity not in skill.hit and entity != skill.user:
                        entity.take_damage(skill.damage)
                        skill.set_hit(entity)
            
    def update_all(self):
            self.reset_platform()
            
            cam_target = None
            for entity in self.database.players + self.database.items:
                if entity.allow_update:
                    entity.update_x()
                    self.apply_collision_x()
                        
                    entity.update_y()
                    self.apply_collision_y()
                if isinstance(entity, Player): 
                    entity.update_carried_item()
                    if entity.name == "aglaea": cam_target = entity
    
            if cam_target: self.camera.update_camera(cam_target)

            self.update_platform()
                
    def draw_all(self,window):
        window.blit(BACKGROUND_IMG, (0 - int(self.camera.camera_x/10),0 - int(self.camera.camera_y/10)))
        for entity in self.database.get_entities():
            window.blit(entity.surface, (entity.rect.left - self.camera.camera_x, entity.rect.top - self.camera.camera_y))
            self.health.draw_self(target=entity, window=window, camera=self.camera)
        for effect in self.database.skills:
            if effect.active:
                current_frame = effect.frames[effect.active_index]
                window.blit(current_frame.surface, (current_frame.rect.left - self.camera.camera_x, current_frame.rect.top- self.camera.camera_y))
        
        
class CameraSystem:
    def __init__(self, target):
        self.camera_x = target.rect.centerx - WINDOW_WIDTH/2
        self.camera_y = target.rect.centery - WINDOW_HEIGHT/2 - 100
    
    def update_camera(self, target: Player):
        right_treshold = self.camera_x + WINDOW_WIDTH/2 + target.rect.width
        left_treshold = self.camera_x + WINDOW_WIDTH/2 - target.rect.width

        if target.rect.centerx > right_treshold :
            self.camera_x = target.rect.centerx - WINDOW_WIDTH/2 - target.rect.width

        elif target.rect.centerx < left_treshold:
            self.camera_x = target.rect.centerx - WINDOW_WIDTH/2  + target.rect.width
        self.camera_y = target.rect.centery - WINDOW_HEIGHT/2 - 100
        
    
class HealthSystem:
    def __init__(self):
        self.hp_frame_surf = loadImage(join("assets", "hp_bar", "hp_frame.png")).convert_alpha()
        self.hp_frame_rect = self.hp_frame_surf.get_rect()
        self.hp_bar_surf = loadImage(join("assets", "hp_bar", "blue_bar.png")).convert_alpha()
        self.hp_bar_rect = self.hp_bar_surf.get_rect()
        self.empty_bar_surf = loadImage(join("assets", "hp_bar", "empty_bar.png")).convert_alpha()
        self.container_height = 20
        self.container_width = 100
        self.container_surface = pygame.Surface((self.container_width,self.container_height), pygame.SRCALPHA)
        self.container_rect = self.container_surface.get_rect()
        
    def draw_self(self, target : Entity, window, camera : CameraSystem):
        self.container_rect.bottom = target.rect.top
        self.container_rect.centerx = target.rect.centerx
        
        # update
        current_hp_bar = int(target.current_hp/target.max_hp * self.container_width)
        
        for i in range(self.container_width):
            if i <= current_hp_bar: self.container_surface.blit(self.hp_bar_surf, (i,0))
            else: self.container_surface.blit(self.empty_bar_surf, (i, 0))
            
        self.hp_frame_surf = setSize_W(self.hp_frame_surf, self.container_width)        
        self.container_surface.blit(self.hp_frame_surf, (0,0))
        
        window.blit(self.container_surface, (self.container_rect.left-camera.camera_x, self.container_rect.top - camera.camera_y))
        