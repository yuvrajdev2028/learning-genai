class Vehicle:
    price = 1200000

    def describe(self):
        return f"Vehicle price: {self.price}"
    
v1 = Vehicle()
print(v1.describe())
print(Vehicle.describe(v1))

v2 = Vehicle()
v2.price = 129999
print(Vehicle.describe(v2))