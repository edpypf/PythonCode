from abc import ABC
from enum import Enum

class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)

class WhatToQuery(Enum):
    ATTACK = 0
    DEFENSE = 1    

class Query:
    def __init__(self, creature_name, what_to_query, default_value):
        self.creature_name = creature_name
        self.what_to_query = what_to_query
        self.value = default_value

class Game:
    def __init__(self):
        self.queries = Event()
        
    def perform_queries(self, sender, query):
        self.queries(sender, query)

class Creature:
    def __init__(self, game, name, attack, defense):
        self.name = name
        self.game = game
        self.initial_attack = attack
        self.initial_defense = defense

    @property
    def attack(self):
        q = Query(self.name, WhatToQuery.ATTACK, self.initial_attack)
        self.game.perform_queries(self, q)
        return q.value
    
    @property
    def defense(self):
        q = Query(self.name, WhatToQuery.DEFENSE, self.initial_defense)
        self.game.perform_queries(self, q)
        return q.value
    
    def __str__(self):
        return f'{self.name}: {self.attack}/{self.defense}'
    
class CreatureModifier(ABC):
    def __init__(self, creature, game):
        self.creature = creature
        self.game = game
        self.game.queries.append(self.handle)

    def handle(self, sender, query):
        pass

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.game.queries.remove(self.handle)

class DoubleAttackModifier(CreatureModifier):
    def handle(self, sender, query):
        if (sender.name == self.creature.name and query.what_to_query == WhatToQuery.ATTACK):
            query.value *= 2 

class IncreaseDefenseModifier(CreatureModifier):
    def handle(self, sender, query):
        if (sender.name == self.creature.name and query.what_to_query == WhatToQuery.DEFENSE):
            query.value += 3

if __name__ == '__main__':
    game = Game()
    gablin = Creature(game, 'Strong Goblin', 2, 2)
    print(gablin)

    with DoubleAttackModifier(gablin, game):
        print(gablin)
        with IncreaseDefenseModifier(gablin, game):
            print(gablin)

    print(gablin)
