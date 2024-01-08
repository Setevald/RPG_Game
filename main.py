import pygame
from sprites import *
from config import * 
import sys

#starts the game (main class)
class Game:
    def __init__(self):
        pygame.init()
        # create game window and setting the frame rate (measures in pixels)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('arial.ttf', 32)
        
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.intro_background = pygame.image.load('./img/introbackground.png')
        self.go_background = pygame.image.load('./img/gameover.png')
        
        # Initialize sprite groups here
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j , i)
        
    def new(self):
        self.createTilemap()
        # a new game starts (important to see if the player dies or not or quits the game)
        self.playing = True
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        
        self.createTilemap()
        
    def events(self):
        # game loops events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.playing = False
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
        
    def update(self):
        # game loop updates
        self.all_sprites.update()
        
    def draw(self):
        # game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
        
    def main(self):
        # game loop 
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    def game_over(self):
        game_over_text = self.font.render('Game Over', True, WHITE)
        game_over_text_rect = game_over_text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        
        subtext = self.font.render('Imagine dying', True, WHITE)
        subtext_rect = subtext.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 + 50))
        
        restart_button = Button(10, WIN_HEIGHT - 120, 120, 50, WHITE, BLACK, 'Restart', 32)
        quit_button = Button(WIN_WIDTH - 130, WIN_HEIGHT - 120, 120, 50, WHITE, BLACK, 'Quit', 32)
        
        for sprite in self.all_sprites:
            sprite.kill()
            
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            elif quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False
                
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(game_over_text, game_over_text_rect)
            self.screen.blit(subtext, subtext_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
        
    def intro_screen(self):
        intro = True
        
        title = self.font.render('game game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)
        
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                    
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
    
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
    
pygame.quit()
sys.exit()