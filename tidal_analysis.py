# Import required modules
import datetime
import os
import math
import csv
import glob
import argparse
import wget
import numpy as np
import uptide
import pytz
import pandas as pd
import matplotlib.pyplot as plt

#Use 1946/7 data
filename1 = "data/1946ABE.txt"
filename2 = "data/1947ABE.txt"

# Create read_tidal_data function
def read_tidal_data(filename):
    read_tidal_data = pd.read_csv(filename, skiprows = 11, names=["Cycle", "Date", "Time", "Sea Level", "Residual"], delimiter = r"\s+")
    # Combine 'Date' and 'Time' columns into 'Datetime' column
    read_tidal_data['Datetime'] = pd.to_datetime(read_tidal_data['Date'] + ' ' + read_tidal_data['Time'], format="%Y/%m/%d %H:%M:%S")
    # Drop all columns not required
    read_tidal_data = read_tidal_data.drop(['Cycle','Date', 'Time', 'Residual'], axis='columns')
    read_tidal_data.set_index('Datetime', inplace=True)
    # Replace M, N, and T vlaues in 'Sea Level' column, replace with NaN
    read_tidal_data.replace(to_replace=".*M$",value={'Sea Level':np.nan},regex=True,inplace=True)
    return read_tidal_data
    
# Create year_data function
def extract_single_year_remove_mean(year, data):
    year_string_start = str(year)+"0101"
    year_string_end = str(year)+"1231"
    # Read data between Jan 1 and Dec 31
    year_data = data.loc[year_string_start:year_string_end, ['Sea Level']]
    year_mean = np.mean(year_data['Sea Level'])
    # Remove year mean
    year_data['Sea Level'] -= year_mean
    return year_data

# Create section_data function
def extract_section_remove_mean(start, end, data):
    section_start = str(start)
    section_end = str(end)
    # Read data in the given section
    section_data = data.loc[section_start:section_end, ['Sea Level']]
    section_mean = np.mean(section_data['Sea Level'])
    # Remove section mean
    section_data['Sea Level'] -= section_mean
    return section_data

# Create complete_data function with a loop joining all location files. Sort data into chronological order.
def join_data(data1, data2):

    return 


# Calculate the rate of SLR for each location
def sea_level_rise(data):

                                                     
    return 

# Calculate M2 and S2 tidal components for each station
def tidal_analysis(data, constituents, start_datetime):


    return 

# Create function to show longest continuous segment of data???
def get_longest_contiguous_data(data):


    return 

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                      prog="UK Tidal analysis",
                      description="Calculate tidal constiuents and RSL from tide gauge data",
                      epilog="Copyright 2024, Jon Hill"
                      )

    parser.add_argument("directory",
                    help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    default=False,
                    help="Print progress")

    args = parser.parse_args()
    dirname = args.directory
    verbose = args.verbose
    