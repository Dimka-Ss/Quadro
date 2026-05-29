from utility_func import *
from BigFloat import *
from BigFloat_Arithmetic_Newton_division import main_newton_division as div
from BigFloat_Arithmetic_Fouriera  import main_multiply as mul
 
 
NAN_VARIABLE = ['nan']
INF_VARIABLE = ['inf', 'infinity']
 
 
def is_special(x) -> bool:
        return isinstance(x, SpecialVariables)
 
 
def is_special_in_coefs(coefs: Coefs) -> bool:
        return any(is_special(x) for x in [coefs.a, coefs.b, coefs.c])
 
 
def is_zero_bigf(x) -> bool:
    return isinstance(x, BigFloat) and mantiss_is_zero(x.chunks)
 
 
def spec_lin_nspec_spec_roots(b, c):
    if is_zero_bigf(b):
            return Answer(answer_type=Answer_options.NO_SOLUTIONS)
    else:
        result_pos = c.is_neg_inf() == (b.sign == 1)
        x1 = SpecialVariables(SpecialVariables.PosInf) if result_pos else SpecialVariables(SpecialVariables.NegInf)
        return Answer(answer_type=Answer_options.SPECIAL_VARIABLES, x1=x1)
        
 
def any_nan(a, b, c):
    if any(is_special(x) and x.is_nan() for x in [a, b, c]):
        return True
    return False
 
 
def inf_a(a):
    if is_special(a) and a.is_inf():
        return True
    return False
 
 
def nzero_spec_spec(a, b, c):
    if not is_zero_bigf(a) and is_special(b) and is_special(c):
        return True
    return False
 
 
def ans_nan(a, b, c):
    if any_nan(a, b, c):
        return True
    if inf_a(a):
        return True
    if nzero_spec_spec(a, b, c):
        return True
    return False
        
 
def nzero_spec_nspec(a, b, c):
    if not is_zero_bigf(a) and is_special(b) and not is_special(c):
        return True
    return False
 
 
def nzero_spec_nspec_roots(a, b, c, NAN, POS_INF, NEG_INF):
    if b.is_pos_inf(): 

        x1 = NEG_INF if a.sign == 1 else POS_INF
        x2 = NAN
        return Answer(answer_type=Answer_options.SPECIAL_VARIABLES, x1=x1, x2=x2)
    else:
        x1 = POS_INF if a.sign == 1 else NEG_INF
        x2 = NAN
        return Answer(answer_type=Answer_options.SPECIAL_VARIABLES, x1=x1, x2=x2)
 
 
def nzero_nspec_spec(a, b, c):
    if not is_zero_bigf(a) and not is_special(b) and is_special(c):
        return True
    return False
 
 
def ac_pos(a, c):
    return (a.sign == 1) == c.is_pos_inf()
 
 
def ac_pos_roots(a, b, POS_INF, NEG_INF):
    TWO = BigFloat(1, [2], 0)
    neg_b = BigFloat(b.sign * -1, list(b.chunks), b.exponent)
    two_a = mul(TWO, a)
 
    real_part = div(neg_b, two_a)
    x1 = ComplexBigFloat(real=real_part, imag=POS_INF)
    x2 = ComplexBigFloat(real=real_part, imag=NEG_INF)
 
    return Answer(answer_type=Answer_options.SPECIAL_VARIABLES, x1=x1, x2=x2)
 
 
def ac_neg_roots(a, POS_INF, NEG_INF):
    x1 = POS_INF if a.sign == 1 else NEG_INF
    x2 = NEG_INF if a.sign == 1 else POS_INF
    return Answer(answer_type=Answer_options.SPECIAL_VARIABLES, x1=x1, x2=x2)
 
 
def special_linear_sol(b, c):
 
    if is_special(b) and is_special(c):
        return Answer(answer_type=Answer_options.SPECIAL_VARIABLES, x1=SpecialVariables(SpecialVariables.NAN))
 
    if is_special(b) and not is_special(c):
        return Answer(answer_type=Answer_options.SPECIAL_VARIABLES, x1=BigFloat(1, [0], 0))
 
    if not is_special(b) and is_special(c):
        return spec_lin_nspec_spec_roots(b, c)
 
 
def nzero_nspec_spec_roots(a, b, c, NAN, POS_INF, NEG_INF):
    if ac_pos(a, c):
        return ac_pos_roots(a, b, POS_INF, NEG_INF)
    else:
        return ac_neg_roots(a, POS_INF, NEG_INF)
 
 
def special_solver(coefs: Coefs):
    NAN     = SpecialVariables(SpecialVariables.NAN)
    POS_INF = SpecialVariables(SpecialVariables.PosInf)
    NEG_INF = SpecialVariables(SpecialVariables.NegInf)
 
    a, b, c = coefs.a, coefs.b, coefs.c
 
    if ans_nan(a, b, c):
        return Answer(answer_type=Answer_options.SPECIAL_VARIABLES, x1=NAN, x2=NAN)
 
    if is_zero_bigf(a):
        return special_linear_sol(b, c)
 
    if nzero_spec_nspec(a, b, c):
        return nzero_spec_nspec_roots(a, b, c, NAN, POS_INF, NEG_INF)
 
    if nzero_nspec_spec(a, b, c):
        return nzero_nspec_spec_roots(a, b, c, NAN, POS_INF, NEG_INF)
 