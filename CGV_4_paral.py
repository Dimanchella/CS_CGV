import csv
import json
import math
import sys
import threading
from datetime import datetime

from CGV_4 import ERROR_CODE, generate_symmetrical_mut_primes, generate_prime_number, \
    find_prime_multipliers


def symmetrical_mut_primes(num: int, indent: int, length_indent, to_write: list, name: str):
    less = num - indent
    more = num + indent
    limit_primes = []
    prime_generator = generate_prime_number()
    for pr in prime_generator:
        if pr > more // 2:
            break
        limit_primes.append(pr)
    next_pr = next(prime_generator)
    while True:
        if next_pr <= more // 2:
            limit_primes.append(next_pr)
            next_pr = next(prime_generator)
        num_mults = find_prime_multipliers(num, limit_primes)
        less_mults = find_prime_multipliers(less, limit_primes)
        more_mults = find_prime_multipliers(more, limit_primes)
        if len(set(less_mults.keys()) & set(more_mults.keys())) == 0 \
                and len(set(less_mults.keys()) & set(num_mults.keys())) == 0 \
                and len(set(num_mults.keys()) & set(more_mults.keys())) == 0:
            to_write.append((num - less, less, less_mults, more, more_mults))
        less -= 1
        more += 1
        if less < num - length_indent:
            break
        if less < 2:
            break
    print(f"Thread {name} end: {datetime.now()}")  # Вывод времени окончания потока. Всегда кривой


if __name__ == '__main__':
    n: int
    dd: int
    mm: int
    yyyy: int
    try:
        with open("input.json", "r", encoding='utf-8') as json_file:
            reading_data = json.load(json_file)
            n = reading_data["N"]
            dd = reading_data["DD"]
            mm = reading_data["MM"]
            yyyy = reading_data["YYYY"]
    except ValueError:
        sys.exit(ERROR_CODE)
    # pc2 = pow(2, 18 + n) if n <= 6 else pow(2, 31 - n)
    pc2 = pow(2, 16)
    pc3 = pow(3, 13 + n) if (n + mm + dd) % 11 > 6 else pow(3, 19 - n)
    print("pc2 =", pc2)
    print(datetime.now())
    #    pp3 = find_symmetrical_simple(pc3)
    save_data = [("pc2 = ", pc2), ("pc3 = ", pc3), ("ind", "r2", "pl2", "ml", "pm2", "mm")]
    start = 1
    sub_threads = []
    sub_threads_amount = 16  # Можно даже через файл задавать
    length = math.ceil(pc2 / sub_threads_amount)
    print("length =", length)
    # sub_length = length // sub_threads_amount
    sub_lists = [[] * 1 for i in range(sub_threads_amount)]
    print("sub_lists", sub_lists)
    # print("sub_length", sub_length)

    for i in range(1, sub_threads_amount + 1):
        new_thread = threading.Thread(target=symmetrical_mut_primes,
                                      args=(pc2, start, length, sub_lists[i - 1], i))
        start += length
        sub_threads.append(new_thread)
    print("sum length:",
          start)  # Вполне возможно что мы считаем лишний элемент (начинаем с 1), сравните длины
    print("sub_threads:", sub_threads)
    for th in sub_threads:
        th.start()
        print("thread start")
    for th in sub_threads:
        th.join()
        print("thread end", datetime.now())

    # Не уверен что вы тут складывали, так что написал что написал
    result = []
    for el in sub_lists:
        result.extend(el)
    print(len(result))
    r = result[-3:-1]
    print(r)
    ress = map(tuple, r)

    with open("output4par.csv", "w+", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows(ress)
