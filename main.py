import pygame
from os.path import join

# Blue Print
class Environment:
    def __init__(self):
        self.gravity = 1
        self.players: list[Player] = []
        self.platforms: list[Platforms] = []
        self.items: list[Cheese] = []
        self.collide_items: list[Entity] = []
    
    def register_player(self, player):
        self.players.append(player)
        self.collide_items.append(player)
        
    def register_platform(self, platforms):
        self.platforms.append(platforms)
        
    def register_item(self, item):
        self.items.append(item)
        self.collide_items.append(cheese)
        
    def apply_gravity(self):
        for entity in self.players + self.items:
            if entity.rect.bottom >= WINDOW_HEIGHT:
                entity.velocity_y = 0
                entity.rect.bottom = WINDOW_HEIGHT - ground_height
            else:
                entity.velocity_y += self.gravity
            
    def apply_collision_x(self):
        for item in self.collide_items:
                for platform in self.platforms:
                    if item.rect.colliderect(platform.rect):
                        platform.surface.fill((0, 0, 0, 0))
                        pygame.draw.rect(platform.surface, (255, 255, 255, 255), platform.surface.get_rect(), width=2)
                        if item.velocity_x > 0: 
                            item.velocity_x = 0
                            item.rect.right = platform.rect.left
                            
                        elif item.velocity_x < 0:
                            item.velocity_x = 0
                            item.rect.left = platform.rect.right
                            
                           
                        
    def apply_collision_y(self):
        for item in self.collide_items:
                for platform in self.platforms:
                    if item.rect.colliderect(platform.rect):
                        platform.surface.fill((0, 0, 0, 0))
                        pygame.draw.rect(platform.surface, (255, 255, 255, 255), platform.surface.get_rect(), width=2)
                        if item.velocity_y > 0: 
                            item.velocity_y = 0
                            item.rect.bottom = platform.rect.top
                            if isinstance(item, Player):
                                item.jump_left = 2
                        elif item.velocity_y < 0:
                            item.velocity_y = 0
                            item.rect.top = platform.rect.bottom
                            
                        if isinstance(item, Cheese):
                            print("cheese collide ground")
                            item.velocity_x = 0
        

    def draw_platform(self, color):
        for platform in self.platforms:
            platform.surface.fill((0, 0, 0, 0))
            pygame.draw.rect(platform.surface, (color), platform.surface.get_rect(), width=2)
            
class Entity:
    def __init__(self, left, top, surface):
        self.surface = surface
        self.rect = self.surface.get_rect(topleft=(left, top))
        self.velocity_y = 0
        self.velocity_x = 0
        
    def update_x(self):
            self.rect.left += self.velocity_x
            
    def update_y(self):
        self.rect.top += self.velocity_y

    
class Platforms(Entity):
    def __init__(self, left, top, surface):
        super().__init__(left, top, surface)
                
class Player(Entity):
    def __init__(self, name, left, top, surface):
        super().__init__(left, top, surface)
        self.name = name
        self.active_autopilot = False
        self.carried = []
        self.max_carried = 2
        
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
        
    def handle_input(self, keys):
        if keys[pygame.K_d]:
            self.velocity_x = min(self.max_speed, self.velocity_x + self.ACCELERATION)
            if self.face_direction != "right":
                self.face_direction = "right"  #ciptakan momentum dimana prev dan face direction sama (mengindikasikan perubahan)
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
    
    
        
    def update_carried_item(self):
        if self.carried:
            for item in self.carried:
                item.rect.bottom = self.rect.top + int(item.rect.width/3)
                item.rect.centerx = self.rect.centerx
                
    def pick_item(self, item):
        item.taken = True
        self.carried.append(item)
    
    def throw_item(self):
        for item in self.carried:
            item.velocity_y = -self.THROW_POWER_Y + self.velocity_y
            if self.face_direction == "right":
                item.velocity_x = self.THROW_POWER_X + self.velocity_x
            else: item.velocity_x = -self.THROW_POWER_X + self.velocity_x
            
            item.taken = False
        self.carried.clear()
        
        
    def apply_autopilot(self):
        self.active_autopilot = not self.active_autopilot

        
    def autopilot(self, target : Player, gap):
        if(self.active_autopilot):
            if target.velocity_y != 0:
                self.velocity_y = target.velocity_y
            # jika target gerak ke kanan
            if target.face_direction == "right" or target.velocity_x > 0:
                if (self.rect.left > target.rect.left): # jika self di depan pindahkan ke belakang target
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
        else:
            self.velocity_x = 0
            
        
        
        if self.velocity_x > 0 and self.face_direction != "right":
            self.face_direction = "right"
            self.surface = flip_x(self.surface)
            
        elif self.velocity_x < 0 and self.face_direction != "left":
            self.face_direction = "left"
            self.surface = flip_x(self.surface)
            
            
    
        
class Cheese(Entity):
    def __init__(self, left, top, surface):
        super().__init__( left, top, surface)  
        # direction
        self.facing_right = True
        # state
        self.taken = False

# --- Utility Functions ---
def setSize_W(image, width): 
    w, h = image.get_size()
    ratio = w / h
    height = int(width / ratio)
    return pygame.transform.scale(image, (width, height))

def setSize_WH(image, width, height):
    return pygame.transform.scale(image, (width, height))

def loadImage(path):
    return pygame.image.load(path)

def calc_align_right(surface):
    return WINDOW_WIDTH - surface.get_width()

def calc_align_bottom(surfce):
    return WINDOW_HEIGHT - surfce.get_height()

def flip_x(surface):
    return pygame.transform.flip(surface, True, False)

def flip_y(surface):
    return pygame.transform.flip(surface, False, True)

def flip_xy(surface):
    return pygame.transform.flip(surface, True, True)

def fade_on_approach(player_x, target_x, target_img):
    distance = target_x - player_x
    if distance <= 100:
        target_img.set_alpha(int(255 * distance / 100))
    else:
        target_img.set_alpha(255)



WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
BACKGROUND_IMG = loadImage(join("assets","amphoreus.png"))
BACKGROUND_IMG = setSize_W(BACKGROUND_IMG, 1000)
WIDTH_MARGIN = 20
HEIGHT_MARGIN = 34

pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# --- Platform Setup ---
ground_height = 20
box0 = pygame.Surface((WINDOW_WIDTH, ground_height), pygame.SRCALPHA)
pygame.draw.rect(box0, (255, 255, 255), (0, 0, WINDOW_WIDTH, ground_height), width=4)
ground = Platforms(left=0, top=calc_align_bottom(box0), surface=box0)

box1 = pygame.Surface((100,100), pygame.SRCALPHA)
pygame.draw.rect(box1, (0, 255, 0), (0, 0, 100,100), width=2)
platform1 = Platforms(left=calc_align_right(box1) - 100, top= calc_align_bottom(box1) - ground_height, surface=box1 )

box2 = pygame.Surface((100,100), pygame.SRCALPHA)
pygame.draw.rect(box2, (0, 255, 0), (0, 0, 100,100), width=2)
platform2 = Platforms(left=calc_align_right(box2) - 400, top= calc_align_bottom(box2) - ground_height, surface=box2 )

# --- Player Setup ---
aglaea_surf_init = loadImage(join("assets","aglaea","agy-1.jpe")).convert_alpha()
aglaea_surf_init = setSize_W(aglaea_surf_init, 100)
aglaea_top_init = WINDOW_HEIGHT - aglaea_surf_init.get_height() - ground_height
aglaea = Player( name="aglaea", left = 20,  top= aglaea_top_init, surface=aglaea_surf_init)

caelus_suf = loadImage(join("assets","caelus","caelus-0.jpe")).convert_alpha()
caelus_suf = setSize_W(caelus_suf, 100)
caelus_top = WINDOW_HEIGHT - caelus_suf.get_height() - ground_height
caelus = Player( name="aglaea", left = 0,  top= caelus_top, surface=caelus_suf)

# --- Cheese Setup ---
cheese_initial_img = loadImage(join("assets","cheese.png")).convert_alpha()
cheese_initial_img = setSize_W(cheese_initial_img, 40)
cheese_initial_top = calc_align_bottom(cheese_initial_img)
cheese_initial_left = calc_align_right(cheese_initial_img) - cheese_initial_img.get_width()
cheese = Cheese(top=cheese_initial_top, left=cheese_initial_left, surface=cheese_initial_img)

# --- environment setup ==
env = Environment()
env.register_player(aglaea)
env.register_player(caelus)
env.register_platform(ground)
env.register_platform(platform1)
env.register_platform(platform2)
env.register_item(cheese)


# --- Main Loop ---
running = True
while running:
#===============================================INPUT==============================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                aglaea.jump()
            if event.key == pygame.K_p:
                caelus.apply_autopilot()
            if event.key == pygame.K_f:
                if aglaea.rect.colliderect(cheese.rect):
                    if len(aglaea.carried) > 0:
                        aglaea.throw_item()
                    else: aglaea.pick_item(cheese)
    
    keys = pygame.key.get_pressed()
    aglaea.handle_input(keys)
    
        
        
    caelus.autopilot(aglaea, 10)
    
#==============================================PHYSICS==============================================
    env.apply_gravity()
    env.draw_platform(color=(0, 0, 0, 255))
    
    if not cheese.taken: cheese.update_x()
    aglaea.update_x()
    caelus.update_x()
    env.apply_collision_x()
    
    print("Velocity_X cheese", cheese.velocity_x)
    
    if not cheese.taken: cheese.update_y()
    aglaea.update_y()
    caelus.update_y()
    env.apply_collision_y()
    
    if cheese.taken: aglaea.update_carried_item()
    
    
    
# SECTION(RENDER)
    display.blit(BACKGROUND_IMG, (0,0))
    display.blit(aglaea.surface, (aglaea.rect.left, aglaea.rect.top))
    display.blit(caelus.surface, (caelus.rect.left, caelus.rect.top))
    display.blit(ground.surface, (ground.rect.left, ground.rect.top))
    display.blit(platform1.surface, (platform1.rect.left, platform1.rect.top))
    display.blit(platform2.surface, (platform2.rect.left, platform2.rect.top))
    
    
    display.blit(cheese.surface, cheese.rect)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()