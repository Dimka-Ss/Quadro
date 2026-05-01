
from BigFloat import *




def calculate_of_align(mantiss: list, diff: int, base: BigFloat):
    
    align_multiplier = 10**diff

    result_mantiss = []
    carry = 0

    for i in range(len(mantiss)):

        chunk = carry + mantiss[i] * align_multiplier
        carry = chunk // base
        result_mantiss.append(chunk % base)

    while carry > 0:
        result_mantiss.append(carry % base)
        carry = carry // base

    return result_mantiss


def align(bigf1: BigFloat, bigf2: BigFloat):
    
    bigf1_exponent = bigf1.exponent
    bigf2_exponent = bigf2.exponent

    bigf1_mantiss = bigf1.chunks
    bigf2_mantiss = bigf2.chunks

    bigger_of_exponent = max(bigf1_exponent, bigf2_exponent)
    smaller_of_exponent = min(bigf1_exponent, bigf2_exponent)

    result_exponent = smaller_of_exponent
    diff = bigger_of_exponent - smaller_of_exponent

    if diff == 0:
        return bigf1, bigf2

    elif bigf1_exponent < bigf2_exponent:

        aligned_mantiss = calculate_of_align(bigf2_mantiss, diff, BigFloat.BASE)
        result_bigf1 = bigf1
        result_bigf2 = BigFloat(bigf2.sign, aligned_mantiss, result_exponent)

    else:
        aligned_mantiss = calculate_of_align(bigf1_mantiss, diff, BigFloat.BASE)
        result_bigf1 = BigFloat(bigf1.sign, aligned_mantiss, result_exponent)
        result_bigf2 = bigf2

    return result_bigf1, result_bigf2


def compare_bigfs_chunks(bigf1: BigFloat, bigf2: BigFloat):
    ''' сравнение двух чисел по чанкам, вывод:  
    A > B = 1;  A < B = (-1);  A == B = 0'''
    aligned_bigf1, aligned_bigf2 = align(bigf1, bigf2)

    if len(aligned_bigf1.chunks) > len(aligned_bigf2.chunks):
        return 1
    
    elif len(aligned_bigf1.chunks) < len(aligned_bigf2.chunks):
        return -1
    else:
        for i in range(len(aligned_bigf1.chunks) - 1, -1, -1):
            if aligned_bigf1.chunks[i] > aligned_bigf2.chunks[i]:
                return 1
            
            if aligned_bigf1.chunks[i] < aligned_bigf2.chunks[i]:
                return -1
        return 0
            

def common_add(bigf1: BigFloat, bigf2: BigFloat, base: int):
    
    mantiss_bigf1, mantiss_bigf2 = bigf1.chunks, bigf2.chunks
    result_mantiss = []
    carry = 0

    max_length_mantiss = max(len(mantiss_bigf1), len(mantiss_bigf2))

    for i in range(max_length_mantiss):

        if i < len(mantiss_bigf1) :
            chunk_bigf1 = mantiss_bigf1[i]
        else:
            chunk_bigf1 = 0
        
        if i < len(mantiss_bigf2):
            chunk_bigf2 = mantiss_bigf2[i]
        else:
            chunk_bigf2 = 0

        value = carry + chunk_bigf1 + chunk_bigf2
        carry = value // base
        result_mantiss.append(value % base)
    
    while carry > 0:
        result_mantiss.append(carry % base)
        carry = carry // base
    
    return result_mantiss


def common_sub(bigf1: BigFloat, bigf2: BigFloat, base: int):
    
    mantiss_bigf1, mantiss_bigf2 = bigf1.chunks, bigf2.chunks
    result_mantiss = []
    borrow = 0

    max_length_mantiss = max(len(mantiss_bigf1), len(mantiss_bigf2))

    for i in range(max_length_mantiss):

        if i < len(mantiss_bigf1) :
            chunk_bigf1 = mantiss_bigf1[i]
        else:
            chunk_bigf1 = 0
        
        if i < len(mantiss_bigf2):
            chunk_bigf2 = mantiss_bigf2[i]
        else:
            chunk_bigf2 = 0

        diff = chunk_bigf1 - chunk_bigf2 - borrow

        if diff < 0:
            diff += base
            borrow = 1
        else:
            borrow = 0
        
        result_mantiss.append(diff)    
    return result_mantiss


def addition(bigf1: BigFloat, bigf2: BigFloat):
    
    aligned_bigf1, aligned_bigf2 = align(bigf1, bigf2)

    result_exponent = aligned_bigf1.exponent

    if aligned_bigf1.sign == aligned_bigf2.sign:
        
        result_of_addition = common_add(aligned_bigf1, aligned_bigf2, BigFloat.BASE)
        new_bigf = BigFloat(aligned_bigf1.sign, 
                            result_of_addition, 
                            result_exponent)
        
        return normalize(new_bigf)
    else:
        result_of_compare = compare_bigfs_chunks(aligned_bigf1, aligned_bigf2)

        if result_of_compare == 1:
            result_sign = aligned_bigf1.sign
            result_of_substraction = common_sub(aligned_bigf1, 
                                                aligned_bigf2, 
                                                BigFloat.BASE)
        elif result_of_compare == -1:
            result_sign = aligned_bigf2.sign
            result_of_substraction = common_sub(aligned_bigf2, 
                                                aligned_bigf1, 
                                                BigFloat.BASE)
        elif result_of_compare == 0:
            result_sign = 1
            result_of_substraction = [0]

        new_bigf = BigFloat(result_sign, 
                            result_of_substraction, 
                            result_exponent)
        return normalize(new_bigf)


def subtruction(bigf1: BigFloat, bigf2: BigFloat):
    negative_copy_bigf2 = BigFloat(bigf2.sign * -1, bigf2.chunks, bigf2.exponent)
    return addition(bigf1, negative_copy_bigf2)


















