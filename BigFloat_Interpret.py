from BigFloat import BigFloat


class Result:
    def __init__(self, success: bool, value: str, remaining: str, error=None):
        self.success = success
        self.value = value
        self.remaining = remaining
        self.error = error
    
    @staticmethod
    def good(value: str, remaining: str):
        return Result(True, value, remaining)
    
    @staticmethod
    def fail(error: str, remaining: str):
        return Result(False, '', remaining, error)
    

class Interpretator:
    def interpret(self, text: str):
        pass


class Input(Interpretator):
    
    def interpret(self, text: str):
        coefficients = text.split()
        if len(coefficients) != 3:
            return Result.fail(f'Неверное количество коэффициентов: {len(coefficients)} из 3', '')
        
        for i in coefficients:
            if len(i) > 10000:
                return Result.fail(f'Превышен лимит длинны коэффициента: {len(i)} из 10000', '')
        
        result_string = []
        for coef in coefficients:
            result = FloatParser().interpret(coef)
            if not result.success:
                return Result.fail(result.error, '')
        
            result_string.append(result.value)
        return Result.good(tuple(result_string), '')


def is_digit(char):

    if char is not None and '0' <= char <= '9':
        return True
    return False


def is_nonzero_digit(char):
    
    if char is not None and '1' <= char <= '9':
        return True
    return False


def build_BigFloat(sign_value, int_value, frac_value, exp_value):

    sign = -1 if sign_value == '-' else 1
    exp = int(exp_value) if exp_value != '' else 0
    
    mantiss = int_value + frac_value
    exp -= len(frac_value)
    mantiss = mantiss.lstrip('0')
    
    if mantiss == '':
        return BigFloat(1, (0,), 0)
    
    chunks = []
    for i in range(len(mantiss), 0, -BigFloat.CHUNK_SIZE):
    
        chunk_boarder = max(0, i - BigFloat.CHUNK_SIZE)
        chunks.append(int(mantiss[chunk_boarder : i]))

    return BigFloat(sign, tuple(chunks), exp)


class FloatParser(Interpretator):

    def interpret(self, text: str):
        sign_value, text = self.parse_sign(text)
        
        if text == '':
            return Result.fail("введена пустая строка", '')
        
        int_result = self.parse_integer_or_skip(text)

        if isinstance(int_result, Result):
            return int_result
        
        int_value, text = int_result
        
        frac_result = self.call_parser(FractionalParser(), text)

        if isinstance(frac_result, Result):
            return frac_result
        
        frac_value, text = frac_result
        
        exp_result = self.call_parser(ExponentParser(), text)

        if isinstance(exp_result, Result):
            return exp_result
        
        exp_value, text = exp_result
        
        if text != '':
            return Result.fail(f"лишние символы в конце: {text!r}", text)
        
        bigf = build_BigFloat(sign_value, int_value, frac_value, exp_value)
        return Result.good(bigf, '')
    
    
    def parse_sign(self, text):
        result = SignParser().interpret(text)
        return result.value, result.remaining
    

    def parse_integer_or_skip(self, text):

        if text[0] in '.,':
            return '', text
        
        if not is_digit(text[0]):
            return Result.fail("ожидалась цифра, точка или запятая", text)
        
        return self.call_parser(IntegerParser(), text)
    

    def call_parser(self, parser, text):

        result = parser.interpret(text)

        if not result.success:
            return Result.fail(result.error, text)
        
        return result.value, result.remaining



class SignParser(Interpretator):

    def interpret(self, text: str):
        if text == '':
            return Result.good('', '')
        
        if text[0] == '-':
            return Result.good('-', text[1:])
        
        if text[0] == '+':
            return Result.good('+', text[1:])
        
        return Result.good('', text)



class IntegerParser(Interpretator):

    def interpret(self, text: str):
        if text == '':
            return Result.fail('в целочисленной части ожидалась цифра', text)

        if text[0] == '0':
            return Result.good('0', text[1:])
        
        if is_nonzero_digit(text[0]):
            value = text[0]
            remaining = text[1:]

            while len(remaining) > 0 and is_digit(remaining[0]):
                value += remaining[0]
                remaining = remaining[1:]

            return Result.good(value, remaining)
        
        return Result.fail('в целочисленной части ожидалась цифра', text)



class FractionalParser(Interpretator):

    def interpret(self, text: str):
        if text == '' or text[0] not in ',.':
            return Result.good('', text)
        
        if text[0] in ',.':
            remaining = text[1:]
            if remaining == '':
                return Result.fail('после точки обязательно должно идти число', '')
            
            if not is_digit(remaining[0]):
                return Result.fail('после точки обязательно должно идти число', '')
            
            value = ''
            while len(remaining) > 0 and is_digit(remaining[0]):
                value += remaining[0]
                remaining = remaining[1:]

            return Result.good(value, remaining)



class ExponentParser(Interpretator):

    def interpret(self, text: str):
        if text == '' or text[0] not in 'Ee':
            return Result.good('', text)
        
        if text[0] in 'Ee':
            remaining = text[1:]
            sign_result = SignParser().interpret(remaining)
            sign_value = sign_result.value
            remaining = sign_result.remaining

            if remaining == '' or not is_nonzero_digit(remaining[0]):
                return Result.fail('после "e" обязательно должно идти число', text)

            value = sign_value
            while len(remaining) > 0 and is_digit(remaining[0]):
                value += remaining[0]
                remaining = remaining[1:]
            
            return Result.good(value, remaining)















































