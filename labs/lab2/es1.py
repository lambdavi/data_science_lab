# Imports
from csv import reader
from random import gauss
import matplotlib.pyplot as plt

# Functions Section 
def clean(dataset, city_set):
    avg_list_city = {c: [] for c in city_set}
    for (_, avg, _, city, _, _, _) in dataset:
        avg_list_city[city].append(avg)
    
    for c, l in avg_list_city.items():
        new_l = clean_t(l)
        avg_list_city[c] = new_l

    return avg_list_city

def clean_t(lista):
    for i in range(0,len(lista)):
        if i == 0 and lista[i]=='':
            t = i
            while lista[t] == '':
                t+=1
            lista[i] = float(lista[t]) / 2
        elif i == len(lista)-1 and lista[i]=='':
            t = i
            while lista[t] == '':
                t-=1
            lista[i] = float(lista[t]) / 2
        else:
            if lista[i] == '':
                sx = i
                dx = i
                while lista[sx] == '' and sx >= 0:
                    sx-=1
                while lista[dx] == '':
                    if dx+1>len(lista)-1:
                        break
                    else:
                        dx+=1
                if lista[dx]=='':
                    lista[i] = (float(lista[sx]))/ 2
                else:
                    lista[i] = (float(lista[sx]) + float(lista[dx]))/ 2                 
            else:
                lista[i] = float(lista[i])
    return(lista)

def top_n(city_name, N, avg_city_dict):
    new_l=avg_city_dict[city_name]
    new_s_l = sorted(new_l)
    print(f"Max values in {city_name} are: {new_s_l[-N:]}")
    print(f"Min values in {city_name} are: {new_s_l[:N]}")

# Setup of variables
dataset = []
city_set = set() 

# Reading of dataset
with open("GLT_filtered.csv") as f:
    csv_reader = reader(f)
    header = next(csv_reader)

    for data, avg, uncert, city, country, lat, long in csv_reader:
        dataset.append([data, avg, uncert, city, country, lat, long])
        city_set.add(city)

# Clean dataset
avg_city_dict = clean(dataset, city_set)

# Find N highest/coldest measurement of a given city
top_n('Tokyo', 5, avg_city_dict)

# Plotting
plt.figure(0)
plt.hist(avg_city_dict['Rome'])
plt.hist(avg_city_dict['Bangkok'])
plt.figure(1)
plt.hist(list(map(lambda x: (x-32)/1.8, avg_city_dict['Bangkok'])))
plt.hist(avg_city_dict['Rome'])
plt.show()
