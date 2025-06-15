import Product_Storage as PS
import os
from datetime import datetime

def calculate_change(change):
    coins = {"1000": 0, "500": 0, "100": 0}

    coins["1000"] = change // 1000
    change %= 1000

    coins["500"] = change // 500
    change %= 500

    coins["100"] = change // 100
    change %= 100

    return coins

def receipt(product_name, price, PayMethod, money=0):
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
        if PayMethod == "card" and money is not None:
            f.write(f"잔액 (Остаток на карте): {money}₩\n")
        f.write(f"구매 시간 (Время покупки): {now}\n")
        f.write("====================\n")
    print(f"✅ Чек сохранён: {filepath}")

def select(number, PayMethod=None, money=0):
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
    if selected_product["count"] != 0:
        if PayMethod == "cash":
            if money < price:
                print("❌ Недостаточно наличных (현금 부족)")
            else:
                change = money - price
                selected_product["count"] -= 1
                print(f"✅ Вы купили {product_name} за {price}₩ (남은 재고: {selected_product['count']}개)")
                receipt(product_name, price, PayMethod)

                if change > 0:
                    coins = calculate_change(change)
                    print(f"✅ Сдача (잔돈): {change}₩")
                    print(f" - 1000원: {coins['1000']}개")
                    print(f" - 500원: {coins['500']}개")
                    print(f" - 100원: {coins['100']}개")
                else:
                    print("✅ Сдачи нет (잔돈 없음)")

        elif PayMethod == "card":
            if money >= price:
                money -= price
                selected_product["count"] -= 1
                print(f"✅ Оплата картой успешна. Остаток на карте: {money}₩")
                print(f"✅ Вы купили {product_name} (남은 재고: {selected_product['count']}개)")
                receipt(product_name, price, PayMethod, money)
            else:
                print("❌ Недостаточно средств на карте (잔액 부족)")

        else:
            print("❌ Не выбран способ оплаты (결제 방법이 선택되지 않음)")
    else:
        print("❌ Товар распродан (상품 매진)")