from decimal import Decimal, getcontext
 
from BigFloat import (
    BigFloat,
    Coefs,
    SpecialVariables,
    Answer_options,
)
from utility_func import to_string_for_output
 
 
getcontext().prec = 200000
 
 
 
 
class DecComplex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
 
 
class DecAnswer:
    
    def __init__(self, kind, x1=None, x2=None):
        self.kind = kind
        self.x1 = x1
        self.x2 = x2
 

 
def to_decimal_one(x):
    
    if isinstance(x, SpecialVariables):
        return x.type                    

    if isinstance(x, BigFloat):
        return Decimal(to_string_for_output(x))

 
def coefs_to_decimal(coefs: Coefs):
    
    return (to_decimal_one(coefs.a),
            to_decimal_one(coefs.b),
            to_decimal_one(coefs.c))
 
 
def is_special(x):
    return isinstance(x, str)
 
def is_nan(x):
    return x == 'nan'
 
def is_inf(x):
    return x == 'inf' or x == '-inf'
 
def is_pos_inf(x):
    return x == 'inf'
 
def is_neg_inf(x):
    return x == '-inf'
 
def is_zero_dec(x):
    return isinstance(x, Decimal) and x == 0
 
def sign_dec(x):
    
    return 1 if x > 0 else -1
 
 
def root_calculations_decimal(dec_coefs):
    a, b, c = dec_coefs
 
    if has_special(a, b, c):
        return special_solver_decimal(a, b, c)
 
    if a == 0:
        return linear_decimal(b, c)
    return quadratic_decimal(a, b, c)
 
 
def has_special(a, b, c):
    return is_special(a) or is_special(b) or is_special(c)

 
def linear_decimal(b, c):
    if b == 0:
        if c == 0:
            return DecAnswer(Answer_options.INFINITY_SOLUTIONS)
        return DecAnswer(Answer_options.NO_SOLUTIONS)
    return DecAnswer(Answer_options.LINEAR, x1=-c / b)
 
 
def quadratic_decimal(a, b, c):
    d = b * b - 4 * a * c
 
    if d == 0:
        return DecAnswer(Answer_options.SAME_ROOTS, x1=-b / (2 * a))
 
    if d > 0:
        sq = d.sqrt()
        
        if b > 0:
            x1 = (-b - sq) / (2 * a)
        else:
            x1 = (-b + sq) / (2 * a)
        x2 = c / (a * x1)
        return DecAnswer(Answer_options.DIFFERENT_ROOTS, x1=x1, x2=x2)
 
    re = -b / (2 * a)
    im = (-d).sqrt() / (2 * a)
    return DecAnswer(Answer_options.COMPLEX_SOLUTIONS,
                     x1=DecComplex(re, im),
                     x2=DecComplex(re, -im))
 
 
 
NAN     = 'nan'
POS_INF = 'inf'
NEG_INF = '-inf'
 
 
def any_nan(a, b, c):
    return is_nan(a) or is_nan(b) or is_nan(c)
 
 
def nonzero_a(a):
    return isinstance(a, Decimal) and a != 0
 
 
def inf_a(a):
    return is_inf(a)
 
 
def nonzero_a_spec_b_spec_c(a, b, c):
    return nonzero_a(a) and is_special(b) and is_special(c)
 
 
def ans_all_nan(a, b, c):
    if any_nan(a, b, c):
        return True
    if inf_a(a):
        return True
    if nonzero_a_spec_b_spec_c(a, b, c):
        return True
    return False
 
 
def special_solver_decimal(a, b, c):
    
    if ans_all_nan(a, b, c):
        return DecAnswer(Answer_options.SPECIAL_VARIABLES, x1=NAN, x2=NAN)
 
    if is_zero_dec(a):
        return special_linear(b, c)
 
    if nonzero_a(a) and is_special(b) and not is_special(c):
        return nonzero_spec_nonspec(a, b)
 
    if nonzero_a(a) and not is_special(b) and is_special(c):
        return nonzero_nonspec_spec(a, b, c)
 
    return DecAnswer(Answer_options.SPECIAL_VARIABLES, x1=NAN, x2=NAN)
 
 
def special_linear(b, c):

    if is_special(b) and is_special(c):
        return DecAnswer(Answer_options.SPECIAL_VARIABLES, x1=NAN)
 
    if is_special(b) and not is_special(c):
        return DecAnswer(Answer_options.SPECIAL_VARIABLES, x1=Decimal(0))
 
    if not is_special(b) and is_special(c):
        
        if b == 0:
            return DecAnswer(Answer_options.NO_SOLUTIONS)
        
        result_pos = is_neg_inf(c) == (b > 0)
        x1 = POS_INF if result_pos else NEG_INF
        return DecAnswer(Answer_options.SPECIAL_VARIABLES, x1=x1)
 
 
def nonzero_spec_nonspec(a, b):
    if is_pos_inf(b):
        x1 = NEG_INF if a > 0 else POS_INF
    else:
        x1 = POS_INF if a > 0 else NEG_INF
    x2 = Decimal(0)
    return DecAnswer(Answer_options.SPECIAL_VARIABLES, x1=x1, x2=x2)
 
 
def nonzero_nonspec_spec(a, b, c):
    
    if (a > 0) == is_pos_inf(c):
        
        real_part = -b / (2 * a)
        x1 = DecComplex(real_part, POS_INF)
        x2 = DecComplex(real_part, NEG_INF)
        return DecAnswer(Answer_options.SPECIAL_VARIABLES, x1=x1, x2=x2)
    
    x1 = POS_INF if a > 0 else NEG_INF
    x2 = NEG_INF if a > 0 else POS_INF
    return DecAnswer(Answer_options.SPECIAL_VARIABLES, x1=x1, x2=x2)