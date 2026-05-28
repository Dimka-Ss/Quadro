from BigFloat import *
from utility_func import *

CHUNK_SIZE = BigFloat.CHUNK_SIZE
BASE = BigFloat.BASE


def calculate_align(bigf: BigFloat, target_exp: int):

    diff = bigf.exponent - target_exp
    count_chunks = diff // CHUNK_SIZE
    remainder = diff % CHUNK_SIZE

    aligned_bigf = short_mul(bigf, 10**remainder, -diff)
    mantiss = [0] * count_chunks + aligned_bigf.chunks
    aligned_bigf.chunks = mantiss

    return aligned_bigf


def align(bigf1: BigFloat, bigf2: BigFloat):

    if bigf1.exponent > bigf2.exponent:
        bigf1 = calculate_align(bigf1, bigf2.exponent)

    elif bigf1.exponent < bigf2.exponent:
        bigf2 = calculate_align(bigf2, bigf1.exponent)

    return bigf1, bigf2


def common_add(bigf1: BigFloat, bigf2: BigFloat):

    bigf1_mantiss, bigf2_mantiss = bigf1.chunks, bigf2.chunks

    if len(bigf1_mantiss) > len(bigf2_mantiss):
        bigger, smaller = bigf1_mantiss, bigf2_mantiss
    else:
        bigger, smaller = bigf2_mantiss, bigf1_mantiss

    for i in range(len(smaller)):
        bigger[i] += smaller[i]

    bigger = transf_remainder(bigger, BASE)
    return bigger


def a_is_greater_b(a: BigFloat, b: BigFloat):
    a_mantiss, b_mantiss = a.chunks, b.chunks

    if len(a_mantiss) != len(b_mantiss):
        return len(a_mantiss) > len(b_mantiss)

    for i in range(len(a_mantiss) - 1, -1, -1):
        if a_mantiss[i] != b_mantiss[i]:
            return a_mantiss[i] > b_mantiss[i]
    return True


def subtract(minuend, subtrahend):
    borrow = 0
    for i in range(len(subtrahend)):
        diff = minuend[i] - subtrahend[i] - borrow
        if diff < 0:
            diff += BASE
            borrow = 1
        else:
            borrow = 0
        minuend[i] = diff

    i = len(subtrahend)
    while borrow and i < len(minuend):
        diff = minuend[i] - borrow
        if diff < 0:
            diff += BASE
            borrow = 1
        else:
            borrow = 0
        minuend[i] = diff
        i += 1
    return minuend


def common_sub(bigf1: BigFloat, bigf2: BigFloat):

    bigf1_mantiss, bigf2_mantiss = bigf1.chunks, bigf2.chunks
    sign = bigf1.sign

    if a_is_greater_b(bigf1, bigf2):
        result = subtract(bigf1_mantiss, bigf2_mantiss)
        return BigFloat(sign, result, bigf1.exponent)

    result = subtract(bigf2_mantiss, bigf1_mantiss)
    sign = -sign
    return BigFloat(sign, result, bigf1.exponent)


def addition(bigf1: BigFloat, bigf2: BigFloat):

    if mantiss_is_zero(bigf1.chunks):
        return normalize(copy_BF(bigf2))
    
    if mantiss_is_zero(bigf2.chunks):
        return normalize(copy_BF(bigf1))

    a, b = align(copy_BF(bigf1), copy_BF(bigf2))

    if a.sign == b.sign:
        result = BigFloat(a.sign, common_add(a, b), a.exponent)
        return normalize(result)

    result = common_sub(a, b)
    return normalize(result)


def subtruction(bigf1: BigFloat, bigf2: BigFloat):
    negative_copy_bigf2 = BigFloat(bigf2.sign * -1, bigf2.chunks, bigf2.exponent)
    return addition(bigf1, negative_copy_bigf2)
