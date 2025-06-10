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
rack_opened = False

RACK_POSITION = pygame.Rect(32, 166, 438 - 32, 793 - 166)
PANEL_POSITION = pygame.Rect(456, 386, 588 - 456, 558 - 386)
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

def mouse_click_handler(events):
    global panel_opened

    for event in events:
        #escape from panel
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            panel_opened = False

        #Checking click on the panel
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            #Checking if clicked on panel or rack or card reader or cash reader
            if PANEL_POSITION.collidepoint(x, y): #Panel
                panel_opened = True

            if RACK_POSITION.collidepoint(x, y): #Rack
                rack_opened = True  

            #Clicked on the Panel
            if panel_opened:
                for i, rect in enumerate(BUTTON_POSITION):
                    if rect.collidepoint(x, y):
                        print("Ты нажал кнопку:", i + 1)
            
            #Clicked on the Rack
            if rack_opened:
                pass

    if panel_opened:
        screen.blit(PANEL_IMAGE, (0, 0))

#Main
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.blit(WENDING_MACHINE_IMAGE, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
