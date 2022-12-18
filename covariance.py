#calculating covariance
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

#let's define covariance
def cov(x,y) :
    ux = mean(x)
    uy = mean(y)
    c = 0
    for i in range(x.size) :
       c= c +(x[i]-ux)*(y[i]-uy)
    c = c/(x.size)
    return c

covariance = cov(appledata[appledata.size-bikedata.size:appledata.size],bikedata)
print(covariance)