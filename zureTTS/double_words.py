# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 16:28:56 2016

@author: vurga
"""

import sys

with open(sys.argv[1], 'r') as source:
    words = source.read().split()

new_words = []
for i, word in enumerate(words):
    if i % 2 == 0:
        new_words.append(word)
    else:
        new_words.append(word)
        new_words.append(word)

with open(sys.argv[2], 'w') as target:
    target.write(' '.join(new_words))
    