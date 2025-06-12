import pygame
import Product_Storage as PS

# Screen dimensions and frame rate
WIDTH = 600
HEIGHT = 970
FPS = 144

# Load and scale images
WENDING_MACHINE_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Main Body.png")
WENDING_MACHINE_IMAGE = pygame.transform.scale(WENDING_MACHINE_IMAGE, (WIDTH, HEIGHT))

RACK_IMAGE = pygame.image.load("src/assets/Wending Machine/rack_inside without product.png")
RACK_IMAGE = pygame.transform.scale(RACK_IMAGE, (WIDTH, HEIGHT))

PANEL_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Panel.png")

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wending Machine")
clock = pygame.time.Clock()

# Panel and rack state
panel_opened = False
rack_opened = False

# Clickable areas (positions)
RACK_POSITION = pygame.Rect(32, 166, 438 - 32, 793 - 166)           # Rack area
PANEL_POSITION = pygame.Rect(456, 386, 588 - 456, 558 - 386)        # Panel button area

# Button areas inside the panel
BUTTON_POSITION = (
    pygame.Rect(36, 32, 150 - 36, 150 - 32),     # Button 1
    pygame.Rect(191, 30, 305 - 191, 147 - 30),   # Button 2
    pygame.Rect(350, 33, 466 - 350, 149 - 33),   # Button 3
    pygame.Rect(34, 191, 151 - 34, 310 - 191),   # Button 4
    pygame.Rect(191, 191, 304 - 191, 306 - 191), # Button 5
    pygame.Rect(352, 193, 460 - 352, 303 - 193), # Button 6
    pygame.Rect(38, 354, 147 - 38, 463 - 354),   # Button 7
    pygame.Rect(195, 350, 301 - 195, 465 - 350), # Button 8
    pygame.Rect(353, 355, 461 - 353, 457 - 355), # Button 9
)

def Rack():
    # Координаты для отрисовки продуктов (пример, можно настроить по кнопкам)
    product_positions = [
        (-5, 20),  # позиция для первого продукта
        (60, 20), # второго
        (110, 20),
        (160, 20),
        (210, 20),
        (260, 20),
        (310, 20),
        (360, 20),
        (410, 20),
    ]

    # Индекс для позиции продукта
    pos_index = 0

    # Проходим по всем продуктам из базы данных (PS.drinks)
    for product_name, product_info in PS.drinks.items():
        # Проверяем наличие (count > 0)
        if product_info["count"] > 0:
            # Загружаем изображение продукта
            product_image = pygame.image.load(product_info["src"])
            # Масштабируем изображение до размера, например, 100x100
            product_image = pygame.transform.scale(product_image, (90, 100))

            # Берем позицию для отрисовки из списка product_positions
            if pos_index < len(product_positions):
                x, y = product_positions[pos_index]
                # Отрисовываем изображение продукта на экране
                screen.blit(product_image, (x, y))
                pos_index += 1
            else:
                # Если продуктов больше, чем позиций, можно прекратить
                break



# Handle mouse clicks and key presses
def mouse_click_handler(events):
    global panel_opened, rack_opened

    for event in events:
        # Close panel or rack if ESC or ENTER is pressed
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            panel_opened = False
            rack_opened = False

        # Mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # Check if the panel area was clicked
            if PANEL_POSITION.collidepoint(x, y):
                panel_opened = True

            # Check if the rack area was clicked
            if RACK_POSITION.collidepoint(x, y):
                rack_opened = True

            # If panel is open, check which button was clicked
            if panel_opened:
                for i, rect in enumerate(BUTTON_POSITION):
                    if rect.collidepoint(x, y):
                        print("Button pressed:", i + 1)

            

    # Display rack overlay
    if rack_opened:
        screen.blit(RACK_IMAGE, (0, 0))
        Rack()
        

    # Display panel overlay
    if panel_opened:
        screen.blit(PANEL_IMAGE, (0, 0))

# Main game loop
running = True
while running:
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Draw base vending machine
    screen.blit(WENDING_MACHINE_IMAGE, (0, 0))

    # Handle clicks and overlays
    mouse_click_handler(events)

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Exit Pygame
pygame.quit()
