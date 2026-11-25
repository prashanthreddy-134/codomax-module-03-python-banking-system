# OOP Application Design — Student Banking System

## 1. Purpose and scope
This command-line application models a small educational bank. It supports account creation, deposits, withdrawals, transfers, account lookup, and transaction history. Data is persisted locally in JSON.

It is a demonstration of OOP concepts, not a real financial product.

## 2. OOP concepts demonstrated

| Concept | Implementation |
|---|---|
| Class and object | `Bank`, `SavingsAccount`, `CurrentAccount`; each created account is an object |
| Constructor | `__init__` initializes account identity, balance, rules, and transaction list |
| Encapsulation | `Account._balance` is internal; `balance` is a read-only property; balance changes occur through methods |
| Inheritance | `SavingsAccount` and `CurrentAccount` inherit from abstract `Account` |
| Polymorphism | Both subclasses implement `withdraw()` with different rules |
| Abstraction | `Account` is an abstract base class and declares abstract `withdraw()` |
| Composition | `Bank` owns/manages account objects; it uses `JSONStorage` for persistence |
| Single responsibility | Storage, account rules, bank coordination, and CLI are separated into modules |

## 3. Main classes

### Account (abstract)
Common account identity, private-by-convention balance, transaction history, deposit, serialization, and shared validation. It requires subclasses to implement `withdraw()`.

### SavingsAccount
Inherits `Account`. Withdrawals cannot exceed the available balance. Includes a simple interest operation.

### CurrentAccount
Inherits `Account`. Allows withdrawals up to the configured overdraft limit.

### Bank
Creates accounts, allocates account numbers, retrieves accounts, lists accounts, transfers funds, and coordinates saving/loading.

### JSONStorage
Loads and saves the bank's data document. It writes to a temporary file and replaces the data file to reduce the risk of partially written JSON.

## 4. Transaction flow

1. CLI collects user input.
2. `Bank` locates the account.
3. The account validates the amount and its account-specific rule.
4. The account changes its balance and appends a transaction record.
5. `Bank` persists the updated state through `JSONStorage`.

For a transfer, the source and destination are validated before balances are changed. The source is debited and the destination credited, then the updated bank state is saved.

## 5. Clean-code choices
- Descriptive class and method names.
- Type-focused modules and clear responsibility boundaries.
- `Decimal` is used for money rather than binary floating-point arithmetic.
- Validation is centralized in the account base class where possible.
- Errors are raised as `ValueError` and handled at the CLI boundary.
- Unit tests cover core behavior, rules, transfer, and persistence.

## 6. Limitations
- No login, authentication, authorization, encryption, audit-grade ledger, concurrency control, database transactions, or real bank integration.
- JSON is suitable for a small local learning exercise only.
- Account numbers are sequential and are not secure identifiers.
- The sample interest rate and overdraft limit are educational defaults.
