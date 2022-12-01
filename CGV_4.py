import copy
import csv
import json
import math
import sys

ERROR_CODE = -1

PROGRESS_BAR_LENGTH = 50
LIMIT_NUMBERS = -1

LIMIT_OUTPUT = 20


def download_prime_numbers():
    primes = []
    try:
        with open("prime_numbers.txt", "r", encoding='utf-8') as txt_file:
            while line := txt_file.readline():
                primes.append(int(line))
    except FileNotFoundError:
        return []
    except ValueError:
        return []
    return primes


def save_prime_numbers(primes_list: list[int]):
    try:
        with open("prime_numbers.txt", "w+", encoding='utf-8') as txt_file:
            txt_file.write('\n'.join(map(str, primes_list)))
    except FileExistsError:
        return
    except ValueError:
        return
    return


def generate_prime_number(primes=()):
    prime_nums = copy.copy(sorted(primes))
    for number in prime_nums[:-1]:
        yield number
    s = prime_nums[-1] if len(prime_nums) else 2
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


def collect_prime_numbers(limit: int):
    part_pc = limit // PROGRESS_BAR_LENGTH
    counter_pc = part_pc
    prime_numbers = sorted(download_prime_numbers())
    prime_generator = generate_prime_number(prime_numbers)
    primes_list = []
    save_new_primes = False
    for pr in prime_generator:
        if pr > max(pc2, pc3):
            break
        save_new_primes = not len(prime_numbers) or pr > prime_numbers[-1]
        primes_list.append(pr)
        if pr > counter_pc:
            print('.', end='')
            counter_pc += part_pc
    primes_list.append(next(prime_generator))
    if counter_pc < limit:
        print('.', end='')
    if save_new_primes:
        save_prime_numbers(primes_list)
    return primes_list, prime_generator


def is_prime(num: int, primes_list=None):
    sqrt_num = math.floor(math.sqrt(num))
    num_list = primes_list if primes_list and primes_list[-1] > sqrt_num else range(2, sqrt_num + 1)
    for i in num_list:
        if i > sqrt_num:
            return True
        if num % i == 0:
            return False
    return True


def find_prime_multipliers(num: int, primes_list=generate_prime_number()):
    mults = {}
    for pr in primes_list:
        if pr > num // 2:
            break
        temp = num
        while temp % pr == 0:
            temp //= pr
            mults[pr] = mults.setdefault(pr, 0) + 1
    if not len(mults):
        mults[num] = 1
    return mults


def generate_symmetrical_primes(num: int, primes_list=None):
    less = num - 1
    more = num + 1
    while True:
        if is_prime(less, primes_list) and is_prime(more, primes_list):
            yield num - less, less, more
        less -= 1
        more += 1
        if less < 2:
            break


def generate_symmetrical_mut_primes(num: int):
    less = num - 1
    more = num + 1
    while True:
        if math.gcd(num, less) == 1 and math.gcd(less, more) == 1 and math.gcd(num, more) == 1:
            yield num - less, less, more
        less -= 1
        more += 1
        if less < 2:
            break


def calculate_pairs(primes_list: list[int], prime_generator, pc: int, prime_pairs: bool):
    part_pc = pc // PROGRESS_BAR_LENGTH
    counter_pc = part_pc
    ind = 0
    last_ss = None
    result_list = []
    generator = generate_symmetrical_primes(pc, primes_list) if prime_pairs \
        else generate_symmetrical_mut_primes(pc)
    for ss in generator:
        if primes_list[-1] < ss[2] // 2:
            primes_list.append(next(prime_generator))
        if LIMIT_OUTPUT < 0 or ind < LIMIT_OUTPUT:
            if prime_pairs:
                result_list.append((ind + 1, ss[0], ss[1], ss[2]))
            else:
                result_list.append((
                    ind + 1, ss[0],
                    ss[1], find_prime_multipliers(ss[1], primes_list),
                    ss[2], find_prime_multipliers(ss[2], primes_list)
                ))
        elif LIMIT_OUTPUT > 0:
            last_ss = ss
        ind += 1
        if 0 < LIMIT_NUMBERS > ind:
            break
        if ss[0] > counter_pc:
            print('.', end='')
            counter_pc += part_pc
    if last_ss:
        if prime_pairs:
            result_list.append((ind + 1, last_ss[0], last_ss[1], last_ss[2]))
        else:
            result_list.append((
                ind + 1, last_ss[0],
                last_ss[1], find_prime_multipliers(last_ss[1], primes_list),
                last_ss[2], find_prime_multipliers(last_ss[2], primes_list)
            ))
    if counter_pc < pc:
        print('.', end='')
    return ind + 1, result_list


def save_results(
        pc2_save: int, num_pc2_p_save: int, num_pc2_mp_save: int,
        pc3_save: int, num_pc3_p_save: int, num_pc3_mp_save: int,
        pc2_p_pairs_save: list, pc2_mp_pairs_save: list,
        pc3_p_pairs_save: list, pc3_mp_pairs_save: list
):
    saving_data = [("pc2 =", pc2_save),
                   ("number prime pairs:", num_pc2_p_save),
                   ("number mutually prime pairs:", num_pc2_mp_save),
                   (),
                   ("pc3 =", pc3_save),
                   ("number prime pairs:", num_pc3_p_save),
                   ("number mutually prime pairs:", num_pc3_mp_save),
                   (), ("pc2 prime pairs:",),
                   ("i", "difference", "less prime", "most prime")]
    for pair in pc2_p_pairs_save:
        saving_data.append((pair[0], pair[1], pair[2], pair[3]))
    saving_data.extend([(), ("pc2 mutually prime pairs:",),
                        ("i", "difference",
                         "less prime", "multiplier",
                         "most prime", "multiplier")])
    for pair in pc2_mp_pairs_save:
        str_ml = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", pair[3].items()))
        str_mm = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", pair[5].items()))
        saving_data.append((pair[0], pair[1], pair[2], str_ml, pair[4], str_mm))
    saving_data.extend([(), ("pc3 prime pairs:",),
                        ("i", "difference", "less prime", "most prime")])
    for pair in pc3_p_pairs_save:
        saving_data.append((pair[0], pair[1], pair[2], pair[3]))
    saving_data.extend([(), ("pc3 mutually prime pairs:",),
                        ("i", "difference",
                         "less prime", "multiplier",
                         "most prime", "multiplier")
                        ])
    for pair in pc3_mp_pairs_save:
        str_ml = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", pair[3].items()))
        str_mm = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", pair[5].items()))
        saving_data.append((pair[0], pair[1], pair[2], str_ml, pair[4], str_mm))

    with open("output4.csv", "w+", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows(saving_data)


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
    except FileNotFoundError:
        sys.exit(ERROR_CODE)
    pc2 = pow(2, 12 + n) if n <= 6 else pow(2, 25 - n)
    pc3 = pow(3, 7 + ns) if (ns := (n + mm + dd) % 7) > 3 else pow(3, 13 - ns)
    # pc2 = pow(2, 25)
    # pc3 = pow(3, 13)

    print(f"PROCES                                  |{'-' * (PROGRESS_BAR_LENGTH - 2)}|"
          "\nSearch for prime numbers                ", end='')
    limit_primes, prime_gen = collect_prime_numbers(max(pc2, pc3))
    print("\nSearch for prime pairs for pc2          ", end='')
    num_pc2_p, res_pc2_p = calculate_pairs(limit_primes, prime_gen, pc2, True)
    print("\nSearch for mutually prime pairs for pc2 ", end='')
    num_pc2_mp, res_pc2_mp = calculate_pairs(limit_primes, prime_gen, pc2, False)
    print("\nSearch for prime pairs for pc3          ", end='')
    num_pc3_p, res_pc3_p = calculate_pairs(limit_primes, prime_gen, pc3, True)
    print("\nSearch for mutually prime pairs for pc3 ", end='')
    num_pc3_mp, res_pc3_mp = calculate_pairs(limit_primes, prime_gen, pc3, False)

    save_results(
        pc2, num_pc2_p, num_pc2_mp,
        pc3, num_pc3_p, num_pc3_mp,
        res_pc2_p, res_pc2_mp,
        res_pc3_p, res_pc3_mp
    )
    print("\nSUCCESS")
