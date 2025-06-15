import pygame
import Product_Storage as PS
import Brain
import sys

# 화면 크기 및 FPS 설정
WIDTH = 600  # 화면 가로 크기 (픽셀)
HEIGHT = 970  # 화면 세로 크기 (픽셀)
FPS = 144  # 초당 프레임 수 (게임 속도)

# 이미지 불러오기 및 크기 조절
WENDING_MACHINE_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Main Body.png")  # 자판기 본체 이미지
WENDING_MACHINE_IMAGE = pygame.transform.scale(WENDING_MACHINE_IMAGE, (WIDTH, HEIGHT))  # 이미지 크기 맞춤
SOLD_OUT_IMAGE = pygame.image.load("src/assets/Product/sold out.png")  # 품절 표시 이미지

RACK_IMAGE = pygame.image.load("src/assets/Wending Machine/rack_inside without product.png")  # 선반 이미지 (제품 없음)
RACK_IMAGE = pygame.transform.scale(RACK_IMAGE, (WIDTH, HEIGHT))  # 크기 조절

PANEL_IMAGE = pygame.image.load("src/assets/Wending Machine/Wending Machine Panel.png")  # 조작 패널 이미지

# Pygame 초기화 및 화면 설정
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 윈도우 크기 설정
pygame.display.set_caption("자판기")  # 윈도우 제목 설정
clock = pygame.time.Clock()  # FPS 제어용 클락 객체

# 폰트 설정 (한글 폰트 포함)
font_path = "C:\\Users\\HENTAI\\Desktop\\IC-PBL-Vending-Machine-Team-Project\\src\\fonts\\Nanum_Gothic\\NanumGothic-Regular.ttf"
font = pygame.font.Font(font_path, 50)  # 기본 폰트 크기 50

# 패널과 선반 상태 변수
panel_opened = False  # 조작 패널 열림 여부
rack_opened = False  # 선반 열림 여부
payment_mode = False  # 결제 모드 활성화 여부
selected_number = ""  # 사용자가 입력한 음료 번호
payMethod = None  # 결제 수단 (현금 또는 카드)
user_card_balance = 500000  # 사용자의 카드 잔액 (예시)
total_inserted = 0  # 투입한 현금 총액

# 마우스 클릭을 받을 영역 지정 (Rect 객체)
RACK_POSITION = pygame.Rect(32, 166, 438 - 32, 793 - 166)  # 선반 클릭 영역
PANEL_POSITION = pygame.Rect(456, 386, 588 - 456, 558 - 386)  # 조작 패널 클릭 영역

# 패널 버튼 위치 배열 (숫자 버튼 등)
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

# 결제 버튼 영역 설정 (현금, 카드)
cash_button = pygame.Rect(100, 600, 180, 80)
card_button = pygame.Rect(320, 600, 180, 80)

def choose_cash():
    # 현금 결제 선택 화면
    cash_font = pygame.font.Font(font_path, 20)  # 작은 폰트

    # 현금 버튼 영역 설정 (1000원, 5000원, 10000원, 결제)
    btn_1000 = pygame.Rect(100, 700, 120, 60)
    btn_5000 = pygame.Rect(240, 700, 120, 60)
    btn_10000 = pygame.Rect(380, 700, 120, 60)
    btn_pay = pygame.Rect(200, 800, 200, 60)

    total_inserted = 0  # 초기 투입 금액 0원

    while True:
        screen.fill((255, 255, 255))  # 화면 흰색으로 초기화
        screen.blit(WENDING_MACHINE_IMAGE, (0, 0))  # 자판기 본체 이미지 출력

        # 현금 버튼 그리기 (사각형)
        pygame.draw.rect(screen, (220, 220, 220), btn_1000)
        pygame.draw.rect(screen, (200, 200, 250), btn_5000)
        pygame.draw.rect(screen, (250, 200, 200), btn_10000)
        pygame.draw.rect(screen, (180, 255, 180), btn_pay)

        # 버튼 텍스트 렌더링 및 화면 출력
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

        pygame.display.flip()  # 화면 업데이트

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트
                if btn_1000.collidepoint(event.pos):  # 1000원 버튼 클릭 시
                    total_inserted += 1000
                elif btn_5000.collidepoint(event.pos):  # 5000원 버튼 클릭 시
                    total_inserted += 5000
                elif btn_10000.collidepoint(event.pos):  # 10000원 버튼 클릭 시
                    total_inserted += 10000
                elif btn_pay.collidepoint(event.pos):  # 결제 버튼 클릭 시
                    return total_inserted  # 투입 금액 반환 후 종료

def Rack():
    # 자판기 선반에 있는 제품 표시 함수
    for product_name, product_info in PS.drinks.items():
        if product_info["count"] > 0:  # 재고가 있으면
            product_image = pygame.image.load(product_info["src"])  # 제품 이미지 로드
            product_image = pygame.transform.scale(product_image, (90, 100))  # 이미지 크기 조절
            x, y = product_info["position"]  # 위치 정보
            screen.blit(product_image, (x, y))  # 화면에 그림
        else:
            # 재고가 없으면 품절 이미지 표시
            x, y = product_info["position"]
            screen.blit(pygame.transform.scale(SOLD_OUT_IMAGE, (90, 100)), (x, y))

def draw_payment_buttons():
    # 결제 방법 버튼 그리기
    pygame.draw.rect(screen, (200, 200, 200), cash_button)
    pygame.draw.rect(screen, (200, 200, 200), card_button)

    cash_text = font.render("현금", True, (0, 0, 0))
    card_text = font.render("카드", True, (0, 0, 0))

    screen.blit(cash_text, (cash_button.x + 10, cash_button.y + 20))
    screen.blit(card_text, (card_button.x + 10, card_button.y + 20))

def mouse_click_handler(events):
    global panel_opened, rack_opened, selected_number, payment_mode, payMethod, user_card_balance

    for event in events:
        # 키보드 이벤트 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC 누르면 패널, 선반, 결제모드 닫기
                panel_opened = False
                rack_opened = False
                payment_mode = False

            if event.key == pygame.K_RETURN and panel_opened and selected_number:
                # 엔터 누르면 음료 번호 확정 후 결제 모드 진입
                print("음료 선택됨:", selected_number)
                payment_mode = True
                panel_opened = False

        # 마우스 클릭 이벤트 처리
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # 결제 모드에서 결제 수단 선택
            if payment_mode:
                if cash_button.collidepoint(x, y):  # 현금 버튼 클릭 시
                    payMethod = "cash"
                    print("현금 결제 선택됨")

                    cash = choose_cash()  # 현금 투입 창 호출
                    print(f"입금한 금액: {cash}원")

                    payment_mode = False
                    rack_opened = False
                    Brain.select(selected_number, payMethod, cash)  # 결제 처리 함수 호출
                    selected_number = ""
                    return

                elif card_button.collidepoint(x, y):  # 카드 버튼 클릭 시
                    payMethod = "card"
                    print("카드 결제 선택됨")
                    payment_mode = False
                    rack_opened = False
                    Brain.select(selected_number, payMethod, user_card_balance)  # 카드 결제 처리
                    selected_number = ""
                    return

            # 패널 또는 선반 열기 처리
            if PANEL_POSITION.collidepoint(x, y):
                panel_opened = True
                rack_opened = False

            elif RACK_POSITION.collidepoint(x, y) and not panel_opened and not payment_mode:
                rack_opened = True
                panel_opened = False

            # 패널 버튼 클릭 처리 (숫자 입력)
            if panel_opened:
                for i, rect in enumerate(BUTTON_POSITION):
                    if rect.collidepoint(x, y):
                        selected_number += str(i + 1)  # 버튼 번호를 선택 번호에 추가
                        if len(selected_number) > 2:  # 최근 2자리만 유지
                            selected_number = selected_number[-2:]
                        print("현재 입력:", selected_number)

    # 화면에 오버레이 표시
    if panel_opened:
        screen.blit(PANEL_IMAGE, (0, 0))  # 조작 패널 이미지 표시
    if rack_opened:
        screen.blit(RACK_IMAGE, (0, 0))  # 선반 이미지 표시
        Rack()  # 선반에 제품 그림 표시

# 메인 루프
running = True
while running:
    events = pygame.event.get()  # 이벤트 받기

    for event in events:
        if event.type == pygame.QUIT:  # 창 닫기 이벤트
            running = False

    screen.blit(WENDING_MACHINE_IMAGE, (0, 0))  # 자판기 본체 이미지 출력
    mouse_click_handler(events)  # 입력 이벤트 처리 함수 호출

    if payment_mode:
        draw_payment_buttons()  # 결제 버튼 표시

    pygame.display.flip()  # 화면 업데이트
    clock.tick(FPS)  # FPS 유지

pygame.quit()
sys.exit()
