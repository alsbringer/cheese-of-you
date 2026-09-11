from entities import Player, Cheese, Platforms, Frame
from effect import Effect
from environment import Environment
import pygame
from os.path import join
from utils import setSize_W, loadImage, calc_align_right, calc_align_bottom
from config import WINDOW_HEIGHT, WINDOW_WIDTH, BACKGROUND_IMG

pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# frame setup
slash_0 = loadImage(join("assets", "sword", "slash-0.png")).convert_alpha()
slash_0 = setSize_W(slash_0, 100)
slash_1 = loadImage(join("assets", "sword", "slash-1.png")).convert_alpha()
slash_1 = setSize_W(slash_1, 100)
slash_2 = loadImage(join("assets", "sword", "slash-2.png")).convert_alpha()
slash_2 = setSize_W(slash_2, 100)
slash_3 = loadImage(join("assets", "sword", "slash-3.png")).convert_alpha()
slash_3 = setSize_W(slash_3, 100)
slash_images = [slash_0, slash_1, slash_2, slash_3]
slash_rect = []
for image in slash_images:
    slash_rect_temp = Frame(left=0, top=0, surface=image)
    slash_rect.append(slash_rect_temp)
slash_effect = Effect(type="slash", frames=slash_rect, delay=3)

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
cheese_initial_top = calc_align_bottom(WINDOW_HEIGHT, cheese_initial_img)
cheese_initial_left = calc_align_right(WINDOW_WIDTH, cheese_initial_img) - cheese_initial_img.get_width()
cheese = Cheese(top=cheese_initial_top, left=cheese_initial_left, surface=cheese_initial_img)

# --- environment setup ==
env = Environment()
env.register_entity(aglaea)
env.register_entity(caelus)
env.register_entity(ground)
env.register_entity(platform1)
env.register_entity(platform2)
env.register_entity(cheese)
env.register_effect(slash_effect)


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
                caelus.apply_autopilot(env.items)
            if event.key == pygame.K_f:
                if aglaea.rect.colliderect(cheese.rect):
                    if len(aglaea.carried) > 0:
                        aglaea.throw_item()
                    else: aglaea.pick_item(cheese)
            if event.key == pygame.K_k:
                for effect in env.effects:
                    if  effect.type == "slash":
                        effect.start_effect(aglaea)
    
    keys = pygame.key.get_pressed()
    aglaea.handle_input(keys)
    caelus.autopilot(target=aglaea, gap=10)
    
#==============================================PHYSICS==============================================
    env.reset_platform()
    env.apply_gravity(ground_height)
    env.apply_effects()
    env.update_position()
    env.update_platform()
    
# SECTION(RENDER)
    display.blit(BACKGROUND_IMG, (0,0))
    display.blit(aglaea.surface, (aglaea.rect.left, aglaea.rect.top))
    display.blit(caelus.surface, (caelus.rect.left, caelus.rect.top))
    display.blit(ground.surface, (ground.rect.left, ground.rect.top))
    display.blit(platform1.surface, (platform1.rect.left, platform1.rect.top))
    display.blit(platform2.surface, (platform2.rect.left, platform2.rect.top))
    env.display_effect(display)
    
    
    display.blit(cheese.surface, cheese.rect)
    pygame.display.update()
    clock.tick(60)

pygame.quit()