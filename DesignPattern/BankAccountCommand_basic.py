from abc import ABC
from enum import Enum

class BankAccount:
    OVER_DRAFT_LIMIT = -500
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f'deposit {amount} and balance now is {self.balance}')

    def withdraw(self, amount):
        if self.balance - amount <= self.OVER_DRAFT_LIMIT:
            print('the withdraw amount exceeds the over draft lime: {self.OVER_DRAFT_LIMIT}')
            return False
        else:
            self.balance -= amount
            print(f'withdraw {amount}, and balance is {self.balance}')
        return True

    def __str__(self):
        return f'Account Balance: {self.balance}'

class BankAccountCommand:
    def __init__(self, account, action, amount):
        self.account = account
        self.action = action
        self.amount = amount
        self.success = None

    class Action(Enum):
        DEPOSIT = 1 
        WITHDRAW = 2

    def invoke(self):
        if self.action == self.Action.DEPOSIT:
            self.account.deposit(self.amount)
            self.success = True
        elif self.action == self.Action.WITHDRAW:
            self.success = self.account.withdraw(self.amount)

    def undo(self):
        if not self.success:
            return
        if self.action == self.Action.DEPOSIT:
            self.account.withdraw(self.amount)
        elif self.action == self.Action.WITHDRAW:
            self.account.deposit(self.amount)
            

if __name__ == '__main__':
    ba = BankAccount(100)
    bac = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 500)
    bac.invoke()
    print(ba)
    bac.undo()
    print(ba)

    illegal_cmd = BankAccountCommand(ba, BankAccountCommand.Action.WITHDRAW, 1000)
    illegal_cmd.invoke()
    print('After impossible withdrawal:', ba)
    illegal_cmd.undo()
    print('After undo:', ba)
