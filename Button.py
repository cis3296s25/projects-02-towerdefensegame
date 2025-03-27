import pygame as pg

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        action = False
        # get mouse position   
        pos = pg.mouse.get_pos()
        
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                action = True
                
        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
        
    