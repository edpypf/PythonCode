from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class TextEditor:
    def __init__(self):
        self.text = ""

    def type_text(self, text):
        self.text += text

    def delete_text(self, num_chars):
        self.text = self.text[:-num_chars]

    def get_text(self):
        return self.text

class TypeTextCommand(Command):
    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text

    def execute(self):
        self.editor.type_text(self.text)

    def undo(self):
        self.editor.delete_text(len(self.text))

class DeleteTextCommand(Command):
    def __init__(self, editor: TextEditor, num_chars: int):
        self.editor = editor
        self.num_chars = num_chars

    def execute(self):
        self.editor.delete_text(self.num_chars)

    def undo(self):
        # We need to store the deleted text to undo this action
        self.deleted_text = self.editor.get_text()[-self.num_chars:]
        self.editor.type_text(self.deleted_text)

class TextEditorInvoker:
    def __init__(self):
        self.history = []
        self.undo_history = []

    def execute_command(self, command: Command):
        command.execute()
        self.history.append(command)
        self.undo_history.clear()  # Clear redo history on new action

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
            self.undo_history.append(command)

    def redo(self):
        if self.undo_history:
            command = self.undo_history.pop()
            command.execute()
            self.history.append(command)

if __name__ == "__main__":
    editor = TextEditor()
    invoker = TextEditorInvoker()

    type_hello = TypeTextCommand(editor, "Hello")
    type_world = TypeTextCommand(editor, " World")
    delete_world = DeleteTextCommand(editor, 6)

    invoker.execute_command(type_hello)
    invoker.execute_command(type_world)
    print(editor.get_text())  # Output: Hello World

    invoker.undo()
    print(editor.get_text())  # Output: Hello

    invoker.redo()
    print(editor.get_text())  # Output: Hello World

    invoker.execute_command(delete_world)
    print(editor.get_text())  # Output: Hello
