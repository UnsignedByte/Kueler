import pickle
import re
import itertools

cmu = {}
normaltrans = {}

with open("dictionary/compileddict.txt", 'rb') as f:
    cmu = pickle.load(f)

with open("dictionary/compiledipa.txt", 'rb') as f:
    normaltrans = pickle.load(f)

with open("dictionary/dialect.txt", 'r') as f:
    dialect = dict((k, re.findall('/(.*?)/', v)) for (k, v) in list(itertools.zip_longest(*[iter([a.strip() for a in f.readlines()])] * 2, fillvalue="")))
    dialectrev = dict((v,k) for k in dialect for v in dialect[k])

with open("dictionary/dialect2.txt", 'r') as f:
    dialect2 = dict((k, re.findall('/(.*?)/', v)) for (k, v) in list(itertools.zip_longest(*[iter([a.strip() for a in f.readlines()])] * 2, fillvalue="")))
    dialectrev2 = dict((v,k) for k in dialect2 for v in dialect2[k])

mods = ['', 'Y', 'O', 'OY']

def translate(sentence):
    transsent = []
    for word in sentence.split():
        print(word)
        try:
            ud = re.sub(r'[a-zA-Z]+', lambda x:cmu[x.group().upper()][0], word)
            print(ud)
        except KeyError:
            ud = re.sub(r'(\w)\1+', r'\1\1', word).lower()
            for a in normaltrans:
                try:
                    ud = re.sub(a[0], a[1]+r'\1', ud)
                except Exception:
                    ud = re.sub(a[0], a[1], ud)
        transsent.append(ud)
    transsent = ' '.join(transsent)
    return (transsent,
            ' '.join(''.join(dialectrev[c]+mods[dialect[dialectrev[c]].index(c)] if c in dialectrev else c for c in x) for x in transsent.lower().split()),
            ' '.join(''.join(dialectrev2[c] if c in dialectrev2 else c for c in x) for x in transsent.lower().split())
            )

while True:
    print('\n\n'.join(translate(input())))
