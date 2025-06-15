import Product_Storage as PS  # 제품 정보가 저장된 모듈 임포트
import os
from datetime import datetime  # 영수증 시간 기록용

# 잔돈 계산 함수: 입력받은 잔돈 금액을 1000원, 500원, 100원 단위로 계산해서 딕셔너리로 반환
def calculate_change(change):
    coins = {"1000": 0, "500": 0, "100": 0}

    coins["1000"] = change // 1000  # 1000원짜리 몇 개?
    change %= 1000                  # 1000원 단위 뺀 나머지

    coins["500"] = change // 500    # 500원짜리 몇 개?
    change %= 500

    coins["100"] = change // 100    # 100원짜리 몇 개?
    change %= 100

    return coins  # 계산된 동전 개수 딕셔너리 반환

# 영수증 생성 함수
# product_name: 상품명, price: 가격, PayMethod: 결제 방법 (현금 or 카드), money: 카드 잔액(카드 결제 시)
def receipt(product_name, price, PayMethod, money=0):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시각 문자열
    filename = f"receipt_{product_name}_{now.replace(':', '-')}.txt"  # 파일명에 시간 포함(파일명에 ':' 사용 불가해서 '-'로 변경)
    
    # receipts 폴더가 없으면 생성
    if not os.path.exists("receipts"):
        os.makedirs("receipts")
    
    filepath = os.path.join("receipts", filename)  # 전체 경로 생성

    with open(filepath, "w", encoding="utf-8") as f:  # UTF-8 인코딩으로 쓰기 모드
        f.write("=== 영수증 ===\n")
        f.write(f"상품명: {product_name}\n")
        f.write(f"가격: {price}₩\n")
        f.write(f"결제 방법: {PayMethod}\n")
        if PayMethod == "card" and money is not None:
            f.write(f"잔액: {money}₩\n")  # 카드 결제 시 남은 잔액 표시
        f.write(f"구매 시간: {now}\n")
        f.write("====================\n")
    print(f"✅ 영수증 저장함: {filepath}")

# 음료 선택 및 결제 처리 함수
# number: 선택한 음료 번호, PayMethod: 결제 방식 ('cash' 또는 'card'), money: 투입 금액 또는 카드 잔액
def select(number, PayMethod=None, money=0):
    selected_product = None

    # 선택한 번호에 해당하는 음료 찾기
    for name, info in PS.drinks.items():
        if info["number"] == number:
            selected_product = info
            product_name = name
            break

    if selected_product is None:
        print("없는 제품을 선택했습니다 (존재하지 않는 제품 선택)")
        return
    
    price = selected_product["price"]

    # 재고가 있는 경우에만 결제 진행
    if selected_product["count"] != 0:
        if PayMethod == "cash":
            # 현금 투입액이 가격보다 적으면 실패
            if money < price:
                print("현금 부족")
            else:
                change = money - price  # 잔돈 계산
                selected_product["count"] -= 1  # 재고 차감
                print(f"구매완료 {product_name} 가격 {price}₩ (남은 재고: {selected_product['count']}개)")
                receipt(product_name, price, PayMethod)  # 영수증 출력

                if change > 0:
                    coins = calculate_change(change)  # 잔돈 동전별 계산
                    print(f"잔돈: {change}₩")
                    print(f" - 1000원: {coins['1000']}개")
                    print(f" - 500원: {coins['500']}개")
                    print(f" - 100원: {coins['100']}개")
                else:
                    print("잔돈 없음")

        elif PayMethod == "card":
            # 카드 잔액이 충분한지 확인
            if money >= price:
                money -= price  # 결제 후 잔액 차감
                selected_product["count"] -= 1  # 재고 차감
                print(f"카드 결제 성공. 카드 잔액: {money}₩")
                print(f"구매완료 {product_name} (남은 재고: {selected_product['count']}개)")
                receipt(product_name, price, PayMethod, money)  # 영수증 출력 및 잔액 포함
            else:
                print("카드 잔액 부족")

        else:
            print("결제 방법이 선택되지 않음")
    else:
        print("상품 매진")
