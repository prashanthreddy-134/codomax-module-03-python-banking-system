from decimal import Decimal
from .savings_account import SavingsAccount
from .current_account import CurrentAccount
class Bank:
    """Coordinates account creation, lookup, transfers, and persistence."""
    ACCOUNT_TYPES = {
        "savings": SavingsAccount,
        "current": CurrentAccount,
    }
    def __init__(self, storage):
        self.storage = storage
        self.accounts = {}
        self._next_account_number = 1001
        self._load()
    def _load(self):
        data = self.storage.load()
        self._next_account_number = int(data.get("next_account_number", 1001))
        for item in data.get("accounts", []):
            cls = self.ACCOUNT_TYPES.get(item.get("account_type", "").replace("Account", "").lower())
            # Accept the stored concrete class names.
            if cls is None:
                cls = SavingsAccount if item.get("account_type") == "SavingsAccount" else CurrentAccount
            account = cls(item["account_number"], item["holder_name"], 0)
            account._balance = Decimal(item["balance"])
            account._transactions = list(item.get("transactions", []))
            if isinstance(account, SavingsAccount):
                account.interest_rate = Decimal(item.get("interest_rate", "0.02"))
            else:
                account.overdraft_limit = Decimal(item.get("overdraft_limit", "1000.00"))
            self.accounts[account.account_number] = account

    def _save(self):
        records = []
        for account in self.accounts.values():
            record = account.to_dict()
            if isinstance(account, SavingsAccount):
                record["interest_rate"] = str(account.interest_rate)
            else:
                record["overdraft_limit"] = str(account.overdraft_limit)
            records.append(record)
        self.storage.save({
            "next_account_number": self._next_account_number,
            "accounts": records,
        })
    def create_account(self, account_type, holder_name, opening_balance=0):
        account_type = account_type.lower().strip()
        if account_type not in self.ACCOUNT_TYPES:
            raise ValueError("Account type must be 'savings' or 'current'.")
        number = str(self._next_account_number)
        account = self.ACCOUNT_TYPES[account_type](number, holder_name, opening_balance)
        self.accounts[number] = account
        self._next_account_number += 1
        self._save()
        return account
    def get_account(self, account_number):
        try:
            return self.accounts[str(account_number)]
        except KeyError:
            raise ValueError("Account not found.") from None
    def transfer(self, from_number, to_number, amount):
        source = self.get_account(from_number)
        destination = self.get_account(to_number)
        amount = source._to_money(amount)
        if source.account_number == destination.account_number:
            raise ValueError("Cannot transfer to the same account.")
        # Validate destination and source before changing either balance.
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")
        if isinstance(source, SavingsAccount):
            source._ensure_sufficient_funds(amount)
        elif amount > source.balance + source.overdraft_limit:
            raise ValueError("Transfer exceeds the overdraft limit.")
        source._deduct(amount, "TRANSFER_OUT", f"To account {destination.account_number}")
        destination.deposit(amount)
        destination._transactions[-1]["type"] = "TRANSFER_IN"
        destination._transactions[-1]["note"] = f"From account {source.account_number}"
        self._save()
        return True
    def list_accounts(self):
        return list(self.accounts.values())
