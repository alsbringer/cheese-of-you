from entities import Player, Cheese, Platforms
import pygame
from config import WINDOW_HEIGHT, WINDOW_WIDTH, BACKGROUND_IMG

class Environment:
    def __init__(self):
        self.gravity = 1
        self.players: list[Player] = []
        self.platforms: list[Platforms] = []
        self.items: list[Cheese] = []

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
            
    def apply_collision_x(self):
        for platform in self.platforms:
            platform.active = False
            for item in self.players + self.items:
                if item.rect.colliderect(platform.rect):
                    platform.active = True
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
                    platform.active = True
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
            platform.update_appearance()
            
    def reset_platform(self):
        for platform in self.platforms:
            platform.reset_appearance()