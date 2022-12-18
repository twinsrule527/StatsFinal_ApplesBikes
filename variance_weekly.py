#accounting for day-to-day changes, B'
import openpyxl
import os
import numpy as np
import matplotlib.pyplot as plt

def variance(x) :
    if x.size < 2 :
        return 0
    s = 0
    x_mean = mean(x)
    for i in range(x.size) :
        s = s + (x[i]-x_mean)**2
    s = s/(x.size-1)
    return s
def mean(x) :
    return np.sum(x)/x.size
    
#Gets the path for, and then opens the sheets for my apple data and bike data
base_path = os.path.dirname(os.path.abspath(__file__))
path1 = base_path +"\AppleData.xlsx"
path2 = base_path + "\BikeData.xlsx"

wb_apple = openpyxl.load_workbook(path1, read_only=True)
wb_bike = openpyxl.load_workbook(path2, read_only=True)
sheet_apple = wb_apple.active
sheet_bike = wb_bike.active

#sends the apple and bike data to numpy arrays, making them easier to manipulate
applesheet = np.array([[i.value for i in j] for j in sheet_apple['A3':'B1090']])
bikesheet = np.array([[i.value for i in j] for j in sheet_bike['A3':'B832']])

appledata = applesheet[:,1]
bikedata = bikesheet[:,1]

bprime_data = np.zeros(bikedata.size-6)
for i in range(bprime_data.size) :
    #take the average of 1 week of data
    bprime_data[i] = mean(bikedata[i:i+7])

print(mean(bprime_data))
print(variance(bprime_data))
#I don't use this plot, but wanted to create it just to see if there's anything immediately visible
plt.plot(bikedata)
plt.plot(bprime_data)
plt.show()
