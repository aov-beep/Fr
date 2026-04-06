import requests

URL = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"

def get_rates():
    try:
        data = requests.get(URL, timeout=5).json()
        rates = {}
        for item in data:
            if item["ccy"] in ("EUR", "USD"):
                rates[item["ccy"]] = {
                    "buy": float(item["buy"]),
                    "sale": float(item["sale"]),
                }
        return rates
    except Exception as e:
        print(f"Помилка отримання курсів: {e}")
        return None

def print_rates(rates):
    print("\n--- Курс валют ---")
    for cur, r in rates.items():
        print(f"  {cur}: купівля {r['buy']:.2f} / продаж {r['sale']:.2f} UAH")

def print_balance(balance):
    print("\n--- Баланс обмінника ---")
    for cur, amount in balance.items():
        print(f"  {cur}: {amount:,.2f}")

def buy(balance, rates, currency):
    rate = rates[currency]["sale"]
    print(f"\nКупівля {currency} | Курс продажу банку: {rate:.2f} UAH")
    try:
        amount = float(input(f"Скільки {currency} купити? "))
        if amount <= 0:
            print("Сума має бути більше 0.")
            return
    except ValueError:
        print("Невірне значення.")
        return

    cost = amount * rate
    if cost > balance["UAH"]:
        print(f"Недостатньо UAH. Потрібно: {cost:,.2f}, є: {balance['UAH']:,.2f}")
        return
    if amount > balance[currency]:
        print(f"В обміннику недостатньо {currency}. Є: {balance[currency]:,.2f}")
        return

    balance["UAH"] -= cost
    balance[currency] -= amount
    print(f"Куплено {amount:,.2f} {currency} за {cost:,.2f} UAH.")

def sell(balance, rates, currency):
    rate = rates[currency]["buy"]
    print(f"\nПродаж {currency} | Курс купівлі банку: {rate:.2f} UAH")
    try:
        amount = float(input(f"Скільки {currency} продати? "))
        if amount <= 0:
            print("Сума має бути більше 0.")
            return
    except ValueError:
        print("Невірне значення.")
        return

    income = amount * rate
    if amount > balance[currency]:
        print(f"Недостатньо {currency}. Є: {balance[currency]:,.2f}")
        return

    balance[currency] -= amount
    balance["UAH"] += income
    print(f"Продано {amount:,.2f} {currency}, отримано {income:,.2f} UAH.")

def main():
    balance = {"UAH": 100_000.0, "EUR": 1_000.0, "USD": 1_000.0}

    print("Завантаження курсів валют...")
    rates = get_rates()
    if not rates:
        print("Не вдалося отримати курси. Перевірте з'єднання.")
        return

    print_rates(rates)
    print_balance(balance)

    menu = {
        "1": ("Купити EUR",  lambda: buy(balance, rates, "EUR")),
        "2": ("Продати EUR", lambda: sell(balance, rates, "EUR")),
        "3": ("Купити USD",  lambda: buy(balance, rates, "USD")),
        "4": ("Продати USD", lambda: sell(balance, rates, "USD")),
        "5": ("Оновити курс", None),
        "0": ("Вихід", None),
    }

    while True:
        print("\n=== МЕНЮ ===")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")

        choice = input("Оберіть дію: ").strip()

        if choice == "0":
            print("До побачення!")
            break
        elif choice == "5":
            print("Оновлення курсів...")
            new_rates = get_rates()
            if new_rates:
                rates = new_rates
                print_rates(rates)
            else:
                print("Не вдалося оновити курси.")
        elif choice in menu:
            _, action = menu[choice]
            action()
            print_balance(balance)
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()