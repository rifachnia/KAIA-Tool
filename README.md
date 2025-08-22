## 💸 send.py — Bulk KAIA Transfer Script

This script automates sending all available KAIA from multiple wallets to a single destination address.

### 🔹 Features
- Reads multiple private keys from `privkeys.txt`
- Calculates available balance and subtracts gas fees
- Sends the **entire balance** to a predefined recipient
- Uses **EIP-1559 gas fee mechanism** for Kaia chain

### 🔹 Usage
1. Prepare a `privkeys.txt` file in the same folder:  
