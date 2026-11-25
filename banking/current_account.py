from decimal import Decimal
from .account import Account
class CurrentAccount(Account):
    """Current account with a configurable overdraft limit."""
    def __init__(self, account_number, holder_name, opening_balance=0, overdraft_limit=1000):
        super().__init__(account_number, holder_name, opening_balance)
        self.overdraft_limit = self._to_money(overdraft_limit)
        if self.overdraft_limit < 0:
            raise ValueError("Overdraft limit cannot be negative.")
    def withdraw(self, amount):
        amount = self._to_money(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Withdrawal exceeds the overdraft limit.")
        return self._deduct(amount)
