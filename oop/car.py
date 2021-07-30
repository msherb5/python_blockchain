class Car:
    #class definition
    top_speed = 100

    def drive(self):
        print('I am driving but certainly not faster than {}'.format(self.top_speed))

#creating a new car object
car1 = Car()

#using the car object
car1.drive()