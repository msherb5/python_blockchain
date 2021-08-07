# 1) Create a Food class with a “name” and a “kind” attribute as well as a “describe() ” method (which prints “name” and “kind” in a sentence).

# 2) Try turning describe()  from an instance method into a class and a static method. Change it back to an instance method thereafter.

# 3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook() ” method to “Meat” and “clean() ” to “Fruit”.

# 4) Overwrite a “dunder” method to be able to print your “Food” class.

# CLASS METHOD PART
# class Food:

#     name = 'X'
#     kind = 'X'
#     # def __init__(self, name, kind):
#     #     self.name = name
#     #     self.kind = kind

#     @classmethod
#     def describe(cls):
#         print('this food is {}, a kind of {}'.format(cls.name, cls.kind))


# Food.name = 'Apple'
# Food.kind = 'fruit'
# Food.describe()


#STATIC METHOD PART
# class Food:

#     name = 'X'
#     kind = 'X'
#     # def __init__(self, name, kind):
#     #     self.name = name
#     #     self.kind = kind

#     @staticmethod
#     def describe(name, kind):
#         print('this food is {}, a kind of {}'.format(name, kind))


# Food.name = 'Apple'
# Food.kind = 'fruit'
# Food.describe('apple', 'fruit')

# Instance method
