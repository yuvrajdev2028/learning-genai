class Vehicle:
    def __init__(self, make, year):
        self.make = make
        self.year = year

    def summary(self):
        return f"{self.make} {self.year}"
    
v1 = Vehicle("Mustang",1970)
v2 = Vehicle("Charger",1972)

print(v1.summary())
print(v2.summary())