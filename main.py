import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
from datetime import timedelta
from ta import add_all_ta_features
from ta.utils import dropna
from data_process_helpers import *

# get data in desirved format
dow_files_addr = "./Data/Dow_30_1_min/"
etf_files_addr = "./Data/50_ETFs_1min/"

dow_files_names = [f for f in listdir(dow_files_addr)]
etf_files_names = [f for f in listdir(etf_files_addr)]

dow_names = [f.split(".")[0] for f in dow_files_names]
etf_names = [f.split(".")[0] for f in etf_files_names]

dow_dfs = []
etf_dfs = []
headers = ["date", "time", "open_price", "close_price", "highest_price", "lowest_price", "volumn"]
dtypes={"date": "str", 
    "time":"str",
    "open_price": "float", 
    "highest_price": "float",
    "lowest_price": "float", 
    "close_price": "float",
    "volumn": "int"}

print("Start read dow file...")
dow_dfs = read_files(dow_files_names, dow_files_addr)
print("Finish read dow file.")
print("---------------------")
print("Start read etf file...")
etf_dfs = read_files(etf_files_names, etf_files_addr)
print("Finish read etf file.")


# get start and end for both dow and etf that cove evey df
dow_time_slice = [min(dow_dfs[0]["datetime"]), max(dow_dfs[0]["datetime"])]
etf_time_slice = [min(etf_dfs[0]["datetime"]), max(etf_dfs[0]["datetime"])]

print("Start check dow date...")
dow_time_slice = find_common_time_slice(dow_dfs, dow_time_slice, dow_files_names)
print("Finish check dow date...")
print("---------------------")
print("Start check etf date...")
etf_time_slice = find_common_time_slice(etf_dfs, etf_time_slice, etf_files_names)
print("Finish check etf date...")


# limit all of the df to the same time frames
for i in range(len(dow_dfs)):
    dow_dfs[i] = dow_dfs[i].loc[(dow_dfs[i]["datetime"] >= dow_time_slice[0]) & (dow_dfs[i]["datetime"] <= dow_time_slice[1])]
for i in range(len(etf_dfs)):
    etf_dfs[i] = etf_dfs[i].loc[(etf_dfs[i]["datetime"] >= etf_time_slice[0]) & (etf_dfs[i]["datetime"] <= etf_time_slice[1])]