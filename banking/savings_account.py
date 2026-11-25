from decimal import Decimal
from .account import Account
class SavingsAccount(Account):
    """Savings account: withdrawals cannot exceed the available balance."""
    def __init__(self, account_number, holder_name, opening_balance=0, interest_rate=0.02):
        super().__init__(account_number, holder_name, opening_balance)
        self.interest_rate = Decimal(str(interest_rate))
    def withdraw(self, amount):
        amount = self._to_money(amount)
        self._ensure_sufficient_funds(amount)
        return self._deduct(amount)
    def apply_interest(self):
        interest = (self.balance * self.interest_rate).quantize(Decimal("0.01"))
        if interest > 0:
            self._balance += interest
            self._record("INTEREST", interest, f"Rate: {self.interest_rate}")
        return interest
