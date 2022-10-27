import json
import pandas as pd
from mlxtend.frequent_patterns import apriori
import timeit


dataset = []
with open("modified_coco.json") as f:
    obj = json.load(f)

items_set = set()
for o in obj:
    dataset.append(list(set(o["annotations"])))
    items_set=items_set.union(set(o["annotations"]))

all_items = list(items_set)
print(all_items[71])
huge_matrix = []
for l in dataset:
    temp_list= [False]*len(all_items)
    for item in l:
        temp_list[all_items.index(item)]=True
    huge_matrix.append(temp_list)

df = pd.DataFrame(data=huge_matrix, columns=all_items)

"""f1 = apriori(df, 0.01)
print(f1.to_string())"""

print(timeit.timeit(lambda: apriori(df, 0.01), number=1))