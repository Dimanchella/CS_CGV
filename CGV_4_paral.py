import csv
import json
import math
import sys
import threading
from datetime import datetime

from CGV_4 import ERROR_CODE, generate_symmetrical_mut_primes, generate_prime_number, find_prime_multipliers


def symmetrical_mut_primes(num: int, indent: int, length_indent, to_write: list):
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
    pc2 = pow(2, 18 + n) if n <= 6 else pow(2, 31 - n)
    pc3 = pow(3, 13 + n) if (n + mm + dd) % 11 > 6 else pow(3, 19 - n)
    print("pc2 =", pc2)
    print(datetime.now())
    #    pp3 = find_symmetrical_simple(pc3)
    save_data = [("pc2 = ", pc2), ("pc3 = ", pc3), ("ind", "r2", "pl2", "ml", "pm2", "mm")]

    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    list7 = []
    list8 = []
    list9 = []
    list10 = []
    list11 = []
    list12 = []
    list13 = []
    list14 = []
    list15 = []
    list16 = []

    start = 1
    length = math.ceil(pc2 / 16)
    print("length =", length)
    t1 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list1))
    start += length
    t2 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list2))
    start += length
    t3 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list3))
    start += length
    t4 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list4))
    start += length
    t5 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list5))
    start += length
    t6 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list6))
    start += length
    t7 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list7))
    start += length
    t8 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list8))
    start += length
    t9 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list9))
    start += length
    t10 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list10))
    start += length
    t11 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list11))
    start += length
    t12 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list12))
    start += length
    t13 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list13))
    start += length
    t14 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list14))
    start += length
    t15 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list15))
    start += length
    t16 = threading.Thread(target=symmetrical_mut_primes, args=(pc2, start, length, list16))

    t1.start()
    print("thread start")
    t2.start()
    print("thread start")
    t3.start()
    print("thread start")
    t4.start()
    print("thread start")
    t5.start()
    print("thread start")
    t6.start()
    print("thread start")
    t7.start()
    print("thread start")
    t8.start()
    print("thread start")
    t9.start()
    print("thread start")
    t10.start()
    print("thread start")
    t11.start()
    print("thread start")
    t12.start()
    print("thread start")
    t13.start()
    print("thread start")
    t14.start()
    print("thread start")
    t15.start()
    print("thread start")
    t16.start()
    print("thread start")

    t1.join()
    print("thread end", datetime.now())
    t2.join()
    print("thread end", datetime.now())
    t3.join()
    print("thread end", datetime.now())
    t4.join()
    print("thread end", datetime.now())
    t5.join()
    print("thread end", datetime.now())
    t6.join()
    print("thread end", datetime.now())
    t7.join()
    print("thread end", datetime.now())
    t8.join()
    print("thread end", datetime.now())
    t9.join()
    print("thread end", datetime.now())
    t10.join()
    print("thread end", datetime.now())
    t11.join()
    print("thread end", datetime.now())
    t12.join()
    print("thread end", datetime.now())
    t13.join()
    print("thread end", datetime.now())
    t14.join()
    print("thread end", datetime.now())
    t15.join()
    print("thread end", datetime.now())
    t16.join()
    print("thread end", datetime.now())

    res = list1 + list2 + list3 + list4 + list5 + list6 + list7 + list8 + list9 \
          + list10 + list11 + list12 + list13 + list14 + list15 + list16

    print(len(res))
    r = res[-3:-1]
    print(r)
    ress = map(tuple, r)

    with open("output4par.csv", "w+", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows(ress)
