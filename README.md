 
# XKPW Password Generator

This project generates secure passwords and PINs from four words (adjective, noun, verb, noun). See [XKCD](https://xkcd.com/936/). The major improvement is that the passwords generated can now also align with archaic banking password rules, most notably being less than 12 characters and within the restricted selection of special characters. Why banks passwords have length limits and ban meaningful special characters is left as a ponderance to the reader.

---

## Features

- Generate **long mnemonic passwords** or **bank-accepted short passwords**.
- Derive **4-digit PIN**, and **6-digit PIN** from the words.
- Copy passwords to clipboard easily.
- Fully responsive design for **phone, tablet, and laptop**.
- Wordlists are loaded dynamically from local static files.

---

## How It Works

1. **RANDOMLY generate 4 words**: adjective, noun, verb, noun. (These will be rerolled if any word is less than 3 characters or the long password is more than 30 characters)
2. **Capitalize the first letter** of each word → ensures mixed uppercase and lowercase letters.
3. **Compute a base number**:
  - Take the **first three letters** of each word and convert to numbers (A=1 … Z=26)
  - For EACH word:
    - Add the 3 numbers together
    - Multiply sum by the **word length**
    - Multiply again by a **prime weight** for each word (first prime of that digit length ending in 7):
      - 1st word (adjective) → 7
      - 2nd word (noun) → 17
      - 3rd word (verb) → 107
      - 4th word (noun) → 1087
  - **Add the results for each word together** to produce the **base number**
- Derive PINs from the base number:
  - 2-digit number: `NN = base mod 100`
  - 4-digit PIN: `PIN4 = base mod 10000`
  - 6-digit PIN: `PIN6 = base mod 1000000`

5. **Password versions**:

- **Long Password**: `Adjective-Noun1-Verb-Noun2-NN`
- **Bank-accepted (short)**: first 2 letters of each word + `!` + `NN`
  - Ensures compliance with most banking password rules: uppercase, lowercase, symbol, number.
  - Within 8-12 characters to satify all bank password length requirements
---

## Docker Quick Start

### Using Docker Compose (Recommended)
```
docker-compose up --build
```

The service will be available at `http://localhost:8080`

## CLI Script

You can also generate passwords using the original Python CLI script:

```bash
python3 password_gen.py \
--adjectives adjectives.txt \
--nouns nouns.txt \
--verbs verbs.txt
```

The script outputs:
- Words
- Long mnemonic password
- Bank-accepted password
- 2-digit number, 4-digit PIN, 6-digit PIN


## Wordlists Credit
Wordlists used in this project are from [top-english-wordlists](https://github.com/david47k/top-english-wordlists).

Files used:
- `top_english_adjs_lower_10000.txt`
- `top_english_nouns_lower_10000.txt`
- `top_english_verbs_lower_10000.txt`
