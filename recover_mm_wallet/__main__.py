import os
import sys
import configparser
import discover_mnemonics
from seeds_to_addresses import add_addresses_from_seeds
from check_wallets import update_addrs_with_account_info
import asyncio

config = configparser.ConfigParser()
root_path = os.path.dirname(__file__)
config_fp = os.path.join(root_path, 'conf.ini')
config.readfp(open(config_fp))

ASSUME_LAST = config.getboolean("discover_mnemonics", "ASSUME_LAST")
# ASSUME_ORDER = config.getboolean("discover_mnemonics", "ASSUME_ORDER")  # Not used at the moment

incomplete_mnemonic = sys.argv[1:]

len_to_complete = len(incomplete_mnemonic)
assert len_to_complete < 13
print(
    f"Attempting to complete {len_to_complete} words: {incomplete_mnemonic}")

possible_mnemonics = discover_mnemonics.get_complete_mnemonic(
    incomplete_mnemonic, ASSUME_LAST)


accounts_info = []
for test_mnemonic in possible_mnemonics:
    try:
        assert len(test_mnemonic) == 13
        seed = discover_mnemonics.mn_decode(test_mnemonic[:])
        addr_info = {
            'mnemonic': test_mnemonic,
            'seed': seed
        }
        accounts_info.append(addr_info)
    except ValueError as E:
        expected_error = "Your private key could not be verified."
        # This error comes up when the completed mnemonic is wrong but
        #   still in the correct form.
        # Any other error would need to be diagnosed
        if str(E) != expected_error:
            print(E)
            break

print(f"Discovered {len(accounts_info)} valid seeds!")

print("Converting Seeds to Addresses ...")
add_addresses_from_seeds(accounts_info)


print("Retrieving transaction information ...")
loop = asyncio.get_event_loop()
loop.run_until_complete(update_addrs_with_account_info(accounts_info))


print("Discovered Used Wallets:")
for account_info in accounts_info:
    if 'total_received' in account_info \
            and int(account_info["total_received"]) > 0:
        print("Mnemonic was used: ", " ".join(account_info['mnemonic']))
