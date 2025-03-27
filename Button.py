import pygame as pg

class Button:
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.single_click = single_click
        

    def draw(self, screen):
        action = False
        # get mouse position   
        pos = pg.mouse.get_pos()
        
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False: #check if left mouse button is clicked
                action = True
                if self.single_click:
                    self.clicked = True
                
        if pg.mouse.get_pressed()[0] == 0: #check if left mouse button is unclicked
            self.clicked = False
                
        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
        
    