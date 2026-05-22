from utility_func import *
from math import pi, sin, cos

roots_cache = {}
perm_cache = {}
BOARD_NAIVE_MUL = 20
BOARD_KAR_MUL = 200


def add_chunks(a, b):
    if len(a) < len(b):
        a, b = b, a
    result = a[:]
    for i in range(len(b)):
        result[i] += b[i]
    return result


def sub_chunks(a, b):
    result = a[:]
    for i in range(len(b)):
        result[i] -= b[i]
    return result


def shift_chunks(a, m):
    return [0] * m + a


def kar_convolution(a, b):
    if len(a) <= BOARD_NAIVE_MUL or len(b) <= BOARD_NAIVE_MUL:
        return naive_convolution(a, b)
    
    m = max(len(a), len(b)) // 2

    a_low = a[:m]
    a_high = a[m:]
    b_low = b[:m]
    b_high = b[m:]

    z0 = kar_convolution(a_low, b_low)
    z2 = kar_convolution(a_high, b_high)
    z1 = kar_convolution(add_chunks(a_low, a_high), add_chunks(b_low, b_high))

    z1 = sub_chunks(z1, z0)
    z1 = sub_chunks(z1, z2)

    result = add_chunks(z0, shift_chunks(z1, m))
    result = add_chunks(result, shift_chunks(z2, m * 2))

    return result


def naive_convolution(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            c[i + j] += a[i] * b[j]
    return c


def get_bit_reverse_permutation(n):
    if n not in perm_cache:
        perm = list(range(n))
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            perm[i] = j
        perm_cache[n] = perm
    return perm_cache[n]


def apply_bit_reverse(a, perm):
    n = len(a)
    for i in range(n):
        if i < perm[i]:
            a[i], a[perm[i]] = a[perm[i]], a[i]


def get_roots(n):
    if n not in roots_cache:
        w_forward = [0] * (n // 2)
        w_inverse = [0] * (n // 2)
        for k in range(n // 2):
            angle = 2 * pi * k / n
            w = complex(cos(angle), sin(angle))
            w_forward[k] = w
            w_inverse[k] = w.conjugate()
        roots_cache[n] = (w_forward, w_inverse)
    return roots_cache[n]


def FFT(a, roots_w):

    n = len(a)
    perm = get_bit_reverse_permutation(n)
    apply_bit_reverse(a, perm)
    if n == 1:
        return a
    length = 2
    while length <= n:
        step = n // length
        half= length // 2
        for start in range(0, n, length):    
            for k in range(half):
                w = roots_w[k * step]
                temp_E = a[k + start]
                temp_O = w * a[k + start + half]
                a[start + k] = temp_E + temp_O
                a[start + k + half] = temp_E - temp_O

        length *= 2
    return a


def padding_values(a, b):
    n = len(a) + len(b) - 1
    power_2 = 2
    while power_2 < n:
        power_2 <<= 1

    a_padded = a + [0] * (power_2 - len(a))
    b_padded = b + [0] * (power_2 - len(b))

    return a_padded, b_padded, power_2


def mul_fft(a_padded, b_padded, power_2):
    
    w_forward, w_inverse = get_roots(power_2)
    c = [0] * power_2
    for i in range(power_2):
        c[i] = (complex(a_padded[i], b_padded[i]))
    c_fft = FFT(c, w_forward)
    
    fft_a_b_mul = [0] * power_2
    for k in range(power_2):
        conj = c_fft[(power_2 - k) % power_2].conjugate()
        fft_a_k = (c_fft[k] + conj) / 2
        fft_b_k = (c_fft[k] - conj) / 2j
        fft_a_b_mul[k] = (fft_a_k * fft_b_k)

    res = FFT(fft_a_b_mul, w_inverse)
    return [int(x.real / power_2 + 0.5) for x in res]


def main_multiply(bigf1: BigFloat, bigf2: BigFloat, precision=2550):

    result_sign = bigf1.sign * bigf2.sign
    result_exponent = bigf1.exponent + bigf2.exponent

    a, b = bigf1.chunks, bigf2.chunks

    if len(a) < BOARD_NAIVE_MUL and len(b) < BOARD_NAIVE_MUL:
        result_mul = naive_convolution(a, b)

    elif len(a) < BOARD_KAR_MUL and len(b) < BOARD_KAR_MUL:
        result_mul = kar_convolution(a, b)
        
    else:
        a_padded, b_padded, power_2 = padding_values(a, b)
        result_mul = mul_fft(a_padded, b_padded, power_2)

    final_result = transf_remainder(result_mul, BigFloat.BASE)

    new_bigf = normalize(BigFloat(result_sign, final_result, result_exponent))
    if precision != 0:
        new_bigf = BigFloat_round(new_bigf, precision)

    return new_bigf




