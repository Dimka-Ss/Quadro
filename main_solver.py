from BigFloat_Interpret import *
from special_solver import *
from utility_func import *
from BigFloat import *
from output import*
from BigFloat_Arithmetic_Newton_division import main_newton_division as div
from BigFloat_Arithmetic_Fouriera import main_multiply as mul
from BigFloat_Arithmetic_Add_Sub import addition as add, subtruction as sub
from BigFloat_Arithmetic_sqrt import Sqrt



'''
1. ввод данных
2. вычисление результата
3. вывод результата
'''

    

def set_minus_to_coef(bigf: BigFloat):
    return BigFloat(bigf.sign * -1, list(bigf.chunks), bigf.exponent)


def input_data(text=None):
    text = input() if not text else text
    result = Input().interpret(text)
    if not result.success:
        print(f"ошибка: {result.error}")
        return None
    else:
        a, b, c = result.value
        return Coefs(a, b, c)


def is_linear(a: BigFloat):
    if mantiss_is_zero(a.chunks):
        return True
    return False


def less_then_zero(bigf: BigFloat):
    if bigf.sign == -1:
        return True
    return False


def linear_solution(b: BigFloat, c: BigFloat):
    if mantiss_is_zero(b.chunks):
        if mantiss_is_zero(c.chunks):
            return Answer(answer_type=Answer_options.INFINITY_SOLUTIONS)
        else:
            return Answer(answer_type=Answer_options.NO_SOLUTIONS)
    neg_c = set_minus_to_coef(c)
    x = div(neg_c, b)
    return Answer(answer_type=Answer_options.LINEAR, x1=x)


def calculate_discriminant(a: BigFloat, b: BigFloat, c: BigFloat):
    FOUR = BigFloat(1, [4], 0)
    square_b = mul(b, b)
    four_a_c = mul(FOUR, mul(a, c))
    return sub(square_b, four_a_c)


def the_same_roots(a: BigFloat, 
                   b: BigFloat, TWO: BigFloat):
    neg_b = set_minus_to_coef(b)
    two_a = mul(TWO, a)
    x = div(neg_b, two_a)
    return Answer(answer_type=Answer_options.SAME_ROOTS, x1 = x)


def complex_roots(discriminant: BigFloat, a: BigFloat, 
                  b: BigFloat, TWO: BigFloat):
    
    neg_discriminant = set_minus_to_coef(discriminant)       
    sqrt_neg_d = Sqrt(neg_discriminant)              
 
    neg_b = set_minus_to_coef(b)
    two_a = mul(TWO, a)
 
    real_part = div(neg_b, two_a)                  
    imag_part = div(sqrt_neg_d, two_a)              
 
    # x1 = real + imag*i,  x2 = real - imag*i
    x1 = ComplexBigFloat(real_part, imag_part)
    x2 = ComplexBigFloat(real_part, set_minus_to_coef(imag_part))
 
    return Answer(answer_type=Answer_options.COMPLEX_SOLUTIONS, x1=x1, x2=x2)


def the_diff_roots(discriminant: BigFloat, a: BigFloat, 
                   b: BigFloat, c: BigFloat, TWO: BigFloat):
    
    neg_b = set_minus_to_coef(b)
    sqrt_discriminant = Sqrt(discriminant)
    two_a = mul(TWO, a)

    if b.sign == 1 and not mantiss_is_zero(b.chunks):
        neg_sqrt = set_minus_to_coef(sqrt_discriminant)
        root1 = div(add(neg_b, neg_sqrt), two_a)
    else:
        root1 = div(add(neg_b, sqrt_discriminant), two_a)

    root2 = div(c, mul(a, root1))

    return Answer(answer_type=Answer_options.DIFFERENT_ROOTS,
                  x1 = root1,
                  x2 = root2)


def quadratic_solution(a: BigFloat, b: BigFloat, c: BigFloat):
    TWO = BigFloat(1, [2], 0)
    discriminant = calculate_discriminant(a, b, c)

    if mantiss_is_zero(discriminant.chunks):
        return the_same_roots(a, b, TWO)
    
    if less_then_zero(discriminant):
        return complex_roots(discriminant, a, b, TWO)
    else:
        return the_diff_roots(discriminant, a, b, c, TWO)
    


def root_calculations(coefs: Coefs):
    
    if is_special_in_coefs(coefs):
        return special_solver(coefs)

    else:
        a = coefs.a
        b = coefs.b
        c = coefs.c
        
        if is_linear(a):
            return linear_solution(b, c)
        else:
            return quadratic_solution(a, b, c)



if __name__ == "__main__":
    coefs = input_data()
    if coefs is not None:
        result = root_calculations(coefs)
        output_result(result)