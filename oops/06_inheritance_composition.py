class Vehicle:
    def __init__(self, model, make, year):
        self.model = model
        self.make = make
        self.year = year

    def drive(self):
        print(f"Driving {self.year} {self.model} {self.make}")
    
class Car(Vehicle):
    def openTrunk(self):
        print(f"Opening trunk of {self.year} {self.model} {self.make}")
    
# COMPOSITION
class Showroom:
    vehicle_class = Vehicle

    def __init__(self):
        self.vehicle = self.vehicle_class("Ford","GT",2005)

    def openDoor(self):
        print(f"Open {self.vehicle.model} showroom door")
        self.vehicle.drive()

v1 = Vehicle("Porsche","Carrera 911 GT",2013)

v1.drive()

c1 = Car("Ford","Mustang GT",2009)

c1.drive()
c1.openTrunk()

s1 = Showroom()

s1.openDoor()