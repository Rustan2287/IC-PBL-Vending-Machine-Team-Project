# 진열대 Y 좌표 값 설정 (모든 음료의 Y 좌표는 동일)
RACK_Y = 20

# 음료 진열대 각 칸의 위치 좌표 (X, Y) 딕셔너리
Rack_Number = {
    "1": (0, RACK_Y),       # 1번 칸 위치 (왼쪽 끝)
    "2": (70, RACK_Y),      # 2번 칸 위치
    "3": (150, RACK_Y),     # 3번 칸 위치
    "4": (220, RACK_Y),     # 4번 칸 위치
    "5": (300, RACK_Y),     # 5번 칸 위치
    "6": (370, RACK_Y),     # 6번 칸 위치
    "7": (320, RACK_Y)      # 7번 칸 위치 (6번과 X 좌표가 겹침, 수정 필요)
}

# 음료 정보 딕셔너리
drinks = {
    "fanta": {
        "price": 1900,                      # 가격 (원)
        "src": "src/assets/Product/fanta.jpg",  # 이미지 경로
        "count": 1,                        # 재고 수량
        "position": Rack_Number["1"],      # 진열 위치 좌표 (1번 칸)
        "number": "1"                      # 음료 번호 (고유 식별자)
    },
    "fanta_pain": {
        "price": 1900,
        "src": "src/assets/Product/fanta pain.jpg",
        "count": 20,
        "position": Rack_Number["2"],      # 2번 칸 위치
        "number": "2"
    },
    "Milks": {
        "price": 1900,
        "src": "src/assets/Product/Milks.jpg",
        "count": 20,
        "position": Rack_Number["3"],      # 3번 칸 위치
        "number": "3"
    },
    "pepsi": {
        "price": 1900,
        "src": "src/assets/Product/pepsi.jpg",
        "count": 20,
        "position": Rack_Number["4"],      # 4번 칸 위치
        "number": "4"
    },
    "pocari": {
        "price": 1900,
        "src": "src/assets/Product/pocari.jpg",
        "count": 20,
        "position": Rack_Number["5"],      # 5번 칸 위치
        "number": "5"
    },
    "Sprite": {
        "price": 1900,
        "src": "src/assets/Product/Sprite.jpg",
        "count": 20,
        "position": Rack_Number["6"],      # 6번 칸 위치
        "number": "6"
    }
}
