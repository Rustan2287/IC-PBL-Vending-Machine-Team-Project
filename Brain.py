import Product_Storage as PS

def select(number, PayMethod=None, user_card_balance=0):
    if number in PS.drinks and PS.drinks[number]["count"] > 0:
        PS.drinks[number]["count"] -= 1
        price = PS.drinks[number]["price"]
        payment(price, PayMethod, user_card_balance)

def payment(price, PayMethod=None, user_card_balance=0):
        if PayMethod == "cash":
            pass
            
        elif PayMethod == "card":
             if user_card_balance >= price:
                user_card_balance -= price
                print(f"Payment successful. Remaining balance: {user_card_balance}")
             else:
                 print("Insufficient balance.")