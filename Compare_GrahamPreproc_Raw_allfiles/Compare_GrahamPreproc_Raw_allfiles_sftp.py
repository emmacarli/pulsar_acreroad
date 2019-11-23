# =============================================================================
# 
# This code plots raw data and data preprocessed using Graham's routine.
# PDFs are useful to save all the plots but interactive plots can be looked at with more precision, although individually.
# This code does not need to be run from ettus. I have a local copy of the raw files and download Graham's preprocessed files on campus or using a VPN. 
# Author: Emma Carli emma.carli@outlook.com
#
# =============================================================================


#%% Clear variables

from IPython import get_ipython
get_ipython().magic('reset -f') 

#%% Import packages

import numpy as np
import matplotlib.pyplot as plt
import pysftp
from astropy.time import Time
import os
import glob

#%% Set matplotlib general parameters

#Make everything larger for readability on graphs
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['font.size'] = 14
#Set same fonts as my LaTeX document
plt.rcParams['font.family'] = 'STIXGeneral' 
plt.rcParams['mathtext.fontset'] = 'stix'
#other plotting params
plt.rcParams['axes.grid'] = True
plt.rcParams["figure.figsize"] = [10,10]


#%% Make lists of the preprocessed and raw files on ettus.

#initialise lists of the preprocessed and raw files on ettus
preproc_files = []
raw_files = []

sftp = pysftp.Connection(host='ettus.astro.gla.ac.uk', username='astro') #connect to ettus, no password as I am on the .authorised_keys list
print('Connection successfully established.')
sftp.cwd('/home/astro/pulsartelescope/data') #change working directory
for file in sftp.listdir():
    if file.endswith('-PSRB0329-2ms-sampling-dd.dat'): #raw file name format
        raw_files.append(file)
    if file.endswith('-preproc.dat'): #preprocessed file name format
        preproc_files.append(file)

#%% Set known data rates

sampling_period = 2e-3 #2 ms

#%% Get the raw and preprocessed data

for file_raw in raw_files:
    
    start_time_GPS = float(file_raw[:-29])

    #if this file has already been plotted, skip it and go to the next in raw_files
    if glob.glob('Plots/'+str(start_time_GPS)+'*.pdf') != []:
        print(str(start_time_GPS)+' already plotted.')
        continue
    

    
    #Raw data
    handle_file_raw = open('/home/emma/Desktop/Raw_Datafiles/'+file_raw, mode='rb') #change path here to your local copy of raw files
    data_raw = np.fromfile(handle_file_raw,'f4')
    
    #Preprocessed data - download from ettus temporarily, I don't keep it on my computer for less disk space usage
    file_preproc = str(start_time_GPS)+'-preproc.dat'
    try: 
        print('Downloading '+file_preproc+'...')
        sftp.get(file_preproc) #downloads the preprocessed file in the current working directory
        print(file_preproc+' downloaded.')
        f_preproc = open(file_preproc, mode='rb')
        data_preproc = np.fromfile(f_preproc, 'f4')
        preproc_file_exists = True
    except FileNotFoundError: #if the preprocessed file is not on ettus
        preproc_file_exists = False  
        print('Preprocessed file does not exist.')
    
    #%% Calculate values for axes and ticks
    
    flag = '' #create a flag for data with different lengths
    
    #Raw dataset
    total_seconds_raw = len(data_raw)*sampling_period
    total_hours_raw =  total_seconds_raw / 3600
    total_hours_rounded_raw = np.ceil(total_hours_raw)
    total_hours_rounded_datapoints_raw =total_hours_rounded_raw*3600/sampling_period
    0
    
        #Preprocessed dataset
    if preproc_file_exists == True:
        total_seconds_preproc = len(data_preproc)*sampling_period #total seconds in dataset
        total_hours_preproc =  total_seconds_preproc / 3600 #total hours in dataset
        total_hours_rounded_preproc = np.ceil(total_hours_preproc) #total rounded hours in dataset
        total_hours_rounded_datapoints_preproc = total_hours_rounded_preproc*3600/sampling_period #how many datapoints in total rounded hours in dataset
        
        if total_hours_preproc == 8.0:
            flag = '_preproc_doubled'
            print('Preprocessed data points doubled. Dividing axes by two...')
            total_seconds_preproc = total_seconds_preproc/2
            total_hours_preproc = total_hours_preproc/2
            total_hours_rounded_preproc =  total_hours_rounded_preproc/2
            #leave datapoints measure as is
        if total_hours_rounded_preproc not in [4.0, 5.0, 8.0]:
            flag = '_different_length'
            
    if total_hours_rounded_raw not in [4.0, 5.0]:
        flag = '_different_length'
            
    
    
            
        
    #%% Set axes and ticks
    
    #Preprocessed dataset
    if preproc_file_exists == True:
        major_ticks_preproc = np.linspace(0, total_hours_rounded_datapoints_preproc, num=total_hours_rounded_preproc+1) #set big ticks every hour
        minor_ticks_preproc = np.linspace(0, total_hours_rounded_datapoints_preproc, num=((total_hours_rounded_preproc*60)+1)) #set small ticks every minute
    
    #Raw dataset
    major_ticks_raw = np.linspace(0, total_hours_rounded_datapoints_raw, num=total_hours_rounded_raw+1) #set big ticks every hour
    minor_ticks_raw = np.linspace(0, total_hours_rounded_datapoints_raw, num=((total_hours_rounded_raw*60)+1)) #set small ticks every minute
    
    #%% Plot raw and preprocessed files
    
    fig1 = plt.figure()
    
    if preproc_file_exists == True: #if there is a preprocessed file corresponding to the raw one, make a plot comparing the two.
        #Preprocessed dataset
        fig1_top = fig1.add_subplot(2,1,1)
        fig1_top.plot(data_preproc, color='black',  marker='None', linewidth=0.05) 
        fig1_top.set_ylabel('Power (arbitrary units)')
        fig1_top.set_xticks(major_ticks_preproc)
        fig1_top.set_xticks(minor_ticks_preproc, minor=True)
        fig1_top.grid(which='minor', alpha=0.2)
        fig1_top.grid(which='major', alpha=0.5)
        fig1_top.set_xticklabels(np.linspace(0, total_hours_rounded_preproc, num=total_hours_rounded_preproc+1))
        fig1_top.set_title('Preprocessed Data')
        
        #Raw dataset
        fig1_bottom = fig1.add_subplot(2,1,2)
        fig1_bottom.plot(data_raw, color='black', marker='None', linewidth=0.05) 
        fig1_bottom.set_xlabel('Time since start (hours)')
        fig1_bottom.set_ylabel('Power (arbitrary units)')
        fig1_bottom.set_xticks(major_ticks_raw)
        fig1_bottom.set_xticks(minor_ticks_raw, minor=True)
        fig1_bottom.grid(which='minor', alpha=0.2)
        fig1_bottom.grid(which='major', alpha=0.5)
        fig1_bottom.set_xticklabels(np.linspace(0, total_hours_rounded_raw, num=total_hours_rounded_raw+1))
        fig1_bottom.set_title('Raw data')
        
        # =============================================================================
        # 
        # HERE THE TIME FORMAT HAS BEEN SET BUT NOT THE SCALE/TIME STANDARD. THIS IS NOT PRECISE -- BUT ONLY FOR A PLOT SO THAT'S OK.
        # 
        # =============================================================================
        
        #now convert the GPS time string  into astropy time format
        start_time_GPS_astropy = Time(start_time_GPS, format='gps') 
        start_time_ISO_astropy = Time(start_time_GPS_astropy, format='iso')
        
        
        fig1.suptitle('Start of recording: ' + start_time_ISO_astropy.value)
        plt.subplots_adjust(hspace=0.5)
        
        
        plt.savefig('Plots/'+str(start_time_GPS)+'_Compare_GrahamPreproc_Raw'+flag+'.pdf') 
        
    else: #if there is no preprocessed file,  plot the raw one on its own.
        ax1 = plt.gca()
        ax1.plot(data_raw, color='black',  marker='None', linewidth=0.05) 
        ax1.set_ylabel('Power (arbitrary units)')
        ax1.set_xticks(major_ticks_raw)
        ax1.set_xticks(minor_ticks_raw, minor=True)
        ax1.set_xlabel('Time since start (hours)')
        ax1.grid(which='minor', alpha=0.2)
        ax1.grid(which='major', alpha=0.5)
        ax1.set_xticklabels(np.linspace(0, total_hours_rounded_raw, num=total_hours_rounded_raw+1))
        
        # =============================================================================
        # 
        # HERE THE TIME FORMAT HAS BEEN SET BUT NOT THE SCALE/TIME STANDARD. THIS IS NOT PRECISE -- BUT ONLY FOR A PLOT SO THAT'S OK.
        # 
        # =============================================================================
        
        #now convert the GPS time string  into astropy time format
        start_time_GPS_astropy = Time(start_time_GPS, format='gps') 
        start_time_ISO_astropy = Time(start_time_GPS_astropy, format='iso')
        
        
        ax1.set_title('Preprocessed Data, Start of recording: ' + start_time_ISO_astropy.value)
        
        plt.savefig('Plots/'+str(start_time_GPS)+'_GrahamRaw'+flag+'.pdf') 
        

    os.remove(file_preproc) #sftp creates an empty file when trying download even if preproc file does not exist on ettus
    plt.close() #comment out if want an interactive plot in debugging
    print('File(s) plotted and deleted.')

sftp.close()
