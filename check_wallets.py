"""
Check Wallets

Uses myMonero.com to check the
"""
import json
import requests


mymonero_request_header = {
    'origin': 'https://mymonero.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'content-type': 'application/json;charset=UTF-8',
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://mymonero.com/',
    'authority': 'api.mymonero.com:8443',
}


def lookup_address_on_my_monero(address, view_key):

    data = '{"address":"%s","view_key":"%s"}' % (address, view_key)
    resp = requests.post('https://api.mymonero.com:8443/get_address_info',
                         headers=mymonero_request_header, data=data)

    return resp


def get_stored_mnemonic(index):
    with open("output/discovered_seeds.json", 'r') as seeds_fp:
        mnemonics = json.load(seeds_fp)
        return mnemonics[index]


def get_stored_keys():
    with open("output/myMoneroAddressKeySets.json", 'r') as addresses_fp:
        address_key_sets = json.load(addresses_fp)
    return address_key_sets


if __name__ == "__main__":
    address_key_sets = get_stored_keys()

    for key_set_i, key_set in enumerate(address_key_sets):
        resp = lookup_address_on_my_monero(key_set[0], key_set[1])

        try:
            if int(json.loads(resp.content)["total_received"]) > 0:
                print("Discovered Used Wallet")
                print("Key Set:", key_set)
                print("Mnemonic to use: ", get_stored_mnemonic(key_set_i))
        except KeyError as e:
            if resp.status_code == 500:
                pass
            else:
                print("Last keyset tried: ", key_set_i, key_set)
                raise
