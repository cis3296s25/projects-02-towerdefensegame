import pygame
import pygame as pg

class Button:
    def __init__(self, x, y, image, single_click, tower_name="None", tooltip_text=None, w_ratio = 1, h_ratio = 1):
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.single_click = single_click
        self.name = tower_name  
        self.x = x
        self.y = y

        self.tooltip_text = tooltip_text  # Tooltip text
        self.font = pg.font.Font(None, 20 * h_ratio)  # Font for the tooltip
        self.tooltip_bg = (0,0,0)  # Background color for the tooltip
        self.tooltip_fg = (255, 255, 255)  # Foreground color for the tooltip
        self.w_ratio = w_ratio 
        self.h_ratio = h_ratio
        

    def draw(self, screen, show_stats=False):
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
        if not show_stats and self.rect.collidepoint(pos) and self.tooltip_text and self.font:
            self.draw_tooltip(screen, (-5, 395))
        
        return action # Return if the button was clicked
    
    def draw_tooltip(self, screen, pos):
        # Scale font size dynamically using h_ratio
        scaled_font_size = int(20 * self.h_ratio)  # Base font size is 20
        font = pg.font.Font(None, scaled_font_size)

        # Split the tooltip text into multiple lines
        lines = self.tooltip_text.split("\n")
        
        # Calculate the width and height of the tooltip box
        max_width = max(font.size(line)[0] for line in lines)  # Find the widest line
        total_height = sum(font.size(line)[1] for line in lines) + (len(lines) - 1) * int(5 * self.h_ratio)  # Add scaled spacing between lines

        # Scale the tooltip position using w_ratio and h_ratio
        tooltip_x = int(pos[0] * self.w_ratio) + int(10 * self.w_ratio)
        tooltip_y = int(pos[1] * self.h_ratio) + int(10 * self.h_ratio)

        # Create a rectangle for the tooltip background
        tooltip_rect = pg.Rect(tooltip_x, tooltip_y, max_width + int(10 * self.w_ratio), total_height + int(10 * self.h_ratio))

        # Draw the background rectangle
        pg.draw.rect(screen, self.tooltip_bg, tooltip_rect)
        pg.draw.rect(screen, (255, 255, 255), tooltip_rect, 1)  # Optional: Add a border

        # Render and draw each line of text
        y_offset = tooltip_rect.y + int(5 * self.h_ratio)
        for line in lines:
            line_surface = font.render(line, True, self.tooltip_fg)
            screen.blit(line_surface, (tooltip_rect.x + int(5 * self.w_ratio), y_offset))
            y_offset += font.size(line)[1] + int(5 * self.h_ratio)
            
    def resize(self, w_ratio, h_ratio):
            self.image = pg.transform.scale(self.original_image,(int(self.original_image.get_width() * w_ratio), int(self.original_image.get_height() * h_ratio)))
            self.rect = self.image.get_rect(topleft=(self.x * w_ratio, self.y * h_ratio))
            
        