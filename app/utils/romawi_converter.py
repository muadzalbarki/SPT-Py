ROMAN_MAP = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def angka_ke_romawi(angka: int) -> str:
    result = []
    remaining = angka
    for value, numeral in ROMAN_MAP:
        while remaining >= value:
            result.append(numeral)
            remaining -= value
    return "".join(result)
