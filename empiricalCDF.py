#Empirical CDF
import openpyxl
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

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

#generate the CDF by cycling through all elements of the data, and adding 1 to all elements in the CDF <= the given element
appleCDF = np.zeros(8)
for i in range(appledata.size) :
    a = int(appledata[i])
    for j in range(a,appleCDF.size) :
        appleCDF[j]= appleCDF[j]+1
for i in range(appleCDF.size) :
    appleCDF[i] = appleCDF[i]/appledata.size

#Create a second array that doubles up on values to make it easy to plot the stairs in a basic plot function
appleCDF_plot = np.zeros(16)
x_a = np.zeros(16)
for i in range(appleCDF.size) :
    appleCDF_plot[2*i] = appleCDF[i]
    appleCDF_plot[2*i+1] = appleCDF[i]
    x_a[2*i] = i
    x_a[2*i+1] = i+1
    
#Plot it with an error band
#error constant
e_apple = np.sqrt(1/(2*appledata.size)*np.log(2/0.05))
#lower bound and upper bound
L_apple = appleCDF_plot - e_apple
U_apple = appleCDF_plot + e_apple
for i in range(appleCDF_plot.size) :
    L_apple[i] = max(L_apple[i],0)
    U_apple[i] = min(U_apple[i],1)
plt.fill_between(x_a,L_apple,U_apple, label = "confidence band",color="lightblue")
plt.plot(x_a,appleCDF_plot, label = "Empirical CDF")#, color='blue')
plt.xlabel("Apples")
plt.legend()
plt.title("Empirical CDF: Apples per Day")
plt.show()

bikeCDF = np.zeros(150)
for i in range(bikedata.size) :
    b = int(bikedata[i])
    for j in range(b, bikeCDF.size) :
        bikeCDF[j] = bikeCDF[j]+1
for i in range(bikeCDF.size) :
    bikeCDF[i] = bikeCDF[i]/bikedata.size
bikeCDF_plot = np.zeros(301)
print(bikeCDF[40])
x_b = np.zeros(301)
for i in range(bikeCDF.size) :
    bikeCDF_plot[2*i+1] = bikeCDF[i]
    bikeCDF_plot[2*i+2] = bikeCDF[i]
    x_b[2*i+1] = i
    x_b[2*i+2] = i+1

#Plot with an error band
#error constant
e_bike = np.sqrt(1/(2*bikedata.size)*np.log(2/0.05))
L_bike = bikeCDF_plot - e_bike
U_bike = bikeCDF_plot + e_bike
for i in range(bikeCDF_plot.size) :
    L_bike[i] = max(L_bike[i],0)
    U_bike[i] = min(U_bike[i],1)
plt.fill_between(x_b,L_bike,U_bike, label = "confidence band",color="moccasin")
plt.plot(x_b,bikeCDF_plot,color = "orange", label = "Empirical CDF")
plt.title("Empirical CDF: Miles Biked per Day")
plt.legend()
plt.xlabel("Miles Biked")
plt.show()
#this is a version of the plot where I cut off the outlier data to show how the general idea of the CDF looks
plt.plot(x_b[0:100],bikeCDF_plot[0:100],color = "orange")
plt.title("Empirical CDF: Miles Biked per Day")
plt.show()

#I would also like to generate the Empirical CDF of A', for the sake of the Exact Test
new_appledata = appledata[appledata.size-bikedata.size:appledata.size]
new_appleCDF = np.zeros(8)
for i in range(new_appledata.size) :
    a = int(new_appledata[i])
    for j in range(a,new_appleCDF.size) :
        new_appleCDF[j]= new_appleCDF[j]+1
for i in range(new_appleCDF.size) :
    new_appleCDF[i] = new_appleCDF[i]/new_appledata.size
new_appleCDF_plot = np.zeros(16)
x_a2 = np.zeros(16)
for i in range(appleCDF.size) :
    new_appleCDF_plot[2*i] = new_appleCDF[i]
    new_appleCDF_plot[2*i+1] = new_appleCDF[i]
    x_a2[2*i] = i
    x_a2[2*i+1] = i+1
plt.plot(x_a2,new_appleCDF_plot, label = "Empirical CDF")
plt.xlabel("Apples")
plt.legend()
plt.title("Empirical CDF: Apples per Day")
plt.show()

#let's attempt to give an approximate 
x_normal = np.linspace(-15,15, 1000)
normal_cdf = stats.norm.cdf(x_normal)
#plot the apple cdf again
plt.fill_between(x_a,L_apple,U_apple, label = "confidence band",color="lightblue")
plt.plot(x_a,appleCDF_plot, label = "Empirical CDF")
plt.xlabel("Apples")
#create the correct normal plot by taking the standard normal distribution and manipulating it so its mean and variance matches that of the appledata
x_norm_plot = x_normal*(np.sqrt(variance(appledata))) + mean(appledata)

x_0 = 0
norm_0 = 10
x_1 = 0
norm_1 = 10
#this iteration makes sure we will only plot the portion of the distribution that matches up with the appledata cdf
for i in range(x_norm_plot.size) :
    if(np.abs(x_norm_plot[i]) < norm_0) :
        x_0 = i
        norm_0 = np.abs(x_norm_plot[i])
    if(np.abs(x_norm_plot[i]-8) < norm_1) :
        x_1 = i
        norm_1 = np.abs(x_norm_plot[i]-8)
#plot the cdf
plt.plot(x_norm_plot[x_0-1:x_1+1],normal_cdf[x_0-1:x_1+1], label = "Normal Approximation")
plt.legend()
plt.title("Empirical CDF: A & Normal Approximation")
plt.show()

plt.fill_between(x_b,L_bike,U_bike, label = "confidence band",color="moccasin")
plt.plot(x_b,bikeCDF_plot,color = "orange", label = "Empirical CDF")
plt.xlabel("Miles Biked")
#create the correct normal plot by taking the standard normal distribution and manipulating it so its mean and variance matches that of the bikedata
x_norm_plot = x_normal*(np.sqrt(variance(bikedata))) + mean(bikedata)

x_0 = 0
norm_0 = 10
x_1 = 0
norm_1 = 10

for i in range(x_norm_plot.size) :
    if(np.abs(x_norm_plot[i]) < norm_0) :
        x_0 = i
        norm_0 = np.abs(x_norm_plot[i])
    if(np.abs(x_norm_plot[i]-150) < norm_1) :
        x_1 = i
        norm_1 = np.abs(x_norm_plot[i]-150)
#plot it!
plt.plot(x_norm_plot[x_0-1:x_1],normal_cdf[x_0-1:x_1], label = "Normal Approximation")
plt.legend()
plt.title("Empirical CDF: B & Normal Approximation")
plt.show()
