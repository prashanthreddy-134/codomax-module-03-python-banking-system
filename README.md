# Python Banking System — Codomax Module 03

An educational command-line banking application demonstrating Object-Oriented Programming (OOP) in Python.

## Features
- Create savings and current accounts
- Deposit and withdraw funds with validation
- Transfer funds between accounts
- View account details and transaction history
- Persist account and transaction data in JSON
- Encapsulated account balance with controlled operations
- Inheritance (`SavingsAccount`, `CurrentAccount`)
- Polymorphism through account-specific withdrawal rules
- Abstraction through the `Account` abstract base class
- Unit tests using Python's built-in `unittest`

> This is a learning project, not production banking software. It does not connect to real banks, process real money, provide authentication, or implement regulatory/security controls.

## Requirements
- Python 3.10 or later
- No third-party packages required

## Run
Open a terminal in the `student_banking_system` folder:

```bash
python main.py
```

Data is saved automatically to `data/bank_data.json`.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Project structure
```text
student_banking_system/
├── banking/
│   ├── __init__.py
│   ├── account.py
│   ├── savings_account.py
│   ├── current_account.py
│   ├── bank.py
│   └── storage.py
├── data/
│   └── .gitkeep
├── docs/
│   ├── OOP_DESIGN.md
│   └── class_diagram.mmd
├── tests/
│   └── test_banking.py
├── main.py
├── requirements.txt
└── README.md
```

## Example workflow
1. Create an account and note its generated account number.
2. Deposit money.
3. Withdraw money (subject to account rules).
4. Transfer money to another account.
5. View transaction history.
6. Exit; data remains in the JSON file for the next run.

## Design notes
See [`docs/OOP_DESIGN.md`](docs/OOP_DESIGN.md) and [`docs/class_diagram.mmd`](docs/class_diagram.mmd).
