import itertools
import re
import pickle

dct = {}

oldword = ""
toipa = {}

with open("toipa.txt", 'r') as f:
    toipa = dict(itertools.zip_longest(*[iter([a.strip() for a in f.readlines()])] * 2, fillvalue=""))

with open("cmudict.txt", 'r') as f:
    for a in f.readlines():
        removesuff = re.compile('(?:\(|\)|\d)')
        splitted = [removesuff.sub('', x) for x in a.strip().split()]
        word = splitted.pop(0)
        pronunciation = [toipa[i] for i in splitted]
        if word == oldword:
            dct[word].append(''.join(pronunciation))
        else:
            dct[word] = [''.join(pronunciation)]
        oldword = word

with open('compileddict.txt', 'wb') as f:
    pickle.dump(dct, f)
