# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:29:23 2016

Splits text into sentences.

Usage: python split_sents.py <input> <output>

@author: vurga
"""

import sys, re 
from nltk import tokenize

with open(sys.argv[1], 'r', errors='ignore') as target:
    text = target.read().lower()
with open(sys.argv[2], 'w'):
    pass
    
text = re.sub('"', '', text)
sents = tokenize.sent_tokenize(text)

for sent in sents:
    with open(sys.argv[2], 'a+') as target:
        target.write(sent + ' \n')