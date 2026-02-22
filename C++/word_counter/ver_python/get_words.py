# get_words.py
import random

def gen(n=5_000_000):
    words = [f"word{i}" for i in range(1000)]
    with open("../words_data/words.txt", "w") as f:
        for _ in range(n):
            f.write(random.choice(words) + "\n")

if __name__ == "__main__":
    gen()
