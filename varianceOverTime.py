#variance over time - let's investigate how the variance of the apple data changes with respect to time
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

new_appledata = appledata[appledata.size-bikedata.size:appledata.size]

#let's calculate the change in variance over time for both A and A'
applevar_time = np.zeros(appledata.size)
new_applevar_time = np.zeros(new_appledata.size)
for i in range(appledata.size) :
    applevar_time[i] = variance(appledata[0:i])
for i in range(new_appledata.size) :
    new_applevar_time[i] = variance(new_appledata[0:i])

#plot both variances
x = np.arange(0,appledata.size)
plt.plot(x,applevar_time,label="Variance of A")
plt.plot(x[appledata.size-bikedata.size:x.size],new_applevar_time, label = "Variance of A'")
plt.legend()
plt.title("Variance over Time")
plt.xlabel("Days since 12/2/2019")
plt.ylabel("Variance")
plt.show()

#calculate the max variance, and the day it occurs on
x=0
var = 0
for i in range(applevar_time.size) :
    if(var < applevar_time[i]) :
        var = applevar_time[i]
        x = i
print("Day: ", x, " Variance: ", var)