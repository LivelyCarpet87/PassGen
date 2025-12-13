 
# Password Generator

This project generates secure passwords and PINs from four words (adjective, noun, verb, noun). See [XKCD](https://xkcd.com/936/). The major improvement is that the passwords generated can now also align with archaic banking password rules, most notably being less than 12 characters and within the restricted selection of special characters. Why banks passwords have length limits and ban meaningful special characters is left as a ponderance to the reader.

---

## Features

- Generate **long mnemonic passwords** or **bank-accepted short passwords**.
- Derive **4-digit PIN**, and **6-digit PIN** from the words.
- Copy passwords to clipboard easily.
- Fully responsive design for **phone, tablet, and laptop**.
- Wordlists are loaded dynamically from local static files.

---

## How It Works (Browser Version)

1. **Select or generate 4 words**: adjective, noun, verb, noun.
2. **Capitalize the first letter** of each word → ensures mixed uppercase and lowercase letters.
3. **Compute a base number** from the first letters of the words: `base = sum of first letters (A=1, B=2, ..., Z=26)`
4. **Derive numeric codes from base**:

- 2-digit number: `NN = base % 100`
- 4-digit PIN: `PIN4 = (base × 137) % 10000`
- 6-digit PIN: `PIN6 = (base × 137 × 53) % 1000000`

5. **Password versions**:

- **Long mnemonic**: `Word1-Word2-Word3-Word4-NN`
- **Bank-accepted (short)**: first 2 letters of each word + `!` + `NN`
  - Ensures compliance with most banking password rules: uppercase, lowercase, symbol, number.

6. **Browser-based generation** ensures **security and privacy** because everything runs locally.

---

## Docker Quick Start
```
cd Docker
docker build -t password-generator .
docker run -d -p 8080:8080 password-generator
```

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
