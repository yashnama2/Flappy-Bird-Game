import pygame
import sys
import time
from pygame import mixer
from bird import Bird
from pipe import Pipe
pygame.init()
mixer.init()

class Game:
    def __init__(self):
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.move_speed = 200
        self.bird = Bird(self.scale_factor)
        self.start_monitoring = False
        self.is_enter_pressed = False
        self.is_game_started = True
        self.pipes = []
        self.pipe_generate_counter = 71
        self.score = 0
        self.font = pygame.font.Font("assets/font.ttf", 24)
        self.score_text = self.font.render("Score: 0 ", True, (255,255,255))
        self.score_rect = self.score_text.get_rect(center=(100,30))
        self.restart_text = self.font.render("Restart", True, (0,0,0))
        self.restart_rect = self.restart_text.get_rect(center=(300,700))
        mixer.music.load("assets/sfx/flap.wav")
        mixer.music.set_volume(0.7)
        self.setUpBgAndGround()

        self.gameLoop()


    def gameLoop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time-last_time
            last_time = new_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.is_game_started:
                    if event.key == pygame.K_RETURN:
                        self.is_enter_pressed = True
                    if event.key == pygame.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)
                        mixer.music.play()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.restart_rect.collidepoint(pygame.mouse.get_pos()):
                        self.restartGame()

            self.updateEverything(dt)
            self.checkCollision()
            self.checkScore()
            self.drawEverything()    
            pygame.display.update() 
            self.clock.tick(60)           

    def restartGame(self):
        self.score = 0
        self.score_text = self.font.render("Score: 0 ", True, (255,255,255))
        self.is_enter_pressed = False
        self.is_game_started = True
        self.pipe_generate_counter = 71
        self.bird.update_on = True
        self.bird.resetPos()
        self.pipes.clear()

    def checkScore(self):
        if len(self.pipes)>0:
            if (self.bird.rect.left>self.pipes[0].rect_up.left and self.bird.rect.right < self.pipes[0].rect_up.right and not self.start_monitoring):
                self.start_monitoring = True
            if self.bird.rect.left > self.pipes[0].rect_up.right and self.start_monitoring:
                self.start_monitoring = False
                self.score += 1
                self.score_text = self.font.render(f"Score: {self.score} ", True, (255,255,255))

    def checkCollision(self):
        if len(self.pipes):
            if (self.bird.rect.bottom>568 or self.bird.rect.colliderect(self.pipes[0].rect_up) or 
                self.bird.rect.colliderect(self.pipes[0].rect_down)):
                self.bird.update_on = False
                self.is_enter_pressed = False
                self.is_game_started = False
                
    def updateEverything(self, dt):
        if self.is_enter_pressed:

            self.ground1_rect.x -= int(self.move_speed*dt)
            self.ground2_rect.x -= int(self.move_speed*dt)

            if self.ground1_rect.right<0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right<0:
                self.ground2_rect.x = self.ground1_rect.right

            if self.pipe_generate_counter > 70:
                self.pipes.append(Pipe(self.scale_factor,self.move_speed))
                self.pipe_generate_counter = 0
            self.pipe_generate_counter += 1

            for pipe in self.pipes:
                pipe.update(dt)

            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)

            self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_image, (0, -300))  
        for pipe in self.pipes:
            pipe.draw(self.win)
        self.win.blit(self.ground1_image, self.ground1_rect)
        self.win.blit(self.ground2_image, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)
        self.win.blit(self.score_text, self.score_rect)
        if not self.is_game_started:
            self.win.blit(self.restart_text, self.restart_rect)
        

    def setUpBgAndGround(self):
        self.bg_image = pygame.transform.scale_by(pygame.image.load("assets/bg.png").convert(),self.scale_factor)
        self.ground1_image = pygame.transform.scale_by(pygame.image.load("assets/ground.png").convert(),self.scale_factor)
        self.ground2_image = pygame.transform.scale_by(pygame.image.load("assets/ground.png").convert(),self.scale_factor)
        self.ground1_rect = self.ground1_image.get_rect()
        self.ground2_rect = self.ground1_image.get_rect()
        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568
        
game = Game()        