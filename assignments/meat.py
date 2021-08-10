
from food import Food

class Meat(Food):
    def __init__(self, name):
        self.name = name
        self.kind = 'meat'

    def cook(self):
        print('This {}, a type of {}, is now cooked!'.format(self.name, self.kind))


steak = Meat('steak')
steak.cook()