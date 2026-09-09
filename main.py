import pygame
from os.path import join

# Blue Print
class Entity:
    def __init__(self, left, top, img):
        self.left = left
        self.top = top
        self.height = img.get_height()
        self.width = img.get_width()
        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.img = img
    
class Platforms(Entity):
    def __init__(self, left, top, img):
        super().__init__(left, top, img)
                
class Player(Entity):
    def __init__(self, left, top, img):
        super().__init__(left, top, img)
        
        # direction state
        self.move_speed = 10
        self.jump_speed = 10
        self.fall_speed = 20
        self.face_direction = "right"
        self.forward_blocked = False
        self.backward_blocked = False
        # jumping state
        self.jumping = False
        self.jumping_direction = "down"
        self.can_jump = True
        self.can_double_jump = False
        self.jump_height = 100
        self.extra_jump_height = 0
        # ground state
        self.player_ground = self.bottom
        self.on_platform = False
        self.starting_ground = self.bottom

class Cheese(Entity):
    def __init__(self, left, top, img):
        super().__init__( left, top, img)  
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

def calc_align_right(image):
    return WINDOW_WIDTH - image.get_width()

def calc_align_bottom(image):
    return WINDOW_HEIGHT - image.get_height()

def flip_x(image):
    return pygame.transform.flip(image, True, False)

def flip_y(image):
    return pygame.transform.flip(image, False, True)

def flip_xy(image):
    return pygame.transform.flip(image, True, True)

def fade_on_approach(player_x, target_x, target_img):
    distance = target_x - player_x
    if distance <= 100:
        target_img.set_alpha(int(255 * distance / 100))
    else:
        target_img.set_alpha(255)


# --- Environtment Setup ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
BACKGROUND_IMG = loadImage(join("assets","amphoreus.png"))
BACKGROUND_IMG = setSize_W(BACKGROUND_IMG, 1000)
WIDTH_MARGIN = 20
HEIGHT_MARGIN = 34

pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# --- Avatar Setup ---
aglaea_initial_img = loadImage(join("assets","aglaea","agy-1.jpe")).convert_alpha()
aglaea_initial_img = setSize_W(aglaea_initial_img, 100)
aglaea_initial_top = WINDOW_HEIGHT-aglaea_initial_img.get_height()
aglaea_initial_left = 0
aglaea = Player( top= aglaea_initial_top ,left = aglaea_initial_left , img=aglaea_initial_img)

caelus_initial_img = loadImage(join("assets","caelus","caelus-2.jpe")).convert_alpha()
caelus_initial_img = setSize_W(caelus_initial_img, 100)
caelus_initial_top = WINDOW_HEIGHT-caelus_initial_img.get_height()
caelus_initial_left = 0
caelus = Player( top= caelus_initial_top ,left = caelus_initial_left , img=caelus_initial_img)

# --- Cheese Setup ---
cheese_initial_img = loadImage(join("assets","cheese.png")).convert_alpha()
cheese_initial_img = setSize_W(cheese_initial_img, 40)
cheese_initial_top = calc_align_bottom(cheese_initial_img)
cheese_initial_left = calc_align_right(cheese_initial_img) - cheese_initial_img.get_width()
cheese = Cheese(top=cheese_initial_top, left=cheese_initial_left, img=cheese_initial_img)

# --- Firewall Setup ---
firewall_initial_img = loadImage("assets/firewall.png").convert_alpha()
firewall_initial_img = setSize_WH(firewall_initial_img, 100, 200)
firewall_initial_left = calc_align_right(firewall_initial_img) - 400
firewall_initial_top = int(calc_align_bottom(firewall_initial_img) + firewall_initial_img.get_height() / 3)
firewall = Platforms(left= firewall_initial_left, top= firewall_initial_top, img=firewall_initial_img)


# --- Main Loop ---
running = True
while running:
    prev_ground = aglaea.player_ground
    keys = pygame.key.get_pressed()

#SECTION: STATE_&_INPUT_MANAGEMENT
    # Logic(close game, jump_permission, double_jump_permission, cheese_taken_state);
    # Input(QUIT, SPACE, F);
    # Log(jump coordinate, double jump coordinate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("can_jump:", aglaea.can_jump)
                if aglaea.can_double_jump and not aglaea.can_jump:
                    print("second jump at", aglaea.bottom)
                    aglaea.jumping_direction = "up"
                    aglaea.extra_jump_height += 80
                    aglaea.can_double_jump = False
                elif aglaea.can_jump:
                    aglaea.jumping = True
                    aglaea.jumping_direction = "up"
                    aglaea.can_jump = False
                    aglaea.can_double_jump = True
                    print("Jumping:", aglaea.jumping, "at", aglaea.bottom)
                    aglaea.starting_ground = aglaea.player_ground
            if event.key == pygame.K_f:
                if (
                    aglaea.right >= cheese.left and aglaea.right <= cheese.right
                    or aglaea.left >= cheese.left and aglaea.left <= cheese.right 
                    ):
                    if cheese.taken: cheese.taken = False
                    else: cheese.taken = True
    # Logic(move foreward, move backward, flip direction)
    # Input(D, A)
    if keys[pygame.K_d]:
        if not aglaea.forward_blocked:
            aglaea.left += aglaea.move_speed
            if aglaea.face_direction != "right":
                aglaea.face_direction = "right"
                aglaea.img = flip_x(aglaea.img)
        # else: print("forward Blocked"
    if keys[pygame.K_a] and not aglaea.backward_blocked:
        aglaea.left -= aglaea.move_speed
        if aglaea.face_direction != "left":
            aglaea.face_direction = "left"
            aglaea.img = flip_x(aglaea.img)
    
    # Logic(collision blocking)
    if (
        (aglaea.right >= firewall.left + int(firewall.width / 2) - WIDTH_MARGIN)   
        and 
        (aglaea.right <= firewall.left + int(firewall.width / 2) + WIDTH_MARGIN)
        and 
        (aglaea.bottom > firewall.top + HEIGHT_MARGIN)
        ):
        aglaea.forward_blocked = True
    else:
        aglaea.forward_blocked = False    
    if (
        (aglaea.left >= firewall.left + int(firewall.width / 2) - WIDTH_MARGIN )
        and 
        (aglaea.left <= firewall.left + int(firewall.width / 2) + WIDTH_MARGIN)
        and
        (aglaea.bottom > firewall.top + HEIGHT_MARGIN)
        ):
        aglaea.backward_blocked = True
    else:
        aglaea.backward_blocked = False

    # Logic(ground to firewall)
    if (aglaea.bottom <= firewall.top + HEIGHT_MARGIN
        and aglaea.right >= firewall.left
        and aglaea.left <= firewall.right):
        aglaea.on_platform = True
        aglaea.player_ground = firewall.top + HEIGHT_MARGIN
    else:
        aglaea.on_platform = False
    # Logic(firewall to ground)
    if not aglaea.on_platform:
        aglaea.player_ground = WINDOW_HEIGHT
    if aglaea.player_ground != prev_ground:
        print("ground berubah")
        print("on platform", aglaea.on_platform)
        if not aglaea.on_platform and not aglaea.jumping:
            print("guing_up false")
            aglaea.jumping = True
            aglaea.jumping_direction = "down"
    # Log(ground changing)
    if aglaea.player_ground != prev_ground:
        print("prev ground: ", prev_ground)
        print("current ground ", aglaea.player_ground)

    # Logic(update postition)
    # Log(foot coordinate)
    aglaea.right = aglaea.left + aglaea.width
    if aglaea.jumping:
        # start jumping
        if aglaea.jumping_direction == "up":
            aglaea.bottom -= aglaea.jump_speed
            aglaea.top = aglaea.bottom - aglaea.height
            print("going up: ", aglaea.bottom)
        # reach maxiimun
        elif aglaea.jumping_direction == "down" and aglaea.bottom < aglaea.player_ground:
            print("going down: ", aglaea.bottom)
            aglaea.bottom += aglaea.fall_speed
            aglaea.top = aglaea.bottom - aglaea.height
        # reach the ground === makes stay
        if aglaea.bottom >= aglaea.player_ground:
            aglaea.jumping = False
            aglaea.can_jump = True
            print("on the ground: ", aglaea.bottom)
            aglaea.can_double_jump = False
            aglaea.extra_jump_height = 0
        #fall switch === makes fall permission
        if aglaea.starting_ground - aglaea.bottom >= (aglaea.jump_height + aglaea.extra_jump_height) and aglaea.jumping_direction == "up":
            print("fall at", aglaea.bottom)
            print("jump height:", aglaea.jump_height+ aglaea.extra_jump_height)
            aglaea.jumping_direction = "down"
            
# SECTION(RENDER)
    display.blit(BACKGROUND_IMG, (0,0))
    display.blit(caelus.img, (caelus.left,caelus.top))
    # firewall & avatar render
    if aglaea.right <= (firewall.right - firewall.width/2): 
        print("aglaea on top")
        sprites = [
            (firewall.img, firewall.left, firewall.top),
            (aglaea.img, aglaea.left, aglaea.top),
        ] 
    else:
        print("aglaea on the bottom")
        sprites = [
            (aglaea.img, aglaea.left, aglaea.top),
            (firewall.img, firewall.left, firewall.top),
        ]
        print(sprites)
    for sprite_img, sprite_x, sprite_y in sprites:
        display.blit(sprite_img, (sprite_x, sprite_y))
    
    # cheese render
    if cheese.taken:
        if aglaea.face_direction =="right":
            cheese.left = aglaea.right - 40
            cheese.top = aglaea.bottom - 40
            display.blit(cheese.img, (cheese.left, cheese.top))
        if aglaea.face_direction == "left":
            cheese.left = aglaea.left
            cheese.top = aglaea.bottom - 40
            display.blit(cheese.img, (cheese.left, cheese.top))
    else:
        cheese.top = calc_align_bottom(cheese.img)
        display.blit(cheese.img, (cheese.left, cheese.top))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()