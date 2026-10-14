import random
import math
from collections import Counter

import matplotlib.pyplot as plt


SAMPLES = 100_000

random.seed(12345)

with open('Wordlists/top_english_nouns_lower_10000.txt', encoding="utf-8") as f:
    NOUNS = list(dict.fromkeys(
        line.strip().lower()
        for line in f
        if line.strip()
    ))
with open('Wordlists/top_english_adjs_lower_10000.txt', encoding="utf-8") as f:
    ADJS = list(dict.fromkeys(
        line.strip().lower()
        for line in f
        if line.strip()
    ))
with open('Wordlists/top_english_verbs_lower_10000.txt', encoding="utf-8") as f:
    VERBS = list(dict.fromkeys(
        line.strip().lower()
        for line in f
        if line.strip()
    ))

def word_score(word):
    word = word.lower()
    if len(word) < 3 or not word.isalpha():
        raise ValueError(f"Invalid word: {word!r}")

    letter_sum = sum(ord(c) - ord("a") + 1 for c in word[:3])
    return letter_sum * len(word)


def candidate_pin(words):
    weights = [7, 17, 107, 1087]
    total = sum(
        weight * word_score(word)
        for weight, word in zip(weights, words)
    )
    return f"{total % 1_000_000:06d}"


def print_digit_distribution(pins, position):
    counts = Counter(pin[position] for pin in pins)
    expected = len(pins) / 10

    chi2 = sum(
        (counts[str(d)] - expected) ** 2 / expected
        for d in range(10)
    )

    print(f"\nDigit position {position + 1}:")
    for d in "0123456789":
        print(f"  {d}: {counts[d] / len(pins):.2%}")
    print(f"  Chi-square: {chi2:.2f}")


def plot_pin_spread(pins):
    # First 3 digits -> x; last 3 digits -> y.
    x = [int(pin[:3]) for pin in pins]
    y = [int(pin[3:]) for pin in pins]

    # Count duplicate coordinates and plot each unique point once.
    point_counts = Counter(zip(x, y))
    xs = list(point_counts.keys())
    counts = list(point_counts.values())

    plot_x = [p[0] for p in xs]
    plot_y = [p[1] for p in xs]

    plt.figure(figsize=(10, 8))

    scatter = plt.scatter(
        plot_x,
        plot_y,
        c=counts,
        s=8,
        cmap="viridis",
        alpha=0.7,
        edgecolors="none",
    )

    plt.colorbar(scatter, label="Number of occurrences")
    plt.xlim(0, 999)
    plt.ylim(0, 999)
    plt.xlabel("First three digits (000–999)")
    plt.ylabel("Last three digits (000–999)")
    plt.title("PIN Output Spread")
    plt.grid(alpha=0.15)
    plt.tight_layout()
    plt.show()

def choose_four_words():
    words = []
    for lst in [ADJS,NOUNS,VERBS,NOUNS]:
        while True:
            word = random.choice(lst)
            if len(word) < 3 or not word.isalpha():
                continue
            words.append(word)
            break
    return words

def main():

    pins = [
        candidate_pin(choose_four_words())
        for _ in range(SAMPLES)
    ]

    counts = Counter(pins)

    print("=== PIN statistics ===")
    print(f"Samples: {len(pins):,}")
    print(f"Unique PINs: {len(counts):,}")
    print(f"Repeated outputs: {len(pins) - len(counts):,}")

    print("\n=== Digit distributions ===")
    for position in range(6):
        print_digit_distribution(pins, position)

    entropy = -sum(
        (n / len(pins)) * math.log2(n / len(pins))
        for n in counts.values()
    )
    print(f"\nEmpirical output entropy: {entropy:.3f} bits")
    print("Maximum six-digit PIN entropy: 19.932 bits")

    plot_pin_spread(pins)


if __name__ == "__main__":
    main()
