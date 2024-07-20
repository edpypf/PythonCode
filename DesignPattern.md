# Design Pattern

![Project Logo](images/designPattern.png)
Design Patter is used in OOP programming, this page listed all the patterns, logic and example code, here's the index of it.

# Pattern Category 🚀
| Category       | Description                                                                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Creational     | to create objects in a manner suitable for the situation. solve design problem by controlling the object creation process                                    |
| Structural     | deal with object composition, creating relationships between objects to form larger structures, ensure no impact to other part if one part of system changed |
| Behavioral     | managing complex control flows in a system with algorithms and the assignment of responsibilities between objects                                            |

## List of Patterns
-  Creational Patterns：- [Singleton](#singleton) - [Factory](#factory) - [Abstract](#abstract) - [Builder](#builder) - [Prototype](#prototype) 
-  Structural Patterns：- [Adapter](#adapter) - [Bridge](#bridge) - [Composite](#composite) - [Flyweight](#flyweight) - [Decorator](#decorator) - [Proxy](#proxy) - [Facade](#facade)
-  Behavioral Patterns：- [Visitor](#VisitorPattern) - [Template](#template) - [Strategy](#strategy) - [State](#state) - [observer](#observer) - [Memento](#memento) - [Mediator](#mediator) - [Command](#command) - [Chain of Responsibility](#chainofresponsibility) - [Interpreter](#interpreter) - [Iterator](#iterator)

## VisitorPattern  
[Visitor-Employee Hierarchy Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Visitor.py)
- **Element Interface**: (Employee): Declares the accept method.
- **Concrete Element**: (Engineer, Manager): Implement the accept method to accept a visitor and call the appropriate visit method.
- **Visitor Interface**: (EmployeeVisitor): Defines methods for visiting engineers and managers.
- **Concrete Visitor**: (CompensationVisitor, DetailsVisitor): Implement the specific operations for calculating total compensation and collecting details.

The visitor pattern fits for the situation of : **Hierarchy of elements X multi features**

## Template Pattern 
define the skeleton of an algorithm in a base class but allows subclasses to provide specific implementations for some of the steps. 
- [Template Game Chess Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/TemplateGameChess.py)
- **Template Method**: (Employee): **Abstract Class** typically consists of a sequence of method calls, including both concrete and abstract methods. <ABC, abstractmethod, > for **Primitive Operaations**
  ```class Game(ABC):
    def run(self):
        self.start()
        while not self.have_winner:
            self.take_turn()
        print(f'Player {self.winning_player} wins!')

    @abstractmethod
    def start(self): pass

    @property
    @abstractmethod
    def have_winner(self): pass

    @abstractmethod
    def take_turn(self): pass

    @property
    @abstractmethod
    def winning_player(self): pass```
- **Concrete Class**: (Chess):  It customizes the behavior of the algorithm by providing specific details for some of the steps in the subclass.
- ```
  class Chess(Game):
    def __init__(self):
        super().__init__()
        self.max_turns = 10
        self.turn = 1

    def start(self):
        print('Starting a game of chess.')

    @property
    def have_winner(self):
        return self.turn > self.max_turns

    def take_turn(self):
        print(f'Turn {self.turn} taken.')
        self.turn += 1

    @property
    def winning_player(self):
        return 'Player 1'  # Example static winner
```

The Template pattern fits for the situation of : **creating a fixed sequence of steps in an algorithm while allowing some flexibility in how individual steps are executed.**
