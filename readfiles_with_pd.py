import pandas as pd

data= pd.read_csv("data.csv", delimiter= " ", header=None)
data.values

print(data)
print(data.columns)