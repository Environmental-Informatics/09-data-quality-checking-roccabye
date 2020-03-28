#!/bin/env python
# Created on Wednesday Mar 25 14:08:42 2020
# Author:  Alka Tiwari (username:tiwari13, githhub: roccabye)
# Program description: This script uses daily climate data for a single site.
# and checks the dataset for gross error, inconsistencies and range problems
# for the variables (Precipitation (mm), Maximum and minimum Air Temperature(°C),
# Wind Speed (m/s). It also creates plot for all the variables before and 
# after data quality check.

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # add your code here
    # Replace all values of -999 in this file with the 
    # NumPy NaN values (e.g., numpy.NaN or np.NaN).

    DataDF = DataDF.replace(to_replace=-999, value= np.NaN)
    
    #count of the data replaced from -999 to nan.
    Count = DataDF.isna().sum()
    
    # Record the number of values replaced for each 
    # data type in the dataframe ReplacedValuesDF with the index "1. No Data"
    ReplacedValuesDF.loc["1. No Data",:] = Count
    
    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    # Apply the following error thresholds: 0 ≤ P ≤ 25; -25≤ T ≤ 35, 0 ≤ WS ≤ 10.
    
    #check for gross error
    a = (len(DataDF.loc[(DataDF['Precip'] < 0)]) 
         +len(DataDF.loc[(DataDF['Precip'] > 25)]) 
        )
    
    b = (len(DataDF.loc[(DataDF['Max Temp'] < -25)]) 
         +len(DataDF.loc[(DataDF['Max Temp'] > 35)]) 
        )

    c = (len(DataDF.loc[(DataDF['Min Temp'] < -25)]) 
         +len(DataDF.loc[(DataDF['Min Temp'] > 35)]) 
        )
    d = (len(DataDF.loc[(DataDF['Wind Speed'] < 0)]) 
         +len(DataDF.loc[(DataDF['Wind Speed'] > 10)]) 
        )
    
    # remove the outsiders with nan
    DataDF.Precip[(DataDF['Precip']>25) | (DataDF['Precip']<0)]=np.nan
    DataDF['Max Temp'][(DataDF['Max Temp']>35) | (DataDF['Max Temp']<-25)]=np.nan
    DataDF['Min Temp'][(DataDF['Min Temp']>35) | (DataDF['Min Temp']<-25)]=np.nan
    DataDF['Wind Speed'][(DataDF['Wind Speed']>10) | (DataDF['Wind Speed']<0)]=np.nan
   
    # count of data that are outside the threshold
    ReplacedValuesDF.loc["2. Gross Error"] = [a,b,c,d]
    
    # Replace values outside this range with NaN. 
    # Record the number of values replaced for each data type in the dataframe ReplacedValuesDF with the index "2. Gross Error"
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    # number of days when Tmax < Tmin (Air Temperature)
       
    Count_T= len(DataDF.loc[DataDF['Max Temp'] < DataDF['Min Temp']])
   
    # swapping the values where Tmax <Tmin
    DataDF.loc[DataDF['Max Temp']<DataDF['Min Temp'],['Max Temp','Min Temp']]= DataDF.loc[ DataDF['Max Temp']<DataDF['Min Temp'],['Min Temp','Max Temp']].values 
   
    # count of data thathas been fixed 
    ReplacedValuesDF.loc["3. Swapped"]=[0,Count_T,Count_T,0]
    
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    # number of days when Tmax - Tmin (Air Temperature) >25 deg C
       
    Count_TD= len(DataDF.loc[(DataDF['Max Temp'] - DataDF['Min Temp']>25)])
   
    # replacing the values where Tmax-Tmin>25 with 'nan'
    DataDF.loc[(DataDF['Max Temp']-DataDF['Min Temp']>25),['Max Temp','Min Temp']]= np.nan
    # count of data that has been replaced as nan.
    ReplacedValuesDF.loc["4. Range"]=[0,Count_TD,Count_TD,0]
    

    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    ##############################################################
    # Saving the processed files.
    # 1. output data that has passed the quality check into a new file

    DataDF.to_csv('After_DataQualityCheck.txt', sep=" ", header=None)

    # 2.file to store output information on failed checks 

    ReplacedValuesDF.to_csv("Failed_Checks.txt", sep="\t")
    
    ##############################################################
    # Plot each dataset before and after correction has been made.
    #Use a single set of axis for each variable, and 
   
    # Original data provided before data quality check
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF_Raw = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF_Raw = DataDF_Raw.set_index('Date')
    
    # PRECIPITATION

    plt.scatter(DataDF.index, DataDF_Raw['Precip'],color = 'chartreuse',label = 'Before Data Quality Check' )
    plt.plot(DataDF.index, DataDF['Precip'],color = 'orangered', label = 'After Data Quality Check')
    plt.xlabel('Date (1915-1916)')
    plt.ylabel('Precipitation (mm)')
    plt.xticks(rotation=70)
    plt.legend(loc='lower left')
    plt.savefig('PRECIPITATION.png')
    plt.close()
    
    # MAXIMUM AIR TEMPERATURE

    plt.scatter(DataDF.index, DataDF_Raw['Max Temp'],color = 'chartreuse',label = 'Before Data Quality Check' )
    plt.plot(DataDF.index, DataDF['Max Temp'],color = 'orangered', label = 'After Data Quality Check')
    plt.xlabel('Date (1915-1916)')
    plt.ylabel("Max Air Temperature (°C)")
    plt.xticks(rotation=70)
    plt.legend(loc='lower left')
    plt.savefig('Max Air Temp.png')
    plt.close()
  
    # MINIMUM AIR TEMPERATURE

    plt.scatter(DataDF.index, DataDF_Raw['Min Temp'],color = 'chartreuse',label = 'Before Data Quality Check' )
    plt.plot(DataDF.index, DataDF['Min Temp'],color = 'orangered', label = 'After Data Quality Check')
    plt.xlabel('Date (1915-1916)')
    plt.ylabel("Min Air Temperature (°C)")
    plt.xticks(rotation=70)
    plt.legend(loc='lower left')
    plt.savefig('Min Air Temp.png')
    plt.close()
  
    # WIND SPEED

    plt.scatter(DataDF.index, DataDF_Raw['Wind Speed'],color = 'chartreuse',label = 'Before Data Quality Check' )
    plt.plot(DataDF.index, DataDF['Wind Speed'],color = 'orangered', label = 'After Data Quality Check')
    plt.xlabel('Date (1915-1916)')
    plt.ylabel("Wind Speed (m/s)")
    plt.xticks(rotation=70)
    plt.legend(loc='upper right')
    plt.savefig('Wind Speed.png')
    plt.close() 
    

    
    