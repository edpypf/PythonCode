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
-  Behavioral Patterns：- [Visitor](#VisitorPattern) - [Template](#TemplatePattern) - [Strategy](#StrategyPattern) - [State](#StatePattern) - [observer](#observer) - [Memento](#memento) - [Mediator](#mediator) - [Command](#command) - [Chain of Responsibility](#chainofresponsibility) - [Interpreter](#interpreter) - [Iterator](#iterator)

## VisitorPattern  
The visitor pattern fits for the situation of : **Hierarchy of elements X multi features**
[Visitor-Employee Hierarchy Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Visitor.py)
- **Element Interface**: (Employee): Declares the accept method.
- **Concrete Element**: (Engineer, Manager): Implement the accept method to accept a visitor and call the appropriate visit method.
- **Visitor Interface**: (EmployeeVisitor): Defines methods for visiting engineers and managers.
- **Concrete Visitor**: (CompensationVisitor, DetailsVisitor): Implement the specific operations for calculating total compensation and collecting details.

## TemplatePattern 
define the skeleton of an algorithm in a base class but allows subclasses to provide specific implementations for some of the steps. 
The Template pattern fits for the situation of : **creating a fixed sequence of steps in an algorithm while allowing some flexibility in how individual steps are executed.**
[Template Game Chess Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/TemplateGameChess.py)
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
  ```
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
  
## StrategyPattern  
The Strategy Pattern is used to define a family of algorithms, encapsulate each one, and make them interchangeable. It allows the client to select an algorithm at runtime.
The Strategy pattern fits for the situation of : **a list of option methods can be provided, and up to client to choose at runtime**
[Strategy Pattern - Payment Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/StrategyPayment.py)
- **Strategy Interface**: (PaymentStrategy): base class with ABC, abstractmethod.
- **Concrete Strategies**: (CreditCardPayment, PayPalPayment): Each concrete strategy provides a element and derived method(same name) on top of base class
- **Context**: (ShopperingCart--> set_payment_strategy): Defines methods for visiting engineers and managers.

## StatePattern  
The State Pattern allows an object to change its behavior when its internal state changes. Instead of managing state transitions within a single class, the State Pattern delegates this responsibility to state-specific classes.
The Strategy pattern fits for the situation of : **It is useful for objects that need to exhibit different behaviors based on their current state.**
[Strategy Pattern - Payment Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/StrategyPayment.py)
- **State Enum**: (PaymentStrategy): base class with ABC, abstractmethod.
- **State Interface**: (PaymentStrategy): base class with ABC, abstractmethod.
- **Concrete Strategies**: (CreditCardPayment, PayPalPayment): Each concrete strategy provides a element and derived method(same name) on top of base class
- **Context**: (ShopperingCart--> set_payment_strategy): Defines methods for visiting engineers and managers.
