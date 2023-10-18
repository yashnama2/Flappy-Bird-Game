import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, scale_factor):
        super(Bird,self).__init__()
        self.img_list = [pygame.transform.scale_by(pygame.image.load("assets/birdup.png").convert_alpha(), scale_factor),
                         pygame.transform.scale_by(pygame.image.load("assets/birddown.png").convert_alpha(), scale_factor)]
        self.img_index = 0
        self.image = self.img_list[self.img_index]
        self.rect = self.image.get_rect(center=(100,100))
        self.y_velocity = 0
        self.gravity = 10
        self.flap_speed = 200
        self.anim_counter = 0
        self.update_on = True

    def update(self, dt):
        if self.update_on:
            self.playAnimation()
            self.applyGravity(dt)
            if self.rect.y<0:
                self.rect.y = 0

    def applyGravity(self,dt):
        
        self.y_velocity += self.gravity*dt
        self.rect.y += self.y_velocity

    def flap(self,dt):
        self.y_velocity =- int(self.flap_speed*dt)

    def playAnimation(self):
        if self.anim_counter == 5:
            self.image = self.img_list[self.img_index]
            if self.img_index == 0: 
                self.img_index = 1
            else: self.img_index = 0
            self.anim_counter = 0

        self.anim_counter += 1

    def resetPos(self):
        self.rect.center = (100,100)
        self.y_velocity = 0