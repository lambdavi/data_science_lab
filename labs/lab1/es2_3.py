import csv

def translate(row):
    new_row = len(row)*[" "]
    for i,r in enumerate(row):
        if r>=0 and r<64:
            new_row[i] = " "
        elif r>=64 and r<128:
            new_row[i] = "."
        elif r>=128 and r<192:
            new_row[i] = "*"
        else:
            new_row[i] = "#"
    return new_row

def printa(row):
    new_row = translate(row)
    r = c = 0
    k=0
    while r < 28:
        while c < 28:
            print(new_row[c+k], end="")
            c+=1
        r+=1
        k+=c
        c=0
        print("\n")

dataset = []
with open("mnist_test.csv") as f:
    for cols in csv.reader(f):
        dataset.append([int(c) for c in cols])

k = input("Insert k-th value: ")
printa(dataset[int(k)])