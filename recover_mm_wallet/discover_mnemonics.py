'''
Discover Mnemonics

Includes all the functions and information necessary to discover a mnemonic
    when there are words missing.

This will search for any number of missing words. WARNING: one or two words is
    reasonable, but the search space grows very rapidly.

Assumes a 13 word mnemonic.
'''
import os
import json
import binascii
import configparser

config = configparser.ConfigParser()
root_path = os.path.dirname(__file__)
config_fp = os.path.join(root_path, 'conf.ini')
config.readfp(open(config_fp))

words_filename = config.get("discover_mnemonics", "words_filepath")
words_filepath = os.path.join(root_path, words_filename)
words = json.load(open(words_filepath))

truncated_words_filename = config.get(
    "discover_mnemonics", "truncated_words_filepath")

truncated_words_filepath = os.path.join(root_path, truncated_words_filename)
truncated_words = json.load(open(truncated_words_filepath))

MNEMONIC_LENGTH = 13

wordset = {
    "words": words,
    "trunc_words": truncated_words,
    "prefix_len": 3
}


def mn_swap_endian_4byte(input_string):
    """
    Translated from mymonero.com

    :param input_string:
    :return: string
    """
    if len(input_string) != 8:
        raise Exception('Invalid input length: ')
    return input_string[6: 8] + input_string[4: 6] + input_string[2: 4] + input_string[0: 2]


def mn_get_checksum_index(words, prefix_len):
    """
    Translated from mymonero.com

    :param words: list of words used to generate the seed
    :param prefix_len:
    :return: index of the checksum word
    """
    trimmed_words = ""
    for word in words:
        trimmed_words += word[0: prefix_len]
    trimmed_words_bytes = bytearray(trimmed_words, 'utf-8')
    checksum = binascii.crc32(trimmed_words_bytes) % (1 << 32)
    index = checksum % len(words)
    return index


def mn_decode(mnemonic_word_list):
    """
    Takes a mnemonic and returns the seed that can be used to generate an address.
    Translated from mymonero.com with the option to use non english character sets removed.

    :param mnemonic: str
    :return: str
    """
    out = ''
    n = len(words)
    checksum_word = ''

    if len(mnemonic_word_list) < 12:
        raise Exception("You've entered too few words.")

    if (wordset["prefix_len"] == 0 and len(mnemonic_word_list) % 3 != 0) \
       or (wordset["prefix_len"] > 0 and len(mnemonic_word_list) % 3 == 2):
        raise Exception("You've entered too few words.")

    if wordset["prefix_len"] > 0 and (len(mnemonic_word_list) % 3 == 0):
        raise Exception(
            "You seem to be missing the last word in your private key.")

    if wordset["prefix_len"] > 0:
        checksum_word = mnemonic_word_list.pop()

    # Decode mnemonic
    for i in range(0, len(mnemonic_word_list), 3):
        if wordset["prefix_len"] == 0:
            w1 = wordset["words"].index(mnemonic_word_list[i])
            w2 = wordset["words"].index(mnemonic_word_list[i + 1])
            w3 = wordset["words"].index(mnemonic_word_list[i + 2])
        else:
            w1 = wordset["trunc_words"].index(
                mnemonic_word_list[i][0: wordset["prefix_len"]])
            w2 = wordset["trunc_words"].index(
                mnemonic_word_list[i + 1][0: wordset["prefix_len"]])
            w3 = wordset["trunc_words"].index(
                mnemonic_word_list[i + 2][0: wordset["prefix_len"]])

        if w1 == -1 or w2 == -1 or w3 == -1:
            raise Exception("invalid word in mnemonic")

        x = w1 + n * (((n - w1) + w2) % n) + n * n * (((n - w2) + w3) % n)

        if x % n != w1:
            raise Exception(
                'Something went wrong when decoding your private key.')

        out += mn_swap_endian_4byte(('0000000' + str(hex(x))[2:])[-8:])

    # Verify checksum
    if wordset["prefix_len"] > 0:
        checksum_index = mn_get_checksum_index(
            mnemonic_word_list, wordset["prefix_len"])
        expected_checksum_word = mnemonic_word_list[checksum_index]
        if expected_checksum_word[0: wordset["prefix_len"]] != checksum_word[0: wordset["prefix_len"]]:
            raise ValueError(
                "Your private key could not be verified.")
    return out


def get_complete_mnemonic(incomplete_mnemonic, assume_last=False):
    """
    Takes in a mnemonic of unknown length and yields complete mnemonics
        recursively.

    Works by iterating through each word in the word list and systematically
        placing it everywhere.

    :param mnemonic: list
    :return: list
    """
    missing_word_count = MNEMONIC_LENGTH - len(incomplete_mnemonic)

    if missing_word_count > 0:
        for word in words:
            if assume_last:
                updated_mnemonic = incomplete_mnemonic + [word]
                # Recursive Step to add more than one new word
                for new_mnemonic in get_complete_mnemonic(updated_mnemonic):
                    yield new_mnemonic
            else:
                for place in range(len(incomplete_mnemonic)):
                    updated_mnemonic = (
                        incomplete_mnemonic[:place]
                        + [word]
                        + incomplete_mnemonic[place:])

                    for new_mnemonic in get_complete_mnemonic(updated_mnemonic):
                        yield new_mnemonic
    else:
        yield incomplete_mnemonic
