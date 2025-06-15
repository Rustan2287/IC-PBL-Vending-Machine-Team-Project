import Product_Storage as PS

def select(number, PayMethod=None, user_card_balance=0):
    # Ищем товар по номеру
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

    # Проверяем оплату
    if PayMethod == "cash":
        # Здесь логика оплаты наличными (можно реализовать позже)
        print(f"Оплата наличными: {price}₩")
        selected_product["count"] -= 1
        print(f"✅ Вы купили {product_name} (남은 재고: {selected_product['count']}개)")
            
    elif PayMethod == "card":
        if user_card_balance >= price:
            user_card_balance -= price
            selected_product["count"] -= 1
            print(f"✅ Оплата картой успешна. Остаток на карте: {user_card_balance}₩")
            print(f"✅ Вы купили {product_name} (남은 재고: {selected_product['count']}개)")
        else:
            print("❌ Недостаточно средств на карте (잔액 부족)")

    else:
        print("❌ Не выбран способ оплаты (결제 방법이 선택되지 않음)")
