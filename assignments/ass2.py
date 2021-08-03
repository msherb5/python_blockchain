names = ['stacy', 'nincompoop', 'Nancille', 'Michael', 'Norbert', 'Nick', 'Daniel', 'Sean', 'Lluc']


#Problem 1: get lengths of all names
def get_lengths():
    names_index = 0
    for names_index in range(len(names)):
        print(len(names[names_index]))

#Problem 2: if length greater than 5, print
def names_check_1():
    names_index = 0
    for names_index in range(len(names)):
        if len(names[names_index]) > 5:
            print(names[names_index])

#problem 3: if length greater than 5 and contains n or N, print
def names_check_2():
    names_index = 0
    for names_index in range(len(names)):
        if len(names[names_index]) > 5:
            if 'n' in names[names_index] or 'N' in names[names_index]:
                print(names[names_index])


#problem 4: pop'em all
def pop_em_all():
    while len(names) > 0:
        names.pop()
    print(len(names))
        
            
get_lengths()
print('*' * 20)
names_check_1()
print('-' * 20)
names_check_2()
print('&' * 20)
pop_em_all()