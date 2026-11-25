import tempfile
import unittest
from pathlib import Path
from banking import Bank
from banking.storage import JSONStorage
from banking.account import Account
from banking.savings_account import SavingsAccount
from banking.current_account import CurrentAccount
class BankingSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.bank = Bank(JSONStorage(Path(self.temp_dir.name) / "bank.json"))
    def tearDown(self):
        self.temp_dir.cleanup()
    def test_create_savings_account(self):
        account = self.bank.create_account("savings", "Asha", "500")
        self.assertIsInstance(account, SavingsAccount)
        self.assertEqual(account.balance, 500)
    def test_deposit_and_withdraw(self):
        account = self.bank.create_account("savings", "Ravi", "100")
        account.deposit("50")
        account.withdraw("25")
        self.assertEqual(account.balance, 125)
    def test_savings_cannot_overdraw(self):
        account = self.bank.create_account("savings", "Maya", "100")
        with self.assertRaises(ValueError):
            account.withdraw("101")
    def test_current_account_overdraft(self):
        account = self.bank.create_account("current", "Dev", "100")
        account.withdraw("500")
        self.assertEqual(account.balance, -400)
    def test_transfer_and_history(self):
        first = self.bank.create_account("savings", "A", "300")
        second = self.bank.create_account("savings", "B", "50")
        self.bank.transfer(first.account_number, second.account_number, "75")
        self.assertEqual(first.balance, 225)
        self.assertEqual(second.balance, 125)
        self.assertEqual(first.transactions[-1]["type"], "TRANSFER_OUT")
        self.assertEqual(second.transactions[-1]["type"], "TRANSFER_IN")
    def test_persistence_after_reload(self):
        account = self.bank.create_account("savings", "Persist", "200")
        account.deposit("10")
        self.bank._save()
        reloaded = Bank(JSONStorage(Path(self.temp_dir.name) / "bank.json"))
        self.assertEqual(reloaded.get_account(account.account_number).balance, 210)
    def test_invalid_deposit(self):
        account = self.bank.create_account("savings", "Test", "0")
        with self.assertRaises(ValueError):
            account.deposit("-1")
    def test_abstract_account(self):
        with self.assertRaises(TypeError):
            Account("1", "Abstract", 0)
if __name__ == "__main__":
    unittest.main()
