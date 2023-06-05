import os
import requests
import codecs
import ecdsa
import hashlib
from colorama import Fore, Style, init
import concurrent.futures


API_KEY = 'API KEY HERE'
MAX_WORKERS = 1
ENABLE_BALANCE_SCANNING = True
ENABLE_TRANSACTION_COUNT_SCANNING = False

init(autoreset=True)

def checksum_encode(addr_str): # Takes a hex (string) address as input
    out = ''
    addr = addr_str.lower().replace('0x', '')
    hash_addr = hashlib.sha3_256(addr.encode('ascii')).hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

def privToAddr(priv):
    priv = bytes.fromhex(priv)
    pub = '04' + ecdsa.SigningKey.from_string(priv, curve=ecdsa.SECP256k1).get_verifying_key().to_string().hex()
    address = hashlib.sha3_256(bytes.fromhex(pub)).hexdigest()[24:]
    return checksum_encode(address)

def get_balance_and_tx_status(address):
    balance = 0
    tx_status = False
    tx_status_display = 'Transactions scanning disabled'

    if ENABLE_BALANCE_SCANNING:
        # Get balance
        balance_url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}'
        balance_response = requests.get(balance_url).json()
        balance = int(balance_response['result']) / 1e18

    if ENABLE_TRANSACTION_COUNT_SCANNING:
        # Get transaction status
        tx_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={API_KEY}'
        tx_response = requests.get(tx_url).json()
        tx_status = tx_response['status'] == '1'

        # For display, we'll use the message from the API response
        tx_status_display = tx_response['message']

    return balance, tx_status, tx_status_display

def check_address_and_generate_keys():
    address = 'TEST WITH YOUR OWN WALLET ADDRESS'
    balance, tx_status, tx_status_display = get_balance_and_tx_status(address)
    print(f'Ethereum Address: {address}\nBalance: {balance} ETH\nTransaction Status: {tx_status_display}')
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while True:
            priv_keys = [os.urandom(32).hex() for _ in range(4)]
            futures = [executor.submit(get_balance_and_tx_status, privToAddr(priv_key)) for priv_key in priv_keys]
            for future, priv_key in zip(futures, priv_keys):
                balance, tx_status, tx_status_display = future.result()
                address = privToAddr(priv_key)
                if tx_status:
                    print(f'{Fore.GREEN}Private Key: {priv_key}\nEthereum Address: {address}\nBalance: {balance} ETH\nTransaction Status: {tx_status_display}')
                    with open('balances.txt', 'a') as f:
                        f.write(f'Private Key: {priv_key}\nEthereum Address: {address}\nBalance: {balance} ETH\nTransaction Status: {tx_status_display}\n\n')
                    break
                else:
                    print(f'Private Key: {priv_key}\nEthereum Address: {address}\nBalance: {balance} ETH\nTransaction Status: {tx_status_display}')

check_address_and_generate_keys()
