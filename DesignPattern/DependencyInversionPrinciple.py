
# DIP -- the problem is that we define the self.relations=[], what if we want to change it to dict
# then all the other codes would be needed to change and a lot of changes.
# so the solution is to put part of Research: loop nd checking to the lower level class Relationships, 
# not the high level class - Research  

from abc import abstractmethod
from enum import Enum

class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2

class Person:  
    def __init__(self, name):
        self.name = name 

# Add one more lower level class to handle this checking
# this is good for unit testing, also it is storage and lower level class, 
# you can easily replace it with DB content without affecting and break the Research function
class RelationshipBrowser:
    @abstractmethod
    def find_all_children_of(self, name):
        pass         

class Relationships:  
    def __init__(self):
        self.relations = []

    def add_parent_and_child(self, parent, child):
        self.relations.append(
            (parent, Relationship.PARENT, child)
        )
        self.relations.append(
            (child, Relationship.CHILD, parent)
        )

# Add function here to handle this checking, and once list changed to list, 
# we just need to modify the code here at lower level    
    def find_all_children_of(self, name):
        for r in self.relations:
            if r[0].name==name and r[1] == Relationship.PARENT:
                yield r[2].name

class Research:  
    # def __init__(self, relationships):
    #     relations = relationships.relations
    #     for r in relations:
    #         if r[0].name=='John' and r[1]==Relationship.PARENT:
    #             print(f'John has a child called {r[2].name}')

    def __init__(self, browser):
        for p in browser.find_all_children_of('John'):
            print(f'John has a child called {p}')


parent = Person('John')
child1 = Person('chris')
child2 = Person('Alex')

relationships = Relationships()
relationships.add_parent_and_child(parent, child1)
relationships.add_parent_and_child(parent, child2)

Research(relationships)
