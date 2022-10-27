import csv
from collections import Counter
with open("iris.csv") as f:
    dataset = [cols for cols in csv.reader(f)]

n = len(dataset)
m = len(dataset[0])-1

categories = dict(Counter([l[m] for l in dataset]))
means = {cat:m*[0.0] for cat in categories.keys()}
st_devs = {cat:m*[0.0] for cat in categories.keys()}

for features in dataset:
    for l,f in enumerate(features):
        if l < m:
            means[features[-1]][l] += float(f)/categories[features[-1]]

for features in dataset:
    for l, f in enumerate(features):
        if l < m:
            st_devs[features[-1]][l] += ((float(f)-means[features[-1]][l])**2)/categories[features[-1]]


for cat in categories.keys():
    for st in st_devs[cat]:
        st_devs[cat] = [s**(1/2) for s in st_devs[cat]]

print(means)
print(st_devs)