#Fisher's Exact Test
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

#now, let's create the contingency table
rows = np.arange(0,6,1)
columns = np.array([0,10,20,30,40,150])
table = np.zeros([rows.size,columns.size])
for k in range(new_appledata.size) :
    for i in range(rows.size) :
        if(new_appledata[k] <= rows[i]) :
            for j in range(columns.size) :
                if(bikedata[k] <= columns[j]) :
                    table[i][j] = table[i][j]+1
                    break;
            break;
print(table)

#lets create our second contingency table
new_table = np.zeros([2,2])
for k in range(new_appledata.size) :
    if new_appledata[k] < 3 or new_appledata[k] > 4 :
        if bikedata[k] <= 20 :
            new_table[0][0]= new_table[0][0] + 1
        else :
            new_table[0][1]= new_table[0][1] + 1
    else :
        if bikedata[k] <= 20 :
            new_table[1][0]= new_table[1][0] + 1
        else :
            new_table[1][1]= new_table[1][1] + 1

print(new_table)



#rows = np.array([0,2,4,5])#ray([0,2,4,5])
#columns = np.array([0,20,40,150])
#new_table = np.zeros([rows.size,columns.size])
#for k in range(new_appledata.size) :
#    for i in range(rows.size) :
#        if(new_appledata[k] <= rows[i]) :
#            for j in range(columns.size) :
#                if(bikedata[k] <= columns[j]) :
#                    new_table[i][j] = new_table[i][j]+1
#                    break;
#            break;
#print(new_table)
#print(sum(new_table))
