from BigFloat_Arithmetic_Add_Sub import *
from BigFloat_Arithmetic_Fouriera import *
from BigFloat import *
from utility_func import *

chunk_size = BigFloat.CHUNK_SIZE
base = BigFloat.BASE

root_10 = BigFloat(1, [79331, 1683, 27766, 3162], -18)
constant_newton = BigFloat(1, [3], 0)

def Sqrt(bigf: BigFloat):
    x = copy_BF(bigf)
    x_null = first_approximation(x)
    inv_sqrt = newton_reciprocal(x, x_null) 
    return main_multiply(x, inv_sqrt)


def first_approximation(bigf: BigFloat):
    bigf_chunks = list(bigf.chunks)
    top = bigf_chunks[-1] * base + (bigf_chunks[-2] if len(bigf_chunks) >= 2 else 0)
    approx = 1 / top**0.5
    approx = f"{approx:.50f}"

    approx = from_string(approx)
    total = (bigf.exponent + chunk_size * len(bigf_chunks)) % 2
    if total == 0:
        new_exponent = approx.exponent - (bigf.exponent + chunk_size * (len(bigf_chunks) - 2)) // 2
    else:
        new_exponent = approx.exponent - (bigf.exponent + chunk_size * (len(bigf_chunks) - 2)) // 2 - 1

    approx.set_exponent(new_exponent)
    approx.set_sign(1)
    if total == 1:
        approx = main_multiply(approx, root_10)
    return approx


def newton_reciprocal(x, x_null):
    precision = 2
    for i in range(11):
        precision *= 2
        num = BigFloat_round(x, precision + 10)
        x_n = main_multiply(main_multiply(x_null, x_null, precision + 20), num, precision + 20)
        x_n = short_mul(subtruction(constant_newton, x_n), 5, -1)
        x_null = main_multiply(x_null, x_n, precision + 20)
    return x_null































