#initial analysis of apple/bike data
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

#calculate the base mean and variance
apple_mean = mean(appledata)
bike_mean = mean(bikedata)
apple_var = variance(appledata)
bike_var = variance(bikedata)
print("Apple Mean: ", apple_mean)
print("Bike Mean: ", bike_mean)
print("Apple Variance: ", apple_var)
print("Bike Variance: ", bike_var)

#also, calculate the apple mean/variance starting from x_0 = bikedata[0], because when comparing the datasets, I will ignore all data points before this one
a_data_new = appledata[appledata.size-bikedata.size:appledata.size]
new_apple_mean = mean(a_data_new)
new_apple_var = variance(a_data_new)
print("Apple Mean New: ", new_apple_mean)
print("Apple Variance New: ", new_apple_var)
