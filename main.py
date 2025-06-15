import pygame
import Product_Storage as PS
import Brain
import sys

# Screen dimensions and frame rate
WIDTH = 600
HEIGHT = 970
FPS = 144

# Load and scale images
WENDING_MACHINE_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Main Body.png")
WENDING_MACHINE_IMAGE = pygame.transform.scale(WENDING_MACHINE_IMAGE, (WIDTH, HEIGHT))
SOLD_OUT_IMAGE = pygame.image.load("src/assets/Product/sold out.png")

RACK_IMAGE = pygame.image.load("src/assets/Wending Machine/rack_inside without product.png")
RACK_IMAGE = pygame.transform.scale(RACK_IMAGE, (WIDTH, HEIGHT))

PANEL_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Panel.png")

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wending Machine")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 50)

# Panel and rack state
panel_opened = False
rack_opened = False
payment_mode = False
selected_number = ""
payMethod = None
user_card_balance= 500000
user_cash_balance = 0

# Clickable areas
RACK_POSITION = pygame.Rect(32, 166, 438 - 32, 793 - 166)
PANEL_POSITION = pygame.Rect(456, 386, 588 - 456, 558 - 386)

# Panel button positions
BUTTON_POSITION = (
    pygame.Rect(36, 32, 150 - 36, 150 - 32),
    pygame.Rect(191, 30, 305 - 191, 147 - 30),
    pygame.Rect(350, 33, 466 - 350, 149 - 33),
    pygame.Rect(34, 191, 151 - 34, 310 - 191),
    pygame.Rect(191, 191, 304 - 191, 306 - 191),
    pygame.Rect(352, 193, 460 - 352, 303 - 193),
    pygame.Rect(38, 354, 147 - 38, 463 - 354),
    pygame.Rect(195, 350, 301 - 195, 465 - 350),
    pygame.Rect(353, 355, 461 - 353, 457 - 355),
)

# Payment buttons
cash_button = pygame.Rect(100, 600, 180, 80)
card_button = pygame.Rect(320, 600, 180, 80)

def Rack():
    for product_name, product_info in PS.drinks.items():
        if product_info["count"] > 0:
            product_image = pygame.image.load(product_info["src"])
            product_image = pygame.transform.scale(product_image, (90, 100))
            x, y = product_info["position"]
            screen.blit(product_image, (x, y))
        else:
            x, y = product_info["position"]
            screen.blit(pygame.transform.scale(SOLD_OUT_IMAGE, (90, 100)), (x, y))

def draw_payment_buttons():
    pygame.draw.rect(screen, (200, 200, 200), cash_button)
    pygame.draw.rect(screen, (200, 200, 200), card_button)

    cash_text = font.render("Cash (현금)", True, (0, 0, 0))
    card_text = font.render("Card (카드)", True, (0, 0, 0))

    screen.blit(cash_text, (cash_button.x + 10, cash_button.y + 20))
    screen.blit(card_text, (card_button.x + 10, card_button.y + 20))

def mouse_click_handler(events):
    global panel_opened, rack_opened, selected_number, payment_mode, payMethod, user_card_balance

    for event in events:
        # Нажатие ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                panel_opened = False
                rack_opened = False
                payment_mode = False

            # Нажатие Enter – подтверждение выбора напитка
            if event.key == pygame.K_RETURN and panel_opened and selected_number:
                print("Напиток выбран:", selected_number)
                payment_mode = True
                panel_opened = False

        # Нажатие мышки
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # Выбор способа оплаты
            if payment_mode:
                if cash_button.collidepoint(x, y):
                    payMethod = "cash"
                    print("Вы выбрали 현금 (Cash)")
                    payment_mode = False
                    rack_opened = False
                    Brain.select(selected_number, payMethod, user_card_balance)
                    return  # ← Остановить обработку клика

                elif card_button.collidepoint(x, y):
                    payMethod = "card"
                    print("Вы выбрали 카드 (Card)")
                    payment_mode = False
                    rack_opened = False
                    Brain.select(selected_number, payMethod, user_card_balance)
                    return  # ← Остановить обработку клика

            # Открытие панели/стойки
            if PANEL_POSITION.collidepoint(x, y):
                panel_opened = True
                rack_opened = False

            elif RACK_POSITION.collidepoint(x, y) and not panel_opened and not payment_mode:
                rack_opened = True
                panel_opened = False

            # Нажатие на кнопку на панели
            if panel_opened:
                for i, rect in enumerate(BUTTON_POSITION):
                    if rect.collidepoint(x, y):
                        selected_number += str(i + 1)
                        if len(selected_number) > 2:
                            selected_number = selected_number[-2:]  # Ограничение до последних двух цифр
                        print("Текущий ввод:", selected_number)

    # Overlay
    if panel_opened:
        screen.blit(PANEL_IMAGE, (0, 0))
    if rack_opened:
        screen.blit(RACK_IMAGE, (0, 0))
        Rack()

# Main loop
running = True
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.blit(WENDING_MACHINE_IMAGE, (0, 0))
    mouse_click_handler(events)

    if payment_mode:
        draw_payment_buttons()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit() 
