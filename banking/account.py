from abc import ABC, abstractmethod
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
class Account(ABC):
    """Abstract base class for all bank account types."""
    def __init__(self, account_number: str, holder_name: str, opening_balance=0):
        if not holder_name.strip():
            raise ValueError("Account holder name cannot be empty.")
        self.account_number = account_number
        self.holder_name = holder_name.strip()
        self._balance = self._to_money(opening_balance)
        if self._balance < 0:
            raise ValueError("Opening balance cannot be negative.")
        self._transactions = []
        if self._balance > 0:
            self._record("OPENING_DEPOSIT", self._balance, "Opening balance")
    @staticmethod
    def _to_money(amount) -> Decimal:
        try:
            value = Decimal(str(amount)).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            raise ValueError("Enter a valid monetary amount.") from None
        if not value.is_finite():
            raise ValueError("Amount must be a finite number.")
        return value
    @property
    def balance(self) -> Decimal:
        """Read-only balance; changes must go through account operations."""
        return self._balance
    @property
    def transactions(self):
        return [dict(item) for item in self._transactions]
    def _record(self, transaction_type, amount, note=""):
        self._transactions.append({
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "type": transaction_type,
            "amount": str(self._to_money(amount)),
            "balance_after": str(self._balance),
            "note": note,
        })
    def deposit(self, amount):
        amount = self._to_money(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self._balance += amount
        self._record("DEPOSIT", amount)
        return self._balance
    @abstractmethod
    def withdraw(self, amount):
        """Withdraw funds according to the concrete account's rules."""
    def _deduct(self, amount, transaction_type="WITHDRAWAL", note=""):
        amount = self._to_money(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        self._balance -= amount
        self._record(transaction_type, amount, note)
        return self._balance
    def _ensure_sufficient_funds(self, amount):
        amount = self._to_money(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
    def to_dict(self):
        return {
            "account_type": self.__class__.__name__,
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "balance": str(self._balance),
            "transactions": self.transactions,
        }