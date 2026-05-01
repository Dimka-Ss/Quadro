
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


def BigFloat_round(bigf: BigFloat, precision: int):

    chunks = list(bigf.chunks)
    exp = bigf.exponent
    old_len = len(chunks)

    if old_len < precision:
        return bigf

    chunks = chunks[-precision:]
    exp = exp + (old_len - len(chunks)) * BigFloat.CHUNK_SIZE

    return BigFloat(bigf.sign, chunks, exp)


def get_mantiss(chunks: list):
    
    result_mantiss_string = ''
    for i in range(len(chunks) - 1, -1, -1):
        result_mantiss_string += str(chunks[i]).zfill(BigFloat.CHUNK_SIZE)
    return result_mantiss_string


def normalize(bigf: BigFloat):
    '''1. Убирает незначащие нули 
       2. Переопределяет знак 0'''
    
    sign = bigf.sign
    chunks_copy = list(bigf.chunks)
    exponent = bigf.exponent

    chunk_result = []

    while chunks_copy and chunks_copy[-1] == 0:
        chunks_copy.pop()

    if not chunks_copy:
        return BigFloat(1, (0,), 0)
    
    mantiss = get_mantiss(chunks_copy)

    while exponent < 0 and mantiss and mantiss[-1] == '0':
        mantiss = mantiss[:-1]
        exponent += 1

    if mantiss == '0':
        return BigFloat(1, (0,), 0)
    
    new_chunks = divide_to_chunks(mantiss, BigFloat.CHUNK_SIZE)    
    
    return BigFloat(sign, new_chunks, exponent)


def get_sign(input_text: str):

    if input_text[0] == '-':
        new_text = input_text[1:]
        sign = -1
    
    elif input_text[0] == '+':
        new_text = input_text[1:]
        sign = 1
    else:
        new_text = input_text
        sign = 1
    
    # print(f"знак = {sign}")
    return sign, new_text


def divide_to_mantiss_and_to_exponent(input_text: str):
    
    dot_position = input_text.find('.')

    if dot_position != -1:
        exponent = dot_position - len(input_text) + 1
        mantiss = input_text.replace('.', '')
    else:
        mantiss, exponent = input_text, 0
    # print(f"мантисса = {mantiss}, экспонента = {exponent}")
    return mantiss, exponent


def divide_to_chunks(mantiss: str, base: int):

    chunks = []
    
    for i in range(len(mantiss), 0, -base):
    
        chunk_boarder = max(0, i - base)
        chunks.append(int(mantiss[chunk_boarder : i]))
    # print(f"чанки = {tuple(chunks)}")
    return chunks


def from_string(input_text: str):

    sign, string_without_sign = get_sign(input_text)
    mantiss, exponent = divide_to_mantiss_and_to_exponent(string_without_sign)
    chunks = divide_to_chunks(mantiss, BigFloat.CHUNK_SIZE)
    
    return BigFloat(sign, chunks, exponent)


def to_string_for_output(bigf: BigFloat):

    sign = bigf.sign
    chunks = bigf.chunks
    exponent = bigf.exponent
    chunk_size = bigf.CHUNK_SIZE    

    result_string = ''

    for i in range(len(chunks) - 1, -1, -1):
        
        if i != len(chunks) - 1:
            result_string += str(chunks[i]).zfill(chunk_size)
        else:
            result_string += str(chunks[i])

    if exponent != 0:

        need_length = -exponent + 1
        
        if len(result_string) < need_length:
            result_string = result_string.zfill(need_length) 
        result_string = result_string[:len(result_string) + exponent] + '.' + result_string[len(result_string) + exponent:] 

    if sign == -1:
        result_string = '-' + result_string

    return result_string






















    
