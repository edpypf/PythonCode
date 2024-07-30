from copy import deepcopy

class DocumentPrototype:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}"

    def clone(self):
        return deepcopy(self)

class Report(DocumentPrototype):
    def __init__(self, title, content, report_type):
        super().__init__(title, content)
        self.report_type = report_type

    def __str__(self):
        return f"Report Type: {self.report_type}\n" + super().__str__()

class Invoice(DocumentPrototype):
    def __init__(self, title, content, invoice_number):
        super().__init__(title, content)
        self.invoice_number = invoice_number

    def __str__(self):
        return f"Invoice Number: {self.invoice_number}\n" + super().__str__()

# Client code
def create_document(prototype, **kwargs):
    new_document = prototype.clone()
    for key, value in kwargs.items():
        setattr(new_document, key, value)
    return new_document

# Creating prototypes
report_prototype = Report("Monthly Report", "This is the content of the monthly report.", "Monthly")
invoice_prototype = Invoice("Invoice for July", "This is the content of the invoice.", "INV-007")

# Creating new documents based on prototypes
new_report = create_document(report_prototype, title="Updated Monthly Report")
new_invoice = create_document(invoice_prototype, title="Updated Invoice for July", invoice_number="INV-008")

print(new_report)
print(new_invoice)
