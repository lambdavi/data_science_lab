import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -- FUNCTIONS SECTION --    
def plot_histogram(df, categories):
    for c in categories:
            new_tab = df[c].value_counts()
            max = new_tab.iloc[0]
            nn = new_tab[new_tab>int(0.2*max)]
            plt.figure()
            nn.plot.bar()
    plt.show()

def plot_on_map(path_to_map, df, cat):
    # Filter
    new_tab = df[cat].value_counts()
    max = new_tab.iloc[0]
    nn = new_tab[new_tab>int(0.2*max)].index
    img = plt.imread(path_to_map)
    _, ax = plt.subplots()
    df = df[df[cat].notnull()]
    for u in nn: # u stands for unique value
        mask=df[cat]==u
        new = df[mask]
        ax.scatter(new["@lon"], new["@lat"], zorder=1, alpha= 0.8, s=10)
    x_sx, x_dx = ax.get_xlim()
    y_sx, y_dx = ax.get_ylim()
    ax.imshow(img, zorder=0, extent=[x_sx, x_dx, y_sx, y_dx])    
    plt.show(block="True")

def create_grid(path_to_map, df) -> pd.DataFrame: 
    # Displaying
    img = plt.imread(path_to_map)
    _, ax = plt.subplots()
    df = df.dropna(thresh=3)
    ax.scatter(df["@lon"], df["@lat"], zorder=1, alpha= 0.8, s=10)
    x_sx, x_dx = ax.get_xlim()
    y_sx, y_dx = ax.get_ylim()
    print(x_sx, x_dx)
    print(y_sx, y_dx)

    ax.set_aspect('equal')
    ax.set_xticks(np.arange(x_sx, x_dx, step=((x_dx-x_sx)/6)))
    ax.set_yticks(np.arange(y_sx, y_dx, step=((y_dx-y_sx)/5)))
    ax.grid()
    ax.imshow(img, zorder=0, extent=[x_sx, x_dx, y_sx, y_dx])    
    plt.show(block="True")

    # Creating dataframe
    ll = df.dropna(subset=["@id", "@lat", "@lon"]) # ll = lat-lon
    ll["@lon_n"] = ((ll["@lon"]+74.280424825)*10).astype(int)
    ll["@lat_n"] = ((ll["@lat"]-40.48184828)*10).astype(int)
    ll = ll.assign(coord=lambda x: x["@lat_n"]*6+x["@lon_n"])
    return ll

def per_type_grid(df):
    # Preparing the dataframe
    ret_df = df.drop(columns=["@type", "@lat", "@lon", "@lon_n", "@lat_n"])
    ret_df = pd.pivot_table(ret_df, index=['coord'], values=['shop', 'public_transport', 'highway','amenity name'], aggfunc="count").iloc[6]
    print(ret_df)
    return ret_df


# -- MAIN SECTION --

if __name__ == "__main__":
    # Importing the dataframes
    pois = pd.read_csv('lab5/NYC_POIs/pois_all_info.tsv', delimiter="\t", index_col=False)
    pois_metadata = pd.read_csv('lab5/NYC_POIs/ny_municipality_pois_id.csv', header=None)
    # Finding nan values
    for col in pois.columns:
        print(f"Col {col} has {pois[col].isna().sum()} null values")
    
    # Filtering data
    pois = pois[pois['@id'].isin(pois_metadata[0])]

    # Histograms of most frequent types of each category
    categories = pois.columns[4:]
    #plot_histogram(pois, categories)
    NY_map_path = "lab5/NYC_POIs/New_York_City_Map.PNG"
    plot_on_map(NY_map_path, pois, "shop")
    ll_df = create_grid(NY_map_path, pois)
    per_type_grid(ll_df)


"""
# CODE HINT FOR GETTING MODULAR ROWS AND COLUMNS OF GRID
df = pd.read_csv('pois_all_info.tsv', sep='\t', index_col=False)
pois_metadata = pd.read_csv('ny_municipality_pois_id.csv', header=None)

ll = df.dropna(subset=["@id", "@lat", "@lon"])
ll = ll[ll['@id'].isin(pois_metadata[0])]

offset_x = (-73.67247847499999 - (-74.280424825)) / 10
offset_y = (40.93448112 - 40.48184828) / 10 
print(offset_x, offset_y)
ll["@lon_n"] = ((ll["@lon"]+74.280424825)/offset_x).astype(int)
ll["@lat_n"] = ((ll["@lat"]-40.48184828)/offset_y).astype(int)
# ll = ll.assign(coord= lambda x: x["@lat_n"]*6+x["@lon_n"])

# ll[["@lon_n", "@lat_n"]]
ll
"""