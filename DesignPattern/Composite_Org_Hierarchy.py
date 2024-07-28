from abc import ABC, abstractmethod

# Step 1: Define the Component Interface
class Employee(ABC):
    @abstractmethod
    def show_details(self):
        pass

# Step 2: Create Leaf Classes
class Developer(Employee):
    def __init__(self, name, position):
        self.name = name
        self.position = position
    
    def show_details(self):
        print(f"Developer: {self.name}, Position: {self.position}")

class Designer(Employee):
    def __init__(self, name, position):
        self.name = name
        self.position = position
    
    def show_details(self):
        print(f"Designer: {self.name}, Position: {self.position}")

# Step 3: Create Composite Classes
class Manager(Employee):
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.subordinates = []
    
    def add(self, employee):
        self.subordinates.append(employee)
    
    def remove(self, employee):
        self.subordinates.remove(employee)
    
    def show_details(self):
        print(f"Manager: {self.name}, Position: {self.position}")
        for subordinate in self.subordinates:
            subordinate.show_details()

# Step 4: Build the Organization Structure
# Create leaf objects
dev1 = Developer("John Doe", "Senior Developer")
dev2 = Developer("Jane Smith", "Junior Developer")
des1 = Designer("Emily Davis", "Lead Designer")

# Create composite objects
mgr1 = Manager("Michael Scott", "Regional Manager")
mgr2 = Manager("Dwight Schrute", "Assistant to the Regional Manager")

# Add leaf objects to composite objects
mgr1.add(dev1)
mgr1.add(dev2)
mgr1.add(des1)

mgr2.add(dev2)  # Dwight is managing one of the developers directly too

# Add composite objects to other composite objects
mgr1.add(mgr2)

# Show details of the organization structure
mgr1.show_details()
