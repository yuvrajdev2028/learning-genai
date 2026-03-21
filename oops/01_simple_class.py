# import sys
# print(sys.version)

class Vehicle:
    pass

class Person:
    pass

print("type of class -> a class is also an object everything is always an object in python")
print(type(Vehicle))

vehicle1 = Vehicle()
print(type(vehicle1))
print(type(vehicle1) is Vehicle)
print(type(vehicle1) is Person)
print(type("hello"))
print(type(123))
print(type(12.30))
print(type(True))
print(type(None))