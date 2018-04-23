# read ctf traces and read perf counter output file of RCP


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


ctf_traces = []

# Add the input trace to the collection
collection = btr.TraceCollection()
directory = "/home/pierre/out_traces"
collection.add_trace(directory, 'ctf')
clock_offset = 1519939145097366944 # first computer

# save timestamp and name of all kernels
for r_event in collection.events:
    name = r_event.name
    if "hcTracer:kernel_begin" in name:
        tmp = str(r_event["timestamp"]+  clock_offset) + "|" + r_event["name"]
        ctf_traces.append(tmp)


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

output_data = []
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
    output_data.append(timestamp_human_readable + " | " + rcp_names[i].strip() + "".join(counters[i]).replace(",", "|"))
    ctf_index += 1
    
# add the header
names = "Timestamp | Method | ExecutionOrder | ThreadID | GlobalWorkSize | WorkGroupSize | LocalMemSize | VGPRs | SGPRs | Wavefronts | VALUInsts | SALUInsts | VFetchInsts | SFetchInsts | VWriteInsts | FlatVMemInsts | FlatLDSInsts | FetchSize | WriteSize | CacheHit \n"
output_data.insert(0, names)

# write the data to a csv file        
with open("/home/pierre/perfcounters.csv", "w") as f:
    f.writelines(output_data)