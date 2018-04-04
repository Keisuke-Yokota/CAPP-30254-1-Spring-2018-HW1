### CAPP 30254 1 (Spring 2018) Homework 1
### Keisuke Yokota


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import numpy as np
from datetime import date


### Problem 1 ###

def get_dataframe(filename, output_name):
    '''
    Get dataframe
    
    Inputs:
        filename:  the name of CSV file as input (string).
        output_name: the name of file as output (string).
     Returns: a data frame
    '''
    df = pd.read_csv(filename, header = 0)
    if 'Vacant' in filename:
        df = pd.read_csv(filename, header = 0)
        df = df.rename(
            columns={'DATE SERVICE REQUEST WAS RECEIVED': 'Creation Date',
                     'X COORDINATE': 'X Coordinate',
                     'Y COORDINATE': 'Y Coordinate',
                     'ZIP CODE': 'ZIP Code',
                     'LATITUDE': 'Latitude',
                     'LONGITUDE': 'Longitude'})
    df = df[df['Creation Date'].str.contains('2017')]
    df = df.reset_index()
    df.to_csv(output_name)
    return df


def get_combined_df(df1, df2, df3):
    '''
    Get combined dataframe
    
    Inputs:
        df1, df2, df3: data frames.
     Returns: a data frame
    '''
    df = pd.concat([df1, df2, df3], axis=0)
    df.to_csv("test.csv")
    return df


def plot(df1,df2,df3):
    '''
    Get bar and line graphes coming from subtype dataframe
    
    Inputs:
        df1, df2, df3: data frames.
     Returns: graphes
    '''
    grouped1 = df1.groupby('Community Area')
    grouped2 = df2.groupby('Community Area')
    grouped3 = df3.groupby('Community Area')

    plt.figure(figsize=(16, 8))
    plt.bar(grouped1.size().index, grouped1.size(), 
            color="#ff9999", width=0.5)
    plt.bar(grouped1.size().index, grouped2.size(), 
            bottom=grouped1.size(),color="#9999ff",  width=0.5)
    plt.plot(grouped3.size().index, grouped3.size())
    return plt.show()


def plot(df1,df2,df3):
    '''
    Get bar and line graphes coming from subtype dataframe
    
    Inputs:
        df1, df2, df3: data frames.
     Returns: graphes
    '''
    grouped1 = df1.groupby('Community Area')
    grouped2 = df2.groupby('Community Area')
    grouped3 = df3.groupby('Community Area')

    plt.figure(figsize=(16, 8))
    plt.bar(grouped1.size().index, grouped1.size(), 
            color="#ff9999", width=0.5)
    plt.bar(grouped1.size().index, grouped2.size(), 
            bottom=grouped1.size(),color="#9999ff",  width=0.5)
    plt.plot(grouped3.size().index, grouped3.size())
    return plt.show()


### Problem 2 ###

def make_augmentated_data1(df1, aug_df, file_name):
    '''
    Make augumented data of Alley Lights Out by merging data frames
    
    Inputs:
        df1: a dataframe of Alley Lights Out
        aug_df: a dataframe of ACS and geographical polygon  
        output_name: the name of file as output (string)
     Returns: a data frame
    '''
    df1 = df1[df1['Creation Date']>='10/01/2017']
    lst = []
    cnt = 0
    for i in range(df1.shape[0]):
        y = float(df1.iat[i,15])
        x = float(df1.iat[i,14])
        point = Point(y, x)
        cnt += 1
        print(cnt)
        for j in range(aug_df.shape[0]):
            if point.within(aug_df.geometry[j]):
                lst.append([df1.iat[i, 2], df1.iat[i,13],
                                      aug_df.iat[j,1], aug_df.iat[j,2],
                                      aug_df.iat[j,3], aug_df.iat[j,7]])
    df1_p3 = pd.DataFrame(lst)
    df1_p3.columns = ['Creation Date', 'Community Area', 'B02001_003E',
                 'B11016_002E', 'B14007_018E','BLKGRPCE']
    grouped1_p3 = df1_p3.groupby('BLKGRPCE')
    df1_p3.to_csv(file_name)
    return df1_p3


def make_augmentated_data3(df3, aug_df, file_name):
    '''
    Make augumented data of Vacant and Abandoned Buildings Reported
    by merging data frames
    
    Inputs:
        df3: a dataframe of Vacant and Abandoned Buildings Reported
        aug_df: a dataframe of ACS and geographical polygon  
        output_name: the name of file as output (string)
     Returns: a data frame
    '''
    df3 = df3[df3['Creation Date']>='10/01/2017']
    lst = []
    cnt = 0
    for i in range(df3.shape[0]):
        y = float(df3.iat[i,22])
        x = float(df3.iat[i,21])
        point = Point(y, x)
        cnt += 1
        print(cnt)
        for j in range(aug_df.shape[0]):
            if point.within(aug_df.geometry[j]):
                lst.append([df3.iat[i, 3], df3.iat[i,20],
                                      aug_df.iat[j,1], aug_df.iat[j,2],
                                      aug_df.iat[j,3], aug_df.iat[j,7]])
    df3_p3 = pd.DataFrame(lst)
    df3_p3.columns = ['Creation Date', 'Community Area', 'B02001_003E',
                 'B11016_002E', 'B14007_018E','BLKGRPCE']
    grouped3_p3 = df3_p3.groupby('BLKGRPCE')
    df3_p3.to_csv(file_name)    
    return df3_p3


def get_ACS_data(filename):
    '''
    Get American Census Search data 
    
    Inputs:
        filename:  the name of CSV file as input (string).
     Returns: a data frame
    '''
    pd.read_json('acs5.json')
    acs.to_csv('acs.csv', header=0)
    acs = pd.read_csv('acs.csv', header = 0)
    acs = acs.rename(columns={'state': 'STATEFP',
                                'county':'COUNTYFP',
                                'tract':'TRACTCE',
                                'block group':'BLKGRPCE'})
    return acs


def Prepare_for_agumention(df):
    '''
    Make a preparation for data augumentation by using ACS data and geopandas
    dataframe and producing a kind of intermediate dataframe for merge.
    
    Inputs:
        df: a data frame (ACS data)
     Returns: a data frame
    '''
        gdf = gpd.read_file('cb_2014_17_bg_500k.shp')
        gdf = gdf.astype({'NAME': int, 'STATEFP': int,
            'COUNTYFP': int, 'TRACTCE': int, 'BLKGRPCE': int})
        aug_df = pd.merge(acs, gdf, 
                on=['STATEFP','COUNTYFP','TRACTCE','BLKGRPCE'])
        return aug_df


### Problem 3 ###

def get_prob(df, zipcode):
    '''
    Get probability for each type of request in a dataframe 
    
    Inputs:
        df: a data frames
        zipcode: zip code for targeted area (integer)
     Returns: a probability (float)
    '''
    total = df["ZIP Code"].dropna().shape[0]
    specific = df[df["ZIP Code"]==zipcode].shape[0]
    prob = specific/total
    return prob