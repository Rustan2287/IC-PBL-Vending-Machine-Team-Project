import pygame

WIDTH = 600
HEIGHT = 970
FPS = 144

WENDING_MACHINE_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Main Body.png")
WENDING_MACHINE_IMAGE = pygame.transform.scale(WENDING_MACHINE_IMAGE, (WIDTH, HEIGHT))
PANEL_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Panel.png")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wending Machine")
clock = pygame.time.Clock()

panel_opened = False

BUTTON_POSITION = (
    pygame.Rect(36, 32, 150 - 36, 150 - 32),     # Button1
    pygame.Rect(191, 30, 305 - 191, 147 - 30),   # Button2
    pygame.Rect(350, 33, 466 - 350, 149 - 33),   # Button3
    pygame.Rect(34, 191, 151 - 34, 310 - 191),   # Button4
    pygame.Rect(191, 191, 304 - 191, 306 - 191), # Button5
    pygame.Rect(352, 193, 460 - 352, 303 - 193), # Button6
    pygame.Rect(38, 354, 147 - 38, 463 - 354),   # Button7
    pygame.Rect(195, 350, 301 - 195, 465 - 350), # Button8
    pygame.Rect(353, 355, 461 - 353, 457 - 355), # Button9
)

def panel(events):
    global panel_opened
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if 456 <= x <= 588 and 386 <= y <= 558:
                panel_opened = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            panel_opened = False
    if panel_opened:
        screen.blit(PANEL_IMAGE, (0, 0))

def get_pressed_button(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i, rect in enumerate(BUTTON_POSITION):
                if rect.collidepoint(x, y):
                    return i + 1
    return None

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.blit(WENDING_MACHINE_IMAGE, (0, 0))
    panel(events)
    pressed = get_pressed_button(events)
    if pressed:
        print("you pressed:", pressed)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
