# topk.py
import time
from collections import Counter

def main():
    start = time.perf_counter()

    with open("../words_data/words.txt") as f:
        counter = Counter(f.read().splitlines())

    top10 = counter.most_common(10)

    elapsed = time.perf_counter() - start
    print("Top10:", top10)
    print("Time:", elapsed)

if __name__ == "__main__":
    main()
