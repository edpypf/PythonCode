class TextEditor:
    def __init__(self):
        self._content = ""
    
    def type(self, words):
        self._content += words
    
    def get_content(self):
        return self._content
    
    def save(self):
        return Memento(self._content)
    
    def restore(self, memento):
        self._content = memento.get_content()

class Memento:
    def __init__(self, content):
        self._content = content
    
    def get_content(self):
        return self._content

class Caretaker:
    def __init__(self):
        self._mementos = []
    
    def save(self, memento):
        self._mementos.append(memento)
    
    def undo(self):
        if not self._mementos:
            return None
        return self._mementos.pop()

# Create instances of the Originator (TextEditor) and the Caretaker
editor = TextEditor()
caretaker = Caretaker()

# Type some text and save the state
editor.type("Hello, world!")
caretaker.save(editor.save())

# Type more text and save the state
editor.type(" This is an example of the Memento Pattern.")
caretaker.save(editor.save())

# Display the current content
print(editor.get_content())  # Output: Hello, world! This is an example of the Memento Pattern.

# Undo the last operation
editor.restore(caretaker.undo())
print(editor.get_content())  # Output: Hello, world!

# Undo again
editor.restore(caretaker.undo())
print(editor.get_content())  # Output: 
