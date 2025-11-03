// --- BANK OF SAM ---

// Initialize balance from localStorage
let balance = parseInt(localStorage.getItem('samBalance')) || 100;

// Display balance on page
const balanceElement = document.getElementById('balance');
balanceElement.textContent = `💵 ${balance} Sam Bucks`;

// Function to update balance
function updateBalance(amountChange) {
  balance += amountChange;
  localStorage.setItem('samBalance', balance);
  balanceElement.textContent = `💵 ${balance} Sam Bucks`;
}

// “Send Sam Bucks” button
document.getElementById('sendBtn').addEventListener('click', () => {
  const amount = parseInt(prompt("How many Sam Bucks would you like to send?"));
  if (!isNaN(amount) && amount > 0 && balance >= amount) {
    updateBalance(-amount);
    alert(`💸 Sent ${amount} Sam Bucks! New balance: ${balance}`);
  } else {
    alert("❌ Invalid or insufficient balance.");
  }
});

// “Deposit Sam Bucks” button
document.getElementById('depositBtn').addEventListener('click', () => {
  const amount = parseInt(prompt("How many Sam Bucks would you like to deposit?"));
  if (!isNaN(amount) && amount > 0) {
    updateBalance(amount);
    alert(`✅ Deposited ${amount} Sam Bucks! New balance: ${balance}`);
  }
});
