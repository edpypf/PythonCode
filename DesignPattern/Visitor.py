from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Engineer(Employee):
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def accept(self, visitor):
        visitor.visit_engineer(self)

class Manager(Employee):
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        self.reports = []
    
    def add_report(self, report):
        self.reports.append(report)
    
    def accept(self, visitor):
        visitor.visit_manager(self)

class EmployeeVisitor(ABC):
    @abstractmethod
    def visit_engineer(self, engineer):
        pass
    
    @abstractmethod
    def visit_manager(self, manager):
        pass

class CompensationVisitor(EmployeeVisitor):
    def __init__(self):
        self.total_compensation = 0

    def visit_engineer(self, engineer):
        self.total_compensation += engineer.salary
    
    def visit_manager(self, manager):
        self.total_compensation += manager.salary
        for report in manager.reports:
            report.accept(self)
    
    def get_total_compensation(self):
        return self.total_compensation

class DetailsVisitor(EmployeeVisitor):
    def __init__(self):
        self.details = []

    def visit_engineer(self, engineer):
        self.details.append(f"Engineer: {engineer.name}, Salary: {engineer.salary}")
    
    def visit_manager(self, manager):
        self.details.append(f"Manager: {manager.name}, Salary: {manager.salary}")
        for report in manager.reports:
            report.accept(self)
    
    def get_details(self):
        return self.details

# Create employees
engineer1 = Engineer("Alice", 100000)
engineer2 = Engineer("Bob", 120000)
manager = Manager("Charlie", 150000)
manager.add_report(engineer1)
manager.add_report(engineer2)

# Calculate total compensation
compensation_visitor = CompensationVisitor()
manager.accept(compensation_visitor)
print(f"Total compensation: ${compensation_visitor.get_total_compensation()}")

# Collect details
details_visitor = DetailsVisitor()
manager.accept(details_visitor)
print("Employee details:")
for detail in details_visitor.get_details():
    print(detail)
