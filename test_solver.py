from decimal import getcontext
from time import perf_counter
from random import choices
 
from BigFloat import Coefs, SpecialVariables
from BigFloat_Interpret import Input
from main_solver import root_calculations, input_data
from decimal_solver import root_calculations_decimal, coefs_to_decimal
from compare import answers_equal
from utility_func import random_bigf, to_string_for_output
from test_arithm import test_add, test_sub, test_mul, test_div, test_sqrt
 
 
getcontext().prec = 250000
 
 
def check_one(coefs: Coefs):
    t0 = perf_counter()
    bf_ans = root_calculations(coefs)
    elapsed = perf_counter() - t0
 
    dec_coefs = coefs_to_decimal(coefs)
    dec_ans   = root_calculations_decimal(dec_coefs)
 
    return answers_equal(bf_ans, dec_ans), elapsed
 
 
def roots_solve(count=10):
    total_time = 0.0
    fails = 0
 
    for _ in range(count):
        coefs = Coefs(random_bigf(), random_bigf(), random_bigf())
        ok, t = check_one(coefs)
        total_time += t
        if not ok:
            fails += 1
 
    avg = total_time / count if count else 0
    status = 'OK' if fails == 0 else f'FAIL ({fails})'
    print(f"квадратка: {status}, среднее время {avg:.6f} с, ошибок {fails}/{count}")
 
 
def test_through_input(count=10):
    total_time = 0.0
    fails = 0

    for _ in range(count):
        a = to_string_for_output(random_bigf())
        b = to_string_for_output(random_bigf())
        c = to_string_for_output(random_bigf())
        line = f"{a} {b} {c}"

        t0 = perf_counter()
        coefs = input_data(line)
        t_parse = perf_counter() - t0

        if coefs is None:
            fails += 1
            continue

        ok, t_solver = check_one(coefs)
        total_time += t_parse + t_solver

        if not ok:
            fails += 1
 
    avg = total_time / count if count else 0
    status = 'OK' if fails == 0 else f'FAIL ({fails})'
    print(f"через ввод: {status}, среднее время {avg:.6f} с, ошибок {fails}/{count}")
 
 
def random_special_line():
    s1 = to_string_for_output(random_bigf())
    s2 = to_string_for_output(random_bigf())
    pool = ['nan', '-inf', 'inf', s1, s2]
    return ' '.join(choices(pool, k=3))
 
 
def test_special_solver(count=10):
    total_time = 0.0
    fails = 0
 
    for _ in range(count):
        line = random_special_line()
        coefs = input_data(line)
        if coefs is None:
            fails += 1
            continue
 
        ok, t = check_one(coefs)
        total_time += t
        if not ok:
            fails += 1
 
    avg = total_time / count if count else 0
    status = 'OK' if fails == 0 else f'FAIL ({fails})'
    print(f"special: {status}, среднее время {avg:.6f} с, ошибок {fails}/{count}")
 
 
if __name__ == "__main__":
    count = 1
 
    # test_add(count)
    # test_sub(count)
    # test_mul(count)
    # test_div(count)
    # test_sqrt(count)
 
    # roots_solve(count)
    # test_through_input(count)
    # test_special_solver(count)