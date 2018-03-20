# read ctf traces and read perf counter output file of RCP
# more complete than the read_kernel.py


#!/usr/bin/python3
import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import sys
from tracing_events_classes import event_classes
from collections import defaultdict
import time
import os
from datetime import datetime
from collections import defaultdict


ctf_traces = []

# Add the input trace to the collection
collection = btr.TraceCollection()
directory = "/home/pierre/out_traces"
collection.add_trace(directory, 'ctf')
clock_offset = 1519939145097366944 # first computer

# get all the sessions time
sessions_time = []
# used to make sure it's coherent
tmp_session_time = [0, 0]

# save timestamp and name of all kernels
for r_event in collection.events:
    name = r_event.name
    if "hccTracer:kernel_begin" in name:
        tmp = str(r_event["timestamp"]+  clock_offset) + "|" + r_event["name"]
        ctf_traces.append(tmp)
    if "tensorflowTracer:session_start" in name:
        if tmp_session_time != [0, 0]:
            print("error start time session")
            exit(0)
        tmp_session_time[0] = r_event.timestamp
    if "tensorflowTracer:session_end" in name:
        if tmp_session_time[1] != 0:
            print("error end time session")
            exit(0)
        tmp_session_time[1] = r_event.timestamp
        sessions_time.append(tmp_session_time)
        tmp_session_time = [0, 0]
        
        


rcp_names = []
counters = []

# read lines from RCP file
with open("/home/pierre/Session1.csv", "r") as f:
    lines = f.readlines()
    # skip the first 10 lines which are not perf counters lines
    for line in lines[10:]:
        # get only the name
        split_line = line.split("_gfx803")
        name = split_line[0].replace("&nbsp;", " ").replace("&comma;", ",")
        rcp_names.append(name)
        # and save the counters
        counters.append(split_line[1:])

# data we will write to the file
output_data = []

# dict of list, key=timestamp, list=[perfcounters, idx_sessions, idx_kernels, idx_k_in_s]
map_timestamp_kernel = defaultdict(list)
ctf_index = 0
# loop to merge the events
for i in range(len(rcp_names)):
    # get the name from ctf line
    name = ctf_traces[ctf_index].split("|")[1].strip() 
    
    # check if it's the same in RCP event
    res =  name in rcp_names[i]

    # if not we check the next CTF event
    if res == False:
        ctf_index += 1
        name = ctf_traces[ctf_index].split("|")[1].strip() 
        res =  name in rcp_names[i]
        
        # If the next one match, it's ok, otherwise exit
        if res == False:
            print("events don't match")
            exit(-1)
    
    # if success, retrieve the timestamp and convert it into human readable timestamp
    timestamp = int(ctf_traces[ctf_index].split("|")[0])
    timestamp_second = datetime.fromtimestamp(timestamp//1000000000)
    timestamp_human_readable = timestamp_second.strftime('%Y-%m-%d %H:%M:%S')
    timestamp_human_readable += '.' + str(int(timestamp % 1000000000)).zfill(9)
    
    # append the result : human readable timestamp, kernel name, counters
    # separation with '|'
    output_data.append(str(timestamp) + "|" + timestamp_human_readable + " | " + rcp_names[i].strip() + "".join(counters[i]).replace(",", "|"))
    map_timestamp_kernel[timestamp].append(ctf_traces[ctf_index])
    ctf_index += 1

    
    
# add the header
names = "Timestamp | Method | ExecutionOrder | ThreadID | GlobalWorkSize | WorkGroupSize | LocalMemSize | VGPRs | SGPRs | Wavefronts | VALUInsts | SALUInsts | VFetchInsts | SFetchInsts | VWriteInsts | FlatVMemInsts | FlatLDSInsts | FetchSize | WriteSize | CacheHit \n"
output_data.insert(0, names)

timestamps = list(map_timestamp_kernel.keys())
timestamps.sort()

idx_sessions = 0 # session index
idx_kernels = 0 # kernel index (among all kernels)
idx_k_in_s = 0 # kernel index (among kernels belonging to the same session)

sessions_nb_kernel = [0 for i in range(len(sessions_time))]

def isInThisInterval(t, index, sessions):
    return (t <= sessions[index][1] and t >= sessions[index][0])

def isBeforeSession(t, sessions):
    return t < sessions[0][0]

for i in timestamps:
    if isBeforeSession(i, sessions_time):
        continue
    while not isInThisInterval(i, idx_sessions, sessions_time):
        idx_sessions += 1
        idx_k_in_s = 0

    map_timestamp_kernel[i].append(idx_sessions)
    map_timestamp_kernel[i].append(idx_kernels)
    map_timestamp_kernel[i].append(idx_k_in_s)
    sessions_nb_kernel[idx_sessions] += 1
    idx_k_in_s += 1
    idx_kernels += 1

# for i in sessions_nb_kernel:
#     print(i, end=" ")
 
# for i in timestamps:
#     print(i)
#     for j in map_timestamp_kernel[i]:
#         print(j)
#     input()
out = []
for i in output_data[1:]:
    tt = int(i.split("|")[0])
    if len(map_timestamp_kernel[tt]) > 1:
        out.append(str(map_timestamp_kernel[tt][1]) + "|" + str(map_timestamp_kernel[tt][3]) + "|" + str(map_timestamp_kernel[tt][2]) + "|" + i)
    else:
        out.append("-1|-1|-1|" + i)

# write the data to a csv file        
with open("/home/pierre/perfcounters_test.csv", "w") as f:
    f.writelines(out)
    # f.writelines(output_data)