import pickle
import re

cmu = {}
with open("dictionary/compileddict.txt", 'rb') as f:
    cmu = pickle.load(f)

while True:
    insent = input()
    ud = re.sub(r'[a-zA-Z]+', lambda x:cmu[x.group().upper()][0], insent)
    print(ud)
