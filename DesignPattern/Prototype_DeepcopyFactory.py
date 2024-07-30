import copy

class Address:
    def __init__(self, street_address, suite, city):
        self.street_address = street_address
        self.suite = suite
        self.city = city
        
    def __str__(self):
        return f'{self.street_address}, Suite #{self.suite}, {self.city}'        
    
class Employee:
    def __init__(self, name, address):
        self.address = address
        self.name = name

    def __str__(self):
        return f'{self.name} works at {self.address}'

class EmployeeFactory:
    # define the prototype
    main_office_employee = Employee('', Address('123 East Dr', 0, 'London'))
    aux_office_employee = Employee('', Address('123 East Dr', 0, 'London'))

    # define the deep copy method of the prototype
    @staticmethod
    def __new_employee(proto, name, suite):
        result = copy.deepcopy(proto)  # Deep copy the prototype
        result.name = name
        # Update the suite in the address
        result.address.suite = suite
        return result
        
    @staticmethod
    def new_main_office_employee(name, suite):
        return EmployeeFactory.__new_employee(EmployeeFactory.main_office_employee, name, suite)

    @staticmethod
    def new_aux_office_employee(name, suite):
        return EmployeeFactory.__new_employee(EmployeeFactory.aux_office_employee, name, suite)
    
# Create new employees using the factory
john = EmployeeFactory.new_main_office_employee('John', 999)
vincent = EmployeeFactory.new_main_office_employee('Vincent', 888888)

print(john)
print(vincent)
