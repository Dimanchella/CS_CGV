import csv
import json
import math
import sys
from copy import copy
from functools import reduce
from itertools import combinations
from multiprocessing import Process, Manager, current_process

ERROR_CODE = -1

NUMBER_SUBTHREADS = 4

LIMIT_OUTPUT_PAIRS = 20
LIMIT_MUTUALLY_PRIMES = 7


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
    prime_nums = copy(sorted(primes))
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
                if s % sn == 0:
                    break


def collect_prime_numbers(limit: int):
    loaded_primes = sorted(download_prime_numbers())
    prime_generator = generate_prime_number(loaded_primes)
    primes_list = []
    current_percent = 0
    print(f"Searching prime numbers {current_percent}%", end='')
    for pr in prime_generator:
        if (new_percent := min(int(pr / limit * 100), 100)) > current_percent:
            print(f"\rSearching prime numbers {new_percent}%", end='')
            current_percent = new_percent
        if pr > limit:
            break
        primes_list.append(pr)
    primes_list.append(next(prime_generator))
    if len(primes_list) > len(loaded_primes):
        save_prime_numbers(primes_list)
    print()
    return primes_list


def is_prime(number: int, primes_set: set[int]):
    if number in primes_set:
        return True
    return False


def is_mutually_prime(*nums: int):
    return reduce(
        lambda res, x: res and (math.gcd(x[0], x[1]) == 1),
        [True] + list(combinations(nums, 2))
    )


def calculate_prime_pairs(arr_pairs: list, primes_list: list[int], output_list: list):
    primes_set = set(primes_list)
    print(f"{current_process().name} start")
    prime_pairs = list(
        filter(
            lambda p: is_prime(p[1], primes_set) and is_prime(p[3], primes_set),
            arr_pairs
        )
    )
    output_list.append(prime_pairs)
    print(f"{current_process().name} end")


def calculate_mut_prime_pairs(arr_pairs: list, output_list: list):
    print(f"{current_process().name} start")
    mut_prime_pairs = list(filter(lambda p: is_mutually_prime(*(p[1:4])), arr_pairs))
    output_list.append(mut_prime_pairs)
    print(f"{current_process().name} end")


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


def collect_prime_pairs(prime_pairs: list, limit: int, take_last=True):
    prime_limited: list
    if 0 <= limit < len(prime_pairs):
        prime_limited = list(
            map(
                lambda pp, ind: (ind, pp[0], pp[1], pp[3]),
                prime_pairs[:limit] + ([prime_pairs[-1]] if take_last else []),
                list(range(1, limit + 1)) + ([len(prime_pairs)] if take_last else [])
            )
        )
    else:
        prime_limited = list(
            map(
                lambda pp, ind: (ind, pp[0], pp[1], pp[3]),
                prime_pairs,
                range(1, len(prime_pairs) + 1)
            )
        )
    return prime_limited


def collect_mut_prime_pairs(mut_prime_pairs: list, primes_list: list[int], limit: int, take_last=True):
    mut_prime_limited: list
    if 0 <= limit < len(mut_prime_pairs):
        mut_prime_limited = list(
            map(
                lambda mpp, ind: (
                    ind, mpp[0], mpp[1],
                    find_prime_multipliers(mpp[1], primes_list),
                    mpp[3],
                    find_prime_multipliers(mpp[3], primes_list)
                ),
                mut_prime_pairs[:limit] + ([mut_prime_pairs[-1]] if take_last else []),
                list(range(1, limit + 1)) + ([len(mut_prime_pairs)] if take_last else [])
            )
        )
    else:
        mut_prime_limited = list(
            map(
                lambda mpp, ind: (
                    ind, mpp[0], mpp[1],
                    find_prime_multipliers(mpp[1], primes_list),
                    mpp[3],
                    find_prime_multipliers(mpp[3], primes_list)
                ),
                mut_prime_pairs,
                range(1, len(mut_prime_pairs) + 1)
            )
        )
    return mut_prime_limited


def collect_mut_prime_nums(mut_prime_pairs: list, primes_list: list[int], limit: int):
    mut_prime_list = [mut_prime_pairs[0][2]] if len(mut_prime_pairs) and limit > 0 else []
    limit -= 1
    for pair in mut_prime_pairs:
        if limit <= 0:
            break
        if is_mutually_prime(*(mut_prime_list + [pair[1]])):
            mut_prime_list.append(pair[1])
            limit -= 1
            if limit > 0 and is_mutually_prime(*(mut_prime_list + [pair[3]])):
                mut_prime_list.append(pair[3])
                limit -= 1
    mut_prime_list = list(
        map(
            lambda number, ind: (ind, number, find_prime_multipliers(number, primes_list)),
            sorted(mut_prime_list),
            range(1, len(mut_prime_list) + 1)
        )
    )
    return mut_prime_list


def calculate_pairs(pc: int, primes_list: list[int], output_key: str, output_dict: dict):
    print(f"{current_process().name} start")
    sub_prs = []
    manager = Manager()
    sub_prime_pairs = manager.list()
    sub_mut_prime_pairs = manager.list()
    part_pc = (pc - 2) // NUMBER_SUBTHREADS
    add_parts = (pc - 2) % NUMBER_SUBTHREADS
    start_deff = 1
    for i in range(NUMBER_SUBTHREADS):
        end_deff = start_deff + part_pc
        if add_parts > 0:
            add_parts -= 1
            end_deff += 1
        sub_arr_pairs = [(d, pc - d, pc, pc + d) for d in range(start_deff, end_deff)]
        start_deff = end_deff

        prime_pr = Process(
            target=calculate_prime_pairs,
            name=f"{output_key} {i + 1} prime pares subprocess",
            args=(sub_arr_pairs, primes_list, sub_prime_pairs)
        )
        mut_prime_pr = Process(
            target=calculate_mut_prime_pairs,
            name=f"{output_key} {i + 1} mutually prime pares subprocess",
            args=(sub_arr_pairs, sub_mut_prime_pairs)
        )
        sub_prs.append(prime_pr)
        sub_prs.append(mut_prime_pr)
        prime_pr.start()
        mut_prime_pr.start()

    for pr in sub_prs:
        pr.join()

    prime_concat = sorted(
        list(reduce(lambda res, spp: res + spp, list(sub_prime_pairs))),
        key=lambda pp: pp[0]
    )
    prime_limited = collect_prime_pairs(prime_concat, LIMIT_OUTPUT_PAIRS)

    mut_prime_concat = sorted(
        list(reduce(lambda res, smpp: res + smpp, list(sub_mut_prime_pairs))),
        key=lambda mpp: mpp[0]
    )
    mut_prime_limited = collect_mut_prime_pairs(mut_prime_concat, primes_list, LIMIT_OUTPUT_PAIRS)

    mut_prime_nums = collect_mut_prime_nums(mut_prime_concat, primes_list, LIMIT_MUTUALLY_PRIMES)

    output_dict[f"{output_key}_pp"] = (len(prime_concat), prime_limited)
    output_dict[f"{output_key}_mpp"] = (len(mut_prime_concat), mut_prime_limited)
    output_dict[f"{output_key}_mpn"] = mut_prime_nums
    print(f"{current_process().name} end")


def save_results(
        pc2_save: int, num_pc2_p_pairs_save: int, num_pc2_mp_pairs_save: int,
        pc2_p_pairs_save: list, pc2_mp_pairs_save: list, pc2_mp_nums_save: list,
        pc3_save: int, num_pc3_p_pairs_save: int, num_pc3_mp_pairs_save: int,
        pc3_p_pairs_save: list, pc3_mp_pairs_save: list, pc3_mp_nums_save: list,
):
    saving_data = [("pc2 =", pc2_save),
                   ("number prime pairs:", num_pc2_p_pairs_save),
                   ("number mutually prime pairs:", num_pc2_mp_pairs_save),
                   (),
                   ("pc3 =", pc3_save),
                   ("number prime pairs:", num_pc3_p_pairs_save),
                   ("number mutually prime pairs:", num_pc3_mp_pairs_save),
                   (), ("pc2 prime pairs:",),
                   ("i", "difference", "less prime", "most prime")]

    for pair in pc2_p_pairs_save:
        saving_data.append((pair[0], pair[1], pair[2], pair[3]))

    saving_data.extend([(), ("pc2 mutually prime pairs:",),
                        ("i", "difference",
                         "less", "multipliers",
                         "most", "multipliers")])
    for pair in pc2_mp_pairs_save:
        str_ml = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", pair[3].items()))
        str_mm = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", pair[5].items()))
        saving_data.append((pair[0], pair[1], pair[2], str_ml, pair[4], str_mm))

    saving_data.extend([(), ("i", "number", "multipliers")])
    for number in pc2_mp_nums_save:
        str_m = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", number[2].items()))
        saving_data.append((number[0], number[1], str_m))

    saving_data.extend([(), ("pc3 prime pairs:",),
                        ("i", "difference", "less prime", "most prime")])
    for pair in pc3_p_pairs_save:
        saving_data.append((pair[0], pair[1], pair[2], pair[3]))

    saving_data.extend([(), ("pc3 mutually prime pairs:",),
                        ("i", "difference",
                         "less", "multipliers",
                         "most", "multipliers")
                        ])
    for pair in pc3_mp_pairs_save:
        str_ml = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", pair[3].items()))
        str_mm = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", pair[5].items()))
        saving_data.append((pair[0], pair[1], pair[2], str_ml, pair[4], str_mm))

    saving_data.extend([(), ("i", "number", "multipliers")])
    for number in pc3_mp_nums_save:
        str_m = '*'.join(map(lambda m: f"{m[0]}^{m[1]}", number[2].items()))
        saving_data.append((number[0], number[1], str_m))

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
    limit_primes = collect_prime_numbers(max(pc2, pc3) * 2)
    # t = datetime.now()

    result_dict = Manager().dict()
    # calculate_pairs(100, limit_primes, '100', result_dict)
    pc2_pr = Process(
        target=calculate_pairs, name="pc2 process",
        args=(pc2, limit_primes, 'pc2', result_dict)
    )
    pc3_pr = Process(
        target=calculate_pairs, name="pc3 process",
        args=(pc3, limit_primes, 'pc3', result_dict)
    )
    pc2_pr.start()
    pc3_pr.start()

    pc2_pr.join()
    pc3_pr.join()

    # print(datetime.now() - t)

    save_results(
        pc2, result_dict["pc2_pp"][0], result_dict["pc2_mpp"][0],
        result_dict["pc2_pp"][1], result_dict["pc2_mpp"][1], result_dict["pc2_mpn"],
        pc2, result_dict["pc3_pp"][0], result_dict["pc3_mpp"][0],
        result_dict["pc3_pp"][1], result_dict["pc3_mpp"][1], result_dict["pc3_mpn"]
    )

    print("\nSUCCESS")
