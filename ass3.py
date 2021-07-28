
#1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.

person_dicts = [{'name': 'Mike', 'age': 21, 'hobbies': ['boinking', 'bonking', 'babbling']}, {'name': 'Matt', 'age': 20, 'hobbies': ['rat', 'dirting', 'krumping']}, {'name': 'Evan', 'age': 14, 'hobbies': ['corn', 'rat', 'bonking']}, {'name': 'klaus', 'age': 69, 'hobbies': ['guns', 'drugs', 'etc']}]
print(person_dicts)
print('-' * 20)

#Use a list comprehension to convert this list of persons into a list of names (of the persons)

names_list = [dicto['name'] for dicto in person_dicts]
print(names_list)
print('-' * 20) 

#3) Use a list comprehension to check whether all persons are older than 20.

age_check = all([dicte['age'] > 20 for dicte in person_dicts])
print(age_check)
print('-' * 20) 

#4) Copy the person list such that you can safely edit the name of the first person (without changing the original list)
dup_list = person_dicts[:]

copy_dic = person_dicts[0].copy()
copy_dic['name'] = 'bob'
dup_list[0] = copy_dic

print(dup_list)
print(person_dicts)

#5)Unpack the persons of the original list into different variables and output these variables.

a, b, c, d = person_dicts
print(a)
print(b)
print(c)
print(d)