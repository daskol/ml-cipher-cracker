#!/usr/bin/env python2

__author__ = 'danielTsky'
__version__ = '0.0'

from sys import argv

USAGE = """\
Encrypt and decrypt transposition ciphers.
Usage: {0:s} ([-e|--encrypt][-d|--decrypt]) <text> <key>"""
INF = '\x1b[34m[INF]\x1b[0m '
ERR = '\x1b[31m[ERR]\x1b[0m '
ABC = 'abcdefghijklmnopqrstuvwxyz'
ENCRYPT = True
DECRYPT = False


def usage(kill=True):
    print(USAGE.format(argv[0]))
    if kill:
        exit()


def check_key(key, abc=ABC):
    """
    Check that each character of key is in the alphabet.
    :param key:
    :param abc:
    :return:
    """
    if len(key) != len(abc):
        return False
    else:
        return False if 0 in map(lambda x: x in abc, key) else True


def inverse_key(key, abc=ABC):
    """
    Build inverse key from a key.
    :param key:
    :param abc:
    :return: inverse key.
    """
    permutation = dict(zip(key, abc))
    return ''.join(map(lambda c: permutation[c], abc))


def encrypt(msg, key=ABC, abc=ABC):
    """
    Encrypt message with passed key in an alphabet.
    :param msg: message to encrypt.
    :param key:
    :param abc: an alphabet.
    :return: cipher text.
    """
    permutation = dict(zip(abc, key))
    return ''.join(map(lambda c: permutation[c], msg))


def decrypt(cipher, key=ABC, abc=ABC):
    """
    Decrypt message with passed key in an alphabet. It is based on key inversion and encryption.
    :param cipher: cipher text.
    :param key:
    :param abc:
    :return: plain text.
    """
    inv_key = inverse_key(key, abc)
    return encrypt(cipher, inv_key, abc)


def main():
    if len(argv) == 3:
        mode, text, key = ENCRYPT, argv[1], argv[2]
    elif len(argv) == 4:
        mode = \
            ENCRYPT if argv[1] == '-e' or argv[1] == '--encrypt' else \
            DECRYPT if argv[1] == '-d' or argv[1] == '--decrypt' else None
        if mode is None:
            usage()
        text, key = argv[2], argv[3]
    else:
        usage()
    if not check_key(key):
        print(ERR + 'Permutation check: %s' % 'FAILED')
        usage()
    if mode == ENCRYPT:
        print(encrypt(text, key))
    elif mode == DECRYPT:
        print(decrypt(text, key))


if __name__ == '__main__':
    main()