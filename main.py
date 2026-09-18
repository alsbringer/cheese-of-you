from entities import Player, Cheese, Platforms, Frame
from skill import Skill
from system import Environment, Database, CameraSystem
import pygame
from os.path import join
from utils import setSize_W, loadImage, calc_align_right, calc_align_bottom
from assets.config import WINDOW_HEIGHT, WINDOW_WIDTH, BACKGROUND_IMG

pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# frame setup
#skill_slash
skill_paths = ["slash-0.png", "slash-1.png", "slash-2.png", "slash-3.png"]
skill_frames = []
for path in skill_paths:
    img = loadImage(join("assets", "sword", path)).convert_alpha()
    img = setSize_W(img, 100)
    skill_frames.append(Frame(left=0, top=0, surface=img))
basic_attack = Skill(type="slash", name="basic_attack", frames=skill_frames, delay=3)

#state
idle_paths = ["aglaea_idle_0001.png", "aglaea_idle_0002.png", "aglaea_idle_0003.png", "aglaea_idle_0004.png"]
idle_frames = []
for path in idle_paths:
    img = loadImage(join("assets", "aglaea", path)).convert_alpha()
    img = setSize_W(img, 100)
    idle_frames.append(Frame(left=0, top=0, surface=img))

walk_paths = ["aglaea_walk2_0001.png", "aglaea_walk2_0002.png", "aglaea_walk2_0003.png", "aglaea_walk2_0004.png"]
walk_frames = []
for path in walk_paths:
    img = loadImage(join("assets", "aglaea", path)).convert_alpha()
    img = setSize_W(img, 100)
    walk_frames.append(Frame(left=0, top=0, surface=img))


# --- Platform Setup ---
ground_height = 20
box0 = pygame.Surface((WINDOW_WIDTH, ground_height), pygame.SRCALPHA)
pygame.draw.rect(box0, (255, 255, 255), (0, 0, WINDOW_WIDTH, ground_height), width=2)
ground = Platforms(left=0, top=calc_align_bottom(WINDOW_HEIGHT, box0), surface=box0)

box1 = pygame.Surface((100,100), pygame.SRCALPHA)
pygame.draw.rect(box1, (0, 255, 0), (0, 0, 100,100), width=2)
platform1 = Platforms(left=calc_align_right(WINDOW_WIDTH, box1) - 100, top= calc_align_bottom(WINDOW_HEIGHT, box1) - ground_height, surface=box1 )

box2 = pygame.Surface((100,100), pygame.SRCALPHA)
pygame.draw.rect(box2, (0, 255, 0), (0, 0, 100,100), width=2)
platform2 = Platforms(left=calc_align_right(WINDOW_WIDTH, box2) - 400, top= calc_align_bottom(WINDOW_HEIGHT, box2) - ground_height, surface=box2 )

# --- Player Setup ---
aglaea_surf_init = loadImage(join("assets","aglaea","aglaea_idle_0001.png")).convert_alpha()
aglaea_surf_init = setSize_W(aglaea_surf_init, 100)
aglaea_top_init = WINDOW_HEIGHT - aglaea_surf_init.get_height() - ground_height
aglaea = Player( name="aglaea", left = 20,  top= aglaea_top_init, surface=aglaea_surf_init)
aglaea.add_skill(basic_attack)
aglaea.add_state(state_name="idle", state_frame=idle_frames)
aglaea.add_state(state_name="walking", state_frame=walk_frames)

caelus_suf = loadImage(join("assets","caelus","caelus_idle.png")).convert_alpha()
caelus_suf = setSize_W(caelus_suf, 100)
caelus_top = WINDOW_HEIGHT - caelus_suf.get_height() - ground_height
caelus = Player( name="caelus", left = 0,  top= caelus_top, surface=caelus_suf)

# --- Cheese Setup ---
cheese_initial_img = loadImage(join("assets","cheese.png")).convert_alpha()
cheese_initial_img = setSize_W(cheese_initial_img, 40)
cheese_initial_top = calc_align_bottom(WINDOW_HEIGHT, cheese_initial_img)
cheese_initial_left = calc_align_right(WINDOW_WIDTH, cheese_initial_img) - cheese_initial_img.get_width()
cheese = Cheese(top=cheese_initial_top, left=cheese_initial_left, surface=cheese_initial_img)

# --- environment setup ==
db = Database()
cam = CameraSystem(aglaea)
db.register_entity(aglaea)
db.register_entity(caelus)
db.register_entity(ground)
db.register_entity(platform1)
db.register_entity(platform2)
db.register_entity(cheese)
env = Environment(db, cam)
print(f"registrasi result:\n player: {env.database.players}\n platform: {env.database.platforms} \n items: {env.database.items}")

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
                caelus.apply_autopilot(env.database.items)
            if event.key == pygame.K_f:
                if aglaea.rect.colliderect(cheese.rect):
                    if len(aglaea.carried) > 0:
                        aglaea.throw_item()
                    else: aglaea.pick_item(cheese)
            if event.key == pygame.K_k:
                aglaea.use_skill("basic_attack")
    
    keys = pygame.key.get_pressed()
    aglaea.handle_input(keys)
    caelus.autopilot(lover=aglaea, gap=10)
    
#==============================================PHYSICS==============================================
    aglaea.update_current_surf(aglaea.current_state)
    
    env.apply_gravity(ground_height)
    env.apply_skill()
    
    
    env.update_all()
    env.display_all(display)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()