from web3 import Web3
from eth_account import Account

# 🔹 Konfigurasi RPC Kaia Chain
KAIA_RPC = "https://public-en.node.kaia.io"
web3 = Web3(Web3.HTTPProvider(KAIA_RPC))

# 🔹 Alamat tujuan (ubah ke format checksum)
recipient_address = web3.to_checksum_address("YOUR_ADDRESS_HERE")

# 🔹 Konfigurasi gas (gunakan EIP-1559)
BASE_FEE = web3.eth.fee_history(1, "latest")["baseFeePerGas"][-1]  # Ambil base fee terbaru
MAX_PRIORITY_FEE = web3.to_wei(2, "gwei")  # Bisa disesuaikan
MAX_FEE = BASE_FEE + MAX_PRIORITY_FEE  # Total fee

GAS_LIMIT = 21000  # Transaksi standar

def send_all_kaia(private_key):
    account = Account.from_key(private_key)
    wallet_address = account.address

    # 🔹 Cek saldo wallet
    balance = web3.eth.get_balance(wallet_address)
    if balance == 0:
        print(f"❌ {wallet_address} | No balance.")
        return

    # 🔹 Hitung jumlah KAIA yang bisa dikirim setelah dikurangi gas fee
    gas_fee = GAS_LIMIT * MAX_FEE
    if balance <= gas_fee:
        print(f"❌ {wallet_address} | Saldo tidak cukup untuk gas fee.")
        return

    send_amount = balance - gas_fee  # Sisa saldo setelah dikurangi gas fee

    # 🔹 Buat transaksi (EIP-1559)
    txn = {
        'to': recipient_address,  # ✅ Format checksum
        'value': send_amount,
        'gas': GAS_LIMIT,
        'maxFeePerGas': MAX_FEE,
        'maxPriorityFeePerGas': MAX_PRIORITY_FEE,
        'nonce': web3.eth.get_transaction_count(wallet_address),
        'chainId': 8217  # ✅ Chain ID Kaia
    }

    # 🔹 Tanda tangani transaksi
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(f"✅ {wallet_address} | Sent {web3.from_wei(send_amount, 'ether')} KAIA | Tx: {txn_hash.hex()}")

# 🔹 Daftar private key (baca dari file `pvkey.txt`)
with open("privkeys.txt", "r") as file:
    private_keys = file.read().splitlines()

for pvkey in private_keys:
    send_all_kaia(pvkey)
