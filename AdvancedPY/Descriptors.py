class Person:
    def __init__(self, name, age, bmi):
        self.name = name
        self.age = age
        self.bmi = bmi
        if self.bmi < 0:
            raise ValueError("Bmi can never be less than zero")

    def __str__(self):
        return "{0} age {1} with a bmi of {2}".format(self.name, self.age, self.bmi)

person1 = Person("John", "25", 17)            
print(person1)
person2 = Person("John", "25", -17)            
print(person2)
