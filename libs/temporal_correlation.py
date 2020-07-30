import os
import gc

import pandas as pd

def get_window(dataframe,t,n):
  #if type(t) == int elif type(t)==str then use .loc, instead of iloc. For the time being, we will just assume t and n are integers 
  return dataframe.iloc[t-n:t,:]

def get_correlation(dataframe1,dataframe2):
  assert dataframe1.shape==dataframe2.shape,'Dataframes must have the same shape'
  ro=dataframe1.corrwith(dataframe2.set_index(dataframe1.index),axis=0) #Force alignment. Make sure size is the same for both dataframes
  return ro.mean() #For the time being we will stop with a general correlation among all zones

def get_correlated_endof_sequence_timestamp(dataframe,t,n=10,min_correlation=0.5):
  endof_sequence_timestamp=[]
  dataframe2=get_window(dataframe,t,n)
  for epoch in reversed(range(2*n,t)):
    dataframe1=get_window(dataframe,epoch-n,n)
    correlation=get_correlation(dataframe1,dataframe2)
    if correlation >= min_correlation:
      #record datetime value. We will use this datetime value to generate all sequences that will go as input to the RNN
      #print(dataframe.index[epoch]) 
      endof_sequence_timestamp.append(dataframe.index[epoch])
  return endof_sequence_timestamp

def get_correlated_sequence_centeredat_timestamp(dataframe,endof_sequence_timestamp,n):
  input={}
  output={}
  for timestamp in endof_sequence_timestamp:
    input[timestamp]=file.loc[pd.date_range(start=timestamp,periods=n,freq='-1D')]
    output[timestamp]=file.loc[pd.date_range(start=timestamp,periods=n,freq='1D')]
  return input,output

def get_IO_series(dataframe,periods,min_correlation=0.5):
  endof_sequence_timestamp=get_correlated_endof_sequence_timestamp(dataframe,len(dataframe),periods)
  input,output=get_correlated_sequence_centeredat_timestamp(dataframe,endof_sequence_timestamp,periods)
  return input,output
