from BigFloat import *
from utility_func import *
from time import perf_counter
from special_solver import *

def special_to_string(x):
    if isinstance(x, SpecialVariables):
        return x.type
    return to_string_for_output(x)


def complex_output(x):
    re_s = special_to_string(x.real)
    im_s = special_to_string(x.imag)

    sign = '-' if im_s.startswith('-') else '+'
    im_abs = im_s.lstrip('-')

    return f"{re_s} {sign} {im_abs}i"


def is_bigf(x1):
    return isinstance(x1, BigFloat)


def is_special(x1):
    return isinstance(x1, SpecialVariables)


def output_of_roots(x1, x2):
    if x1 is not None:
        if isinstance(x1, ComplexBigFloat):
            print(complex_output(x1))
        else:
            print(f'x1 = {special_to_string(x1)}')

    if x2 is not None:
        if isinstance(x2, ComplexBigFloat):
            print(complex_output(x2))
        else:
            print(f'x2 = {special_to_string(x2)}')


def output_result(answer: Answer):
    type_result = answer.answer_type
    print(type_result)

    output_of_roots(answer.get_x1(), answer.get_x2())