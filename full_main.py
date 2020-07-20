import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
from datetime import timedelta
from ta import add_all_ta_features
from ta.utils import dropna

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

def read_files(files_names, files_addr):
    dfs = []
    for name in files_names:
        df = pd.read_csv(files_addr + name, sep=",",names=headers,dtype=dtypes, header=None)
        df["datetime"] = df["date"] + " " + df["time"]
        df["datetime"] = pd.to_datetime(df["datetime"], format="%m/%d/%Y %H:%M")
        df["hour"] = df["time"].str.split(":", expand=True)[0].astype(int)
        df["minute"] = df["time"].str.split(":", expand=True)[1].astype(int)
        df = df.sort_values(by=["datetime"])
        df = df.drop(columns=["date"])
        df = df.drop(columns=["time"])
        dfs.append(df)
    return dfs

print("Start read dow file...")
dow_dfs = read_files(dow_files_names, dow_files_addr)
# for dow_name in dow_files_names:
#     df = pd.read_csv(dow_files_addr + dow_name, sep=",",names=headers,dtype=dtypes, header=None)
#     df["datetime"] = df["date"] + " " + df["time"]
#     df["datetime"] = pd.to_datetime(df["datetime"], format="%m/%d/%Y %H:%M")
#     df["hour"] = df["time"].str.split(":", expand=True)[0].astype(int)
#     df["minute"] = df["time"].str.split(":", expand=True)[1].astype(int)
#     df = df.sort_values(by=["datetime"])
#     df = df.drop(columns=["date"])
#     df = df.drop(columns=["time"])
#     dow_dfs.append(df)
print("Finish read dow file.")
print("---------------------")
print("Start read etf file...")
etf_dfs = read_files(etf_files_names, etf_files_addr)
# for etf_name in etf_files_names:
#     df = pd.read_csv(etf_files_addr + etf_name, sep=",",names=headers,dtype=dtypes, header=None)
#     df["datetime"] = df["date"] + " " + df["time"]
#     df["datetime"] = pd.to_datetime(df["datetime"], format="%m/%d/%Y %H:%M")
#     df["hour"] = df["time"].str.split(":", expand=True)[0].astype(int)
#     df["minute"] = df["time"].str.split(":", expand=True)[1].astype(int)
#     df = df.sort_values(by=["datetime"])
#     df = df.drop(columns=["date"])
#     df = df.drop(columns=["time"])
#     etf_dfs.append(df)
print("Finish read etf file.")

# get start and end for both dow and etf that cove evey df

dow_time_slice = [min(dow_dfs[0]["datetime"]), max(dow_dfs[0]["datetime"])]
etf_time_slice = [min(etf_dfs[0]["datetime"]), max(etf_dfs[0]["datetime"])]

def find_common_time_slice(dfs, time_slice, files_names):
    i = 0
    for df in dfs:
        start = min(df["datetime"])
        if start > time_slice[0]:
            print("start", files_names[i])
            print(start)
            time_slice[0] = start
        end = max(df["datetime"])
        if end < time_slice[1]:
            print("end", files_names[i])
            print(end)
            time_slice[1] = end
        i += 1
    return time_slice

print("Start check dow date...")
dow_time_slice = find_common_time_slice(dow_dfs, dow_time_slice, dow_files_names)
# for df in dow_dfs:
#     start = min(df["datetime"])
#     if start > dow_time_slice[0]:
#         print("start", dow_files_names[i])
#         print(start)
#         dow_time_slice[0] = start
#     end = max(df["datetime"])
#     if end < dow_time_slice[1]:
#         print("end", dow_files_names[i])
#         print(end)
#         dow_time_slice[1] = end
print("Finish check dow date...")
print("---------------------")
print("Start check etf date...")
etf_time_slice = find_common_time_slice(etf_dfs, etf_time_slice, etf_files_names)
# for df in etf_dfs:
#     start = min(df["datetime"])
#     if start > etf_time_slice[0]:
#         print("start", dow_files_names[i])
#         print(start)
#         etf_time_slice[0] = start
#     end = max(df["datetime"])
#     if end < etf_time_slice[1]:
#         print("end", dow_files_names[i])
#         print(end)
#         etf_time_slice[1] = end
print("Finish check etf date...")