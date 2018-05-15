import pickle
import re
import itertools
import sys

thismodule = sys.modules[__name__]
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

with open("dictionary/kueler.txt", 'r') as f:
    kueler = dict((k, re.findall('/(.*?)/', v)) for (k, v) in list(itertools.zip_longest(*[iter([a.strip() for a in f.readlines()])] * 2, fillvalue="")))
    kuelerrev = dict((v,k) for k in kueler for v in kueler[k])

mods = ['', 'Y', 'O', 'OY']

def translate(sentence, f, t):
    return getattr(thismodule, f+t)(sentence)

def engipa(sentence):
    print("hello hello")
    def engipaword(word):
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
    transsent = re.sub(r'[\w\']+', lambda x:engipaword(x.group(0)), sentence)
    return transsent

def ipaeng(sentence):
    def ipawordeng(word):
        try:
            ud = cmurev[word]
        except KeyError:
            ud = untransre.sub(lambda x:revtrans[x.group(0)], word).upper()
        return ud
    transsent = re.sub(r'[\w]+', lambda x:ipawordeng(x.group(0)), sentence)
    return transsent

def kueleripa(sentence):
    return re.sub(r'[a-zA-Z](?:h|H)?', lambda x:(lambda k:(kueler[k][0] if k.isupper() else kueler[k.upper()][1]))(x.group(0)), sentence)

def ipakueler(sentence):
    print(sentence)
    return re.sub(r'[\w]', lambda x:(lambda c:kuelerrev[c].lower() if kueler[kuelerrev[c]].index(c)==1 else kuelerrev[c])(x.group(0)), sentence)

def kuelereng(sentence):
    return ipaeng(kueleripa(sentence))

def engkueler(sentence):
    return ipakueler(engipa(sentence))

while True:
    print(translate(input(), 'eng', 'kueler'))
