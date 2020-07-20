import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
import datetime
from datetime import timedelta
from ta import add_all_ta_features
from ta.utils import dropna

def read_files(files_names, files_addr, headers, dtypes):
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

def modify_time_inteval(dfs, time_slice, time_inteval):
    for i in range(len(dfs)):
        cur_open_price = dfs[i].iloc[0]["open_price"]
        cur_close_price = dfs[i].iloc[0]["close_price"]
        cur_highest_price = dfs[i].iloc[0]["highest_price"]  
        cur_lowest_price = dfs[i].iloc[0]["lowest_price"]
        target_time =  dfs[i].iloc[0]["datetime"]
        cur_volumn = dfs[i].iloc[0]["volumn"]
        
        start_time = time_slice[0]
        end_time = time_slice[1]
        cur_time = (start_time + timedelta(days=1)).replace(hour=9, minute=30)
        prev_time = datetime.datetime.min
        
        headers = ["open_price", "highest_price", "lowest_price", "close_price", "volumn", "datetime", "hour", "minute"]
        df = pd.DataFrame(columns=headers)
        ndfs = []
        ###############################
        print("df: ", i)
        ###############################
        row_num = dfs[i].shape[0]
        j = 0
        while cur_time < end_time:
            print(cur_time)
            is_first = True
            have_updates = False
            prev_close_price = cur_close_price

            cur_highest_price = float("-inf")
            cur_lowest_price = float("inf")
            cur_volumn = 0

            while target_time <= cur_time and j < row_num:
                if target_time < prev_time: continue
                have_updates = True
                target_time = dfs[i].iloc[j]["datetime"]
                k = j if target_time == cur_time else j - 1
                cur_open_price = dfs[i].iloc[k]["open_price"] if is_first else cur_open_price
                is_first = False
                cur_close_price = dfs[i].iloc[k]["close_price"]
                cur_highest_price = dfs[i].iloc[k]["highest_price"] if cur_highest_price < dfs[i].iloc[k]["highest_price"] else cur_highest_price
                cur_lowest_price = dfs[i].iloc[k]["lowest_price"] if cur_lowest_price > dfs[i].iloc[k]["lowest_price"] else cur_lowest_price
                cur_volumn += dfs[i].iloc[k]["volumn"]
                j += 1

            if have_updates:
                df= df.append(pd.DataFrame(np.array([[cur_open_price, cur_close_price, cur_highest_price, cur_lowest_price, cur_volumn,
                cur_time, cur_time.to_pydatetime().hour, cur_time.to_pydatetime().minute]]), columns=headers), ignore_index=True) 
            else:
                df= df.append(pd.DataFrame(np.array([[prev_close_price, prev_close_price, prev_close_price, prev_close_price, 0,
                cur_time, cur_time.to_pydatetime().hour, cur_time.to_pydatetime().minute]]),columns=headers), ignore_index=True)
            # update time
            cur_time += timedelta(minutes=5)
            if cur_time.to_pydatetime().hour >= 16 and cur_time.to_pydatetime().minute != 0:
                cur_time += timedelta(days=1)
                cur_time =  cur_time.replace(hour=9, minute=35)
            prev_time = cur_time - time_delta(minutes=5)
        ndfs.append(df)
    return ndfs