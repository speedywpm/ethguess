# Ethereum Wallet Scanner

This Python script is designed to generate Ethereum private keys, compute the corresponding public addresses, and check for the Ethereum balance and transaction status of each generated address. It uses the Etherscan API for balance and transaction queries.

## Dependencies

This script requires Python 3 and the following libraries:

- `os`
- `requests`
- `codecs`
- `ecdsa`
- `hashlib`
- `colorama`
- `concurrent.futures`

These dependencies can be installed using pip:
```
pip install requests ecdsa colorama
```

## Configuration

The script can be customized by modifying the following variables at the top of the script:

- `API_KEY`: This is your Etherscan API key. You need to [register an account on Etherscan](https://etherscan.io/register) and generate an API key.

- `MAX_WORKERS`: This controls the number of worker threads that the script will use for making requests to Etherscan.

- `ENABLE_BALANCE_SCANNING`: Set this to `True` to enable balance scanning, or `False` to disable it.

- `ENABLE_TRANSACTION_COUNT_SCANNING`: Set this to `True` to enable transaction scanning, or `False` to disable it.

## Usage

1. Customize the script by setting your Etherscan API key and other configuration variables as described above.
2. Run the script: `python3 ethguess.py`
3. The script will continuously generate Ethereum private keys and corresponding addresses, and check each address for balance and transaction status.
4. If a non-zero balance or a transaction is found, the details of the private key and the corresponding address will be printed on the console and saved into a file named `balances.txt`.

## Note

Please respect the Etherscan API usage policy when using this script. Generating large numbers of Ethereum addresses and making large numbers of requests to Etherscan may be seen as unwanted behavior.

Also, it is important to note that this script is purely for educational purposes. It's practically infeasible to find an address with a balance by randomly generating private keys due to the vastness of the Ethereum address space.

## Disclaimer

The author of this script is not responsible for any misuse of this script. It is provided "as is" with no warranty of any kind, and it is the user's responsibility to comply with all applicable laws and regulations.
