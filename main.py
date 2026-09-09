import pygame
from os.path import join

# Blue Print
class Environment:
    def __init__(self):
        self.gravity = 1
        self.players: list[Player] = []
        self.platforms: list[Platforms] = []
    
    def register_player(self, player):
        self.players.append(player)
        
    def register_platform(self, platforms):
        self.platforms.append(platforms)
        
    def apply_gravity(self):
        for player in self.players:
            if player.rect.bottom >= WINDOW_HEIGHT:
                player.velocity_y = 0
                player.rect.bottom = WINDOW_HEIGHT - ground_height
            else:
                player.velocity_y += self.gravity
                
    def activate_gravity(self):
        self.gravity_active = True
            
    def apply_collision_x(self, player_name):
        for player in self.players:
            if player.name == player_name:                
                for platform in self.platforms:
                    if player.rect.colliderect(platform.rect):
                        platform.surface.fill((0, 0, 0, 0))
                        pygame.draw.rect(platform.surface, (255, 255, 255, 255), platform.surface.get_rect(), width=2)
                        if player.velocity_x > 0: 
                            player.velocity_x = 0
                            player.rect.right = platform.rect.left
                        elif player.velocity_x < 0:
                            player.velocity_x = 0
                            player.rect.left = platform.rect.right
                        
    def apply_collision_y(self, player_name):
        for player in self.players:
            if player.name == player_name:                
                for platform in self.platforms:
                    if player.rect.colliderect(platform.rect):
                        platform.surface.fill((0, 0, 0, 0))
                        pygame.draw.rect(platform.surface, (255, 255, 255, 255), platform.surface.get_rect(), width=2)
                        if player.velocity_y > 0: 
                            player.velocity_y = 0
                            player.rect.bottom = platform.rect.top
                            player.jump_left = 2
                        elif player.velocity_y < 0:
                            player.velocity_y = 0
                            player.rect.top = platform.rect.bottom

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

    
class Platforms(Entity):
    def __init__(self, left, top, surface):
        super().__init__(left, top, surface)
                
class Player(Entity):
    def __init__(self, name, left, top, surface):
        super().__init__(left, top, surface)
        self.name = name
        
        # jumping state
        self.JUMP_FORCE = -16
        self.jump_left = 2
                
        # direction state
        self.move_speed = 10
        self.face_direction = "right"
        
    def handle_input(self, keys):
        self.velocity_x = 0
        if keys[pygame.K_d]:
            self.velocity_x = self.move_speed
            if self.face_direction != "right":
                self.face_direction = "right"
                aglaea.surface = flip_x(aglaea.surface)
        elif keys[pygame.K_a]:
            self.velocity_x = -self.move_speed
            if self.face_direction != "left":
                aglaea.face_direction = "left"
                aglaea.surface = flip_x(aglaea.surface)
    
    def jump(self):
        if self.jump_left > 0:
            self.velocity_y = self.JUMP_FORCE
            self.jump_left -= 1
    
    def update_x(self):
        self.rect.left += self.velocity_x
        
    def update_y(self):
        self.rect.top += self.velocity_y
        
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
aglaea_left_init = 0
aglaea = Player( name="aglaea", left = aglaea_left_init,  top= aglaea_top_init, surface=aglaea_surf_init)


# --- Cheese Setup ---
cheese_initial_img = loadImage(join("assets","cheese.png")).convert_alpha()
cheese_initial_img = setSize_W(cheese_initial_img, 40)
cheese_initial_top = calc_align_bottom(cheese_initial_img)
cheese_initial_left = calc_align_right(cheese_initial_img) - cheese_initial_img.get_width()
cheese = Cheese(top=cheese_initial_top, left=cheese_initial_left, surface=cheese_initial_img)

# --- environment setup ==
env = Environment()
env.register_player(aglaea)
env.register_platform(ground)
env.register_platform(platform1)
env.register_platform(platform2)


# --- Main Loop ---
running = True
while running:
    print("aglaea velocity:", aglaea.velocity_y )
    print("aglaea coordinate:", aglaea.rect.top )
#===============================================INPUT==============================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                aglaea.jump()
            if event.key == pygame.K_f:
                if (
                    aglaea.rect.right >= cheese.rect.left and aglaea.rect.right <= cheese.rect.right
                    or aglaea.rect.left >= cheese.rect.left and aglaea.rect.left <= cheese.rect.right 
                    ):
                    if cheese.taken: cheese.taken = False
                    else: cheese.taken = True
    
    keys = pygame.key.get_pressed()
    aglaea.handle_input(keys)
    
#==============================================PHYSICS==============================================
    env.apply_gravity()
    env.draw_platform(color=(0, 0, 0, 255))
    aglaea.update_x()
    env.apply_collision_x(aglaea.name)
    aglaea.update_y()
    env.apply_collision_y(aglaea.name)
        
# SECTION(RENDER)
    display.blit(BACKGROUND_IMG, (0,0))
    display.blit(aglaea.surface, (aglaea.rect.left, aglaea.rect.top))
    display.blit(ground.surface, (ground.rect.left, ground.rect.top))
    display.blit(platform1.surface, (platform1.rect.left, platform1.rect.top))
    display.blit(platform2.surface, (platform2.rect.left, platform2.rect.top))
    
    # cheese render
    if cheese.taken:
        if aglaea.face_direction =="right":
            cheese.rect.left = aglaea.rect.right - 40
            cheese.rect.top = aglaea.rect.bottom - 40
            display.blit(cheese.surface, (cheese.rect.left, cheese.rect.top))
        if aglaea.face_direction == "left":
            cheese.rect.left = aglaea.rect.left
            cheese.rect.top = aglaea.rect.bottom - 40
            display.blit(cheese.surface, (cheese.rect.left, cheese.rect.top))
    else:
        cheese.rect.top = calc_align_bottom(cheese.surface)
        display.blit(cheese.surface, (cheese.rect.left, cheese.rect.top))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()