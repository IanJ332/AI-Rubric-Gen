"""Example solution for CS50x Cash."""
from cs50 import get_float


def main():
    amount = get_float("Change owed: ")
    while amount < 0:
        amount = get_float("Change owed: ")
    cents = round(amount * 100)
    coins = 0
    for denomination in (25, 10, 5, 1):
        count, cents = divmod(cents, denomination)
        coins += count
    print(coins)


if __name__ == "__main__":
    main()
