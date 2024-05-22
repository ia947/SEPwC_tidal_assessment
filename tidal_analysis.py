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
    ''' Perform harmonic analysis and return the amplitude and phase'''
    # Remove NaN values
    tidal_data = tidal_data.dropna()
    # Set the tidal constituents and datetimes given the data read-in
    tide = uptide.Tides(constituents)
    tide.set_initial_time(start_datetime)
    seconds_since = (tidal_data.index.astype('int64').to_numpy()/1e9) - start_datetime.timestamp()
    # Harmonic analysis in seconds, returning amp and pha
    amp,pha = uptide.harmonic_analysis(tide, tidal_data['Sea Level'].to_numpy(), seconds_since)
    return (amp, pha)

def get_longest_contiguous_data(data):
    ''' Create function to find the longest continuous section of datetimes '''
    time_series = pd.Series(data)
    runs = uptide.find_runs(time_series)
    longest_run = max(runs, key=len)
    return longest_run

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

    all_files = glob.glob('*.txt')
    data_list = []

    for file in all_files:
        if verbose:
            print(f"Processing file: {file}")

        tidal_data = read_tidal_data(file)
        data_list.append(tidal_data)

    if data_list:
        combined_data = data_list[0]
        for tidal_data in data_list[1:]:
            combined_data = join_data(combined_data, tidal_data)

        if verbose:
            print("Data successfully combined")

        slope, p_value = sea_level_rise(combined_data)
        if verbose:
            print(f"Sea level rise: {slope} metres per day, p-value: {p_value}")

        constituents = ["M2", "S2"]
        start_datetime = combined_data.index[0].to_pydatetime()
        amp, pha = tidal_analysis(combined_data, constituents, start_datetime)
        if verbose:
            print(f"Tidal Analysis - Amplitude: {amp}, Phase: {pha}")

        longest_run = get_longest_contiguous_data(combined_data['Sea Level'])
        if verbose:
            print(f"Longest contiguous data run: {longest_run}")

    else:
        if verbose:
            print("No data files found in directory")
