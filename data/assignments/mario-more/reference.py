"""Example solution for CS50x 2026 Mario More."""

from cs50 import get_int


def main():
    height = get_int("Height: ")
    while height < 1 or height > 8:
        height = get_int("Height: ")

    for width in range(1, height + 1):
        print(" " * (height - width) + "#" * width + "  " + "#" * width)


if __name__ == "__main__":
    main()
