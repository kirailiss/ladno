import pygame
import os
pygame.init()

def file_path(file_name):
    folder_path = os.path.abspath(__file__+"/..")
    path = os.path.join(folder_path, file_name)
    return path


WIN_WIDTH, WIN_HEIGHT = 700, 500
FPS = 20


window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("bebra game 3000")
clock = pygame.time.Clock()


img_background = pygame.transform.scale(pygame.image.load(file_path("images\\background.png")), (WIN_WIDTH, WIN_HEIGHT))
win_img = pygame.transform.scale(pygame.image.load(file_path("images\\win.png")), (WIN_WIDTH, WIN_HEIGHT))
lose_img = pygame.transform.scale(pygame.image.load(file_path("images\\lose.png")), (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(file_path("sounds\\bg_music.wav"))
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

music_win = pygame.mixer.Sound(file_path("sounds\\victory.wav"))
music_lose = pygame.mixer.Sound(file_path("sounds\\game_over.wav"))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(img),(width, height))
        


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Enemy(GameSprite):
    def __init__(self, x, y, width, height, img, speed, min_cord, max_cord, direction):
        super().__init__(x, y, width, height, img)
        self.speed = speed
        self.min_cord = min_cord
        self.max_cord = max_cord
        self.direction = direction
    
    def update(self):
        if self.direction == "left" or self.direction == "right":
            if self.direction == "right":
                self.rect.x += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed

            if self.rect.right >= self.max_cord:
                self.direction = "left"
            if self.rect.left <=  self.min_cord:
                self.direction = "right"
        elif self.direction == "up" or self.direction == "down":


            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == 'down':
                self.rect.y += self.speed

            if self.rect.top <= self.min_cord:
                self.direction = "down"
            if self.rect.bottom >= self.max_cord:
                self.direction = "up"
        

class Player(GameSprite):
    def __init__(self, x, y, width, height, img):
        super().__init__(x , y, width, height, img)
        self.speed_x = 0
        self.speed_y = 0
        self.direction = "right"
        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)


    def update(self):
        #рух по горизонталі
        if self.speed_x > 0 and  self.rect.right < WIN_WIDTH or self.speed_x < 0 and self.rect.left > 0:
            self.rect.x += self.speed_x
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        if self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)

        #рух по вертикалі
        if self.speed_y < 0 and self.rect.top > 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed_y
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
                


player = Player(30, 102, 50, 50, file_path("images\\player.png"))

enemies = pygame.sprite.Group()
enemy1 = Enemy(300, 150, 50, 50, file_path("images\\enemy.png"), 3, 130, 300, "left")
enemies.add(enemy1)
enemy2 =Enemy(380, 150, 50, 50, file_path("images\\enemy.png"), 5, 0, 500, "down")
enemies.add(enemy2)
enemy3 =Enemy(200, 150, 50, 50, file_path("images\\enemy.png"), 2, 100, 300, "right")
enemies.add(enemy3)
enemy4 =Enemy(600, 150, 50, 50, file_path("images\\enemy.png"), 13, 0, 500, "down")
enemies.add(enemy4)
enemy5 =Enemy(380, 150, 50, 50, file_path("images\\enemy.png"), 10, 0, 500, "down")
enemies.add(enemy5)

wall1 = GameSprite(670, 0, 30, 500, file_path("images\\wall.png"))
goal = GameSprite(600, 100, 50, 110, file_path("images\\goal.png"))

walls = pygame.sprite.Group()
wall1 = GameSprite(95, 0, 30, 300, file_path("images\\wall.png"))
walls.add(wall1)
wall2 = GameSprite(200, 250, 30, 300, file_path("images\\wall.png"))
walls.add(wall2)
wall3 = GameSprite(500, 300, 30, 300, file_path("images\\wall.png"))
walls.add(wall3)
wall4 = GameSprite(500, 0, 30, 200, file_path("images\\wall.png"))
walls.add(wall4)
wall5 = GameSprite(310, 5, 30, 300, file_path("images\\wall.png"))
walls.add(wall5)
play = True
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.direction = "right"
                player.image = player.image_r
                player.speed_x = 5
            if event.key == pygame.K_a:
                player.direction = "left"
                player.image = player.image_l
                player.speed_x = -5
            if event.key == pygame.K_s:
                player.speed_y = 5
            if event.key == pygame.K_w:
                player.speed_y = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.speed_x = 0
            if event.key == pygame.K_a:
                player.speed_x = 0
            if event.key == pygame.K_s:
                player.speed_y = 0
            if event.key == pygame.K_w:
                player.speed_y = 0


    if play ==  True:    
        window.blit(img_background, (0,0))
        player.reset()
        player.update()
        
        enemies.draw(window)
        enemies.update()

        goal.reset()
        walls.draw(window)

        if pygame.sprite.collide_rect(player, goal):
            play = False
            window.blit(win_img, (0,0))
            pygame.mixer.music.stop()
            music_win.play()
        
        if pygame.sprite.spritecollide(player, enemies, False): 
            play = False
            pygame.mixer.music.stop()
            music_lose.play()
            window.blit(lose_img, (0,0))
            



    clock.tick(FPS)
    pygame.display.update()