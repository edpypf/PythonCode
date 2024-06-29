#ISP
# the problem is there are multi features defined in parent class, and it is
# then difficult to apply to child when only a few features are needed

from abc import abstractmethod

class Machine:
    def print(self, document):
        raise NotImplementedError
    
    def fax(self, document):
        raise NotImplementedError
    
    def scan(self, document):
        raise NotImplementedError
    
class MultiFunctionPrinter(Machine):
    """Inherited"""
    def print(self, document):
        pass
    def fax(self, document):
        pass
    def scan(self, document):
        pass

class OldFashionedPrinter(Machine):
    """Inherited"""
    def print(self, document):
        pass
    def fax(self, document):
        pass   # do nothing, but still use will see this, but actually oldFashioned printer doesn't have this feature
    def scan(self, document):
        raise NotImplementedError  # but this will break the automation large application, crashing the application
    
## ***************************** Solution *********************************##
#  instead of having one large interface, you want to keep things granular #      
#  can be one class per feature #      
class Printer:
    @abstractmethod
    def print(self, document):
        pass

class Scanner:
    @abstractmethod
    def scan(self, document):
        pass

class MyPrinter(Printer):
    def print(self, document):
        pass 
    
class Photocopier(Printer, Scanner):
    def print(self, document):
        pass 

    def scan(self, document):
        pass

class MultifunctionDevice(Printer, Scanner):
    @abstractmethod
    def print(self, document):
        pass 
    @abstractmethod
    def scan(self, document):
        pass    

class MultiFunctionMachine(MultifunctionDevice):
    def __init__(self, printer, scanner):
        self.scanner = scanner
        self.printer = printer
        
    def print(self, document):
        self.printer.print(document)
         
    def scan(self, document):
        self.scanner.print(document)    
    
