#!/usr/bin/env python2
#   -*- coding: utf-8 -*-
#

import numpy as np
import math
import random
import metropolis
import random_permutation as rm
import functools as ft

ABC = 'abcdefghijklmnopqrstuvwxyz'

PLAIN_TEXT_FILENAME = 'main/oliver_twist.txt'
TRAIN_TEXT_FILENAME = 'main/war_and_peace.txt'


def gen_key(seed=42):
    key = range(26)
    random.seed(seed)
    random.shuffle(key)
    return key


def read_text(filename):
    with open(filename, 'r') as f:
        text = ''.join(c for c in f.read() if c in ABC)
    return text


def quality(first, second):
    return sum(1 for a, b in zip(first, second) if a != b) / len(first)


def encrypt(plain_text, key=gen_key()):
    permutation = dict((ABC[i], ABC[key[i]]) for i in xrange(26))
    return ''.join(permutation[c] for c in plain_text)


def get_statistics(text):
    stat = dict((a + b, 0.0) for a in ABC for b in ABC)
    length = len(text)
    for i in xrange(0, length / 2, 2):
        letter = text[2 * i: 2 * (i + 1)]
        stat[letter] += 1.0 / (length / 2.0)
    return stat


def get_pdf(key, text, stat):
    likelihood = 0.0
    length = len(text)
    mapping = dict((ABC[i] + ABC[j], ABC[key[i]] + ABC[key[j]])
                   for i in xrange(26) for j in xrange(26))
    for i in xrange(0, length / 2, 2):
        letter = text[2 * i: 2 * (i + 1)]
        freq = stat[mapping[letter]]
        likelihood += math.log(freq) if freq > 0.0 else float('-inf')
    return likelihood


def test():
    key = gen_key()
    print('[INF] Permutation: ', key)
    plain_text = read_text(PLAIN_TEXT_FILENAME)
    train_text = read_text(TRAIN_TEXT_FILENAME)
    cipher_text = encrypt(plain_text, key)
    print('[INF] Texts are read and encrypted.')
    stat = get_statistics(train_text)
    sample = metropolis.metropolis(
        desiredPDF=ft.partial(get_pdf, text=cipher_text, stat=stat),
        initValue=rm.uniform(26),
        computableRVS=lambda t: rm.applyedTranspostions(t))
    print('[INF] Initialization')
    x = sample.next()[0]
    print('[INF] Sampling...')
    x = [sample.next()[0] for i in xrange(9)]
    for i in x:
        print i
    per = x[0]
    for i in xrange(len(per)):
        print (ord('a') + i) == (ord('a') + per[key[i]])

if __name__ == '__main__':
    test()