import pygame

WIDTH = 600
HEIGHT = 970
FPS = 144

# Wending Machine Image
WENDING_MACHINE_IMAGE = pygame.image.load("src/assets/Wending Machine Main Body.png")
WENDING_MACHINE_IMAGE = pygame.transform.scale(WENDING_MACHINE_IMAGE, (WIDTH, HEIGHT))

# Panel Image
PANEL_IMAGE = pygame.image.load("src/assets/Wending Machine Panel.png")

# Game Window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wending Machine")
clock = pygame.time.Clock()

panel_opened = False

def is_panel_clicked(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if 456 <= x <= 588 and 386 <= y <= 558:
                return True
    return False

def draw_panel():
    if panel_opened:
        screen.blit(PANEL_IMAGE, (0, 0))

# Game Loop
running = True
while running:
    events = pygame.event.get() #Get Events

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Check if the panel should be opened
    if is_panel_clicked(events):
        panel_opened = True  # Open the panel when clicked

    # draw the background image
    screen.blit(WENDING_MACHINE_IMAGE, (0, 0))

    # draw the panel if it is opened
    draw_panel()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
