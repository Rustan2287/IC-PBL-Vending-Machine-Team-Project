RACK_Y = 20

Rack_Number = {
# Rack positions for the vending machine
    "1": (0, RACK_Y),
    "2": (70, RACK_Y),
    "3": (150, RACK_Y),
    "4": (220, RACK_Y),
    "5": (300, RACK_Y),
    "6": (370, RACK_Y),
    "7": (320, RACK_Y)
}

drinks = {
    "fanta": {
        "price": 1900,
        "src": "src/assets/Product/fanta.jpg",
        "count": 20,
        "position": Rack_Number["1"],
        "number": "1"
    },
    "fanta_pain": {
        "price": 1900,
        "src": "src/assets/Product/fanta pain.jpg",
        "count": 20,
        "position": Rack_Number["2"],
        "number": "2"
    },
    "Milks": {
        "price": 1900,
        "src": "src/assets/Product/Milks.jpg",
        "count": 20,
        "position": Rack_Number["3"],
        "number": "3"
    },
    "pepsi": {
        "price": 1900,
        "src": "src/assets/Product/pepsi.jpg",
        "count": 20,
        "position": Rack_Number["4"],
        "number": "4"
    },
    "pocari": {
        "price": 1900,
        "src": "src/assets/Product/pocari.jpg",
        "count": 20,
        "position": Rack_Number["5"],
        "number": "5"
    },
    "Sprite": {
        "price": 1900,
        "src": "src/assets/Product/Sprite.jpg",
        "count": 20,
        "position": Rack_Number["6"],
        "number": "6"
    }
}
