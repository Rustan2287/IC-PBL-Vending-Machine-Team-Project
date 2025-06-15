import Product_Storage as PS
import os
from datetime import datetime

def receipt(product_name, price, PayMethod, user_card_balance=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"receipt_{product_name}_{now.replace(':', '-')}.txt"
    # Убедимся, что папка для чеков есть
    if not os.path.exists("receipts"):
        os.makedirs("receipts")
    filepath = os.path.join("receipts", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=== 영수증 (Чек) ===\n")
        f.write(f"상품명 (Товар): {product_name}\n")
        f.write(f"가격 (Цена): {price}₩\n")
        f.write(f"결제 방법 (Метод оплаты): {PayMethod}\n")
        if PayMethod == "card" and user_card_balance is not None:
            f.write(f"잔액 (Остаток на карте): {user_card_balance}₩\n")
        f.write(f"구매 시간 (Время покупки): {now}\n")
        f.write("====================\n")
    print(f"✅ Чек сохранён: {filepath}")

def select(number, PayMethod=None, user_card_balance=0):
    selected_product = None
    for name, info in PS.drinks.items():
        if info["number"] == number:
            selected_product = info
            product_name = name
            break

    if selected_product is None:
        print("❌ Товар с таким номером не найден")
        return
    
    price = selected_product["price"]

    if selected_product["count"] <= 0:
        print("❌ Товар закончился (품절되었습니다)")
        return

    if PayMethod == "cash":
        print(f"Оплата наличными: {price}₩")
        selected_product["count"] -= 1
        print(f"✅ Вы купили {product_name} (남은 재고: {selected_product['count']}개)")
        receipt(product_name, price, PayMethod)

    elif PayMethod == "card":
        if user_card_balance >= price:
            user_card_balance -= price
            selected_product["count"] -= 1
            print(f"✅ Оплата картой успешна. Остаток на карте: {user_card_balance}₩")
            print(f"✅ Вы купили {product_name} (남은 재고: {selected_product['count']}개)")
            receipt(product_name, price, PayMethod, user_card_balance)
        else:
            print("❌ Недостаточно средств на карте (잔액 부족)")

    else:
        print("❌ Не выбран способ оплаты (결제 방법이 선택되지 않음)")
