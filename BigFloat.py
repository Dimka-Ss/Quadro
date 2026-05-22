from random import randrange, choice


class BigFloat:

    CHUNK_SIZE = 5
    BASE = 10 ** CHUNK_SIZE

    def __init__(self, sign: int = 1, chunks: list = [], exponent: int = 0):
        self.sign = sign
        self.chunks = chunks
        self.exponent = exponent

    def set_sign(self, sign: int):
        self.sign = sign

    def set_chunks(self, mantiss: list):
        self.chunks = mantiss

    def set_exponent(self, exponent: int):
        self.exponent = exponent



class Answer_options:
    INFINITY_SOLUTIONS = "infinity solutions"
    NO_SOLUTIONS = "no solutions"
    LINEAR = "linear"
    COMPLEX_SOLUTIONS = "complex solutions"
    DIFFERENT_ROOTS = "different roots"
    SAME_ROOTS = "same roots"
    SPECIAL_VARIABLES = "special variables"



class Answer:
    def __init__(self, answer_type, x1 = None, x2 = None):
        self.answer_type = answer_type
        self.x1 = x1
        self.x2 = x2
    
    def get_answer_type(self):
        return self.answer_type
    
    def get_x1(self):
        return self.x1

    def get_x2(self):
        return self.x2
    


class ComplexBigFloat:
    
    def __init__(self, real: BigFloat, imag: BigFloat):
        self.real = real
        self.imag = imag



class SpecialVariables:
    NAN    = 'nan'
    NegInf = '-inf'
    PosInf = 'inf'

    def __init__(self, type: str):
        self.type = type

    def __str__(self):
        return self.type

    def is_inf(self):
        return self.type == SpecialVariables.NegInf or self.type == SpecialVariables.PosInf

    def is_nan(self):
        return self.type == SpecialVariables.NAN

    def is_pos_inf(self):
        return self.type == SpecialVariables.PosInf

    def is_neg_inf(self):
        return self.type == SpecialVariables.NegInf
    


class Coefs:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c    