# Import required modules
#import datetime
#import os
import math
#import csv
#import glob
import argparse
#import wget
import numpy as np
import uptide
import pytz
import pandas as pd
from matplotlib import dates
from scipy.stats import linregress

#file_paths = glob.glob('data/aberdeen/*.txt') + glob.glob('data/dover/*.txt') + glob.glob('data/whitby/*.txt')
#file_paths = glob.glob('data/*.txt')
filename = ['data/1946ABE.txt', 'data/1947ABE.txt']

# Create read_tidal_data function
def read_tidal_data(filename):
    tidal_data = pd.read_csv(filename, skiprows = 11, names=["Cycle", "Date", "Time", "Sea Level", "Residual"], delimiter = r"\s+")
    # Combine 'Date' and 'Time' columns into 'Datetime' column
    tidal_data['Datetime'] = pd.to_datetime(tidal_data['Date'] + ' ' + tidal_data['Time'], format="%Y/%m/%d %H:%M:%S")
    # Drop all columns not required
    tidal_data = tidal_data.drop(['Cycle','Date', 'Time', 'Residual'], axis='columns')
    tidal_data.set_index('Datetime', inplace=True)
    # Replace M, N, and T vlaues in 'Sea Level' column with NaN
    tidal_data.replace(to_replace=".*[MNT]$",value={'Sea Level':np.nan}, regex=True, inplace=True)
    tidal_data['Sea Level'] = tidal_data['Sea Level'].astype(float)
    return tidal_data

# Create join_data function with a loop joining all location files. Sort data into chronological order.
def join_data(data1, data2):
    # Join data into a new dataframe
    join = pd.concat([data1, data2])
    # Sort values into chronological order
    join.sort_index(inplace=True)
    return join

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

# Calculate the rate of SLR for each location
def sea_level_rise(data):
    # Remove NaN values
    data = data.dropna()
    # Remove mean value
    data_mean = np.mean(data['Sea Level'])
    data['Sea Level'] -= data_mean
    # Turn the index from 'dates2num'
    data.index = dates.date2num(data.index)
    # Calculate SLR using linear regression
    slope, intercept, r_value, p_value, std_err = linregress(data.index, data['Sea Level'])
    return slope, p_value

# Calculate M2 and S2 tidal components for each station
def tidal_analysis(data, constituents, start_datetime):
    
    return 

# Create function to show longest continuous segment of data??? using uptide
def get_longest_contiguous_data(data):
    
    return 
# Re-visit recording from 9/5/24
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
    