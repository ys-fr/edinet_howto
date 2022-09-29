import pandas as pd
import datetime
import requests
import sys

# 0: path to xbrl file , 1: write result to xxx.csv


key = sys.args
data = pd.read_csv(key[0],sep="\n",header=None)

Tags = []
for i in data[0].values:
    i = i.split(" ")
    n = 0
    dic = {}
    N = len(i)
    for j in i:
        if len(j)==0:
            continue
        j = j.strip("<")
        if j[0]=="j":
            Tags.append(j)
        break
    pass

pd.DataFrame(Tags).to_csv(key[1],header=None,index=None)