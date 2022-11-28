import json
import math
import sys
import csv

ERROR_CODE = -1

LIMIT_NUMBERS = 20


def generate_prime_number():
    prime_nums = []
    s = 2
    while True:
        yield s
        prime_nums.append(s)
        find_next = False
        while not find_next:
            s += 1
            for sn in prime_nums:
                if sn * sn > s:
                    find_next = True
                    break
                elif s % sn == 0:
                    break


def is_prime(num: int):
    for i in range(2, math.floor(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def find_prime_multipliers(num: int, primes=generate_prime_number()):
    mults = {}
    for pr in primes:
        if pr > num // 2:
            break
        temp = num
        while temp % pr == 0:
            temp //= pr
            mults[pr] = mults.setdefault(pr, 0) + 1
    return mults


def generate_symmetrical_primes(num: int):
    less = num - 1
    more = num + 1
    while True:
        if is_prime(less) and is_prime(more):
            yield num - less, less, more
        less -= 1
        more += 1
        if less < 2:
            break


def generate_symmetrical_mut_primes(num: int):
    less = num - 1
    more = num + 1
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
            yield num - less, less, less_mults, more, more_mults
        less -= 1
        more += 1
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
    #    pp3 = find_symmetrical_simple(pc3)
    save_data = [("pc2 = ", pc2), ("pc3 = ", pc3)]
    print(f"pc2 = {pc2}")
    print(f"pc3 = {pc3}")

    save_data.append(tuple())
    save_data.append(("ind","r2", "pl2", "pm2"))
    last_p2_prime = ()
    ind = 1
    for ss in generate_symmetrical_primes(pc2):
        # save_data.append((ss[0], ss[1], ss[2]))
        last_p2_prime = (ind, ss[0], ss[1], ss[2])
        # print(f"{ind}: r2 = {ss[0]} pl2 = {ss[1]} pm2 = {ss[2]}")
        ind += 1
        # if ind > LIMIT_NUMBERS:
        #     break
    save_data.append(last_p2_prime)
    save_data.append(tuple())
    save_data.append(("ind", "r2", "pl2", "ml", "pm2", "mm"))
    last_p2 = tuple()
    ind = 1
    # for ss in generate_symmetrical_mut_primes(pc2):
    #     str_ml = '+'.join(map(lambda m: f"{m[0]}^{m[1]}", ss[2].items()))
    #     str_mm = '+'.join(map(lambda m: f"{m[0]}^{m[1]}", ss[4].items()))
    #     # save_data.append((ind, ss[0], ss[1], str_ml, ss[3], str_mm))
    #     last_p2 = (ss[0], ss[1], str_ml, ss[3], str_mm)
    #     # print(f"{ind}: r2 = {ss[0]} pl2 = {ss[1]} ml: {str_ml} pm2 = {ss[3]} mm: {str_mm}")
    #     ind += 1
    #     # if ind > LIMIT_NUMBERS:
    #     #     break
    save_data.append(last_p2)

    save_data.append(tuple())
    save_data.append(("ind", "r3", "pl3", "pm3"))
    last_p3_prime = ()
    ind = 1
    for ss in generate_symmetrical_primes(pc3):
        # save_data.append((ss[0], ss[1], ss[2]))
        last_p3_prime = (ind, ss[0], ss[1], ss[2])
        # print(f"{ind}: r3 = {ss[0]} pl3 = {ss[1]} pm3 = {ss[2]}")
        ind += 1
        # if ind > LIMIT_NUMBERS:
        #     break
    save_data.append(last_p3_prime)
    save_data.append(tuple())
    save_data.append(("ind", "r3", "pl3", "ml", "pm3", "mm"))
    prelast_p3 = ()
    last_p3 = ()
    ind = 1
    for ss in generate_symmetrical_mut_primes(pc3):
        str_ml = '+'.join(map(lambda m: f"{m[0]}^{m[1]}", ss[2].items()))
        str_mm = '+'.join(map(lambda m: f"{m[0]}^{m[1]}", ss[4].items()))
        # save_data.append((ss[0], ss[1], str_ml, ss[3], str_mm))
        prelast_p3 = last_p3
        last_p3 = (ind, ss[0], ss[1], str_ml, ss[3], str_mm)
        # print(f"{ind}: r3 = {ss[0]} pl3 = {ss[1]} ml: {str_ml} pm3 = {ss[3]} mm: {str_mm}")
        ind += 1
        # if ind > LIMIT_NUMBERS:
        #     break
    save_data.append(prelast_p3)
    save_data.append(last_p3)
    with open("output4-3.csv", "w+", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows(save_data)
