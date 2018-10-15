"""
Check Wallets

Uses myMonero.com to check the
"""
import json
import asyncio
import aiohttp


mymonero_request_header = {
    'origin': 'https://mymonero.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'content-type': 'application/json;charset=UTF-8',
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://mymonero.com/',
    'authority': 'api.mymonero.com:8443',
}


def get_stored_mnemonic(index):
    with open("output/discovered_seeds.json", 'r') as seeds_fp:
        mnemonics = json.load(seeds_fp)
        return mnemonics[index]


def get_stored_keys():
    with open("output/myMoneroAddressKeySets.json", 'r') as addresses_fp:
        address_key_sets = json.load(addresses_fp)
    return address_key_sets


async def update_addr_with_account_info(address_info, session):
    public_addr = address_info['public_addr']
    view_key = address_info['view']['sec']
    data = '{"address":"%s","view_key":"%s"}' % (public_addr, view_key)
    url = 'https://api.mymonero.com:8443/get_address_info'

    async with session.post(url, headers=mymonero_request_header,
                            data=data) as response:
        try:
            transaction_info = await response.json()
            address_info.update(transaction_info)
        except KeyError as e:
            if response.status_code != 500:
                raise


async def update_addrs_with_account_info(addresses_info):
    coros = []
    async with aiohttp.ClientSession() as session:
        for addr_info in addresses_info:
            coros.append(update_addr_with_account_info(addr_info, session))

        await asyncio.gather(*coros)
