class Creature:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense

    def __str__(self):
        return f'{self.name} has {self.attack}/{self.defense}'
    
class CreatureModifier:
    def __init__(self, creature):
        self.creature = creature
        self.next_modifier = None
    
    def add_modifier(self, modifier):
        if self.next_modifier:
            self.next_modifier.add_modifier(modifier)
        else:
            self.next_modifier = modifier

    def handle(self):
        if self.next_modifier:
            self.next_modifier.handle()

class NoBonusModifier(CreatureModifier):
    def handle(self):
        print('no bouns to you!')

class DoubleAttackModifier(CreatureModifier):
    def handle(self):
        print(f'Doubling {self.creature}''s attack. ')
        self.creature.attack *= 2
        super().handle()

class IncreaseDefenseModifier(CreatureModifier):
    def handle(self):
        if self.creature.attack <= 2:
            print(f'Increasing {self.creature}''s defense. ')
            self.creature.defense += 1
        super().handle()

if __name__ == '__main__':
    gobaling = Creature('Gobaling', 1, 1)        
    print(gobaling)

    gm = CreatureModifier(gobaling)
    # gm.add_modifier(NoBonusModifier(gobaling))
    gm.add_modifier(DoubleAttackModifier(gobaling))
    gm.add_modifier(IncreaseDefenseModifier(gobaling))
    gm.add_modifier(DoubleAttackModifier(gobaling))


    gm.handle()
    print(gobaling)
