from BigFloat_Arithmetic_Add_Sub import *
from BigFloat_Arithmetic_Fouriera import *
from BigFloat_Interpret import *
from utility_func import *



def main_newton_division(bigf1: BigFloat, bigf2: BigFloat):
    x_null = first_approximation(bigf2)
    rev_b = find_reverse_b(bigf2, x_null)
    return main_multiply(bigf1, rev_b)


def first_approximation(bigf: BigFloat):
    bigf_chunks = bigf.chunks
    length = len(bigf_chunks)
    take = min(length, 3)
    dropped = length - take

    top = 0
    for i in range(length - 1, dropped - 1, -1):
        top = top * BigFloat.BASE + bigf_chunks[i]

    count_of_digits = take * BigFloat.CHUNK_SIZE + 2

    power_of_10 = count_of_digits + len(str(top)) - 1
    mantiss_zero_x = divide_to_chunks(str(10**power_of_10 // top), BigFloat.CHUNK_SIZE)
    res_exp = -power_of_10 - dropped * BigFloat.CHUNK_SIZE - bigf.exponent

    return normalize(BigFloat(1, mantiss_zero_x, res_exp))


# xₙ₊₁ = xₙ · (2 - b · xₙ)
def find_reverse_b(bigf: BigFloat, x):
    TWO = BigFloat(1, [2], 0)
    abs_bigf = abs_bigfloat(bigf)
    current_chunks = 2

    for i in range(11):
        current_chunks *= 2
        correction = subtruction(TWO, main_multiply(BigFloat_round(abs_bigf, current_chunks + 10), x, current_chunks + 10))
        x = main_multiply(x, correction, current_chunks + 20)

    result = BigFloat(bigf.sign, x.chunks, x.exponent)

    return normalize(result)

