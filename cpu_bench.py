#!/usr/bin/env python3
"""Сумма чисел из numbers.txt: 1 поток, 4 потока, 4 процесса."""
import multiprocessing
import os
import statistics
import threading
import time

WORKERS = 4
REPEATS = 3


def load_numbers(path="numbers.txt"):
    with open(path) as f:
        return [int(line) for line in f]


def sum_chunk(chunk):
    total = 0
    for x in chunk:          # чистый Python: нагрузка на CPU
        total += x
    return total


def split(data, n):
    size = len(data) // n
    chunks = [data[i * size:(i + 1) * size] for i in range(n - 1)]
    chunks.append(data[(n - 1) * size:])
    return chunks


def run_single(data, chunks):
    return sum_chunk(data)


def run_threads(data, chunks):
    results = [0] * len(chunks)

    def worker(i):
        results[i] = sum_chunk(chunks[i])

    threads = [threading.Thread(target=worker, args=(i,))
               for i in range(len(chunks))]
    for t in threads:        # сначала запускаем ВСЕХ
        t.start()
    for t in threads:        # и только потом ждём
        t.join()
    return sum(results)


def run_processes(data, chunks):
    with multiprocessing.Pool(len(chunks)) as pool:
        return sum(pool.map(sum_chunk, chunks))


def bench(func, data, chunks, expected):
    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        result = func(data, chunks)
        times.append(time.perf_counter() - t0)
        assert result == expected, "сумма не совпала!"
    return times


def main():
    data = load_numbers()                 # вне замеров
    chunks = split(data, WORKERS)         # вне замеров
    expected = sum(data)                  # вне замеров

    cores = len(os.sched_getaffinity(0))  # то же, что показывает nproc
    print(f"nproc={cores}, повторов={REPEATS}, воркеров={WORKERS}, "
          f"чисел={len(data)}, start method={multiprocessing.get_start_method()}")
    print()
    print("| Способ | Прогон 1, с | Прогон 2, с | Прогон 3, с | Медиана, с | Ускорение |")
    print("|---|---|---|---|---|---|")

    base = None
    for name, func in [("1 поток", run_single),
                       (f"{WORKERS} потока (threading)", run_threads),
                       (f"{WORKERS} процесса (multiprocessing)", run_processes)]:
        times = bench(func, data, chunks, expected)
        med = statistics.median(times)
        if base is None:
            base = med
        row = " | ".join(f"{t:.3f}" for t in times)
        print(f"| {name} | {row} | {med:.3f} | x{base / med:.2f} |")


if __name__ == "__main__":
    main()