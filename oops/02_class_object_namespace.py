class Vehicle:
    origin = "India"

print(Vehicle.origin)

Vehicle.is_new = True
print(Vehicle.is_new)

#creating objects of Vehicle

vehicle1 = Vehicle()
print(f"Vehicle1 origin: {vehicle1.origin}")
print(f"Is vehicle1 new?: {vehicle1.is_new}")

vehicle1.is_new = False
print("Class: ",Vehicle.is_new) #true
print("Object: ",vehicle1.is_new) # false -> each object has its own namespace