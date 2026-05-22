from BigFloat import BigFloat, SpecialVariables
from random import randrange, choice


import random
from decimal import Decimal, getcontext, localcontext
from time import perf_counter

getcontext().prec = 250000
COMPARE_PRECISION = 10000



def divide_to_chunks(mantiss: str, base: int):

    chunks = []
    
    for i in range(len(mantiss), 0, -base):
    
        chunk_boarder = max(0, i - base)
        chunks.append(int(mantiss[chunk_boarder : i]))

    return chunks


def abs_bigfloat(bigf: BigFloat):
    return BigFloat(1, bigf.chunks, bigf.exponent)


def normalize(bigfloat_num: BigFloat):

    mantiss = bigfloat_num.chunks
    sign = bigfloat_num.sign
    new_exp = bigfloat_num.exponent

    len_old_mantiss = len(mantiss)

    if mantiss_is_zero(mantiss):
        return make_zero(mantiss)
    else:
        if mantiss_starts_with_zero(mantiss):
            mantiss = processing_starting_zeros(mantiss)
            new_exp = set_new_exp_after_starting_zero_processing(bigfloat_num, len_old_mantiss, mantiss)

        if mantiss_ends_with_zero(mantiss):
            mantiss = ending_zero_processing(mantiss)

    return BigFloat(sign, mantiss, new_exp)


def mantiss_is_zero(mantiss):
    return all(x == 0 for x in mantiss)


def make_zero(mantiss):
    mantiss = [0]
    return BigFloat(1, mantiss, 0)


def mantiss_starts_with_zero(mantiss):
    return mantiss[0] == 0


def processing_starting_zeros(mantiss):
    while mantiss[0] == 0:
        del mantiss[0]
    return mantiss


def set_new_exp_after_starting_zero_processing(bigf: BigFloat, len_old_mantiss, new_mantiss):
    len_new_mantissa = len(new_mantiss)
    old_exp = bigf.exponent
    new_exp = (len_old_mantiss - len_new_mantissa) * BigFloat.CHUNK_SIZE + old_exp
    return new_exp


def mantiss_ends_with_zero(mantiss):
    return mantiss[-1] == 0


def ending_zero_processing(mantiss):
    while mantiss[-1] == 0:
        del mantiss[-1]
    return mantiss


def add_zeros_to_mantissa_blocks(mantiss):
    for i in range(1, len(mantiss)):
            if len(mantiss[i]) < BigFloat.CHUNK_SIZE:
                mantiss[i] = '0' * (BigFloat.CHUNK_SIZE - len(mantiss[i])) + mantiss[i]
    return mantiss


def copy_BF(BF):
    exp = BF.exponent
    mantissa = BF.chunks[:]
    sign = BF.sign
    return BigFloat(sign, mantissa, exp)


def from_string(s):
    s = s.strip().lower()
    if not s:
        return BigFloat()

    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]

    exp = 0
    if 'e' in s:
        idx = s.index('e')
        exp = int(s[idx + 1:] or 0)
        s = s[:idx]

    if '.' in s:
        idx = s.index('.')
        frac_len = len(s) - idx - 1
        s = s.replace('.', '')
        exp -= frac_len
    s = s.lstrip('0') or '0'

    mantissa = []
    for i in range(len(s), 0, -BigFloat.CHUNK_SIZE):
        start = max(0, i - BigFloat.CHUNK_SIZE)
        mantissa.append(int(s[start:i]))
    return BigFloat(sign, mantissa, exp)


def to_string_for_output(BigFloat_num):
    if isinstance(BigFloat_num, SpecialVariables):
        return BigFloat_num
    mantissa = BigFloat_num.chunks
    exp = BigFloat_num.exponent
    sign = BigFloat_num.sign
    big_num_str = mantissa_to_str(mantissa)
    if exp < 0:
        big_num_str = insert_point(big_num_str, exp)
    elif exp > 0:
        big_num_str = insert_zeros(big_num_str, exp)
    if sign == -1:
        big_num_str = insert_sign(big_num_str)
    return big_num_str


def insert_point(mantiss_str, exp):
    if abs(exp) > len(mantiss_str):
        mantiss_str = '0.' + '0' * (abs(exp) - len(mantiss_str)) + mantiss_str
    elif abs(exp) == len(mantiss_str):
        mantiss_str = '0.' + mantiss_str
    else:
        mantiss_str = mantiss_str[:exp] + '.' + mantiss_str[exp:]
    return mantiss_str


def insert_zeros(mantiss_str, exp):
    mantiss_str = mantiss_str + '0' * exp
    return mantiss_str


def insert_sign(mantiss_str):
    return '-' + mantiss_str


def mantissa_to_str(mantiss):
        mantiss = mantiss[::-1]
        mantiss = list(map(str, mantiss))
        mantiss = add_zeros_to_mantissa_blocks(mantiss)
        mantiss = ''.join(mantiss)
        return mantiss


def random_bigf():
    mantiss = []
    exp = randrange(-1000, 1000)
    prec = choice([2000, 1999])
    for _ in range(prec):
        elem = randrange(10000, 100000)
        mantiss.append(elem)
    sign = choice([-1, 1])
    return normalize(BigFloat(sign, mantiss, exp))


def BigFloat_round(bigf: BigFloat, precision):
    
    mantiss = bigf.chunks
    exp = bigf.exponent

    old_len = len(mantiss)
    if old_len < precision:
        return bigf
    
    mantiss = mantiss[-precision:]
    exp = exp + (old_len - len(mantiss)) * BigFloat.CHUNK_SIZE
    bigf = BigFloat(bigf.sign, mantiss, exp)

    return bigf


def int_to_BF(number):
    return from_string(str(number))


def transf_remainder(result, base):
    carry = 0
    for i in range(len(result)):
        result[i] += carry
        carry = result[i] // base
        result[i] = result[i] % base

    while carry > 0:
        result.append(carry % base)
        carry = carry // base
    return result


def short_mul(bigf: BigFloat, integ, exp_delta=0):
    mantiss = bigf.chunks
    for i in range(len(mantiss)):
        mantiss[i] *= abs(integ)
    mantiss = transf_remainder(mantiss, BigFloat.BASE)
    sign = bigf.sign * (1 if integ > 0 else -1)
    return BigFloat(sign, mantiss, bigf.exponent + exp_delta)


def bf_to_dec(bigf: BigFloat) -> Decimal:
    return Decimal(to_string_for_output(bigf))
 
 
def compare(num, dec_val: Decimal, precision: int = COMPARE_PRECISION):
    with localcontext() as ctx:
        ctx.prec = precision + 100
        if isinstance(num, BigFloat):   
            my_string = format(Decimal(to_string_for_output(num)) + 0, 'f')
            dec = format(dec_val + 0, 'f')
        if isinstance(num, Decimal):
            my_string = format(num + 0, 'f')
            dec = format(dec_val + 0, 'f')
    return my_string[:precision] == dec[:precision]

 
def print_mismatch(bigf: BigFloat, res_dec: str, point: str = ''):
    res_bigf = to_string_for_output(bigf)
    for j in range(min(len(res_bigf), len(res_dec))):
        if res_bigf[j] != res_dec[j]:
            start = max(0, j - 10)
            print(f'{point} не совпали на позиции {j}')
            print(f'bigf: {res_bigf[start: j + 10]}')
            print(f'decimal: {res_dec[start: j + 10]}')
            return
    print(f'{point} строки разной длины, расхождение после позиции {min(len(res_bigf), len(res_dec))}')


def get_big_string():
    a = to_string_for_output(random_bigf())
    b = to_string_for_output(random_bigf())
    c = to_string_for_output(random_bigf())
    s = a + ' ' + b + ' ' + c
    return s, a, b, c