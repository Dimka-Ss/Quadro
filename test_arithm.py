from time import perf_counter
 
from BigFloat import BigFloat
from utility_func import (
    random_bigf,
    bf_to_dec,
    compare,
    print_mismatch,
    to_string_for_output,
)
from BigFloat_Interpret import *
from BigFloat_Arithmetic_Fouriera import main_multiply as mul
from BigFloat_Arithmetic_Newton_division import main_newton_division as div
from BigFloat_Arithmetic_Add_Sub import addition as add, subtruction as sub
from BigFloat_Arithmetic_sqrt import Sqrt
 
 
 
def test_add(test_count: int = 100):
    count_true = 0
    total_time = 0.0
 
    for i in range(test_count):
        a_bigf = random_bigf()
        b_bigf = random_bigf()
 
        dec_res = bf_to_dec(a_bigf) + bf_to_dec(b_bigf)
 
        start = perf_counter()
        res_bigf = add(a_bigf, b_bigf)
        total_time += perf_counter() - start
 
 
        if compare(res_bigf, dec_res):
            count_true += 1
        else:
            print_mismatch(res_bigf, format(dec_res + 0, 'f'), f'add {i}')
 
    avg_time = total_time / test_count
    print(f"сложение: {count_true:3}/{test_count} среднее время: {avg_time:.6f} с")
 
 
def test_sub(test_count: int = 100):
    count_true = 0
    total_time = 0.0
 
    for i in range(test_count):
        a_bigf = random_bigf()
        b_bigf = random_bigf()
 
        dec_res = bf_to_dec(a_bigf) - bf_to_dec(b_bigf)
 
        start = perf_counter()
        res_bigf = sub(a_bigf, b_bigf)
        total_time += perf_counter() - start
 
 
        if compare(res_bigf, dec_res):
            count_true += 1
        else:
            print_mismatch(res_bigf, format(dec_res + 0, 'f'), f'sub {i}')
 
    avg_time = total_time / test_count
    print(f"вычитание: {count_true:3}/{test_count} среднее время: {avg_time:.6f} с")
 
 
def test_mul(test_count: int = 100):
    count_true = 0
    total_time = 0.0
 
    for i in range(test_count):
        a_bigf = random_bigf()
        b_bigf = random_bigf()
 
        dec_res = bf_to_dec(a_bigf) * bf_to_dec(b_bigf)
 
        start = perf_counter()
        res_bigf = mul(a_bigf, b_bigf)
        total_time += perf_counter() - start
 
        if compare(res_bigf, dec_res):
            count_true += 1
        else:
            print_mismatch(res_bigf, format(dec_res + 0, 'f'), f'mul {i}')
 
    avg_time = total_time / test_count
    print(f"умножение: {count_true:3}/{test_count} среднее время: {avg_time:.6f} с")
 
 
def test_div(test_count: int = 100):
    count_true = 0
    total_time = 0.0
 
    for i in range(test_count):
        a_bigf = random_bigf()
        b_bigf = random_bigf()
 
        dec_res = bf_to_dec(a_bigf) / bf_to_dec(b_bigf)
 
        start = perf_counter()
        res_bigf = div(a_bigf, b_bigf)
        total_time += perf_counter() - start
 
        if compare(res_bigf, dec_res):
            count_true += 1
        else:
            print_mismatch(res_bigf, format(dec_res + 0, 'f'), f'div {i}')
 
    avg_time = total_time / test_count
    print(f"деление: {count_true:3}/{test_count} среднее время: {avg_time:.6f} с")
 
 
def test_sqrt(test_count: int = 100):
    count_true = 0
    total_time = 0.0
 
    for i in range(test_count):
        a_bigf = random_bigf()
        a_bigf.set_sign(1)    
 
        dec_res = bf_to_dec(a_bigf).sqrt()
 
        start = perf_counter()
        res_bigf = Sqrt(a_bigf)
        total_time += perf_counter() - start
 
        if compare(res_bigf, dec_res):
            count_true += 1
        else:
            print_mismatch(res_bigf, format(dec_res + 0, 'f'), f'sqrt {i}')
 
    avg_time = total_time / test_count
    print(f"корень: {count_true:3}/{test_count} среднее время: {avg_time:.6f} с")
 
 
def test_interpret_small_input_values():
    tests = ( 
          " 13.233",
                "+",
                "-",
                ".",
                ",",
                "01",
                "00 ",
                "0123",
                "1.",
                "1,",
                "+.",
                "-.",
                "e10",
                "1e",
                "1e+",
                "1e-",
                "abc",
                "1abc",
                "abc1",
                "1 2",
                "1.2.3",
                "-1-2-3",
                "0",
                "1",
                "9",
                "10",
                "123",
                "+123",
                "-123",
                "1.5",
                "1,5",
                "0.5",
                "0,5",
                ".5",
                ",5",
                "+.5",
                "-.5",
                "1e2",
                "1E2",
                "1e+2",
                "1e-2",
                "-1.5e+10",
                "1_000",
                "1_000_000",
                "1_000.5",
                "1.5_5",
                "1e1_0",
                "1_0e1_0",
                "_1",          
                "1_",          
                "1__2",        
                "1._5",       
                "1.5_",        
                "1e_5",       
                "1e5_"
                )
 
    for i in tests:
        string = i
        result = FloatParser().interpret(string)
        if not result.success:
            print(f"ошибка в строкке '{string}': {result.error}")
        else:
            print(f"исходная строка: {string} результат: {to_string_for_output(result.value)}")
        print()
 
 
 
 
 
 
if __name__ == '__main__':
    count = 10
    
    # test_interpret_small_input_values()
    # test_add(count)
    # test_sub(count)
    # test_mul(count)
    # test_div(count)
    # test_sqrt(count)




































