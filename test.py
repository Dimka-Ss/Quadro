from BigFloat import *
from BigFloat_Arithmetic_Add_Sub import *
from BigFloat_Interpret import *




def test_normalize():           #00234234.3515124234340
    s1 = normalize(from_string("-18237821.12387000000000000000000"))
    # s2 = normalize(from_string("421.3423"))
    test1 = normalize(s1)
    # test2 = normalize(s2)
    print(to_string_for_output(test1))
    # print(to_string_for_output(test2))
# test_normalize()


def test_align():
    s1 = normalize(from_string("000234234.351512423434"))
    s2 = normalize(from_string("421.3423"))
    test1, test2 = align(s1, s2)
    print(to_string_for_output(test1))
    print(to_string_for_output(test2))

'''234234.351512423434
   421.342300000000'''
# test_align()


# def test_compare_bigfs():
#     s1 = from_string("129837.823492519248")
#     s2 = from_string("1283783847.38472984892374")
#     test = compare_bigfs_chunks(s1, s2)
#     print(test)
# # test_compare_bigfs()


# def test_addition():
#     s1 = from_string("129837.823492519248")
#     s2 = from_string("-1283783847.38472984892374")
#     test = addition(s1, s2)
#     print(to_string_for_output(test))
#     print()


    # val = (to_string_for_output(addition(from_string("1.5"), from_string("2.5"))),
    #     to_string_for_output(addition(from_string("9999"), from_string("1"))),
    #     to_string_for_output(addition(from_string("0.999"), from_string("0.001"))),
    #     to_string_for_output(addition(from_string("5.0"), from_string("-3.0"))),
    #     to_string_for_output(addition(from_string("3.0"), from_string("-5.0"))),
    #     to_string_for_output(addition(from_string("-1.5"), from_string("-2.5"))),
    #     to_string_for_output(addition(from_string("3.14"), from_string("-3.14"))),
    #     to_string_for_output(addition(from_string("1.5"), from_string("0.05")))
    # )

    # for i in val:
    #     print(i, end='\n')
        # print()
# test_addition()


# def test_substraction():
#     s1 = from_string("129837.823492519248")
#     s2 = from_string("-1283783847.38472984892374")
#     test = substruction(s1, s2)
#     print(to_string_for_output(test))
#     print()


#     val =((to_string_for_output(substruction(from_string("5.0"),  from_string("3.0")))),
#         to_string_for_output(substruction(from_string("9999"), from_string("1"))),
#         to_string_for_output(substruction(from_string("0.999"), from_string("0.001"))),
#         to_string_for_output(substruction(from_string("5.0"), from_string("-3.0"))),
#         to_string_for_output(substruction(from_string("3.0"), from_string("-5.0"))),
#         to_string_for_output(substruction(from_string("-1.5"), from_string("-2.5"))),
#         to_string_for_output(substruction(from_string("3.14"), from_string("-3.14"))),
#         to_string_for_output(substruction(from_string("1.5"), from_string("0.05")))
#     )   

#     for i in val:
#         print(i, end='\n')
#         print()
# test_substraction()



def test_interpret_small_input_values():
    tests = (   " 13.233 3.3213213",
                "+ 13.233 3.3213213",
                "- 13.233 3.3213213",
                ". 13.233 3.3213213",
                ", 13.233 3.3213213",
                "01 13.233 3.3213213",
                "00 13.233 3.3213213",
                "0123 13.233 3.3213213",
                "1. 13.233 3.3213213",
                "1, 13.233 3.3213213",
                "+. 13.233 3.3213213",
                "-. 13.233 3.3213213",
                "e10 13.233 3.3213213",
                "1e 13.233 3.3213213",
                "1e+ 13.233 3.3213213",
                "1e- 13.233 3.3213213",
                "abc 13.233 3.3213213",
                "1abc 13.233 3.3213213",
                "abc1 13.233 3.3213213",
                "1 2 13.233 3.3213213",
                "1.2.3 13.233 3.3213213",
                "-1-2-3 13.233 3.3213213",
                "0 13.233 3.3213213",
                "1 13.233 3.3213213",
                "9 13.233 3.3213213",
                "10 13.233 3.3213213",
                "123 13.233 3.3213213",
                "+123 13.233 3.3213213",
                "-123 13.233 3.3213213",
                "1.5 13.233 3.3213213",
                "1,5 13.233 3.3213213",
                "0.5 13.233 3.3213213",
                "0,5 13.233 3.3213213",
                ".5 13.233 3.3213213",
                ",5 13.233 3.3213213",
                "+.5 13.233 3.3213213",
                "-.5 13.233 3.3213213",
                "1e2 13.233 3.3213213",
                "1E2 13.233 3.3213213",
                "1e+2 13.233 3.3213213",
                "1e-2 13.233 3.3213213",
                "-1.5e+10 13.233 3.3213213",
                "+.5E-3 13.233 3.3213213000000000")
                # "8e-4596442 13.233 3.3213213")

    for i in tests:
        string = i
        result = Input().interpret(string)
        if not result.success:
            print(f"ошибка в строкке {string}: {result.error}")

        for j in result.value:
            print(f"результат: {to_string_for_output(j)}")
        print()

# test_interpret_small_input_values()

def test_addition_substraction():

    tests = (
        "0 0 1",           
        "1 0 1",            
        "0 1 1",           
        "1 1 1",            
        "5 3 1",            
        "3 5 1",            
        "5 3 1",           
        "5 -3 1",          
        "-5 3 1",           
        "-5 -3 1",         
        "3 -5 1",          
        "-3 5 1",           
        "5 -5 1",         
        "-5 5 1",          
        "1234 1234 1",    
        "1.234 1.234 1",  
        "1e10 1e10 1",     
        "0.0001 0.0001 1", 
        "9999 1 1",                
        "9999 9999 1",              
        "99999999 1 1",             
        "99999999 9999999 1",      
        "9999999999999999 1 1",     
        "5000 5000",           
        "10000 1 1",                
        "100000000 1 1",           
        "10000000000000000 1 1",   
        "10000 9999 1",            
        "100 99 1",              
        "1 0.1 1",                 
        "1 0.0001 1",              
        "1 0.00001 1",            
        "100 0.001 1",             
        "1e10 1 1",             
        "1e10 1e-10 1",             
        "1e-100 1e100 1",         
        "1.5 0.5 1",               
        "0.1 0.2 1",               
        "0.5 0.5 1",               
        "1.50 2.50 1",              
        "0.999 0.001 1",          
        "1.999 0.001 1",          
        "0.001 0.002 1",           
        "1.5 1.4 1",             
        "1.0001 1 1",              
        "1000000 999999 1",        
        "1.0000001 1 1",          
        "100000000 99999999 1",    
        "1.000000000001 1 1",       
        "1e20 1 1",                
        "12345678 1 1",                              
        "12345678 12345678 1",                      
        "12345678901234567890 1 1",                  
        "12345678901234567890 12345678901234567890 1",
        "99999999999999999999 1 1",                 
        "1 12345678901234567890 1",               
        "12345678901234567890 -1 1",               
        "1e5 1 1",                
        "1e10 1e10 1",              
        "1.5e10 2.5e10 1",         
        "1e+10 1e-10 1",            
        "-1.5e+10 +.5E-3 1",        
        "1E2 2e2 1",                
        "1e0 1 1",                 
        "1,5 2,5 1",               
        "0,001 0,002 1",
        "-1,5 1,5 1",              
        ",5 ,5 1",                  
        "0 5 1",                    
        "5 0 1",                   
        "0 -5 1",                   
        "-0 5 1",                   
        "0.000 5 1",              
        "0e10 5 1",                 
        "0.0 0.0 1",               
        "1 0.000000000000001 1",  
        "0.000000000000001 1 1",   
        "1e-50 1e50 1",             
        "12345.6789 0.00012345 1")

    for i in tests:
        string = i
        result = Input().interpret(string)
        if result.success:

            a = result.value[0]
            b = result.value[1]
            test_addition = addition(a, b)
            test_substraction = substruction(a, b)
            print(f"строка '{i}' сложение a и b результат: {to_string_for_output(test_addition)} ")

            print(f"строка '{i}' вычитание a и b результат: {i}: {to_string_for_output(test_substraction)} ")
            print()
        
        else:
            print(f"ошибка в строкке {string}: {result.error}")
            print()

# test_addition_substraction()


def single_test(string):
    result = Input().interpret(string)
    if result.success:

        a = result.value[0]
        b = result.value[1]
        test_addition = addition(a, b)
        test_substraction = substruction(a, b)
        print(f"результат сложения: {to_string_for_output(test_addition)} ")
        print()
        print(f"результат вычитания: {to_string_for_output(test_substraction)} ")
        print()

    else:
        print(f"ошибка в строкке {string}: {result.error}")

# single_test()