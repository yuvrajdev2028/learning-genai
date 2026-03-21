class Vehicle:
    year = 2010

v1 =Vehicle()

print(v1.year)

v1.year = 2013
v1.make = "Ford Mustang"

print("instance",v1.year)
print("instance",v1.make)
print("class",Vehicle.year)

del v1.year
del v1.make
print("instance",v1.year)
print("instance",v1.make)