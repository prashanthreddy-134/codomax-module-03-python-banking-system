from pathlib import Path
from banking import Bank
from banking.storage import JSONStorage
def money(value):
    return f"₹{value:,.2f}"
def show_account(account):
    print(f"\nAccount number : {account.account_number}")
    print(f"Holder name    : {account.holder_name}")
    print(f"Account type   : {account.__class__.__name__}")
    print(f"Balance        : {money(account.balance)}")
    if hasattr(account, "overdraft_limit"):
        print(f"Overdraft limit: {money(account.overdraft_limit)}")
def show_history(account):
    print(f"\nTransaction history — {account.account_number}")
    if not account.transactions:
        print("No transactions found.")
        return
    for tx in account.transactions:
        print(f"{tx['timestamp']} | {tx['type']:<14} | ₹{DecimalDisplay(tx['amount']):>10} | {tx['note']}")
def DecimalDisplay(value):
    return f"{float(value):,.2f}"
def main():
    data_file = Path(__file__).parent / "data" / "bank_data.json"
    bank = Bank(JSONStorage(data_file))
    actions = {
        "1": "Create account",
        "2": "Deposit",
        "3": "Withdraw",
        "4": "Transfer",
        "5": "View account",
        "6": "Transaction history",
        "7": "List accounts",
        "8": "Apply savings interest",
        "0": "Exit",
    }
    while True:
        print("\n====== STUDENT BANKING SYSTEM ======")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                name = input("Account holder name: ").strip()
                kind = input("Account type (savings/current): ").strip().lower()
                opening = input("Opening deposit (default 0): ").strip() or "0"
                account = bank.create_account(kind, name, opening)
                print(f"Account created. Your account number is {account.account_number}")
            elif choice == "2":
                account = bank.get_account(input("Account number: ").strip())
                account.deposit(input("Deposit amount: ").strip())
                bank._save()
                print(f"Deposit successful. New balance: {money(account.balance)}")
            elif choice == "3":
                account = bank.get_account(input("Account number: ").strip())
                account.withdraw(input("Withdrawal amount: ").strip())
                bank._save()
                print(f"Withdrawal successful. New balance: {money(account.balance)}")
            elif choice == "4":
                source = input("From account: ").strip()
                destination = input("To account: ").strip()
                amount = input("Transfer amount: ").strip()
                bank.transfer(source, destination, amount)
                print("Transfer completed.")
            elif choice == "5":
                show_account(bank.get_account(input("Account number: ").strip()))
            elif choice == "6":
                show_history(bank.get_account(input("Account number: ").strip()))
            elif choice == "7":
                accounts = bank.list_accounts()
                if not accounts:
                    print("No accounts have been created.")
                for account in accounts:
                    print(f"{account.account_number} | {account.holder_name} | {account.__class__.__name__} | {money(account.balance)}")
            elif choice == "8":
                account = bank.get_account(input("Savings account number: ").strip())
                if not hasattr(account, "apply_interest"):
                    print("Interest can only be applied to a savings account.")
                else:
                    interest = account.apply_interest()
                    bank._save()
                    print(f"Interest added: {money(interest)}")
            elif choice == "0":
                print("Thank you for using the Student Banking System.")
                break
            else:
                print("Invalid option. Choose a listed number.")
        except (ValueError, RuntimeError) as exc:
            print(f"Error: {exc}")
if __name__ == "__main__":
    main()
