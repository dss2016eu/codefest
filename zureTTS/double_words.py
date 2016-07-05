# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 16:28:56 2016

Doubles every second word.
Usage: double_words.py <input> <output> [sentence_marker, default=<s>]

@author: vurga
"""

import sys

with open(sys.argv[1], 'r') as source:
    words = source.read().split()
    
if len(sys.argv) == 4:  
    sentence_marker = sys.argv[3]
else:
    sentence_marker = '<s>'
    
new_words = [sentence_marker, words[0]]
for word in words[1:-1]:
    new_words.append(word)
    new_words.append(word)
new_words.append(words[-1])
new_words.append(sentence_marker)

with open(sys.argv[2], 'w') as target:
    target.write(' '.join(new_words))
    