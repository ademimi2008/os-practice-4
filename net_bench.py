#!/usr/bin/env python3
"""Загрузка 20 URL: последовательно, ThreadPoolExecutor, ProcessPoolExecutor."""
import os
import statistics
import time
import urllib.request
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

WORKERS = 4
REPEATS = 3

TOPICS = [
    "Linux", "Python_(programming_language)", "Operating_system",
    "Process_(computing)", "Thread_(computing)", "Kernel_(operating_system)",
    "Scheduling_(computing)", "Virtual_memory", "Page_table",
    "Fork_(system_call)", "Unix", "Bash_(Unix_shell)", "Systemd",
    "Global_interpreter_lock", "Multiprocessing",
    "Concurrency_(computer_science)", "Deadlock", "Semaphore_(programming)",
    "Mutual_exclusion", "File_system",
]
URLS = [f"https://en.wikipedia.org/wiki/{t}" for t in TOPICS]


def fetch(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "os-lab-student/1.0 (educational use)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return len(r.read())
    except Exception:
        return -1


def run_seq():
    return [fetch(u) for u in URLS]


def run_threads():
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        return list(ex.map(fetch, URLS))


def run_procs():
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        return list(ex.map(fetch, URLS))


def bench(func):
    times, failed = [], 0
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        results = func()
        times.append(time.perf_counter() - t0)
        failed += results.count(-1)
    return times, failed


def main():
    run_seq()   # прогрев (DNS, соединения), в таблицу не входит

    cores = len(os.sched_getaffinity(0))
    print(f"nproc={cores}, повторов={REPEATS}, воркеров={WORKERS}, URL={len(URLS)}")
    print()
    print("| Способ | Прогон 1, с | Прогон 2, с | Прогон 3, с | Медиана, с | Ускорение | Ошибок |")
    print("|---|---|---|---|---|---|---|")

    base = None
    for name, func in [("Последовательно", run_seq),
                       (f"ThreadPoolExecutor ({WORKERS})", run_threads),
                       (f"ProcessPoolExecutor ({WORKERS})", run_procs)]:
        times, failed = bench(func)
        med = statistics.median(times)
        if base is None:
            base = med
        row = " | ".join(f"{t:.2f}" for t in times)
        print(f"| {name} | {row} | {med:.2f} | x{base / med:.2f} | {failed} |")


if __name__ == "__main__":
    main()