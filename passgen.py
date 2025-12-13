#!/usr/bin/env python3
import argparse
import secrets
import string
import sys
from pathlib import Path


# -------------------------------
# Load wordlists
# -------------------------------

def load_wordlist(path):
    try:
        words = [
            line.strip().lower()
            for line in Path(path).read_text().splitlines()
            if line.strip()
        ]
        if not words:
            raise ValueError("Wordlist is empty.")
        return words
    except Exception as e:
        print(f"Error loading wordlist '{path}': {e}")
        sys.exit(1)


# -------------------------------
# Utility functions
# -------------------------------

def alpha_index(ch):
    """A=1 .. Z=26"""
    return string.ascii_lowercase.index(ch.lower()) + 1


def derive_base(words):
    """Base number derived from the 1st letters of all 4 words."""
    base = 0
    for i in range(4):
        base += (alpha_index(words[i][0])+alpha_index(words[i][1])+alpha_index(words[i][2]))*len(words[i])*[7,17,107,1087][i]
    return base


def derive_numbers(words):
    base = derive_base(words)

    NN    = f"{base % 100:02d}"
    PIN4  = f"{base % 10000:04d}"
    PIN6  = f"{base % 1000000:06d}"

    return NN, PIN4, PIN6


# -------------------------------
# Generate a new password set
# -------------------------------

def generate(adj_list, noun_list, verb_list):
    while True:
        adj   = secrets.choice(adj_list)
        noun1 = secrets.choice(noun_list)
        verb  = secrets.choice(verb_list)
        noun2 = secrets.choice(noun_list)

        words = [adj, noun1, verb, noun2]
        if len([w for w in words if len(w) < 3 or not w.isascii()])>0:
            continue
        else:
            break
    cap_words = [w.capitalize() for w in words]

    NN, PIN4, PIN6 = derive_numbers(words)

    # Long version
    long_pw = f"{cap_words[0]}-{cap_words[1]}-{cap_words[2]}-{cap_words[3]}-{NN}"

    # Bank-accepted compact version
    short_pw = (
        f"{cap_words[0][:2]}"
        f"{cap_words[1][:2]}"
        f"{cap_words[2][:2]}"
        f"{cap_words[3][:2]}!"
        f"{NN}"
    )

    print("=== Generated Password Set ===")
    print(f"Words:            {', '.join(cap_words)}")
    print(f"Long password:    {long_pw}")
    print(f"Bank-accepted:        {short_pw}")
    print(f"4-digit PIN:      {PIN4}")
    print(f"6-digit PIN:      {PIN6}")


# -------------------------------
# Recover mode
# -------------------------------

def recover(words):
    words_norm = [w.lower() for w in words]
    cap_words = [w.capitalize() for w in words_norm]

    NN, PIN4, PIN6 = derive_numbers(words_norm)

    long_pw = f"{cap_words[0]}-{cap_words[1]}-{cap_words[2]}-{cap_words[3]}-{NN}"
    short_pw = (
        f"{cap_words[0][:2]}"
        f"{cap_words[1][:2]}"
        f"{cap_words[2][:2]}"
        f"{cap_words[3][:2]}!"
        f"{NN}"
    )

    print("=== Recovered Password Set ===")
    print(f"Words:            {', '.join(cap_words)}")
    print(f"Long password:    {long_pw}")
    print(f"Bank-accepted:        {short_pw}")
    print(f"2-digit number:   {NN}")
    print(f"4-digit PIN:      {PIN4}")
    print(f"6-digit PIN:      {PIN6}")


# -------------------------------
# CLI
# -------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate or recover deterministic passwords & PINs from 4 words (adj, noun, verb, noun)."
    )

    parser.add_argument("--adjectives", required=True, help="Adjective wordlist")
    parser.add_argument("--nouns",     required=True, help="Noun wordlist")
    parser.add_argument("--verbs",      required=True, help="Verb wordlist")

    parser.add_argument(
        "--recover",
        nargs=4,
        metavar=("ADJ", "NOUN1", "VERB", "NOUN2"),
        help="Recover numbers and PINs from the four words."
    )

    args = parser.parse_args()

    adj_list   = load_wordlist(args.adjectives)
    noun_list = load_wordlist(args.nouns)
    verb_list  = load_wordlist(args.verbs)

    if args.recover:
        recover(args.recover)
    else:
        generate(adj_list, noun_list, verb_list)
