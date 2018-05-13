import itertools
import re
import pickle

eipa = {}

with open("engipa.txt", 'r') as f:
    eipa = dict((k, v.split(', ')) for (k, v) in list(itertools.zip_longest(*[iter([a.strip() for a in f.readlines()])] * 2, fillvalue="")))
    eipa = sorted(dict((v,k) for k in eipa for v in eipa[k]).items(), key=lambda x:len(re.search(r'\(\?:(.*)\)', x[0]).group(1)), reverse=True)
with open('compiledipa.txt', 'wb') as f:
    pickle.dump(eipa, f)
