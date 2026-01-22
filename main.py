import pygame
import random
import os
import math 

# --- 1. SETUP ---
pygame.init()
pygame.mixer.init()

# GET MONITOR SIZE
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Set Fullscreen Mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Endless Runner: LEGENDARY EDITION")
clock = pygame.time.Clock()

# --- DYNAMIC CONSTANTS ---
PLAYER_SIZE = 130       
OBSTACLE_SIZE = 130     
BOSS_SIZE = 250         

# Ground Tuner
GROUND_HEIGHT = 85     
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT
PLAYER_START_Y = GROUND_Y - PLAYER_SIZE 

# Physics
GRAVITY = 1.8           
JUMP_STRENGTH = -30     
START_SPEED = 12        
DASH_SPEED_BOOST = 12 
DASH_DURATION = 20   
DASH_COOLDOWN = 120
FIRE_COOLDOWN_MAX = 45 

# Fonts
font = pygame.font.Font(None, 60)         
title_font = pygame.font.Font(None, 120) 
shop_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 50)
damage_font = pygame.font.Font(None, 70) 

# --- 2. ASSETS ---
game_folder = os.path.dirname(__file__)
highscore_file = os.path.join(game_folder, "highscore.txt")
coins_file = os.path.join(game_folder, "coins.txt")
shop_file = os.path.join(game_folder, "shop.txt") 

# Load Images
using_images = False 
player_frames = []      
player_gold_frames = [] 
enemy_frames = []
boss_assets = [[], [], []] 
bird_frames = []
coin_frames = [] 
boss_bullet_frames = [] 
sting_frames = [] 

try:
    # --- PLAYER ---
    for i in range(1, 6): 
        filename = f"player_walk{i}.png"
        path = os.path.join(game_folder, filename)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (PLAYER_SIZE, PLAYER_SIZE))
            player_frames.append(img)

    for i in range(1, 6): 
        filename = f"player_gold_walk{i}.png"
        path = os.path.join(game_folder, filename)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (PLAYER_SIZE, PLAYER_SIZE))
            player_gold_frames.append(img)
    
    # --- ENEMY ---
    for i in range(1, 9): 
        filename = f"enemy{i}.png"
        path = os.path.join(game_folder, filename)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (OBSTACLE_SIZE, OBSTACLE_SIZE))
            enemy_frames.append(img)
    if len(enemy_frames) == 0 and os.path.exists(os.path.join(game_folder, "enemy.png")):
        img = pygame.image.load(os.path.join(game_folder, "enemy.png")).convert_alpha()
        img = pygame.transform.scale(img, (OBSTACLE_SIZE, OBSTACLE_SIZE))
        enemy_frames.append(img)

    # --- BOSSES ---
    # Boss 1
    if os.path.exists(os.path.join(game_folder, "boss1.png")):
        img = pygame.image.load(os.path.join(game_folder, "boss1.png")).convert_alpha()
        boss_assets[0].append(pygame.transform.scale(img, (BOSS_SIZE, BOSS_SIZE)))
    elif os.path.exists(os.path.join(game_folder, "boss.png")):
        img = pygame.image.load(os.path.join(game_folder, "boss.png")).convert_alpha()
        boss_assets[0].append(pygame.transform.scale(img, (BOSS_SIZE, BOSS_SIZE)))

    # Boss 2 (Animation)
    for i in range(1, 4):
        fname = f"boss2_{i}.png"
        path = os.path.join(game_folder, fname)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            boss_assets[1].append(pygame.transform.scale(img, (BOSS_SIZE, BOSS_SIZE)))
    if len(boss_assets[1]) == 0 and os.path.exists(os.path.join(game_folder, "boss2.png")):
        img = pygame.image.load(os.path.join(game_folder, "boss2.png")).convert_alpha()
        boss_assets[1].append(pygame.transform.scale(img, (BOSS_SIZE, BOSS_SIZE)))

    # Boss 3
    if os.path.exists(os.path.join(game_folder, "boss3.png")):
        img = pygame.image.load(os.path.join(game_folder, "boss3.png")).convert_alpha()
        boss_assets[2].append(pygame.transform.scale(img, (BOSS_SIZE, BOSS_SIZE)))

    # --- PROJECTILES ---
    # 1. Standard Bullet (Boss 1 & 3)
    if os.path.exists(os.path.join(game_folder, "bullet.png")):
        bullet_img = pygame.image.load(os.path.join(game_folder, "bullet.png")).convert_alpha()
        bullet_img = pygame.transform.scale(bullet_img, (60, 60))
    elif os.path.exists(os.path.join(game_folder, "bullet1.png")):
        bullet_img = pygame.image.load(os.path.join(game_folder, "bullet1.png")).convert_alpha()
        bullet_img = pygame.transform.scale(bullet_img, (60, 60))
    else: bullet_img = None

    # 2. Sting Animation (Boss 2) - Loads sting1..4
    for i in range(1, 5): 
        filename = f"sting{i}.png"
        path = os.path.join(game_folder, filename)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            sting_frames.append(img)

    # Rock
    if os.path.exists(os.path.join(game_folder, "rock.png")):
        rock_img = pygame.image.load(os.path.join(game_folder, "rock.png")).convert_alpha()
        rock_img = pygame.transform.scale(rock_img, (OBSTACLE_SIZE, 90)) 
    elif len(enemy_frames) > 0: rock_img = enemy_frames[0]
    else: rock_img = None
    
    # Bird
    for i in range(1, 4):
        filename = f"bird{i}.png" if i > 1 else "bird.png" 
        path = os.path.join(game_folder, filename)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (160, 120)) 
            bird_frames.append(img)
    if len(bird_frames) == 0 and os.path.exists(os.path.join(game_folder, "bird.png")):
         img = pygame.image.load(os.path.join(game_folder, "bird.png")).convert_alpha()
         bird_frames.append(pygame.transform.scale(img, (160, 120)))

    # Coin
    for i in range(1, 7): 
        filename = f"coin{i}.png"
        path = os.path.join(game_folder, filename)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (80, 80)) 
            coin_frames.append(img)
    if len(coin_frames) == 0 and os.path.exists(os.path.join(game_folder, "coin.png")):
        img = pygame.image.load(os.path.join(game_folder, "coin.png")).convert_alpha()
        img = pygame.transform.scale(img, (80, 80))
        coin_frames.append(img)

    # Items
    if os.path.exists(os.path.join(game_folder, "shield.png")):
        shield_img = pygame.image.load(os.path.join(game_folder, "shield.png")).convert_alpha()
        shield_img = pygame.transform.scale(shield_img, (90, 90))
    else: shield_img = None

    if os.path.exists(os.path.join(game_folder, "magnet.png")):
        magnet_img = pygame.image.load(os.path.join(game_folder, "magnet.png")).convert_alpha()
        magnet_img = pygame.transform.scale(magnet_img, (90, 90))
    else: magnet_img = None

    if os.path.exists(os.path.join(game_folder, "fireball.png")):
        fireball_img = pygame.image.load(os.path.join(game_folder, "fireball.png")).convert_alpha()
        fireball_img = pygame.transform.scale(fireball_img, (100, 60))
    else: fireball_img = None

    # Background
    bg_img = pygame.image.load(os.path.join(game_folder, "background.png")).convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH + 4, SCREEN_HEIGHT))
    
    using_images = True
except Exception as e:
    print(f"Assets error: {e}")

# Load Sounds
using_sounds = False
try:
    jump_sound = pygame.mixer.Sound(os.path.join(game_folder, "jump.mp3"))
    hit_sound = pygame.mixer.Sound(os.path.join(game_folder, "hit.mp3"))
    
    if os.path.exists(os.path.join(game_folder, "coin.mp3")):
        coin_sound = pygame.mixer.Sound(os.path.join(game_folder, "coin.mp3"))
    else: coin_sound = jump_sound 
    
    if os.path.exists(os.path.join(game_folder, "fire.mp3")):
        fire_sound = pygame.mixer.Sound(os.path.join(game_folder, "fire.mp3"))
    else: fire_sound = jump_sound

    if os.path.exists(os.path.join(game_folder, "music.mp3")):
        pygame.mixer.music.load(os.path.join(game_folder, "music.mp3"))
        pygame.mixer.music.set_volume(0.3) 
        pygame.mixer.music.play(-1) 

    jump_sound.set_volume(0.4) 
    hit_sound.set_volume(0.4)
    using_sounds = True
except:
    print("Audio missing.")

# --- SAVE SYSTEM ---
def load_data():
    hs = 0
    money = 0
    gold_status = False 
    fire_status = False 
    if os.path.exists(highscore_file):
        try:
            with open(highscore_file, "r") as f: hs = int(f.read())
        except: pass
    if os.path.exists(coins_file):
        try:
            with open(coins_file, "r") as f: money = int(f.read())
        except: pass
    if os.path.exists(shop_file):
        try:
            with open(shop_file, "r") as f: 
                data = f.read().split(",")
                if len(data) >= 1 and int(data[0]) == 1: gold_status = True
                if len(data) >= 2 and int(data[1]) == 1: fire_status = True
        except: pass
    return hs, money, gold_status, fire_status

def save_data(hs, money, gold_status, fire_status):
    with open(highscore_file, "w") as f: f.write(str(hs))
    with open(coins_file, "w") as f: f.write(str(money))
    with open(shop_file, "w") as f: 
        val1 = 1 if gold_status else 0
        val2 = 1 if fire_status else 0
        f.write(f"{val1},{val2}")

high_score, total_coins, unlocked_gold, unlocked_fire = load_data()
current_skin = "normal" 

# --- UI ELEMENTS ---
buy_skin_rect = pygame.Rect(700, 200, 250, 80) 
buy_fire_rect = pygame.Rect(700, 350, 250, 80) 
exit_button_rect = pygame.Rect(SCREEN_WIDTH - 80, 20, 60, 60)

# --- 3. CLASSES ---

class FloatingText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.timer = 60 
        
    def update(self):
        self.y -= 2 
        self.timer -= 1
        
    def draw(self, screen):
        if self.timer > 0:
            txt_surf = damage_font.render(self.text, True, self.color)
            screen.blit(txt_surf, (self.x, self.y))

class Particle:
    def __init__(self, x, y, color, mode="dust", image=None):
        self.x = x
        self.y = y
        self.color = color
        self.mode = mode
        self.image = image 
        self.size = random.randint(8, 16) 
        self.alpha = 255
        
        if mode == "dust":
            self.vx = random.randint(-6, -2)
            self.vy = random.randint(-3, 0)
            self.decay = 5 
        elif mode == "explosion":
            self.vx = random.randint(-8, 8)
            self.vy = random.randint(-8, 8)
            self.decay = 2 
        elif mode == "ghost":
            self.vx = -10 
            self.vy = 0
            self.decay = 15 

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.mode == "ghost":
            self.alpha -= self.decay
        else:
            self.size -= 0.5 

    def draw(self, screen, offset_x, offset_y):
        if self.mode == "ghost" and self.image:
            if self.alpha > 0:
                ghost_img = self.image.copy()
                ghost_img.set_alpha(self.alpha)
                screen.blit(ghost_img, (self.x + offset_x, self.y + offset_y))
        elif self.mode != "ghost" and self.size > 0:
            pygame.draw.rect(screen, self.color, (int(self.x + offset_x), int(self.y + offset_y), int(self.size), int(self.size)))

class Fireball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 60)
        self.speed = 30
        self.image = fireball_img if using_images else None
    
    def move(self):
        self.rect.x += self.speed
        
    def draw(self, screen, offset_x, offset_y):
        if using_images and self.image:
             screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        else:
            pygame.draw.circle(screen, (255, 69, 0), (self.rect.x + 50 + offset_x, self.rect.y + 30 + offset_y), 30)

class BossBullet:
    def __init__(self, x, y, bullet_type="normal"):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.speed = 15
        self.bullet_type = bullet_type # "normal" or "sting"
        
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = bullet_img if using_images else None # Default
        
    def move(self):
        self.rect.x -= self.speed
        
        # ANIMATE IF STING
        if self.bullet_type == "sting" and using_images and len(sting_frames) > 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(sting_frames):
                self.frame_index = 0
            self.image = sting_frames[int(self.frame_index)]
        elif using_images:
            self.image = bullet_img
        
    def draw(self, screen):
        if using_images and self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            color = (0, 255, 0) if self.bullet_type == "sting" else (100, 0, 100)
            pygame.draw.circle(screen, color, (self.rect.x + 30, self.rect.y + 30), 30)

class Boss:
    def __init__(self, level):
        self.rect = pygame.Rect(SCREEN_WIDTH - 400, GROUND_Y - BOSS_SIZE, BOSS_SIZE, BOSS_SIZE)
        self.level = level
        self.hp = 10 + (level * 5) 
        self.max_hp = self.hp
        
        self.boss_type = (level - 1) % 3 
        
        self.shoot_timer = 0
        self.move_timer = 0
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = None
        
        # Get correct frames for this specific boss type
        if len(boss_assets) > self.boss_type:
            self.frames = boss_assets[self.boss_type]
        else:
            self.frames = []
            
    def update(self, bullets_list):
        self.move_timer += 0.05
        
        # --- AI BEHAVIOR ---
        if self.boss_type == 0: # Tank
            self.rect.y = GROUND_Y - BOSS_SIZE 
            shoot_speed = 60 
            
        elif self.boss_type == 1: # Flyer
            self.rect.y = (GROUND_Y - 450) + math.sin(self.move_timer) * 200
            shoot_speed = 50 
            
        elif self.boss_type == 2: # Berserker
            shake = math.sin(self.move_timer * 10) * 20
            self.rect.y = (GROUND_Y - BOSS_SIZE) + shake
            shoot_speed = 30 

        # --- ANIMATION ---
        if using_images and len(self.frames) > 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

        # --- SHOOTING ---
        self.shoot_timer += 1
        if self.shoot_timer > shoot_speed:
            self.shoot_timer = 0
            
            # Determine bullet type based on boss
            b_type = "sting" if self.boss_type == 1 else "normal"
            
            if random.randint(0, 1) == 0: bullet_y = self.rect.y + BOSS_SIZE - 50 
            else: bullet_y = self.rect.y + 50 
            
            bullets_list.append(BossBullet(self.rect.x, bullet_y, b_type))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            cols = [(150,0,0), (0,150,0), (0,0,150)]
            pygame.draw.rect(screen, cols[self.boss_type % 3], self.rect)
        
        # Health Bar
        pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, self.rect.y - 40, BOSS_SIZE, 30))
        ratio = self.hp / self.max_hp
        if ratio < 0: ratio = 0
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 40, BOSS_SIZE * ratio, 30))


# --- CLASSES (OBSTACLES/ITEMS) ---
class Item:
    def __init__(self, type):
        self.type = type 
        self.rect = pygame.Rect(SCREEN_WIDTH, 0, 80, 80)
        self.frame_index = 0
        self.animation_speed = 0.25
        if self.type == "coin":
            self.rect.y = random.randint(GROUND_Y - 400, GROUND_Y - 150)
            self.image = coin_frames[0] if (using_images and len(coin_frames) > 0) else None
            self.color = (255, 215, 0) 
        elif self.type == "shield":
            self.rect.y = random.randint(GROUND_Y - 350, GROUND_Y - 200)
            self.image = shield_img if using_images else None
            self.color = (0, 0, 255) 
        elif self.type == "magnet":
            self.rect.y = random.randint(GROUND_Y - 350, GROUND_Y - 200)
            self.image = magnet_img if using_images else None
            self.color = (128, 0, 128) 

    def move(self, speed, player_x, player_y, has_magnet):
        self.rect.x -= speed
        if has_magnet and self.type == "coin":
            dx = player_x - self.rect.x
            dy = player_y - self.rect.y
            dist = math.hypot(dx, dy)
            if dist < 500: 
                self.rect.x += int((dx / dist) * 20)
                self.rect.y += int((dy / dist) * 20)
        if self.type == "coin" and using_images and len(coin_frames) > 1:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(coin_frames):
                self.frame_index = 0
            self.image = coin_frames[int(self.frame_index)]

    def draw(self, screen, offset_x, offset_y):
        if using_images and self.image:
            screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        else:
            pygame.draw.rect(screen, self.color, (self.rect.x + offset_x, self.rect.y + offset_y, 80, 80))

class Obstacle:
    def __init__(self, type):
        self.type = type 
        self.rect = pygame.Rect(SCREEN_WIDTH, 300, OBSTACLE_SIZE, OBSTACLE_SIZE) 
        self.image = None
        self.hitbox_inset = 25 
        self.frame_index = 0
        self.animation_speed = 0.2
        self.bob_speed = 0.1 
        self.bob_height = 60 
        self.start_y = 0     
        if self.type == "cactus": 
            self.rect.y = GROUND_Y - OBSTACLE_SIZE 
            self.image = enemy_frames[0] if (using_images and len(enemy_frames) > 0) else None
        elif self.type == "rock": 
            self.rect.height = 90 
            self.rect.y = GROUND_Y - 90 
            self.image = rock_img if using_images else None
        elif self.type == "bird":
            self.rect.y = GROUND_Y - 300 
            self.start_y = self.rect.y
            self.rect.width = 160
            self.rect.height = 120
            if using_images and len(bird_frames) > 0: self.image = bird_frames[0]
            else: self.image = None

    def move(self, speed):
        self.rect.x -= speed
        if self.type == "bird":
            offset = math.sin(pygame.time.get_ticks() * 0.005) * self.bob_height
            self.rect.y = self.start_y + offset
            if using_images and len(bird_frames) > 0:
                self.frame_index += self.animation_speed
                if self.frame_index >= len(bird_frames): self.frame_index = 0
                self.image = bird_frames[int(self.frame_index)]
        if self.type == "cactus" and using_images and len(enemy_frames) > 1:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(enemy_frames): self.frame_index = 0
            self.image = enemy_frames[int(self.frame_index)]

    def draw(self, screen, offset_x, offset_y):
        if using_images and self.image:
            screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        else:
            if self.type == "cactus": color = (200, 0, 0)
            elif self.type == "rock": color = (100, 100, 100) 
            else: color = (0, 200, 200)
            target_rect = pygame.Rect(self.rect.x + offset_x, self.rect.y + offset_y, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, color, target_rect)
    
    def get_hitbox(self):
        return pygame.Rect(self.rect.x + self.hitbox_inset, self.rect.y + self.hitbox_inset, self.rect.width - (self.hitbox_inset*2), self.rect.height - (self.hitbox_inset*2))

# --- 4. GAME VARIABLES ---
def reset_game():
    return 100, PLAYER_START_Y, 0, 0, START_SPEED, 2, 0, 0, False, 0, 0, 1

game_state = "MENU"
player_x, player_y, player_velocity, score, game_speed, jumps_left, dash_timer, dash_cooldown, has_shield, magnet_timer, fire_cooldown, boss_level = reset_game()

bg_x1 = 0
bg_x2 = SCREEN_WIDTH 

obstacles = [] 
items = [] 
particles = [] 
fireballs = [] 
boss_bullets = [] 
floating_texts = [] 
spawn_timer = 0 
item_spawn_timer = 0
animation_timer = 0
player_index = 0
shake_timer = 0 
active_boss = None 

# --- 5. GAME LOOP ---
running = True
while running:
    render_offset_x = 0; render_offset_y = 0
    if shake_timer > 0:
        render_offset_x = random.randint(-15, 15); render_offset_y = random.randint(-15, 15)
        shake_timer -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button_rect.collidepoint(event.pos): running = False
            
            if game_state == "SHOP":
                if buy_skin_rect.collidepoint(event.pos):
                    if unlocked_gold: current_skin = "gold" if current_skin == "normal" else "normal"
                    elif total_coins >= 50:
                        total_coins -= 50; unlocked_gold = True; current_skin = "gold"
                        save_data(high_score, total_coins, unlocked_gold, unlocked_fire)
                if buy_fire_rect.collidepoint(event.pos):
                     if not unlocked_fire and total_coins >= 20:
                         total_coins -= 20; unlocked_fire = True
                         save_data(high_score, total_coins, unlocked_gold, unlocked_fire)

        if event.type == pygame.KEYDOWN:
            # --- NEW SCREENSHOT KEY ---
            if event.key == pygame.K_p:
                pygame.image.save(screen, "screenshot.png") # Saves directly to your folder!
                
            if event.key == pygame.K_ESCAPE: 
                if game_state == "PLAYING" or game_state == "BOSS_FIGHT": game_state = "PAUSED"
                elif game_state == "PAUSED": game_state = "PLAYING" if active_boss is None else "BOSS_FIGHT"
                elif game_state == "SHOP": game_state = "MENU"
                elif game_state == "MENU": running = False 

            if game_state == "MENU":
                if event.key == pygame.K_RETURN:
                    player_x, player_y, player_velocity, score, game_speed, jumps_left, dash_timer, dash_cooldown, has_shield, magnet_timer, fire_cooldown, boss_level = reset_game()
                    obstacles.clear(); particles.clear(); items.clear(); fireballs.clear(); boss_bullets.clear(); floating_texts.clear(); active_boss = None
                    game_state = "PLAYING"
                if event.key == pygame.K_s: game_state = "SHOP"
            
            elif game_state == "PLAYING" or game_state == "BOSS_FIGHT":
                if event.key == pygame.K_SPACE and jumps_left > 0:
                    player_velocity = JUMP_STRENGTH; jumps_left -= 1
                    if using_sounds: jump_sound.play()
                    for _ in range(12): particles.append(Particle(player_x + 65, player_y + 130, (200, 200, 200), "dust"))
                
                if event.key == pygame.K_f and unlocked_fire and fire_cooldown <= 0:
                    fireballs.append(Fireball(player_x + 80, player_y + 40)); fire_cooldown = FIRE_COOLDOWN_MAX
                    if using_sounds: fire_sound.play()
                
                if event.key == pygame.K_LSHIFT and dash_cooldown == 0:
                    dash_timer = DASH_DURATION; dash_cooldown = DASH_COOLDOWN
                    for _ in range(20): particles.append(Particle(player_x, player_y+60, (255, 255, 255), "dust"))

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_SPACE: game_state = "MENU"

    if game_state == "PAUSED":
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(128); s.fill((0,0,0)); screen.blit(s, (0,0))
        pause_text = title_font.render("PAUSED", True, (255, 255, 255)); screen.blit(pause_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        hint_text = font.render("Press ESC to Resume", True, (200, 200, 200)); screen.blit(hint_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50))
        pygame.draw.rect(screen, (200, 0, 0), exit_button_rect); screen.blit(button_font.render("X", True, (255, 255, 255)), (exit_button_rect.x + 18, exit_button_rect.y + 12))
        pygame.display.flip(); clock.tick(60); continue 

    # --- DRAWING ---
    if using_images:
        # Only scroll background if NOT in boss fight
        if game_state != "BOSS_FIGHT":
            bg_x1 -= 2; bg_x2 -= 2
            if bg_x1 <= -SCREEN_WIDTH: bg_x1 = bg_x2 + SCREEN_WIDTH 
            if bg_x2 <= -SCREEN_WIDTH: bg_x2 = bg_x1 + SCREEN_WIDTH
        screen.blit(bg_img, (bg_x1, 0)); screen.blit(bg_img, (bg_x2, 0))
    else: screen.fill((135, 206, 235))

    if game_state == "MENU":
        title = title_font.render("LEGENDARY RUNNER", True, (255, 255, 255))
        instr = font.render("Press ENTER to Start", True, (200, 200, 200))
        shop_hint = font.render("Press 'S' for Shop", True, (255, 215, 0))
        screen.blit(title_font.render("LEGENDARY RUNNER", True, (0,0,0)), (SCREEN_WIDTH//2 - title.get_width()//2 + 4, SCREEN_HEIGHT//3 + 4))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
        screen.blit(instr, (SCREEN_WIDTH//2 - instr.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(shop_hint, (SCREEN_WIDTH//2 - shop_hint.get_width()//2, SCREEN_HEIGHT//2 + 80))
        coin_text = font.render(f"Bank: {total_coins} Coins", True, (255, 215, 0)); screen.blit(coin_text, (40, 40))

    elif game_state == "SHOP":
        screen.fill((50, 50, 50)) 
        shop_title = title_font.render("ITEM SHOP", True, (255, 255, 255)); screen.blit(shop_title, (SCREEN_WIDTH//2 - shop_title.get_width()//2, 50))
        
        skin_text = shop_font.render("1. Shiny Skin", True, (255, 215, 0)); screen.blit(skin_text, (100, 200))
        if unlocked_gold:
            btn_col = (0, 200, 0) if current_skin == "gold" else (100, 100, 100)
            btn_txt = "EQUIPPED" if current_skin == "gold" else "EQUIP"
        else:
            btn_col = (255, 215, 0) if total_coins >= 50 else (150, 0, 0)
            btn_txt = "BUY (50)"
        pygame.draw.rect(screen, btn_col, buy_skin_rect)
        t = button_font.render(btn_txt, True, (255,255,255)); screen.blit(t, t.get_rect(center=buy_skin_rect.center))
        if len(player_gold_frames) > 0: screen.blit(player_gold_frames[0], (550, 180))

        fire_text = shop_font.render("2. Fireball", True, (255, 69, 0)); screen.blit(fire_text, (100, 350))
        if unlocked_fire:
            pygame.draw.rect(screen, (0, 200, 0), buy_fire_rect)
            t = button_font.render("OWNED", True, (255,255,255)); screen.blit(t, t.get_rect(center=buy_fire_rect.center))
        else:
            btn_col = (255, 215, 0) if total_coins >= 20 else (150, 0, 0)
            pygame.draw.rect(screen, btn_col, buy_fire_rect)
            t = button_font.render("BUY (20)", True, (255,255,255)); screen.blit(t, t.get_rect(center=buy_fire_rect.center))

        coin_text = font.render(f"Your Coins: {total_coins}", True, (255, 215, 0)); screen.blit(coin_text, (40, 40))
        back_text = font.render("Press ESC to Back", True, (200, 200, 200)); screen.blit(back_text, (100, 600))

    elif game_state == "PLAYING" or game_state == "BOSS_FIGHT":
        
        # --- PLAYER PHYSICS & DASH MOVEMENT ---
        is_dashing = dash_timer > 0; is_magnet = magnet_timer > 0
        target_player_x = 300 if is_dashing else 100
        if player_x < target_player_x: player_x += 15
        elif player_x > target_player_x: player_x -= 10
        
        if is_dashing:
            dash_timer -= 1; player_velocity = 0 
            frames = player_gold_frames if current_skin == "gold" else player_frames
            if dash_timer % 3 == 0 and using_images and len(frames) > 0: particles.append(Particle(player_x, player_y, None, "ghost", frames[player_index]))
        
        if is_magnet: magnet_timer -= 1
        if dash_cooldown > 0: dash_cooldown -= 1
        if fire_cooldown > 0: fire_cooldown -= 1

        if not is_dashing: player_velocity += GRAVITY; player_y += player_velocity
        if player_y >= PLAYER_START_Y:
            player_y = PLAYER_START_Y; jumps_left = 2
            if not is_dashing and random.randint(0, 5) == 0: particles.append(Particle(player_x, player_y + 120, (220, 220, 220), "dust"))

        # --- BOSS TRIGGER ---
        if game_state == "PLAYING":
            if score > 0 and score % 25 == 0 and active_boss is None:
                game_state = "BOSS_FIGHT"
                obstacles.clear()
                active_boss = Boss(boss_level)
                boss_level += 1 

        # --- OBSTACLE SPAWNING ---
        if game_state == "PLAYING":
            current_speed = game_speed + DASH_SPEED_BOOST if is_dashing else game_speed
            spawn_timer += 1
            if spawn_timer > max(40, 100 - score//50): 
                spawn_timer = 0; choice = random.randint(0, 2)
                if choice == 0: obstacles.append(Obstacle("cactus"))
                elif choice == 1: obstacles.append(Obstacle("rock"))
                else: obstacles.append(Obstacle("bird"))

            item_spawn_timer += 1
            if item_spawn_timer > 60: 
                item_spawn_timer = 0; rand = random.randint(0, 100)
                if rand < 3: items.append(Item("shield"))
                elif rand < 6: items.append(Item("magnet")) 
                elif rand < 40: items.append(Item("coin"))
        
        # --- BOSS LOGIC ---
        if game_state == "BOSS_FIGHT" and active_boss:
            active_boss.update(boss_bullets)
            active_boss.draw(screen)
            
            for f in fireballs[:]:
                if f.rect.colliderect(active_boss.rect):
                    active_boss.hp -= 1
                    fireballs.remove(f)
                    floating_texts.append(FloatingText(active_boss.rect.x + 50, active_boss.rect.y + 50, "-1", (255, 0, 0)))
                    for _ in range(10): particles.append(Particle(f.rect.x, f.rect.y, (255, 50, 0), "explosion"))
                    if active_boss.hp <= 0:
                        active_boss = None
                        game_state = "PLAYING"
                        score += 5; total_coins += 50 
                        obstacles.clear(); boss_bullets.clear()
                        save_data(high_score, total_coins, unlocked_gold, unlocked_fire)

        # --- UPDATE ENTITIES ---
        for ft in floating_texts[:]:
            ft.update(); ft.draw(screen)
            if ft.timer <= 0: floating_texts.remove(ft)

        for p in particles[:]:
            p.update(); p.draw(screen, render_offset_x, render_offset_y)
            if p.mode == "ghost" and p.alpha <= 0: particles.remove(p)
            elif p.mode != "ghost" and p.size <= 0: particles.remove(p)

        for f in fireballs[:]:
            f.move(); f.draw(screen, render_offset_x, render_offset_y)
            if f.rect.x > SCREEN_WIDTH: fireballs.remove(f)
            for obs in obstacles[:]:
                if f.rect.colliderect(obs.get_hitbox()):
                    obstacles.remove(obs); 
                    if f in fireballs: fireballs.remove(f)
                    for _ in range(30): particles.append(Particle(obs.rect.x + 60, obs.rect.y + 60, (255, 100, 0), "explosion"))
                    break 

        for b in boss_bullets[:]:
            b.move(); b.draw(screen)
            if b.rect.x < 0: boss_bullets.remove(b)
            player_rect = pygame.Rect(player_x + 20, player_y + 20, PLAYER_SIZE - 40, PLAYER_SIZE - 40)
            if player_rect.colliderect(b.rect):
                if has_shield: has_shield = False; boss_bullets.remove(b)
                else:
                    game_state = "GAME_OVER"; shake_timer = 30
                    if using_sounds: hit_sound.play()
                    if score > high_score: high_score = score; save_data(high_score, total_coins, unlocked_gold, unlocked_fire) 

        player_rect = pygame.Rect(player_x + 20, player_y + 20, PLAYER_SIZE - 40, PLAYER_SIZE - 40)
        
        for obs in obstacles:
            speed = game_speed if game_state == "PLAYING" else 0 
            obs.move(speed); obs.draw(screen, render_offset_x, render_offset_y)
            if player_rect.colliderect(obs.get_hitbox()):
                if is_dashing: pass 
                elif has_shield:
                    has_shield = False; shake_timer = 15; obstacles.remove(obs)
                    for _ in range(25): particles.append(Particle(player_x+60, player_y+60, (0, 0, 255), "explosion"))
                else:
                    game_state = "GAME_OVER"; shake_timer = 30 
                    if using_sounds: hit_sound.play()
                    if score > high_score: high_score = score; save_data(high_score, total_coins, unlocked_gold, unlocked_fire) 
                    for _ in range(50): particles.append(Particle(player_x+60, player_y+60, (255, 50, 50), "explosion"))

        if obstacles and obstacles[0].rect.x < -150:
            obstacles.pop(0); score += 1; 
            if score % 5 == 0: game_speed += 1

        for item in items[:]:
            speed = game_speed if game_state == "PLAYING" else 0
            item.move(speed, player_x, player_y, is_magnet); item.draw(screen, render_offset_x, render_offset_y)
            if player_rect.colliderect(item.rect):
                if item.type == "coin": 
                    total_coins += 1; 
                    floating_texts.append(FloatingText(player_x + 50, player_y, "+1", (255, 215, 0)))
                elif item.type == "shield": has_shield = True
                elif item.type == "magnet": magnet_timer = 300 
                if using_sounds: coin_sound.play()
                items.remove(item)
            elif item.rect.x < -150: items.remove(item)

        frames = player_gold_frames if current_skin == "gold" else player_frames
        if using_images and len(frames) > 0:
            animation_timer += 0.3
            if animation_timer >= len(frames): animation_timer = 0
            player_index = int(animation_timer)
            screen.blit(frames[player_index], (player_x + render_offset_x, player_y + render_offset_y))
        else: pygame.draw.rect(screen, (255, 215, 0) if current_skin == "gold" else (200, 0, 0), player_rect)
        
        if has_shield: pygame.draw.circle(screen, (0, 191, 255), (int(player_x + PLAYER_SIZE/2), int(player_y + PLAYER_SIZE/2)), 90, 6)
        if is_magnet: pygame.draw.circle(screen, (128, 0, 128), (int(player_x + PLAYER_SIZE/2), int(player_y + PLAYER_SIZE/2)), 110, 4)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255)); screen.blit(score_text, (20 + render_offset_x, 20 + render_offset_y))
        
        if unlocked_fire:
            pygame.draw.rect(screen, (50, 50, 50), (20, 140, 300, 30))
            ratio = 1 - (fire_cooldown / FIRE_COOLDOWN_MAX)
            col = (255, 69, 0) if ratio >= 1 else (100, 100, 100)
            pygame.draw.rect(screen, col, (20, 140, 300 * ratio, 30))
            if ratio >= 1: screen.blit(button_font.render("FIRE (F)", True, (255, 255, 255)), (330, 138))

        if dash_cooldown > 0:
            pygame.draw.rect(screen, (100, 100, 100), (20, 80, 300, 30))
            pygame.draw.rect(screen, (0, 255, 255), (20, 80, 300 * (1 - dash_cooldown/DASH_COOLDOWN), 30))
        else:
            pygame.draw.rect(screen, (0, 255, 255), (20, 80, 300, 30))
            screen.blit(pygame.font.Font(None, 40).render("SWIFT", True, (255, 255, 255)), (330, 78))
        
        if game_state == "BOSS_FIGHT":
            boss_text = title_font.render("BOSS FIGHT!", True, (200, 0, 0))
            screen.blit(boss_text, (SCREEN_WIDTH//2 - boss_text.get_width()//2, 100))

    elif game_state == "GAME_OVER":
        if using_images: screen.blit(bg_img, (bg_x1, 0)); screen.blit(bg_img, (bg_x2, 0))
        for obs in obstacles: obs.draw(screen, render_offset_x, render_offset_y)
        for p in particles: p.draw(screen, render_offset_x, render_offset_y)
        go_text = title_font.render("GAME OVER", True, (255, 255, 255))
        sc_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        bank_text = font.render(f"Total Bank: {total_coins}", True, (255, 215, 0))
        re_text = font.render("Press SPACE to Menu", True, (200, 200, 200))
        screen.blit(go_text, (SCREEN_WIDTH//2 - go_text.get_width()//2, SCREEN_HEIGHT//3))
        screen.blit(sc_text, (SCREEN_WIDTH//2 - sc_text.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(bank_text, (SCREEN_WIDTH//2 - bank_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
        screen.blit(re_text, (SCREEN_WIDTH//2 - re_text.get_width()//2, SCREEN_HEIGHT//2 + 160))
    
    pygame.draw.rect(screen, (200, 0, 0), exit_button_rect)
    screen.blit(button_font.render("X", True, (255, 255, 255)), (exit_button_rect.x + 18, exit_button_rect.y + 12))
    pygame.display.flip(); clock.tick(60)

pygame.quit