from csv import reader
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules, apriori
import timeit

# Read the datasets

items_set = set()
dataset = []
with open("online_retail.csv") as f:
    csv_reader = reader(f)
    header = next(csv_reader)
    for inv_n, _, desc, _, _, _, _, _ in csv_reader:
        if 'C' not in inv_n and desc != '' and desc.isupper() == True:
            desc=desc.strip()
            dataset.append([inv_n,desc])
            items_set.add(desc)

# Create dictionary of items
items_dict = {}

for inv_n, desc in dataset:
    if items_dict.get(inv_n) == None:
        items_dict[inv_n] = set()
    items_dict[inv_n].add(desc)

items_list = [sorted(list(v)) for v in items_dict.values()]

# Create matrix
all_items = sorted(list(items_set))
"""print(all_items[300])
print(all_items[1051])"""

huge_matrix = []
for l in items_list:
    temp_list= [False]*len(all_items)
    for item in l:
        temp_list[all_items.index(item)]=True
    huge_matrix.append(temp_list)

# Transform the matrix to pandas dataset
df = pd.DataFrame(data=huge_matrix, columns=all_items)

# Perform fpgrowth with mlextend
fi = fpgrowth(df, 0.01)
#print(len(fi))
print(fi.to_string())

f2=association_rules(df=fi, min_threshold=0.95)
print(f2.to_string())

# Timing
"""print(timeit.timeit(lambda: fpgrowth(df, 0.01), number=1))
print(timeit.timeit(lambda: apriori(df, 0.01), number=1))"""

