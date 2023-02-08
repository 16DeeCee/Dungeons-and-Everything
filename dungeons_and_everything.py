import pygame
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # player standby
        self.player_standby = create_image_list("Sprites/Knight/idle/Idle", 11)
        self.player_standby_left = create_image_left_list(self.player_standby, 10)
        self.player_jump = create_image_list("Sprites/Knight/jump/Jump", 11)
        self.player_jump_left = create_image_left_list(self.player_jump, 10)
        self.player_attack = create_image_list("Sprites/Knight/attack/Attack", 11)
        self.player_attack_left = create_image_left_list(self.player_attack, 10)
        self.player_walk = create_image_list("Sprites/Knight/walk/Walk", 11)
        self.player_walk_left = create_image_left_list(self.player_walk, 10)
        self.image_index = 0
        self.image = self.player_standby[self.image_index]
        self.rect = self.image.get_rect(midbottom = (150, 590))
        self.rect = self.rect.inflate(-75 , 0)


        self.isAttack = False
        self.isFacing = True
        self.isMoving = False
        self.gravity = 0

    def player_actions(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_SPACE] and self.rect.bottom >= 595:
            self.image_index = 0
            self.gravity = -18
        if self.keys[pygame.K_a]:
            self.image_index = 0
            self.isAttack = True
        if self.keys[pygame.K_RIGHT]:
            self.rect.x += 4
            self.isMoving = True
            self.isFacing = True
        if self.keys[pygame.K_LEFT]:
            self.rect.x -= 4
            self.isMoving = True
            self.isFacing = False
    
    def jump_gravity(self):
        self.gravity += 0.7
        self.rect.y += self.gravity
        if self.rect.bottom >= 595: self.rect.bottom = 595

    def animation(self):
        # walk animation
        if self.isMoving == True and self.isFacing and self.rect.bottom >= 595:
            self.image_index += 0.5
            if self.image_index >= len(self.player_walk):
                self.image_index = 0
                self.isMoving = False
            self.image = self.player_walk[int(self.image_index)]
        
        elif self.isMoving == True and self.isFacing == False and self.rect.bottom >= 595:
            self.image_index += 0.5
            if self.image_index >= len(self.player_walk_left):
                self.image_index = 0
                self.isMoving = False
            self.image = self.player_walk_left[int(self.image_index)]

        # attack animation
        elif self.isAttack == True and self.rect.bottom == 595:
            if self.isFacing:
                self.image_index += 0.5
                if self.image_index >= len(self.player_attack):
                    self.image_index = 0
                    self.isAttack = False
                self.image = self.player_attack[int(self.image_index)]
            else:
                self.image_index += 0.5
                if self.image_index >= len(self.player_attack_left):
                    self.image_index = 0
                    self.isAttack = False
                self.image = self.player_attack_left[int(self.image_index)]

        # jump animation
        elif self.rect.bottom < 595:
            if self.isFacing:
                self.image_index += 0.40
                if self.image_index >= len(self.player_jump):
                    self.image_index = 0
                self.image = self.player_jump[int(self.image_index)]
            else:
                self.image_index += 0.40
                if self.image_index >= len(self.player_jump_left):
                    self.image_index = 0
                self.image = self.player_jump_left[int(self.image_index)]                

        #stand by animation
        else:
            if self.isFacing:
                self.image_index += 0.1
                if self.image_index >= len(self.player_standby):
                    self.image_index = 0
                self.image = self.player_standby[int(self.image_index)]
            else:
                self.image_index += 0.1
                if self.image_index >= len(self.player_standby_left):
                    self.image_index = 0
                self.image = self.player_standby_left[int(self.image_index)]

    def update(self):
        self.player_actions()
        self.jump_gravity()
        self.animation()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type, spawn):
        super().__init__()
        self.spawn = spawn

        if type == "zombie":
            self.zombie_walking = create_image_list("Sprites/Zombie/boy/walk/Walk", 11)
            if spawn == "right":
                self.monster = self.zombie_walking
                x_pos = -100
            else:
                self.monster = create_image_left_list(self.zombie_walking, 10)
                x_pos = 1290
        else:
            self.alien_walking = create_image_list("Sprites/Alien/walk/Walk", 7)
            if spawn == "right":
                self.monster = self.alien_walking
                x_pos = -100
            else:
                self.monster = create_image_left_list(self.alien_walking, 6)
                x_pos = 1290

        self.obstacle_image_index = 0
        y_pos = 590
        self.image = self.monster[self.obstacle_image_index]
        self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))
        self.rect = self.rect.inflate(-70 , 0)
        self.rect.update((self.rect.left, self.rect.top), (self.rect.width, 70))

    def obstacle_animation(self):
        self.obstacle_image_index += 0.1
        if collision_sprite:
            pass
        if self.obstacle_image_index >= len(self.monster):
            self.obstacle_image_index = 0
        self.image = self.monster[int(self.obstacle_image_index)]


    def update(self):
        self.obstacle_animation()
        if self.spawn == "left":
            self.rect.x -= 5
        else:
            self.rect.x += 5
    
    def destroy(self):
        if self.rect.x <= -150 or self.rect.x >= 1350:
            self.kill()


# creates default image list
def create_image_list(location, frame):
    list = []
    for index in range(1, frame):
        list.append(pygame.image.load(f"{location}_{str(index)}.png").convert_alpha())
    return list

# copies and creates another image list facing left
def create_image_left_list(list, frame):
    list_copy = list.copy()
    for index in range(frame):
        list_copy[index] = pygame.transform.flip(list_copy[index], True, False)
    return list_copy

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, True):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()

# screen size
screen = pygame.display.set_mode((1280, 720))
# clock to set the frame rate
clock = pygame.time.Clock()
# set the title
pygame.display.set_caption("Dungeons and Everything")

game_active = False

#background music
game_music = pygame.mixer.Sound("Music/title sequence - little town.ogg")
game_music.set_volume(0.2)
game_music.play(loops = -1)
test_font = pygame.font.Font("Fonts/scribish.ttf", 50)

# opening
opening_background = pygame.image.load("Backgrounds/opening_image.png").convert_alpha()
opening_background_rect = opening_background.get_rect(center = (640, 360))
game_title = test_font.render("Dungeons and Everything", False, (111, 196, 169))
game_title_rect = game_title.get_rect(center = (640, 90))
game_message = test_font.render("Press any key to play", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (640, 590))

# sound
bg_music = pygame.mixer.Sound("Music/title sequence - little town.ogg")
bg_music.set_volume(0.2)


# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# backgrounds
castle_surface = pygame.image.load("Backgrounds/castle background.png").convert_alpha()

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2500)

while True:
    #user events
    for event in pygame.event.get():
        #closing the application
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(["zombie","alien"]), choice(["left", "right"])))
        else:
            if event.type == pygame.KEYDOWN:
                game_active = True

    if game_active:
        bg_music.stop()
        screen.blit(castle_surface, (0, 0))
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision
        # game_active = collision_sprite()
    else:
        screen.blit(opening_background, opening_background_rect)
        screen.blit(game_title, game_title_rect)
        screen.blit(game_message, game_message_rect)
        bg_music.play(loops = -1)

    # display the screen size and frame rate of 60 fps
    pygame.display.update()
    clock.tick(60)