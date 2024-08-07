#########################################33333
Traceback (most recent call last):
  File "c:\Users\edpyp\Downloads\test.py", line 59, in <module>
    t.test_exercise()
  File "c:\Users\edpyp\Downloads\test.py", line 48, in test_exercise
    self.assertEqual('too young', rp.drive())
  File "c:\Users\edpyp\Downloads\test.py", line 35, in drive
    self.person = Person(self.age)
  File "c:\Users\edpyp\Downloads\test.py", line 22, in age
    return self.person.age
AttributeError: 'NoneType' object has no attribute 'age'
################################################################3

from unittest import TestCase

class Person:
  def __init__(self, age):
    self.age = age

  def drink(self):
    return 'drinking'

  def drive(self):
    return 'driving'

  def drink_and_drive(self):
    return 'driving while drunk'

class ResponsiblePerson:
  def __init__(self, peron):
    self.person = None
    
  @property        
  def age(self):
      return self.person.age
      
  @age.setter       
  def age(self, value):
      self.person.age = value
    
  def drink(self):
      if self.age < 18:
          return 'too young'
      else: return self.person.drink()
  
  def drive(self):
      if not self.person:
          self.person = Person(self.age)
          if self.age < 16:
              print('too young')
          else: return self.person.drive()
          
  def drink_and_drive(self):
      print('dead')

class Evaluate(TestCase):
  def test_exercise(self):
    p = Person(10)
    rp = ResponsiblePerson(p)

    self.assertEqual('too young', rp.drive())
    self.assertEqual('too young', rp.drink())
    self.assertEqual('dead', rp.drink_and_drive())

    rp.age = 20

    self.assertEqual('driving', rp.drive())
    self.assertEqual('drinking', rp.drink())
    self.assertEqual('dead', rp.drink_and_drive())

t=Evaluate()
t.test_exercise()
