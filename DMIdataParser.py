import os 
from parse import *
from tkinter import filedialog
import time

startTime = time.time()

folder = "2018"
lineFormat = '{"geometry":{geo},"properties":{"created":{createdDateTime},"observed":"{obsDateTime}","parameterId":"{parameterID}","stationId":"{stationID}","value":{val}},"type":"Feature","id":"{id}"}'
desiredStation = '06031'

#folderPath = os.path.join(os.getcwd(), folder)
folderPath = filedialog.askdirectory()

# create list of files. 
files = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]
# At least one example of list comprehension is mandatory in any python script. 

outputHumidity = ''
outputTemperature = ''
outWindDir = ''
outWindSpeed = ''
outWindSpeedMax = ''
outputAllForStation = ''

#writeParameters = ['humidity_past1h', 'temp_mean_past1h'] 
# One could do something clever like above but i wont bother. 

# For testing purposes:
#files = ['2022-01-01.txt', '2022-01-02.txt'] # Comment this line when running for real 

# reading files in specified folder one by one. 
for file in files:
    print('reading file: ' + file)
    with open(os.path.join(folderPath, file), 'r') as f:
        text = f.read()

    # splitting the text string into a list, where each element in the list is a line from the text file:     
    text = text.split('\n')
    
    # Iterating over each line in the textfile:
    for line in text: 
        try: 
            #Parsing the line according to the format given above. 
            pars = parse(lineFormat, line)
            ### write all data for the station:
            if pars['stationID'] == desiredStation:
               outputAllForStation = outputAllForStation + pars['obsDateTime'] + ';' + pars['parameterID'] + ';' + pars['val'] + '\n'
            
            ### humidity: 
            if pars['stationID'] == desiredStation and pars['parameterID'] == 'humidity_past1h':
               outputHumidity = outputHumidity + pars['obsDateTime'] + ';' + pars['val'] + '\n' 
            
            ### 1hr avg temperature 
            if pars['stationID'] == desiredStation and pars['parameterID'] == 'temp_mean_past1h':
               outputTemperature = outputTemperature + pars['obsDateTime'] + ';' + pars['val'] + '\n'
            
            ### wind speed:
            if pars['stationID'] == desiredStation and pars['parameterID'] == 'wind_speed':
                outWindSpeed = outWindSpeed + pars['obsDateTime'] + ';' + pars['val'] + '\n'
            
            ### wind direction :
            if pars['stationID'] == desiredStation and pars['parameterID'] == 'wind_dir':
                outWindDir = outWindDir + pars['obsDateTime'] + ';' + pars['val'] + '\n'
        except:
            pass

# defines a output csv file with the same name as the folder. 
outputTotalFile = folderPath + 'All.csv'
outputTempFile = folderPath + 'temp.csv'
outputHumidFile = folderPath + 'humid.csv'
outWindSpeedFile = folderPath + 'windspeed.csv'
outWindDirFile = folderPath + 'windDir.csv'

# opening the output file to write stuff to it:
# If you want a big ass file, uncomment this: 
#with open(outputTotalFile, "w") as f:
#    f.write(outputAllForStation)

with open(outWindSpeedFile, "w") as f:
    f.write(outWindSpeed)

with open(outWindDirFile, "w") as f:
    f.write(outWindDir)

time2run= time.time()-startTime
print('Total runtime: ', time2run) 