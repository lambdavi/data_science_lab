import csv

def euclidean_distance(v1, v2):
    return sum([(x-y)**2 for x,y in zip(v1,v2)])**(1/2)

dataset = []
with open("mnist_test.csv") as f:
    for cols in csv.reader(f):
        dataset.append([int(c) for c in cols])

print(euclidean_distance(dataset[25], dataset[29]))
print(euclidean_distance(dataset[25], dataset[31]))
print(euclidean_distance(dataset[25], dataset[34]))

print(euclidean_distance(dataset[29], dataset[31]))
print(euclidean_distance(dataset[29], dataset[34]))

print(euclidean_distance(dataset[31], dataset[34]))