import os
import struct
import hashlib
import ecdsa
import requests

API_URL = "https://blockchain.info/q/addressbalance/"

def check_balance(address):
    try:
        response = requests.get(API_URL + address)
        if response.status_code == 200:
            return int(response.text)
        else:
            return 0
    except:
        return 0

def privkey_to_wif(privkey):
    extended_key = b"\x80" + privkey
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    return base58_encode(extended_key + checksum)

def base58_encode(data):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    count = 0
    for byte in data:
        if byte == 0:
            count += 1
        else:
            break
    num = int.from_bytes(data, 'big')
    encoded = ''
    while num > 0:
        num, mod = divmod(num, 58)
        encoded = alphabet[mod] + encoded
    return '1' * count + encoded

def extract_keys_from_dat(dat_file_path):
    with open(dat_file_path, "rb") as f:
        data = f.read()
    
    private_keys = []
    for i in range(len(data) - 32):
        chunk = data[i:i+32]
        if len(chunk) == 32:
            privkey = chunk
            private_keys.append(privkey)
    return private_keys

def main():
    wallet_dat = "/storage/emulated/0/Download/read_dat"
    
    private_keys = extract_keys_from_dat(wallet_dat)
    
    for privkey in private_keys:
        # Convert private key to Wallet Import Format (WIF)
        wif_key = privkey_to_wif(privkey)

        # Check balance of the address
        balance = check_balance(wif_key)

        if balance > 0:
            # Blue for valid keys with a balance
            print(f"\033[34mPrivate Key: {wif_key} has balance: {balance} satoshis\033[0m")
        elif is_valid_key(wif_key):
            # Green for valid keys
            print(f"\033[32mPrivate Key: {wif_key} is valid but has no balance.\033[0m")
        else:
            # Red for invalid keys
            print(f"\033[31mPrivate Key: {wif_key} is invalid.\033[0m")

def is_valid_key(wif_key):
    # Check if the private key WIF is valid
    return wif_key.startswith('5') or wif_key.startswith('K') or wif_key.startswith('L')

if __name__ == '__main__':
    main()
