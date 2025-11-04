import React, { useState } from 'react';
import { accounts as initialAccounts, transactions as initialTransactions } from "./data";

function Dashboard() {
  const [accounts, setAccounts] = useState(initialAccounts);
  const [transactions, setTransactions] = useState(initialTransactions);

  const handleDeposit = (accountId) => {
    const amountStr = prompt('Enter deposit amount:');
    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) {
      alert('Invalid amount entered.');
      return;
    }
    setAccounts(prevAccounts =>
      prevAccounts.map(account =>
        account.id === accountId
          ? { ...account, balance: account.balance + amount }
          : account
      )
    );
    setTransactions(prevTransactions => [
      ...prevTransactions,
      {
        id: prevTransactions.length + 1,
        accountId,
        type: 'deposit',
        amount,
        date: new Date().toISOString(),
      },
    ]);
  };

  const handleWithdrawal = (accountId) => {
    const amountStr = prompt('Enter withdrawal amount:');
    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) {
      alert('Invalid amount entered.');
      return;
    }
    const account = accounts.find(acc => acc.id === accountId);
    if (!account) {
      alert('Account not found.');
      return;
    }
    if (account.balance < amount) {
      alert('Insufficient funds.');
      return;
    }
    setAccounts(prevAccounts =>
      prevAccounts.map(account =>
        account.id === accountId
          ? { ...account, balance: account.balance - amount }
          : account
      )
    );
    setTransactions(prevTransactions => [
      ...prevTransactions,
      {
        id: prevTransactions.length + 1,
        accountId,
        type: 'withdrawal',
        amount,
        date: new Date().toISOString(),
      },
    ]);
  };

  return (
    <div>
      <h1>Dashboard</h1>
      {accounts.map(account => (
        <div key={account.id} style={{ border: '1px solid black', margin: '10px', padding: '10px' }}>
          <h2>{account.name}</h2>
          <p>Balance: ${account.balance.toFixed(2)}</p>
          <button onClick={() => handleDeposit(account.id)}>Deposit</button>
          <button onClick={() => handleWithdrawal(account.id)}>Withdraw</button>
          <h3>Transactions</h3>
          <ul>
            {transactions
              .filter(tx => tx.accountId === account.id)
              .map(tx => (
                <li key={tx.id}>
                  {tx.type.charAt(0).toUpperCase() + tx.type.slice(1)} of ${tx.amount.toFixed(2)} on {new Date(tx.date).toLocaleString()}
                </li>
              ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default Dashboard;