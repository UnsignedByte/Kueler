import pickle
import re
import itertools

cmu = {}
cmurev = {}
normaltrans = []
revtrans = []
untransre = None

with open("dictionary/compileddict.txt", 'rb') as f:
    cmu = pickle.load(f)
with open("dictionary/compileddictrev.txt", 'rb') as f:
    cmurev = pickle.load(f)

with open("dictionary/compiledipa.txt", 'rb') as f:
    normaltrans = pickle.load(f)
with open("dictionary/compiledeng.txt", 'rb') as f:
    revtrans = pickle.load(f)
    untransre = re.compile('|'.join(k for (k,v) in revtrans))
    revtrans = dict(revtrans)

with open("dictionary/dialect.txt", 'r') as f:
    dialect = dict((k, re.findall('/(.*?)/', v)) for (k, v) in list(itertools.zip_longest(*[iter([a.strip() for a in f.readlines()])] * 2, fillvalue="")))
    dialectrev = dict((v,k) for k in dialect for v in dialect[k])

with open("dictionary/dialect2.txt", 'r') as f:
    dialect2 = dict((k, re.findall('/(.*?)/', v)) for (k, v) in list(itertools.zip_longest(*[iter([a.strip() for a in f.readlines()])] * 2, fillvalue="")))
    dialectrev2 = dict((v,k) for k in dialect2 for v in dialect2[k])

mods = ['', 'Y', 'O', 'OY']

def transword(word):
    try:
        ud = cmu[word.upper()][0]
    except KeyError:
        ud = re.sub(r'(\w)\1+', r'\1\1', word).lower()
        for a in normaltrans:
            try:
                ud = re.sub(a[0], a[1]+r'\1', ud)
            except Exception:
                ud = re.sub(a[0], a[1], ud)
    return ud

def translate(sentence):
    transsent = re.sub(r'[\w\']+', lambda x:transword(x.group(0)), sentence)
    return (transsent,
            untranslate(transsent),
            ' '.join(''.join(dialectrev[c]+mods[dialect[dialectrev[c]].index(c)] if c in dialectrev else c for c in x) for x in transsent.lower().split()),
            ' '.join(''.join((dialectrev2[c].lower() if dialect[dialectrev[c]].index(c)==1 else dialectrev2[c]) if c in dialectrev2 else c for c in x) for x in transsent.lower().split())
            )

def untransword(word):
    try:
        ud = cmurev[word]
    except KeyError:
        ud = untransre.sub(lambda x:revtrans[x.group(0)], word).upper()
    return ud

def untranslate(sentence):
    transsent = re.sub(r'[^\.,\?!\'\":;\-–—\s-]+', lambda x:untransword(x.group(0)), sentence)
    return transsent

while True:
    print('\n\n'.join(translate(input())))
