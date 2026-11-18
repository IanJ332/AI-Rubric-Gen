"""Example solution for CS50x DNA."""
import csv
import sys


def longest_match(sequence, subsequence):
    longest = 0
    for start in range(len(sequence)):
        count = 0
        while sequence[start + count * len(subsequence):start + (count + 1) * len(subsequence)] == subsequence:
            count += 1
        longest = max(longest, count)
    return longest


def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        return
    with open(sys.argv[1], newline='', encoding='utf-8') as database:
        reader = csv.DictReader(database)
        fields = reader.fieldnames[1:]
        people = list(reader)
    with open(sys.argv[2], encoding='utf-8') as source:
        sequence = source.read()
    counts = {field: longest_match(sequence, field) for field in fields}
    for person in people:
        if all(int(person[field]) == counts[field] for field in fields):
            print(person['name'])
            return
    print('No match')


if __name__ == '__main__':
    main()
