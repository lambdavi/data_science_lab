import pandas as pd

fd = pd.read_csv("es2/data.csv", parse_dates=[0])
print(fd.head()["FL_DATE"])
print(fd.info())
print(fd.describe())