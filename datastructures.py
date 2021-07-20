simple_list = [1,2,3,4]
simple_list.extend([5,6,7])
del(simple_list[0])
print(simple_list)


dic = {'name': 'Mike'}
print(dic.items())
for k, v in dic.items():
    print(k, v)
del dic['name']
print(dic)

tup = (1,2,3)
# del t[0] doesnt work - tuples are immutable
print(tup.index(1))

s = {'Mike', 'Ana', 'Mike'}
#del set doesnt work as well
print(s)
