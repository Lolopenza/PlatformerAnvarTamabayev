import sys

import random
import pygame
import pygame_menu
from pygame_menu import themes

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap, Tilemap2
from scripts.clouds import Clouds
from scripts.enemy import Enemy

def load_level(level): 
    if level == 1:
        return lvl1()
    elif level == 2:
        return lvl2()
    else:
        print('end')
        # pygame.quit()
        # sys.exit()


class Game:
    def __init__(self):
        pygame.init()
        self.rx= [640,480]
        pygame.display.set_caption('ninja game')
        self.screen = pygame.display.set_mode(self.rx, pygame.RESIZABLE)
        self.rr = [self.screen.get_width()/2, self.screen.get_height()/2]
        self.display = pygame.Surface(self.rr, pygame.SRCALPHA)
        self.display_2 = pygame.Surface(self.rr)
        
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]

        self.assets = {
            'grass': load_images('tiles/grass'),
            'stone': load_images('tiles/stone'),
            'decor': load_images('tiles/decor'),
            'large_decor': load_images('tiles/large_decor'),
            'player': load_image('entities/player.png'),
            'enemy': load_image('entities/enemy/idle/01.png'),
            'enemy/idle' : Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run' : Animation(load_images('entities/enemy/run'), img_dur=4),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'floor': load_images('level2/floor'),
            'wall': load_images('level2/wall'),
            'background2': load_image('background2.jpg'),
            }
        
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),

        }

        self.sfx['jump'].set_volume(0.1)
        self.sfx['dash'].set_volume(0.1)
        self.sfx['hit'].set_volume(0.1)
        self.sfx['shoot'].set_volume(0.1)



    def update_clouds(self, render_scroll):
        if self.clouds is not None:
            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)
    
    def check_event_game(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_x:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False


    def run(self, background):
        while True:
            self.display.fill((0, 0, 0, 0))
            if background=='background':
                self.display_2.blit(self.assets[background], (0, 0))
            else:
                self.display_2.blit(self.assets[background], (-50, -50))
            self.screenshake = max(0, self.screenshake - 1)

            if self.dead:
                self.dead += 1
                if self.dead>=10:
                    self.transition = min(30, self.transition + 1)
                if self.dead >40:
                    self.__init__()

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level += 1
                    if self.level != 3:
                        next_level = load_level(self.level)
                        next_level.run()
                    else:
                        self.level = 1  
                        game_instance.main_menu()
            if self.transition < 0:
                self.transition += 1

            while True:
                self.scroll[0] += (self.player.rect().centerx  - self.display.get_width() / 2 - self.scroll[0]) / 30
                if self.scroll[0] < 0:
                    self.scroll[0] = 0
                if self.scroll[0] > self.rr[0]:
                    self.scroll[0] = self.rr[0]
                break
                
            while True:
                self.scroll[1] += (self.player.rect().centery  - self.display.get_height() / 2 - self.scroll[1]) / 30
                if self.scroll[1] > self.rr[1]:
                    self.scroll[1] = self.rr[1]
                break
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.update_clouds(render_scroll)
            self.tilemap.render(self.display, offset=render_scroll)


            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0,0))
                enemy.render(self.display, offset = render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)


            #[[x,y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1]- img.get_height() / 2 -render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead +=1
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)

            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)

            self.check_event_game()

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
            
            self.display_2.blit(self.display, (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2 )
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)
            

class lvl1(Game):
    def __init__(self):
        super().__init__()
        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.player = Player(self, (50, 350), (8, 15))
        self.enemies = [Enemy(self, 'enemy',  (300, 350), (8, 15)), 
                        Enemy(self, 'enemy', (230, 200), (8, 15)), 
                        Enemy(self, 'enemy', (185, 415), (8, 15)),  
                        Enemy(self, 'enemy', (360, 415), (8, 15)),
                        Enemy(self, 'enemy', (420, 365), (8, 15)),
                        Enemy(self, 'enemy', (590, 335), (8, 15)),
                        Enemy(self, 'enemy', (388, 225), (8, 15)),]
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.projectiles = []
        self.dead = 0
        self.tick = 0
        self.scroll = [0, 0] #camera pos
        self.screenshake = 0
        self.level = 1
        self.transition = -30
    
    def run(self):
        super().run(background='background')


class lvl2(Game):
    def __init__(self):
        super().__init__()
        self.player = Player(self, (5,350), (8,15))
        self.enemies = [Enemy(self, 'enemy', (100,350), (8,15)), 
                        Enemy(self, 'enemy', (400,350), (8,15)),
                        Enemy(self, 'enemy', (51, 205), (8, 15)),
                        Enemy(self, 'enemy', (240, 320), (8, 15)),
                        Enemy(self, 'enemy', (375, 400), (8, 15))
                        ]
        self.tilemap = Tilemap2(self, tile_size=16)
        self.projectiles = []
        self.dead = 0
        self.tick = 0 
        self.scroll = [0,0]
        self.screenshake = 0
        self.clouds = None
        self.level = 2
        self.transition = -30

    def run(self):
        super().run(background='background2')


class Menu(Game):
    def __init__(self):
        self.music_on = True
        self.game = Game()
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        super().__init__()


    def main_menu(self):
        def set_music(value, value2):
            if value2 == 2:
                self.music_on = False
                pygame.mixer.music.stop()
            if value2 == 1:
                self.music_on = True
                pygame.mixer.music.load('data/music.wav')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
        def start_the_game():
            g = lvl1()
            g.run()

        def sound_menu():
            mainmenu._open(sound)

        mainmenu = pygame_menu.Menu('Welcome', self.rx[0], self.rx[1], theme=themes.THEME_SOLARIZED)
        mainmenu.add.button('Play', start_the_game)
        mainmenu.add.button('Sound', sound_menu)
        mainmenu.add.button('Quit', pygame_menu.events.EXIT)

        sound = pygame_menu.Menu('Sound', self.rx[0], self.rx[1], theme=themes.THEME_BLUE)
        sound.add.selector('Music :', [('On', 1), ('Off', 2)], onchange=set_music)

        mainmenu.mainloop(self.game.screen)

game_instance = Menu()
game_instance.main_menu()