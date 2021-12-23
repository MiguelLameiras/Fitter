import csv
import numpy as np
csv = np.genfromtxt('data.csv', delimiter=" ")
print(csv)
#file = open("data.csv")
#type(file)
#csvreader = csv.reader(file)
#header = []
#header = next(csvreader)
#header
#rows = []
#for row in csvreader:
#        rows.append(row)
#print(rows)
#file.close()
