from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def print(self):
        pass

class Report(Document):
    def print(self):
        print("Printing Report")

class Invoice(Document):
    def print(self):
        print("Printing Invoice")
      
class DocumentCreator(ABC):
    @abstractmethod
    def create_document(self):
        pass

    def print_document(self):
        document = self.create_document()
        document.print()

class ReportCreator(DocumentCreator):
    def create_document(self):
        return Report()

class InvoiceCreator(DocumentCreator):
    def create_document(self):
        return Invoice()

if __name__ == "__main__":
    report_creator = ReportCreator()
    report_creator.print_document()  # Output: Printing Report

    invoice_creator = InvoiceCreator()
    invoice_creator.print_document()  # Output: Printing Invoice
