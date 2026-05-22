from decimal import Decimal, localcontext
 
from BigFloat import (
    BigFloat,
    Answer,
    Answer_options,
    ComplexBigFloat,
    SpecialVariables,
)
from decimal_solver import DecAnswer, DecComplex
from utility_func import to_string_for_output, COMPARE_PRECISION
 
 
def answers_equal(bf_ans: Answer, dec_ans: DecAnswer, precision: int = COMPARE_PRECISION):
    if bf_ans.answer_type != dec_ans.kind:
        return False
 
    kind = bf_ans.answer_type
 
    if kind in (Answer_options.INFINITY_SOLUTIONS, Answer_options.NO_SOLUTIONS):
        return True
 
    if kind == Answer_options.LINEAR:
        return values_equal(bf_ans.x1, dec_ans.x1, precision)
 
    if kind == Answer_options.SAME_ROOTS:
        return values_equal(bf_ans.x1, dec_ans.x1, precision)
 
    if kind == Answer_options.DIFFERENT_ROOTS:
        return two_roots_equal_any_order(bf_ans, dec_ans, precision)
 
    if kind == Answer_options.COMPLEX_SOLUTIONS:
        
        return (values_equal(bf_ans.x1, dec_ans.x1, precision) and
                values_equal(bf_ans.x2, dec_ans.x2, precision))
 
    if kind == Answer_options.SPECIAL_VARIABLES:
        return (values_equal(bf_ans.x1, dec_ans.x1, precision) and
                values_equal(bf_ans.x2, dec_ans.x2, precision))
 
    return False
 
 
def two_roots_equal_any_order(bf_ans, dec_ans, precision):
    a, b = bf_ans.x1, bf_ans.x2
    c, d = dec_ans.x1, dec_ans.x2
    direct  = values_equal(a, c, precision) and values_equal(b, d, precision)
    swapped = values_equal(a, d, precision) and values_equal(b, c, precision)
    return direct or swapped
 
 
 
 
def values_equal(bf_val, dec_val, precision):

    if bf_val is None and dec_val is None:
        return True
    if bf_val is None or dec_val is None:
       return False 
    
    bf_special  = bf_special_str(bf_val)
    dec_special = dec_special_str(dec_val)
 
    if bf_special is not None or dec_special is not None:
        return bf_special == dec_special
 
    if isinstance(bf_val, ComplexBigFloat) and isinstance(dec_val, DecComplex):
        return (values_equal(bf_val.real, dec_val.real, precision) and
                values_equal(bf_val.imag, dec_val.imag, precision))
 
    
    if isinstance(bf_val, ComplexBigFloat) or isinstance(dec_val, DecComplex):
        return False
 
    
    return numbers_equal(bf_val, dec_val, precision)
 
 
def bf_special_str(x):
    if isinstance(x, SpecialVariables):
        return x.type
    return None
 
 
def dec_special_str(x):
    if isinstance(x, str):
        return x
    return None
 
 
def numbers_equal(bf_val: BigFloat, dec_val: Decimal, precision: int):
    
    with localcontext() as ctx:
        ctx.prec = precision + 100
        bf_str  = format(Decimal(to_string_for_output(bf_val)) + 0, 'f')
        dec_str = format(dec_val + 0, 'f')
 
    
    if len(bf_str) <= precision and len(dec_str) <= precision:
    
        return Decimal(bf_str) == Decimal(dec_str)
 
    return bf_str[:precision] == dec_str[:precision]