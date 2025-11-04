// src/pages/Dashboard.jsx

import React, { useState } from 'react';
import { accounts as accountsData, transactions as transactionsData } from '../data';

function Dashboard() {
  const [accounts, setAccounts] = useState(accountsData);
  const [transactions, setTransactions] = useState(transactionsData);
  const [depositAmounts, setDepositAmounts] = useState({});
  const [withdrawAmounts, setWithdrawAmounts] = useState({});
  const [transactionFilters, setTransactionFilters] = useState({});

  const handleDeposit = (accountId) => {
    const amount = parseFloat(depositAmounts[accountId]);
    if (isNaN(amount) || amount <= 0) {
      alert('Please enter a valid positive number.');
      return;
    }
    setAccounts(prev => {
      const updatedAccounts = prev.map(acc =>
        acc.id === accountId ? { ...acc, balance: acc.balance + amount } : acc
      );
      console.log('Updated Accounts after Deposit:', updatedAccounts);
      return updatedAccounts;
    });
    setTransactions(prev => {
      const newTransaction = { id: prev.length + 1, accountId, type: 'Deposit', amount, date: new Date().toISOString().split('T')[0] };
      const updatedTransactions = [newTransaction, ...prev];
      console.log('Updated Transactions after Deposit:', updatedTransactions);
      return updatedTransactions;
    });
    setDepositAmounts(prev => ({ ...prev, [accountId]: '' }));
  };

  const handleWithdrawal = (accountId) => {
    const amount = parseFloat(withdrawAmounts[accountId]);
    if (isNaN(amount) || amount <= 0) {
      alert('Please enter a valid positive number.');
      return;
    }
    const account = accounts.find(acc => acc.id === accountId);
    if (!account || account.balance < amount) {
      alert('Insufficient balance.');
      return;
    }
    setAccounts(prev => {
      const updatedAccounts = prev.map(acc =>
        acc.id === accountId ? { ...acc, balance: acc.balance - amount } : acc
      );
      console.log('Updated Accounts after Withdrawal:', updatedAccounts);
      return updatedAccounts;
    });
    setTransactions(prev => {
      const newTransaction = { id: prev.length + 1, accountId, type: 'Withdrawal', amount, date: new Date().toISOString().split('T')[0] };
      const updatedTransactions = [newTransaction, ...prev];
      console.log('Updated Transactions after Withdrawal:', updatedTransactions);
      return updatedTransactions;
    });
    setWithdrawAmounts(prev => ({ ...prev, [accountId]: '' }));
  };

  return (
    <main>
      <h2>Welcome to Your Dashboard</h2>
      <div className="accounts">
        {accounts.map(acc => {
          const filter = transactionFilters[acc.id] || 'All';
          let accTransactions = transactions.filter(tx => tx.accountId === acc.id);
          if (filter !== 'All') {
            accTransactions = accTransactions.filter(tx => tx.type === filter);
          }
          accTransactions = accTransactions.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
          return (
            <div key={acc.id} className="account-card">
              <h3>{acc.name}</h3>
              <p>Account Number: {acc.number}</p>
              <p>Balance: ${acc.balance.toFixed(2)}</p>
              <div>
                <input
                  type="number"
                  placeholder="Deposit amount"
                  value={depositAmounts[acc.id] || ''}
                  onChange={e => setDepositAmounts(prev => ({ ...prev, [acc.id]: e.target.value }))}
                />
                <button onClick={() => handleDeposit(acc.id)}>Deposit</button>
              </div>
              <div>
                <input
                  type="number"
                  placeholder="Withdraw amount"
                  value={withdrawAmounts[acc.id] || ''}
                  onChange={e => setWithdrawAmounts(prev => ({ ...prev, [acc.id]: e.target.value }))}
                />
                <button onClick={() => handleWithdrawal(acc.id)}>Withdraw</button>
              </div>
              <div>
                <label htmlFor={`filter-${acc.id}`}>Filter Transactions: </label>
                <select
                  id={`filter-${acc.id}`}
                  value={filter}
                  onChange={e => setTransactionFilters(prev => ({ ...prev, [acc.id]: e.target.value }))}
                >
                  <option value="All">All</option>
                  <option value="Deposit">Deposit</option>
                  <option value="Withdrawal">Withdrawal</option>
                </select>
              </div>
              <h4>Transactions</h4>
              <ul>
                {accTransactions.length === 0 && <li>No transactions available.</li>}
                {accTransactions.map(tx => (
                  <li key={tx.id}>
                    <span>{tx.type}: ${tx.amount.toFixed(2)}</span>
                    <span className="date">{tx.date}</span>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </main>
  );
}

export default Dashboard;