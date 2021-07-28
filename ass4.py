#1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
def duplicate(el):
    return el * 2

def outer(method):
    return method(2)


print(outer(duplicate))
print('-' * 20)


#2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.

print(outer(lambda el: el * 4))
print('-' * 20)

#3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed. 

def outer2(method2, *args):
    return method2(args)

outer2(lambda args: print(args), ['hello', 'I', 'am', 'mike'], 5, 4, 3) 
print('-'*20)  

#4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column

def transform_data(fn, *args):
    for arg in args:
        print('Result: {:^20.2f}'.format(fn(arg)))

transform_data(lambda data: data / 5, 10, 15, 22, 30)