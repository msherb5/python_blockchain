
from food import Food

class Fruit(Food):
    def __init__(self, name):
        self.name = name
        self.kind = 'fruit'

    def clean(self):
        print('This {}, a type of {}, is now cleaned!'.format(self.name, self.kind))


banana = Fruit('banana')
banana.clean()