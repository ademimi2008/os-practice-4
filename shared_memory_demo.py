#!/usr/bin/env python3
import multiprocessing
import os
import threading

data = []   # глобальный список


def add_in_thread():
    data.append("поток")
    print(f"[поток]   pid={os.getpid()} data={data} id={id(data)}")


def add_in_process():
    data.append("процесс")
    print(f"[процесс] pid={os.getpid()} data={data} id={id(data)}")


if __name__ == "__main__":
    print(f"start method: {multiprocessing.get_start_method()}")
    print(f"[родитель] pid={os.getpid()} до:             data={data} id={id(data)}")

    t = threading.Thread(target=add_in_thread)
    t.start()
    t.join()
    print(f"[родитель] после потока:   data={data}")

    p = multiprocessing.Process(target=add_in_process)
    p.start()
    p.join()
    print(f"[родитель] после процесса: data={data}")