#!/usr/bin/env python3
import random

N = 10_000_000
random.seed(42)   # одинаковые данные при каждой генерации

with open("numbers.txt", "w") as f:
    for _ in range(N):
        f.write(f"{random.randint(1, 1_000_000)}\n")

print(f"Записано {N} чисел в numbers.txt")