# Abstract Product A
class Button:
    def paint(self):
        pass

# Concrete Product A1
class WindowsButton(Button):
    def paint(self):
        print("Rendering a button in Windows style")

# Concrete Product A2
class MacButton(Button):
    def paint(self):
        print("Rendering a button in Mac style")

# Abstract Product B
class Checkbox:
    def paint(self):
        pass

# Concrete Product B1
class WindowsCheckbox(Checkbox):
    def paint(self):
        print("Rendering a checkbox in Windows style")

# Concrete Product B2
class MacCheckbox(Checkbox):
    def paint(self):
        print("Rendering a checkbox in Mac style")

# Abstract Factory
class GUIFactory:
    def create_button(self):
        pass

    def create_checkbox(self):
        pass

# Concrete Factory 1
class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()

# Concrete Factory 2
class MacFactory(GUIFactory):
    def create_button(self):
        return MacButton()

    def create_checkbox(self):
        return MacCheckbox()

# Client code
def client_code(factory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    button.paint()
    checkbox.paint()

# Usage
print("Client: Testing Windows factory")
windows_factory = WindowsFactory()
client_code(windows_factory)

print("\nClient: Testing Mac factory")
mac_factory = MacFactory()
client_code(mac_factory)
