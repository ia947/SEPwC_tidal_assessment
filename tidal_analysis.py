'''
This module performs tidal analysis including reading, joining,
analysing sea level data from guages, and performing tidal harmonic
analysis using uptide
'''

# Import required modules
import datetime
import argparse
import glob
import os
import numpy as np
import uptide
import pytz
import pandas as pd
from matplotlib import dates
from scipy.stats import linregress

def read_tidal_data(filename):
    ''' Create read_tidal_data function to take a .txt input and format the correct Datetime,
        assert an appropriate name for the Sea Level column, and replace corrupted values with NaN '''
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

def join_data(data1, data2):
    ''' Create join_data function to concat data into a new dataframe,
        then sort into chronological order '''
    # Join data into a new dataframe
    join = pd.concat([data1, data2])
    # Sort chronologically
    join.sort_index(inplace=True)
    return join

def extract_single_year_remove_mean(year, data):
    ''' Create function to only read data for a given year, removing mean so
        tidal values oscillate around zero '''
    year_string_start = str(year)+"0101"
    year_string_end = str(year)+"1231"
    # Read data between Jan 1 and Dec 31
    year_data = data.loc[year_string_start:year_string_end, ['Sea Level']]
    # Remove year mean
    year_data['Sea Level'] -= np.mean(year_data['Sea Level'])
    return year_data

def extract_section_remove_mean(start, end, data):
    ''' Create function to only read data for a given section, removing mean so
        tidal values oscillate around zero '''
    section_start = str(start)
    section_end = str(end)
    # Read data in the given section
    section_data = data.loc[section_start:section_end, ['Sea Level']]
    # Remove section mean
    section_data['Sea Level'] -= np.mean(section_data['Sea Level'])
    return section_data

def sea_level_rise(sea_level_data):
    ''' Calculate the rate of SLR using scipy linregress '''
    # Remove NaN values
    sea_level_data = sea_level_data.dropna()
    # Remove mean value
    sea_level_data['Sea Level'] -= np.mean(sea_level_data['Sea Level'])
    # Turn the index from 'dates2num'
    sea_level_data.index = dates.date2num(sea_level_data.index)
    # Calculate SLR using linear regression
    slope, intercept, r_value, p_value, std_err = linregress(sea_level_data.index, sea_level_data['Sea Level'])
    return slope, p_value

def tidal_analysis(tidal_data, constituents, start_datetime):
    
    return 

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

