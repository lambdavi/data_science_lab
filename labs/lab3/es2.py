from collections import Counter

dataset = [['a','b'], ['b','c','d'], ['a','c','d','e'], ['a','d','e'],['a','b','c'],['a','b','c','d'],['b','c'],['a','b','c'],['a','b','d'], ['b','c','e']]
item_set = {'a', 'b', 'c', 'd', 'e'}
s=1

def apriori(dataset, item_set, s):
    c = Counter()
    for i in item_set:
        for d in dataset:
            if(i in d):
                c[i]+=1
    print(c)
    print("C1:")
    for i in c:
        print(str([i])+": "+str(c[i]))
    print()
    l = Counter()
    for i in c:
        if(c[i] > s):
            l[frozenset([i])]+=c[i]
    print("L1:")
    for i in l:
        print(str(list(i))+": "+str(l[i]))
    print()
    pl = l
    pos = 1
    valid_l=[]
    valid_l.append(l)
    for count in range (2,1000):
        nc = set()
        temp = list(l)
        for i in range(0,len(temp)):
            for j in range(i+1,len(temp)):
                t = temp[i].union(temp[j])
                if(len(t) == count):
                    nc.add(temp[i].union(temp[j]))
        nc = list(nc)
        c = Counter()
        for i in nc:
            c[i] = 0
            for q in dataset:
                temp = set(q)
                if(i.issubset(temp)):
                    c[i]+=1
        print("C"+str(count)+":")
        for i in c:
            print(str(list(i))+": "+str(c[i]))
        print()
        l = Counter()
        for i in c:
            if(c[i] > s):
                l[i]+=c[i]
        print("L"+str(count)+":")
        for i in l:
            print(str(list(i))+": "+str(l[i]))
        print()

        if(len(l) == 0):
            break
        valid_l.append(l)
        pl = l
        pos = count
    print("Result: ")
    for j in range(0,len(valid_l)):
        print("L"+str(j+1)+":")
        print(valid_l[j])
    print()

    return valid_l
    
