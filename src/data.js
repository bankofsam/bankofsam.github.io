export const accounts = [
  { id: 1, name: "Checking Account", number: "123456789", balance: 1500.00 },
  { id: 2, name: "Savings Account", number: "987654321", balance: 3000.00 },
  { id: 3, name: "Crypto Wallet", number: "987654", balance: 3.72 }
];

export const transactions = [
  { id: 1, accountId: 1, type: "Deposit", amount: 500.00, date: "2025-11-01" },
  { id: 2, accountId: 1, type: "Withdrawal", amount: 200.00, date: "2025-11-02" },
  { id: 3, accountId: 2, type: "Deposit", amount: 1000.00, date: "2025-10-30" },
  { id: 4, accountId: 3, type: "Crypto Purchase", amount: 1.2, date: "2025-10-29" }
];