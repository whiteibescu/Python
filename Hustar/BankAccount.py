class BankAccount:
    def __init__(self, balance=0, name='none'):
        self.balance = balance
        self.name = name

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("잔액 부족")

    def deposit(self, amount):
        self.balance += amount

    def get_info(self):
        print("이름: ", self.name)
        print('잔고: ', self.balance)


a = BankAccount(0, "Gildong Hong")
# a.deposit(400)
# a.withdraw(600)

a.deposit(1000)
a.withdraw(900)
a.get_info()