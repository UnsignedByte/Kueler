import pickle
import re

cmu = {}
normaltrans = {}

with open("dictionary/compileddict.txt", 'rb') as f:
    cmu = pickle.load(f)

with open("dictionary/compiledipa.txt", 'rb') as f:
    normaltrans = pickle.load(f)

while True:
    insent = input()
    try:
        ud = re.sub(r'[a-zA-Z]+', lambda x:cmu[x.group().upper()][0], insent)
    except KeyError:
        ud = re.sub(r'(\w)\1+', r'\1\1', insent)
        for a in normaltrans:
            try:
                ud = re.sub(a[0], a[1]+r'\1', ud)
            except Exception:
                ud = re.sub(a[0], a[1], ud)
    print(ud)
