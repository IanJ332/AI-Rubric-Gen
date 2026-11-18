"""Example solution for CS50x Readability."""
from cs50 import get_string


def main():
    text = get_string("Text: ")
    letters = sum('a' <= char <= 'z' or 'A' <= char <= 'Z' for char in text)
    words = len(text.split())
    sentences = sum(char in '.!?' for char in text)
    index = 0.0588 * (100 * letters / words) - 0.296 * (100 * sentences / words) - 15.8
    grade = round(index)
    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


if __name__ == "__main__":
    main()
