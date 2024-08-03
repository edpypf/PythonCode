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
-  Creational Patterns：- [Singleton](#SingletonPattern) - [Factory](#FactoryPattern) - [Abstract](#AbstractPattern) - [Builder](#BuilderPattern) - [Prototype](#PrototypePattern) 
-  Structural Patterns：- [Adapter](#AdapterPattern) - [Bridge](#BridgePattern) - [Composite](#CompositePattern) - [Flyweight](#FlyweightPattern) - [Decorator](#DecoratorPattern) - [Proxy](#ProxyPattern) - [Facade](#FacadePattern)
-  Behavioral Patterns：- [Visitor](#VisitorPattern) - [Template](#TemplatePattern) - [Strategy](#StrategyPattern) - [State](#StatePattern) - [observer](#ObserverPattern) - [Memento](#MementoPattern) - [Mediator](#MediatorPattern) - [Command](#command) - [Chain of Responsibility](#chainofresponsibility) - [Interpreter](#interpreter) - [Iterator](#IteratorPattern)
## -----------------------------------<->**Behavioral** <-> **Behavioral** -----------------------------------
## VisitorPattern  
The visitor pattern fits for the situation of : **Hierarchy of elements X multi features**
[Visitor-Employee Hierarchy Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Visitor.py)
- **Element Interface**: (Employee): Declares the accept method.
- **Concrete Element**: (Engineer, Manager): Implement the accept method to accept a visitor and call the appropriate visit method.
- **Visitor Interface**: (EmployeeVisitor): Defines methods for visiting engineers and managers.
- **Concrete Visitor**: (CompensationVisitor, DetailsVisitor): Implement the specific operations for calculating total compensation and collecting details.

## TemplatePattern 
define the skeleton of an algorithm in a base class but allows subclasses to provide specific implementations for some of the steps. typically marked as **final to prevent subclasses from altering the sequence of the steps**.
The Template pattern fits for the situation of : **creating a fixed sequence of steps in an algorithm while allowing some flexibility in how individual steps are executed.**
[Template Game Chess Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/TemplateGameChess.py) [Template Coffee Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/TemplateCoffee.py)
- **Abstract Class**: (CaffeineBeverage ) typically consists of a sequence of method calls, including both ABC, abstractmethod, for **Primitive Operations** 
- **Concrete Class**: (Tea and Coffee) concrete subclasses that provide specific implementations for brewing and adding condiments.
- **Abstract Methods**:(brew and addCondiments ) The abstract class also contains abstract methods that subclasses need to implement. These methods represent steps in the algorithm that can be customized.
- **Concrete Methods**:(boilWater and pourInCup) The abstract class contains some concrete methods with implementations that are common to all subclasses.  
- **Hook Methods**: (customerWantsCondiments):  Optionally, the abstract class may provide hook methods, which are methods with default implementations that can be overridden by subclasses if needed. hook methods in the Template Method Pattern offer a way to provide optional, extendable behavior in the algorithm defined by the template method. They give subclasses the opportunity to customize specific steps of the algorithm without altering the overall structure of the template method.
  
## StrategyPattern  
The Strategy Pattern is used to define a family of algorithms, encapsulate each one, and make them interchangeable. It allows the client to select an algorithm at runtime.
The Strategy pattern fits for the situation of : **a list of option methods can be provided, and up to client to choose at runtime**
[Strategy Pattern - Payment Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/StrategyPayment.py)
- **Strategy Interface**: (PaymentStrategy): base class with ABC, abstractmethod.
- **Concrete Strategies**: (CreditCardPayment, PayPalPayment): Each concrete strategy provides a element and derived method(same name) on top of base class
- **Context**: (ShopperingCart--> set_payment_strategy): The class that uses a Strategy object. It maintains a reference to a Strategy instance and delegates the algorithm implementation to it.

## StatePattern  
The State Pattern allows an object to change its behavior when its internal state changes. Instead of managing state transitions within a single class, the State Pattern delegates this responsibility to state-specific classes.
Fits situation of : **It is useful for objects that need to exhibit different behaviors based on their current state.**
[State TCP Connection Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/StateTCP.py), [State Manual Phone Script using Enum](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/StatePhoneManual.py)
- **State Enum**: (tcp state): base class with ABC, abstractmethod.
- **State Interface**: (tcp ABC, abstratctmethod--> open, close, send): base class with ABC, abstractmethod. only method of open, close and send
- **Concrete State**: (ClosedState, ListeningState, EstablishedState): Implement the behavior associated with a particular state. using the Enum to manage transitions.
- **Context**: (TCPConnection--> set_state): Manages the current state using a dictionary of states.
``` Bash
In Python, the notation context: 'TCPConnection' is a type hint that specifies the type of the context
parameter as TCPConnection. The quotes around 'TCPConnection' are used to indicate a forward reference,
which is necessary when the TCPConnection class is referenced before it is fully defined. 
```
## ObserverPattern  
Subscription mechanism that allows multiple objects (observers) to listen to and react to events or changes in the state of the subject.
Fits situation of : **distributed event-handling systems, where the subject maintains a list of observers that need to be notified of changes.**
[Property Observer - Age for Vote Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/property_dependencies_age.py), [Property Observer - Age for drive Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/property_observers.py), [Property Price Observer - Stock ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/PropertyObserver_Price_ChatGpt.py) 
- **Subject Interface**: (Stock): maintains a list of observers and notifies them of any state changes. It usually provides methods to attach and detach observers. Manages a list of investors and provides methods to attach, detach, and notify them. set_price() updates the stock price and triggers notifications to all registered investors.
- **Observer Interface**: (Investor): An interface or abstract class that defines the method update() which is called when the subject's state changes. Defines the update() method that observers use to receive notifications of price changes.
- **Concrete Subject**: (ConcreteStock): A concrete implementation of the subject that maintains the state and sends notifications to observers. Implements the Stock interface and provides the specific stock functionality.
- **Concrete Observer**: (IndividualInvestor and InstitutionalInvestor): A concrete implementation of the observer that reacts to state changes in the subject. Implement the update() method to handle notifications. Each observer can customize how it reacts to price changes. Implements the Stock interface and provides the specific stock functionality.
- **Advantages**
Decoupling: The observer pattern promotes loose coupling between the subject and the observers.
Flexibility: Observers can be added or removed at runtime.
Reusability: The same observer can be used with different subjects.
- **Disadvantages**
Memory Leaks: If observers are not properly removed, they can cause memory leaks.
Complexity: The pattern can add complexity to the system due to the need for managing multiple observers and their notifications.

- **Event based observer**
``` Bash
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)

-- Observer interface**
class Observer:
    def update(self, event_data):
        pass

-- Concrete Observer**
class ConcreteObserver(Observer):
    def __init__(self, name):
        self._name = name

    def update(self, event_data):
        print(f'{self._name} received event: {event_data}')

-- Subject with custom event
class Subject:
    def __init__(self):
        self._event = Event()

    def attach(self, observer):
        self._event.append(observer.update)

    def detach(self, observer):
        self._event.remove(observer.update)

    def generate_event(self, event_data):
        print(f'Generating event: {event_data}')
        self._event(event_data)

-- Usage
subject = Subject()

observer1 = ConcreteObserver("Observer1")
observer2 = ConcreteObserver("Observer2")

subject.attach(observer1)
subject.attach(observer2)

subject.generate_event("Event 1")
subject.generate_event("Event 2")
```
- **Classic Observer**
``` Bash
-- Observer interface
class Observer:
    def update(self, event_data):
        pass

-- Concrete Observer
class ConcreteObserver(Observer):
    def __init__(self, name):
        self._name = name

    def update(self, event_data):
        print(f'{self._name} received event: {event_data}')

-- Subject
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event_data):
        for observer in self._observers:
            observer.update(event_data)

    def generate_event(self, event_data):
        print(f'Generating event: {event_data}')
        self.notify(event_data)

-- Usage
subject = Subject()

observer1 = ConcreteObserver("Observer1")
observer2 = ConcreteObserver("Observer2")

subject.attach(observer1)
subject.attach(observer2)

subject.generate_event("Event 1")
subject.generate_event("Event 2")
``` 
## MementoPattern  
The Memento pattern fits for the situation of : **scenarios where maintaining and restoring object states is crucial, such as in undo/redo functionality in applications.**
[Memento-Bank Balance Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MementoBalance.py) | [Memento-Bank Balances redo/undo Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MementoBalanceUndoRedo.py) | [Memento-TextEditor ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MementoTextEditor_ChatGpt.py)
- **Memento**: (Memento): The Memento Pattern ensures that the state of an object is saved and restored without violating its encapsulation. The internal state is only accessible through the Memento, and only the Originator can create and use Mementos.
- **Originator**: (TextEditor): The object whose state needs to be saved and restored.
- **Caretaker**: (Caretaker): Defines undo and redo.
- **Drawback**: Memory Overhead: Storing multiple Mementos can consume a significant amount of memory, especially if the state objects are large or if there are many states to save. Complexity: Implementing the Memento Pattern can add complexity to the code, particularly in managing the Caretaker and ensuring that Mementos are properly created and used.

## MediatorPattern  
The Mediator pattern fits for the situation of : **scenarios where multiple objects need to communicate in a complex manner, and to maintain a clean and decoupled architecture.**
[Mediator-Chatroom Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MediatorChatRoom.py) | [Mediator-with Event Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MediatorWithEvent.py) | [Mediator-Chatroom ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/MediatorChatroom_ChatGpt.py)
- **Mediator**: (ABC used by chatroom): Defines an interface for communication between Colleague objects..
- **ConcreteMediator**: (chatroom): the Mediator interface and coordinates communication between Colleague objects.
- **Users**: (colleague):Represents a user in the chat room. It communicates with other users through the ChatRoom mediator.
- **Drawback**: **Mediator Complexity**: The mediator can become a complex, monolithic class as it handles more interactions and behavior. **Single Point of Failure**: The mediator is a central component; if it fails, the whole system’s communication may be disrupted.

## command  
The Command pattern fits for the situation of : **encapsulates requests as objects, allowing for parameterization, queuing, logging, and support for undoable operations, thereby decoupling the sender from the receiver of the request.**
[Basic Command Example](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/BankAccountCommand_basic.py) | [Composite Command Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/CompositeCommand.py) | [Command TextEditor ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Command_TextEdit_Chatgpt.py)
- **Command Interface**: (ABC,abstractmethod for execute/undo methods)
- **ConcreteCommand**: (TypeTextCommand, DeleteTextCommand): concrete implementations of the Command interface. They each perform specific actions on a TextEditor object and can undo those actions.
- **Invoker**: (TextEditorInvoker):invoker class that stores commands and handles execution, undo, and redo operations.
- **Context or Client**:  The client code creates instances of the TextEditor and command classes, assigns them to the invoker, and triggers their execution, undo, and redo operations.

## chainofresponsibility
The Chain of Responsibility pattern fits for the situation of : **allows multiple objects to handle a request in a sequential chain, decoupling the sender from the receiver and enabling each handler to process the request or pass it to the next handler.**
[Chain Basic Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/ChainMethod.py) | [ChainOR Broker Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Chain_Broker.py) | [ChainOR_Support ChatGpt Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/ChainOfResponsibility_ChatGpt.py) | [ChainOR ETL Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/ChainOfResponsibilityETL.py)
- **EventCaller**: __call__ for item in self: item(*args, **kwargs)
- **Handler Interface**: (CreatureModifier): Base class for all handlers, This class registers itself with the Game's queries event, defines a abstract method 'handle', __exit__ to remove the queries 
- **ConcreteHandler**: (DoubleAttackModifier; IncreaseDefenseModifier): modify the query based on specific conditions.
- **Request**: (Query) represents a request that contains the information needed to perform the action (e.g., creature_name, what_to_query, default_value).
- **Chain**: (list of handlers): Handlers are added to the Game's queries event, forming a chain.  Each handler can either handle the query or pass it to the next handler in the chain. When perform_query is called, it triggers all handlers in the chain.
- **Usage**:
  ``` Bash
  if __name__ == '__main__':
    game = Game()
    goblin = Creature(game, 'Strong Goblin', 2, 2)
    print(goblin)  # Initial state

    with DoubleAttackModifier(game, goblin):
        print(goblin)  # Attack doubled

        with IncreaseDefenseModifier(game, goblin):
            print(goblin)  # Attack doubled and defense increased
    print(goblin)  # Back to initial state
  
## interpreter
The interpreter pattern fits for the situation of : **Configurable systems where behavior is defined by expressions or rules|Expression evaluation|Language parsing**.
[Interpreter Discount Strategy Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/InterpreterDiscountStrategy.py) | [Interpreter ETL Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/IntedpreterETL.py)
- **Rules or Operations**: (Business rules, Grammar or Math Operators): (PercentageDiscount, FlatDiscount, Conditionaldiscount) | (Literal, Variable, Rule according to Grammar) | (+, -, *, Number) 
- **Abstract Expressions**: (DiscountExpression): Abstract base class DiscountExpression for applying discounts.
- **Concrete EXpressions**: (PercentageDiscount, FlatDiscount): Concrete classes for specific discount types 
- **How it works**: (main):Represents a user in the chat room. It communicates with other users through the ChatRoom mediator.
 ```Bash
Define Rules: Create concrete discount expressions (e.g., PercentageDiscount, FlatDiscount, ConditionalDiscount).

**Apply Rules**: Sequentially apply these discount expressions to the total price. Each discount
modifies the price according to its specific rule. Evaluate Final Price: After applying all discount
expressions, compute and return the final price.
Example:
**Construct Discounts**: Define discount rules such as a 10% discount, a $5 discount, and a
conditional 20% discount if the total price exceeds $50.
Apply Discounts: For a total price of $60, apply the discounts to get the final price.
**Benefits**:
Flexibility: Easily add or modify discount rules without changing the core logic.
Extensibility: Supports the addition of new types of discounts by implementing new expression classes.
 ```
## IteratorPattern  
The Iterator pattern fits for the situation of : **scenarios where you need to process a collection of items in a specific way without exposing the internal structure of the collection.**
[Iterator Business Order Processing Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/IteratorBusinessOrder.py) | [Iterator ETL Pyspark Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/IteratorETLPyspark.py)
- **Object Class**: (Order): Represents a customer order with attributes like order_id, customer_name, and total_amount.
- **Iterator Class**: (OrderIterator): Implements the iterator pattern to allow sequential access to orders in the collection. It handles the iteration logic and maintains the current index.providing the __next__() method to fetch the next order.
- **Obj Collection**: (OrderCollection ): Manages a collection of orders and provides an iterator to traverse through them. exposes an iterator through __iter__().
When iterating over order_collection, the for loop uses the iterator to access each Order object. This separation allows the OrderCollection class to focus on managing the orders, while the OrderIterator class handles the iteration logic.
```
How the Iteration is Triggered
Initialization of Iterator:
iterator = DataFrameIterator(df, batch_size) creates an instance of the DataFrameIterator class with the DataFrame & batch size.
Iteration with For Loop:
for batch_df in iterator: triggers the iteration. In Python, a for loop automatically calls the __iter__() method
of the iterator object (which is the DataFrameIterator class here). The __iter__() method returns the iterator object itself.
The for loop then repeatedly calls the __next__() method of the iterator to get the next batch of data until __next__()
raises a StopIteration exception, signaling the end of the iteration.
Detailed Flow
Calling __iter__():
When the for loop starts, it calls the __iter__() method on the iterator object. In the DataFrameIterator, this method
simply returns self, indicating that DataFrameIterator is its own iterator.
Calling __next__():
The for loop then calls __next__() to get the next item. The __next__() method in DataFrameIterator calculates the
next batch of data, updates the current_index, and returns the batch DataFrame.
This process repeats, with __next__() being called in each iteration of the for loop, until all batches have been processed.
Handling StopIteration:
When there are no more batches left to process, __next__() raises a StopIteration exception. This is a signal
to the for loop that the iteration is complete, and the loop terminates.
```

## -------------------------------<-> **Structural** <-> **Structural** <-> -------------------------------
## AdapterPattern    
The Adapter pattern fits for the situation of : **a powerful way to integrate different systems and components, ensuring compatibility and enhancing the flexibility of your application.**
[Adapter DB Save Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/AdapterDBSave.py)
- **TargetInterface**: (DataStorage): The interface that the client expects and interacts with. DataStorage with a method save(data)
- **Adaptee**: (SQLDatabase, NoSQLDatabase, and CloudStorage): The existing class with an incompatible interface. Different storage systems like SQLDatabase, NoSQLDatabase, and CloudStorage with different methods for storing data.
- **Adapter**: (SQLDatabaseAdapter, NoSQLDatabaseAdapter, and CloudStorageAdapter): A class that implements the target interface and translates the client's requests into calls to the adaptee's methods. implement DataStorage and translate save calls to the respective methods of the storage systems.
``` Bash
# Define the Target Interface
class TargetInterface:
    def method(self, param):
        pass

# Define the Adaptee
class Adaptee:
    def incompatible_method(self, param):
        # Implementation
        pass

# Define the Adapter
class Adapter(TargetInterface):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def method(self, param):
        self.adaptee.incompatible_method(param)

# Using the Adapter
adaptee = Adaptee()
adapter = Adapter(adaptee)
adapter.method("example_param") 
```
## BridgePattern  
The Bridge pattern fits for the situation of : **you can create a more flexible, scalable, and maintainable system architecture, especially in complex applications with multiple variations of abstractions and implementations.**
[Bridge Notification Sender Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/BridgeNotificationSender.py)
- **Abstraction**: (Notification): Defines the high-level interface and maintains a reference to an Implementor object.
- **Refined Abstratction**: (AlertNotification, ReminderNotification): extend the abstraction for specific notification types
- **Implementor interface**: (MessageSender): This is the low-level interface for sending notifications through various channels.
- **Concrete Implementor**: (EmailSender, SMSSender) These implement the notification sending methods for specific channels
- **Bridge the Abstraction and Implementor**: The abstraction (Notification) maintains a reference to the implementor (MessageSender), allowing different combinations of notification types and message channels.

```Bash
alert_notification_with_email = AlertNotification(email_sender);
reminder_notification_with_sms = ReminderNotification(sms_sender)
```
## CompositePattern  
The Composite pattern fits for the situation of : **represent a hierarchy of objects, where individual objects and compositions of objects need to be manipulated in the same way.**
[Composite Nerual Network Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Composit_neural_networks.py) | [Composite Org Hierarchy Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Composite_Org_Hierarchy.py)
- **Component**: (Employee): base interface for all objects in the composition, including employees and managers.
- **Leaf**: (Developers, Designer): A basic element of the composition that does not have any children. It implements the Component interface. individual employees who do not have any direct reports.
- **Composite**: (Manager): A composite element that has children. It implements the Component interface and provides mechanisms to add and remove children. managers who can have direct reports, which can be either individual employees or other managers. This setup allows for a flexible and scalable representation of an organizational hierarchy, making it easy to manage complex structures of employees and managers.

## DecoratorPattern  
The Decorator pattern fits for the situation of : **allows behavior to be added to individual objects, either statically or dynamically, without affecting the behavior of other objects from the same class. It is typically used to adhere to the Single Responsibility Principle, allowing functionalities to be divided between classes with unique areas of concern.**
[Decorator Basic Timeit Function Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Decorator_Function.py)| [Decorator Booking System Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/DecoratorBookingSystem.py) | [Decorator Ordering Coffee Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/DecoratorCoffee.py) | [Decorator ETL Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/DecoratorETL.py)
- **Dynamic Behavior Addition**: Adds responsibilities to objects at runtime.
- **Composition over Inheritance**: Promotes composition instead of inheritance, providing greater flexibility in extending functionalities.
- **Single Responsibility Principle**: Each decorator has a specific responsibility, adhering to the Single Responsibility Principle.
- **Component and Concrete Component**: (Booking_Room): A the base interface or class and A class that implements the base interface or class.
- **Decorator and Concrete Decorators**: (Logging, Authentication, Validation Decorator): base interface and contains a reference to a component. Classes that extend the decorator to add functionalities.
- **Apply Decorators to the Base Function**:
  ``` Bash @log_decorator
      @auth_decorator
      @validate_decorator
      def book_room(room_type, customer_id):
        print(f"Booking {room_type} for customer {customer_id}.")
- **@wraps(func)**: The @wraps(func) decorator from the functools module is used to preserve the original function's metadata (such as its name, docstring, and module) when it is wrapped by another function. This is crucial for accurate logging, debugging, and maintaining the integrity of the function's signature and documentation.

## ProxyPattern  
The Proxy Pattern provides a surrogate or placeholder for another object to control access to it. The proxy object acts as an intermediary, adding a level of indirection to support various operations. Suitable for : **access control, lazy initialization, logging, or remote access**
[Proxy_OnlinePayment System Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/ProxyOnlinePaymentSystem.py) | [Proxy DB Connection Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/ProxyDBConnection.py) | [Proxy DB Connection Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/ProxyETL.py)
- **Key Point**: 
``` Bash
Control Access: The proxy can control access to the real object, adding security or validation checks.
Lazy Initialization: The proxy can delay the creation of the real object until it is needed.
Logging/Monitoring: The proxy can log requests or perform other tasks before forwarding requests to the real object.
Remote Proxy: The proxy can represent an object in a different address space, making remote method invocation possible.
```
- **Subject**: (Payment): An abstract base class defining the process_payment method.
- **RealSubject**: (RealPayment): Implements the process_payment method to perform the actual payment processing.
- **Proxy**: (PaymentProxy): Controls access to the RealPayment object. Adds authentication and logging functionalities.

## FlyweightPattern  
The Flyweight pattern aims to reduce memory usage by sharing as much data as possible. Here’s how it’s applied in your code. Suitable for : **scenarios where there is a large number of objects that can share common data to save memory.**
[Flyweight userName Searching Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FlyWeight_Reuse_Name_String.py) | [FlyWeight Doc Management System Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FlyweightDocumentMgmtSystem.py) | [FlyWeight Text Formatting Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FlyWeight_CapChar.py) | [FlyWeight Doc Management System Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FlyweightETLoverFunction.py)
- **Flyweight Class**: (font, color): Represents shared state (e.g., font, color). Represents the shared state (font and color) of a word.
- **Context Class**: (position): Represents unique state (e.g., position in the document). Ensures that flyweight instances are shared and reused to minimize memory usage.
- **Flyweight Factory**: (Manager): Manages the creation and reuse of flyweight objects. Ensures that flyweight instances are shared and reused to minimize memory usage.

## FacadePattern  
The Facade pattern fits for the situation of : **where you need to simplify complex systems, decouple clients from subsystems, create a unified interface, and improve code readability and maintenance.**
[Facade online Hotel Booking Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FacadeOnlineHotelBooking.py) | [Facade OnlineTravel Booking Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FacadeOnLineTravelBooking.py)
| [Facade ETL better than Function Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FacadeETLvsFunction.py)
- **Key Points**: **Simplification**: Provides a simpler interface to a complex system | **Isolation**: Decouples the client from the complex subsystem | **Unified Interface**: Combines multiple interfaces into a single unified interface
- **Step by Step - Subsystem Classes**: (RoomBooking, Payment, Notification):  The simplified interface
- **Step by Step - Facade**: (HotelBookingFacade): The complex system's classes that the Facade interacts with.
- **Step by Step - Client Code**: (facade = HotelBookingFacade()): facade.book_room("single", "customer123")

## -----------------------------------<->**Creational** <-> **Creational** -----------------------------------
## BuilderPattern - Return self 
The Builder pattern suitable for: **Configuration Objects, DB Queries, Game Development, Document Generation, User Interface (UI) Components**
[Builder Facet Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/BuilderFacet.py) | [Builder Inheritence Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/BuilderInheritence.py) | [Builder Pizza with Director Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Builder_Pizza.py)
- **Element Interface**: (Pizza): Defines the structure of the Pizza object with various attributes (size, cheese, pepperoni, veggies).
- **Element Builder**: (Pizza Builder): Contains methods to set the size and add ingredients to the pizza. The build method returns the final Pizza object.
- **Director Class**: (Director): Uses the builder to construct specific types of pizzas by calling the appropriate methods on the builder.
``` Bash
This pattern allows for a flexible and readable way to create different types of pizzas without
having to manually set each attribute every time. The Director controls the construction process,
ensuring that the creation of complex objects follows a consistent and easy-to-understand sequence.
```
## FactoryPattern  
The Factory pattern suitable for: **Configuration Objects, DB Queries, Game Development, Document Generation, User Interface (UI) Components**
[Factory Concept Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FactoryConcept.py) | [Factory Method Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FactoryMethod.py) | [Factory Doc Report Invoice Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FactoryReportInvoiceDoc.py) | [Factory ETL Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/FactoryETL.py)
- **Creator Class**: (DocumentCreator): defines the create_document factory method and the print_document method that uses the factory method to create a Document and print it.
- **Product Interface**: (Document): base class declares the print method that all concrete document classes must implement.
- **Concrete Products**: (Report and Invoice classes): These classes implement the Document interface and provide specific implementations of the print method.
- **Concrete Creators**: (ReportCreator and InvoiceCreator): These classes inherit from DocumentCreator and override the create_document method to return instances of Report and Invoice, respectively.
``` Bash
the Factory Method pattern is used to create different types of documents (Reports and Invoices)
by centralizing and encapsulating the creation logic in the DocumentCreator class and its subclasses.
This makes the system flexible and easy to extend with new document types without modifying existing code.
```
## SingletonPattern  
The Singleton pattern suitable for: **useful when exactly one object is needed to coordinate actions across the system.**
[Singleton DB allocator Concept Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/SingletonDBAllocator.py) | [Singleton Decorator Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/SingletonDecorator.py) | [Singleton Metaclass Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/SingletonMetaclass.py) | [SingletonMonoState Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/SingletonMonoState.py) | [Singleton TestCases Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/SingletonTestCases.py) | [Singleton Configuration Manager Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/SingletonConfigurationManager.py)
``` Bash
Business Example: Configuration Manager
Imagine a business application that requires access to configuration settings from a central repository.
These settings need to be consistent and only loaded once to avoid repeated reads from a configuration
file or database, which can be both time-consuming and error-prone.
Implementation:
Singleton Class: ConfigurationManager
This class reads configuration settings from a file or database and stores them in a dictionary.
It ensures that only one instance of the configuration settings exists throughout the application.
Access Point: getInstance()
The method getInstance() is used to access the single instance of ConfigurationManager.
```
- **Singleton Metaclass**: The Singleton metaclass keeps track of instances using the _instances dictionary. When ConfigurationManager is instantiated, it checks if an instance already exists. If not, it creates and stores the instance. Future instantiations return the stored instance.
- **ConfigurationManager**: On initialization, ConfigurationManager loads the configuration settings into a dictionary. The method get_config() allows access to the configuration settings.
- **Usage**: When config1 and config2 are created, they point to the same instance of ConfigurationManager. Accessing configuration settings through either config1 or config2 yields the same results, ensuring consistency across the application.

## AbstractPattern  
The Abstract pattern suitable for: **Configuration Objects, DB Queries, Game Development, Document Generation, User Interface (UI) Components**
[Abstract Factory Concept, Abstract Factory Coffee Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/AbstractFactory.py) | [Abstract UI Example Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/AbstractUIComponent.py)
| [Abstract Factory ETL Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/AbstractETL.py) 
- **AbstractFactory**: (GUI Factory): Declares creation methods for abstract products. GUIFactory declares methods for creating abstract products. 
- **ConcreteFactory**: (Windows Factory, Mac Factory): Implements the creation methods and returns concrete products.WindowsFactory and MacFactory implement the GUIFactory interface and return concrete products.
- **AbstractProduct**: (Button and Checkbox): Declares the interface for a product. define interfaces for buttons and checkboxes. 
- **Concrete Products**: (WindowsButton and MacButton,WindowsCheckbox and MacCheckbox): Implements the abstract product interface.  implement Button & checkbox for Windows and Mac.
- **Client**: The client code uses the abstract factory to create products. It works with abstract products and factories, so it doesn't depend on the specific classes of the products.
``` Bash
the Abstract Factory Pattern is used to create families of related objects without specifying their
concrete classes, promoting consistency and flexibility in object creation.
```
## PrototypePattern - DeepCopy 
The Prototype pattern suitable for: **is valuable for situations where creating objects from scratch is costly, and where cloning a prototype can streamline the process of object creation.**
[Prototype Concept Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Prototype_deepcopy.py) | [Prototype Employee Factory Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/Prototype_DeepcopyFactory.py) | [Prototype - Doc Mgt Script](https://github.com/edpypf/PythonCode/blob/main/DesignPattern/PrototypeDocMgt.py)
- **Prototype Interface**: (Employee): Defines the method for cloning itself. This is often an abstract class or an interface.
- **Concrete Prototype**: (EmployeeFactory.main_office_employee, EmployeeFactory.aux_office_employee): They have predefined state - address & empty names. used as the base for creating new employees. are prototypes that you clone them to create new instances. provides the implementation of the clone method. It holds the actual state and specifies how to create a new instance by copying itself.
- **Client Code**: (john and vincent): new Employee instances are created by cloning the prototypes and customizing them. Each new employee has its own name and suite while sharing the base address structure from the prototype.
``` Bash
allows you to create new objects by copying an existing object, known as the prototype. useful when the cost of 
creating a new instance of an object is more expensive than copying an existing one. It's often used when objects 
are complex to initialize or when the objects need to be duplicated with slight variations.

import copy
class Prototype:
    def __init__(self, state):
        self.state = state

    def clone(self):
        return copy.deepcopy(self)
-- Client code
original = Prototype("Initial State")
clone1 = original.clone()
clone2 = original.clone()
clone1.state = "Changed State for Clone 1"

print(f"Original: {original.state}")
print(f"Clone 1: {clone1.state}")
print(f"Clone 2: {clone2.state}")
```
