import pygame as pg

class Button:
    def __init__(self, x, y, image, single_click, tower_name="None", tooltip_text=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.single_click = single_click
        self.name = tower_name  

        self.tooltip_text = tooltip_text  # Tooltip text
        self.font = pg.font.Font(None, 15)  # Font for the tooltip
        self.tooltip_bg = (0,0,0)  # Background color for the tooltip
        self.tooltip_fg = (255, 255, 255)  # Foreground color for the tooltip
        

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

        # Draw tooltip if hovering
        if self.rect.collidepoint(pos) and self.tooltip_text and self.font:
            self.draw_tooltip(screen, pos)
        
        return action
    
    def draw_tooltip(self, screen, pos):
        # Split the tooltip text into multiple lines
        lines = self.tooltip_text.split("\n")
        
        # Calculate the width and height of the tooltip box
        max_width = max(self.font.size(line)[0] for line in lines)  # Find the widest line
        total_height = sum(self.font.size(line)[1] for line in lines) + (len(lines) - 1) * 5  # Add spacing between lines

        # Create a rectangle for the tooltip background
        tooltip_rect = pg.Rect(pos[0] + 10, pos[1] + 10, max_width + 10, total_height + 10)

        # Draw the background rectangle
        pg.draw.rect(screen, self.tooltip_bg, tooltip_rect)
        pg.draw.rect(screen, (255, 255, 255), tooltip_rect, 1)  # Optional: Add a border

        # Render and draw each line of text
        y_offset = tooltip_rect.y + 5
        for line in lines:
            line_surface = self.font.render(line, True, self.tooltip_fg)
            screen.blit(line_surface, (tooltip_rect.x + 5, y_offset))
            y_offset += self.font.size(line)[1] + 5  # Move to the next line
            
        