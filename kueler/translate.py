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
normtransre = re.compile(r'(m|n|ŋ|p|t|k|b|d|ɡ|f|θ|s|ʃ|x|h|v|ð|z|ʒ|l|ɹ|j|w|ɪ|i|ʊ|u|e|ə|ɜ|ɔ|a|ɛ|æ|ʌ|ɒ|ɑ)')

with open("data/dictionary/compileddict.txt", 'rb') as f:
    cmu = pickle.load(f)
with open("data/dictionary/compileddictrev.txt", 'rb') as f:
    cmurev = pickle.load(f)

with open("data/dictionary/compiledipa.txt", 'rb') as f:
    normaltrans = pickle.load(f)
with open("data/dictionary/compiledeng.txt", 'rb') as f:
    revtrans = pickle.load(f)
    untransre = re.compile('|'.join(k for (k,v) in revtrans))
    revtrans = dict(revtrans)

with open("data/dictionary/kueler.txt", 'r') as f:
    kueler = dict((k, re.findall('/(.*?)/', v)) for (k, v) in list(itertools.zip_longest(*[iter([a.strip() for a in f.readlines()])] * 2, fillvalue="")))
    kuelerrev = dict((v,k) for k in kueler for v in kueler[k])

mods = ['', 'Y', 'O', 'OY']
def translate(sentence, f, t):
    return getattr(thismodule, f+t)(sentence)

def englishipa(sentence):
    def englishipaword(word):
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
    transsent = re.sub(r'[\w\']+', lambda x:englishipaword(x.group(0)), sentence)
    return transsent

def ipaenglish(sentence):
    def ipawordenglish(word):
        try:
            ud = cmurev[word]
        except KeyError:
            ud = untransre.sub(lambda x:revtrans[x.group(0)], word).upper()
        return ud
    transsent = re.sub(normtransre.pattern+r'+', lambda x:ipawordenglish(x.group(0)), sentence)
    return transsent

def kueleripa(sentence):
    return re.sub(r'[a-zA-Z](?:h|H)?', lambda x:(lambda k:(kueler[k][0] if k.isupper() else kueler[k.upper()][1]))(x.group(0)), sentence)

def ipakueler(sentence):
    return normtransre.sub(lambda x:(lambda c:kuelerrev[c].lower() if kueler[kuelerrev[c]].index(c)==1 else kuelerrev[c])(x.group(0)), sentence)

def kuelerenglish(sentence):
    return ipaenglish(kueleripa(sentence))

def englishkueler(sentence):
    return ipakueler(englishipa(sentence))
