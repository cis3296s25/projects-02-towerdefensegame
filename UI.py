import pygame
import sys #required for .exe creation

def homescreen(screen):
    #fonts
    title_font = pygame.font.SysFont("Arial", 60)
    smaller_font = pygame.font.SysFont("Arial", 20)
    #title
    title_text = title_font.render("My Tower Defense", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30))
    #instruction
    start_text = smaller_font.render("Press SPACE or Click to Start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
    
    screen.fill((0, 0, 0))
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    pygame.display.flip()

def pause_screen(screen, mixer):
    mixer.music.pause() 

    # Create a transparent overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  
    overlay.fill((0, 0, 0, 150))  
    font = pygame.font.SysFont("Arial", 50)
    pause_text = font.render("Game Paused", True, (255, 255, 255))
    resume_text = pygame.font.SysFont("Arial", 30).render("Press ESC to Resume", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
    screen.blit(overlay, (0, 0))  
    screen.blit(pause_text, pause_rect)
    screen.blit(resume_text, resume_rect)
    pygame.display.flip() 

    # Pause gameloop
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    paused = False
    
    mixer.music.unpause()

def draw_sidebar(screen, lives):
    pygame.draw.rect(screen, (50, 50, 50), (600, 0, 150, 400))
    
    font = pygame.font.SysFont("Arial", 18)
    
    # text
    text_Lives = font.render(f"Lives: {lives}", True, (255, 255, 255))
    text_Money = font.render("Money: 69", True, (255, 255, 255))  # (text, antialias, color, background=None)
    text_tower = font.render("Towers", True, (255, 255, 255))  
    
    screen.blit(text_Lives, (610, 10))  # Position the Money text
    screen.blit(text_Money, (610, 30))  # Position the Money text
    screen.blit(text_tower, (610, 60))  # Position the Tower text
    pygame.draw.line(screen, (255, 255, 255), (610, 85), (740, 85), 1) # Draw a line below the Tower text (surface, color, start_pos, end_pos, width)

def draw_grid(screen):
    grid_surface = pygame.Surface((800, 600), pygame.SRCALPHA)  # Create a transparent surface
    grid_surface.set_alpha(15)  # Set transparency (0 = fully transparent, 255 = fully opaque)

    for x in range(0, 600, 40):
        for y in range(0, 600, 40):
            pygame.draw.rect(grid_surface, (255, 255, 255, 100), (x, y, 40, 40), 1)  # Draw on transparent surface

    screen.blit(grid_surface, (0, 0))
    
