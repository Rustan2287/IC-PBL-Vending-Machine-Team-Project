import pygame
import Product_Storage as PS
import Brain
import sys

# 화면 크기와 프레임 속도
WIDTH = 600
HEIGHT = 970
FPS = 144

# 이미지 불러오기 및 크기 조절
WENDING_MACHINE_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Main Body.png")
WENDING_MACHINE_IMAGE = pygame.transform.scale(WENDING_MACHINE_IMAGE, (WIDTH, HEIGHT))
SOLD_OUT_IMAGE = pygame.image.load("src/assets/Product/sold out.png")

RACK_IMAGE = pygame.image.load("src/assets/Wending Machine/rack_inside without product.png")
RACK_IMAGE = pygame.transform.scale(RACK_IMAGE, (WIDTH, HEIGHT))

PANEL_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Panel.png")

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("자동판매기")  # "Wending Machine" → "자동판매기"
clock = pygame.time.Clock()

# 폰트 설정
font_path = "C:\\Users\\HENTAI\\Desktop\\IC-PBL-Vending-Machine-Team-Project\\src\\fonts\\Nanum_Gothic\\NanumGothic-Regular.ttf"
font = pygame.font.Font(font_path, 50)


# 패널과 선반 상태
panel_opened = False
rack_opened = False
payment_mode = False
selected_number = ""
payMethod = None
user_card_balance= 500000
total_inserted = 0

# 클릭 가능한 영역
RACK_POSITION = pygame.Rect(32, 166, 438 - 32, 793 - 166)
PANEL_POSITION = pygame.Rect(456, 386, 588 - 456, 558 - 386)

# 패널 버튼 위치들
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

# 결제 버튼 영역
cash_button = pygame.Rect(100, 600, 180, 80)
card_button = pygame.Rect(320, 600, 180, 80)

def choose_cash():
    cash_font = pygame.font.Font(font_path, 40)

    btn_1000 = pygame.Rect(100, 700, 120, 60)
    btn_5000 = pygame.Rect(240, 700, 120, 60)
    btn_10000 = pygame.Rect(380, 700, 120, 60)
    btn_pay = pygame.Rect(200, 800, 200, 60)

    total_inserted = 0

    while True:
        screen.fill((255, 255, 255))  # 화면 초기화 (또는 배경 삽입)
        screen.blit(WENDING_MACHINE_IMAGE, (0, 0))

        # 버튼 그리기
        pygame.draw.rect(screen, (220, 220, 220), btn_1000)
        pygame.draw.rect(screen, (200, 200, 250), btn_5000)
        pygame.draw.rect(screen, (250, 200, 200), btn_10000)
        pygame.draw.rect(screen, (180, 255, 180), btn_pay)

        # 버튼에 표시할 텍스트
        text_1000 = cash_font.render("1000원", True, (0, 0, 0))
        text_5000 = cash_font.render("5000원", True, (0, 0, 0))
        text_10000 = cash_font.render("10000원", True, (0, 0, 0))
        pay_text = cash_font.render("결제", True, (0, 0, 0))

        screen.blit(text_1000, (btn_1000.x + 10, btn_1000.y + 15))
        screen.blit(text_5000, (btn_5000.x + 10, btn_5000.y + 15))
        screen.blit(text_10000, (btn_10000.x + 10, btn_10000.y + 15))
        screen.blit(pay_text, (btn_pay.x + 10, btn_pay.y + 15))

        # 현재 투입 금액 표시
        total_text = cash_font.render(f"현재 투입 금액: {total_inserted}원", True, (0, 0, 0))
        screen.blit(total_text, (150, 650))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_1000.collidepoint(event.pos):
                    total_inserted += 1000
                elif btn_5000.collidepoint(event.pos):
                    total_inserted += 5000
                elif btn_10000.collidepoint(event.pos):
                    total_inserted += 10000
                elif btn_pay.collidepoint(event.pos):
                    return total_inserted

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

    cash_text = font.render("현금", True, (0, 0, 0))
    card_text = font.render("카드", True, (0, 0, 0))

    screen.blit(cash_text, (cash_button.x + 10, cash_button.y + 20))
    screen.blit(card_text, (card_button.x + 10, card_button.y + 20))

def mouse_click_handler(events):
    global panel_opened, rack_opened, selected_number, payment_mode, payMethod, user_card_balance

    for event in events:
        # ESC 키 눌렀을 때
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                panel_opened = False
                rack_opened = False
                payment_mode = False

            # 엔터키 눌렀을 때 – 음료 선택 확정
            if event.key == pygame.K_RETURN and panel_opened and selected_number:
                print("음료 선택됨:", selected_number)
                payment_mode = True
                panel_opened = False

        # 마우스 클릭 처리
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # 결제 방법 선택
            if payment_mode:
                if cash_button.collidepoint(x, y):
                    payMethod = "cash"
                    print("현금 결제 선택됨")

                    cash = choose_cash()  # 지폐 선택
                    print(f"입금한 금액: {cash}원")

                    payment_mode = False
                    rack_opened = False
                    Brain.select(selected_number, payMethod, cash)  # 금액 전달
                    selected_number = ""
                    return  # 클릭 처리 종료

                elif card_button.collidepoint(x, y):
                    payMethod = "card"
                    print("카드 결제 선택됨")
                    payment_mode = False
                    rack_opened = False
                    Brain.select(selected_number, payMethod, user_card_balance)
                    selected_number = ""  # 결제 후 선택 초기화
                    return  # 클릭 처리 종료

            # 패널 / 선반 열기
            if PANEL_POSITION.collidepoint(x, y):
                panel_opened = True
                rack_opened = False

            elif RACK_POSITION.collidepoint(x, y) and not panel_opened and not payment_mode:
                rack_opened = True
                panel_opened = False

            # 패널 버튼 클릭
            if panel_opened:
                for i, rect in enumerate(BUTTON_POSITION):
                    if rect.collidepoint(x, y):
                        selected_number += str(i + 1)
                        if len(selected_number) > 2:
                            selected_number = selected_number[-2:]  # 최근 두 자리만 유지
                        print("현재 입력:", selected_number)

    # 오버레이 표시
    if panel_opened:
        screen.blit(PANEL_IMAGE, (0, 0))
    if rack_opened:
        screen.blit(RACK_IMAGE, (0, 0))
        Rack()

# 메인 루프
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
