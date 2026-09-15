import pygame
from utils import flip_x
from skill import Skill

class Entity:
    def __init__(self, left, top, surface):
        self.surface = surface
        self.rect = self.surface.get_rect(topleft=(left, top))
        self.velocity_y = 0
        self.velocity_x = 0
        self.allow_update = True
    
    def update_x(self):
        if self.allow_update:
            self.rect.left += self.velocity_x
            
    def update_y(self):
        if self.allow_update:
            self.rect.top += self.velocity_y
        
    def disable_update(self):
        self.allow_update = False

    def enable_update(self):
        self.allow_update = True
        
class Platforms(Entity):
    def __init__(self, left, top, surface):
        super().__init__(left, top, surface)
        self.active = False
        
    def update_color(self):
        if self.active: pygame.draw.rect(self.surface, (255, 255, 255, 255), self.surface.get_rect(), width=2)
        else: pygame.draw.rect(self.surface, (0,0,0, 255), self.surface.get_rect(), width=2)

    def reset_color(self):
        self.surface.fill((0, 0, 0, 0))
    
    def resonate(self):
        self.active = True
        
    def calm(self):
        self.active = False
                
class Player(Entity):
    def __init__(self, name, left, top, surface):
        super().__init__(left, top, surface)
        self.current_state = "idle"
        self.name = name
        self.active_autopilot = False
        self.autopilot_items : list[Cheese] = []
        self.carried : Cheese= []
        self.max_carried = 2
        self.skills: list[Skill] = []
        self.states = {}
        
        self.THROW_POWER_Y = 4
        self.THROW_POWER_X = 6
                
        # jumping state
        self.JUMP_FORCE = -16
        self.jump_left = 2
                
        # direction state
        self.ACCELERATION = 1
        self.max_speed = 10
        self.face_direction = "right"
        self.prev_direction = "left"
        
        # for state (temporary)
        self.counter = -1 
        self.active_index = 0
        self.delay = 8
        
    def handle_input(self, keys):
        if keys[pygame.K_d]:
            self.velocity_x = min(self.max_speed, self.velocity_x + self.ACCELERATION)
            if self.face_direction != "right":
                self.face_direction = "right"
                self.prev_direction = "left" 
                self.surface = flip_x(self.surface)

        elif keys[pygame.K_a]:
            self.velocity_x = max(-self.max_speed, self.velocity_x - self.ACCELERATION)
            if self.face_direction != "left":
                self.prev_direction = "right"
                self.face_direction = "left"
                self.surface = flip_x(self.surface)
                
        else : self.velocity_x = 0
    
    def jump(self):
        if self.jump_left > 0:
            self.velocity_y = self.JUMP_FORCE
            self.jump_left -= 1
    
    # item
    def update_carried_item(self):
        if self.carried:
            for item in self.carried:
                item.rect.bottom = self.rect.top + int(item.rect.width/3)
                item.rect.centerx = self.rect.centerx
                
    def pick_item(self, item : Cheese):
        item.taken = True
        item.disable_update()
        self.carried.append(item)
    
    def throw_item(self):
        for item in self.carried:
            item.velocity_y = -self.THROW_POWER_Y + self.velocity_y
            if self.face_direction == "right":
                item.velocity_x = self.THROW_POWER_X + self.velocity_x
            else: item.velocity_x = -self.THROW_POWER_X + self.velocity_x
            item.taken = False
            item.enable_update()
        self.carried.clear()
    
    # autopilot
    def apply_autopilot(self, item_list):
        self.active_autopilot = not self.active_autopilot
        self.autopilot_items = item_list

    def autopilot(self, target : Player, gap):
        if(self.active_autopilot):
            self.THROW_POWER_Y = 10
            self.THROW_POWER_X = 10
            if target.velocity_y != 0:
                self.velocity_y = target.velocity_y
            # jika target gerak ke kanan
            if target.face_direction == "right" or target.velocity_x > 0:
                if (self.rect.left > target.rect.left): # jika self di kanan pindahkan ke belakang target
                    self.velocity_x = -self.max_speed
                elif ( self.rect.right <= target.rect.left - gap): # ikuti traget jika berada di depan
                    self.velocity_x  = target.velocity_x
                elif (self.rect.right >= target.rect.centerx) and (self.rect.right < target.rect.left ): # berhenti sampai menabrak target dan atur posisi dan jika target sebeumnya ada di kiri
                    self.velocity_x  = 0
                
            # jika target gerak ke kiri
            elif target.face_direction == "left" or target.velocity_x < 0:
                if (self.rect.right < target.rect.right):# jika self di kiri target
                    self.velocity_x = self.max_speed
                elif (self.rect.left >= target.rect.right + gap): # ikuti terget jika self sudah berada di depan
                    self.velocity_x  = target.velocity_x
                elif (self.rect.left < target.rect.centerx) and self.rect.left >= target.rect.right : # berhenti jika self kiri melewati tengah dan berada di kanan
                    self.velocity_x  = 0
                    
            # flip sesuai direction
            if self.velocity_x > 0 and self.face_direction != "right":
                self.face_direction = "right"
                self.surface = flip_x(self.surface)
                
            elif self.velocity_x < 0 and self.face_direction != "left":
                self.face_direction = "left"
                self.surface = flip_x(self.surface)
                   
            # take cheese automaticly
            for item in self.autopilot_items:
                if self.rect.colliderect(item.rect) and not item.taken:
                    self.pick_item(item)
        else:
            self.velocity_x = 0
            
            self.throw_item()
    
    #skill
    def add_skill(self, skill):
        self.skills.append(skill)
        
    def use_skill(self, skill_name):
        for skill in self.skills:
            if skill_name == skill.name:
                skill.cast_skill(self)
                return
        print("skill not found")
    
    #animation_state
    def add_state(self, state_name, state_frame):
        self.states.update({state_name: state_frame})
        
    def update_current_surf(self, status):
        if status in self.states:
            frames : list[Frame]= self.states[status]
            
            for frame in frames:
                if frame.face_direction != self.face_direction:
                    frame.surface = flip_x(frame.surface)
                    frame.face_direction = self.face_direction
                                    
            self.counter += 1
            if self.counter >= self.delay:
                self.counter = 0 # reset frame counter
                
                self.active_index = (self.active_index) % len(frames)
                self.surface = frames[self.active_index].surface
                self.active_index += 1
            
        else: print("status:", status, "not found")

        
class Cheese(Entity):
    def __init__(self, left, top, surface):
        super().__init__( left, top, surface)  
        self.facing_right = True
        self.taken = False
    
    def fade_on_approach(player_x, target_x, target_img):
        distance = target_x - player_x
        if distance <= 100:
            target_img.set_alpha(int(255 * distance / 100))
        else:
            target_img.set_alpha(255)

class Frame(Entity):
    def __init__(self, left, top, surface):
        super().__init__(left, top, surface)
        self.face_direction = "right"
    