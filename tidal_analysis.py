# Import required modules
import datetime
import os
import math
import wget
import numpy as np
import uptide
import pytz
import pandas as pd
import matplotlib.pyplot as plt

# Create tide_data function
def read_tidal_data(filename):

    return 0
    
# Create year_data function
def extract_single_year_remove_mean(year, data):
   year_string_start = str(year)+"0101" # (Remove comment) January 1st
   year_string_end = str(year)+"1231" # (Remove comment) December 31st
   year_data = data.loc[year_string_start:year_string_end, ['Tide']]
   # Remove mean to oscillate around zero
   mmm = np.mean(year_data['Tide'])
   year_data['Tide'] -=mmm

   return year_data


def extract_section_remove_mean(start, end, data):


    return 


def join_data(data1, data2):

    return 



def sea_level_rise(data):

                                                     
    return 

def tidal_analysis(data, constituents, start_datetime):


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
    


