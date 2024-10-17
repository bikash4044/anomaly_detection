# importing required libraries
import matplotlib.pyplot as plt
import time
import numpy as np
import random


# Function to simulate the rainfall data stream using yield
def pseudo_stream():
    for yr in range(10,20):
        for i in range(1,13):
            if i < 3:                               # January or February - winter
                val = random.uniform(10, 28)
            elif i < 6:                             # March to May -  Pre-monsoon
                val = random.uniform(25, 120)
            elif i < 10:                            # June to September -  Monsoon
                val = random.uniform(180, 390)
            else:                                   # October to December -   Post-monsoon
                val = random.uniform(10, 50)

            # Implementing anomaly in place of some normal data
            if random.uniform(0, 10) < 4:
                val /= 4

            yield yr, i, val

# getting valid number of points
try:
    # endp = int(input("Enter the no of data points you want to simulate (min 5): "))
    endp = 100
except:
    print("WRONG INPUT ! ! !  Exiting . .  .")
    exit()

#defining array for normal and anomaly dataset
x_data = []
y_data = []
anomaly_x=[]
anomaly_y=[]


plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()

# Setting x and y axis limits
ax.set_xlim(0, 30)
ax.set_ylim(3, 450)  

# Creating array to store data season-wise to consider seasonality while detecting anomaly
season=[[],[],[],[]]

#Variables initialization 
data_generator = pseudo_stream()
year, month, rainfall = next(data_generator)
x_data.append(f"{month}/{year}")  # Add date label for reference
y_data.append(rainfall)           # Add the new random value to y-axis
anomaly_x.append(f"{month}/{year}")
anomaly_y.append(0)
season[0].append(rainfall)

# Defining mean and standard deviation for each season
s_mean=[rainfall,0,0,0]
s_std=[0,0,0,0]

# Simulate number of data points as given by the user
while True:
    year, month, rainfall = next(data_generator)
    
    x_data.append(f"{month}/{year}")  # Add date label for reference
    y_data.append(rainfall)           # Add the new random value to y-axis

    if(month<3):                      # Defining season serials
        serial_s=0
    elif(month<6):
        serial_s=1
    elif(month<10):
        serial_s=2
    else:
        serial_s=3

    # First 3 years data used to study mean and standard deviation
    if(year == 10 and month in [1,3,6,10]):
        s_mean[serial_s] = rainfall
        s_std[serial_s] = 0
    elif(year<13):
        s_mean[serial_s] = np.mean(season[serial_s])
        s_std[serial_s] = np.std(season[serial_s])

    # Rule to detect anomaly
    if(abs(rainfall - s_mean[serial_s]) > 2 * s_std[serial_s]):
        anomaly_y.append(rainfall)
    else:
        anomaly_y.append(0)

    anomaly_x.append(f"{month}/{year}")
    season[serial_s].append(rainfall)


    # Keep only the latest 30 data points
    x_sub = x_data[-30:]
    y_sub = y_data[-30:]
    a_sub = anomaly_y[-30:]


    # Initiating the plot
    ax.cla()  
    ax.set_xlim(0, len(x_sub) - 1)
    ax.set_ylim(3, 450)
    scatter = ax.scatter(range(len(x_sub)), y_sub, color='blue',s=10, label="No Anomaly")  # Set color to blue for normals
    scatter_a = ax.scatter(range(len(x_sub)), a_sub, color='red',s=15,label="Anomaly")

    # Optionally set x-axis ticks to show months/years
    ax.set_xticks(range(len(x_sub)))
    ax.set_xticklabels(x_sub, rotation=45, ha="right", fontsize=8)
    ax.legend(loc='best')

    # Redraw the plot
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.1)

    if len(x_data) > endp:  # Stop after plotting data points for testing as given by user
        break

plt.ioff()  # Disable interactive mode
plt.show()  # Keep the window open when the loop ends