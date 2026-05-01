from BigFloat import *
from math import *


def bound_power_of_2(bigf1_chunks, bigf2_chunks):
    
    bound_size = 1
    n = len(bigf1_chunks) + len(bigf2_chunks) - 1

    while bound_size < n:
        bound_size <<= 1

    return bound_size


def permutation_index(chunks_list: list):

    n = len(chunks_list)
    bits_count = (n - 1).bit_length()

    for i in range(n):
        j = reverse_bits_index(i, bits_count)

        if i < j:
            chunks_list[i], chunks_list[j] = chunks_list[j], chunks_list[i]

    return chunks_list


def reverse_bits_index(i: int, bits_count: int):

    binary = bin(i)[2:].zfill(bits_count)
    reversed_binary = binary[::-1]
    
    return int(reversed_binary, 2)


def translate_to_complex_value(boundle_size, bigf1_chunks, bigf2_chunks):

    bigf1_complex_chunks = [0j] * boundle_size
    bigf2_complex_chunks = [0j] * boundle_size

    for key, val in enumerate(bigf1_chunks):
        bigf1_complex_chunks[key] = complex(val, 0)

    for key, val in enumerate(bigf2_chunks):
        bigf2_complex_chunks[key] = complex(val, 0)

    return bigf1_complex_chunks, bigf2_complex_chunks


def FFT(bigf_chunks: list, reverse=False):
            
    length_chunks_list = len(bigf_chunks)

    permutation_index(bigf_chunks)
    length = 2
    
    while length <= length_chunks_list:

        half = length // 2
        angle = (-2 if reverse else 2) * pi / length
        phi = complex(cos(angle), sin(angle))
            
        for start in range(0, length_chunks_list, length):
            w = complex(1, 0)
            for j in range(half):

                u = bigf_chunks[start + j]
                v = bigf_chunks[start + j + half] * w

                bigf_chunks[start + j] = u + v
                bigf_chunks[start + j + half] = u - v

                w *= phi
        length *= 2

    if reverse:
        bigf_chunks = [x / length_chunks_list for x in bigf_chunks]

    return bigf_chunks


def multiply_values(bigf1_complex_chunks, bigf2_complex_chunks):

    bigf1_sequence_chunks = FFT(bigf1_complex_chunks, reverse=False)
    bigf2_sequence_chunks = FFT(bigf2_complex_chunks, reverse=False)

    for i in range(len(bigf1_sequence_chunks)):
        bigf1_sequence_chunks[i] *= bigf2_sequence_chunks[i]

    fouriere_transformed_bigf1_chunks = FFT(bigf1_sequence_chunks, reverse=True)

    result_chunks = []

    for i in fouriere_transformed_bigf1_chunks:
        result_chunks.append(int(round(i.real)))
    
    return result_chunks


def transfer_of_remainder(mantiss, base):
        carry = 0

        for i in range(len(mantiss)):
            mantiss[i] += carry
            carry = mantiss[i] // base
            mantiss[i] = mantiss[i] % base
        
        while carry > 0:
            mantiss.append(carry % base)
            carry = carry // base
        
        return mantiss


def main_multiply(bigf1: BigFloat, bigf2: BigFloat, precision = 2050):

    result_sign = bigf1.sign * bigf2.sign
    result_exponent = bigf1.exponent + bigf2.exponent

    bigf1_chunks = bigf1.chunks
    bigf2_chunks = bigf2.chunks

    boundle_size = bound_power_of_2(bigf1_chunks, bigf2_chunks)

    bigf1_complex_chunks, bigf2_complex_chunks = translate_to_complex_value(boundle_size, bigf1_chunks, bigf2_chunks)

    rough_result_chunks = multiply_values(bigf1_complex_chunks, bigf2_complex_chunks)

    final_result_chunks = transfer_of_remainder(rough_result_chunks, BigFloat.BASE)

    new_bigf = normalize(BigFloat(result_sign, final_result_chunks, result_exponent))

    if precision != 0:
        new_bigf = BigFloat_round(new_bigf, precision)

    return new_bigf












