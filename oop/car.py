from vehicle import Vehicle


class Car(Vehicle):
    #class definition
    # top_speed = 100
    # warnings = []
    

    def brag(self):
        print('look how cool my car is')

#creating a new car object
car1 = Car()

#using the car object
car1.drive()

# Car.top_speed = 200
car1.add_warning('New warning')
#car1.__warnings.append([])
#print(car1.__dict__)
print(car1)

car2 = Car(200)
car2.drive()
print(car2.get_warnings())

car3 = Car(250)
car3.drive()
print(car3.get_warnings())