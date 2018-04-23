# get kernels timestamps and sessions timestamps from ctf trace file

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


# Add the input trace to the collection
collection = btr.TraceCollection()
directory = "/home/pierre/out_traces"
collection.add_trace(directory, 'ctf')
clock_offset = 1519939145097366944 # first computer

# sessions
sessions = []
session_tmp_times = [0, 0]

# kernels
kernels = defaultdict(list)
kernel_tmp_times = [0, 0]

for r_event in collection.events:
    name = r_event.name

    # get kernel start event
    if "hcTracer:kernel_begin" in name:
        # check if it's coherent
        if kernel_tmp_times != [0, 0]:
            print("error state")
            exit(0)
        # set the start kernel_tmp_timestamp
        kernel_tmp_times[0] = r_event["timestamp"] + clock_offset

    # get kernel end event
    if "hcTracer:kernel_end" in name:
        # check if it's coherent
        if kernel_tmp_times[1] != 0:
            print("error state")
            exit(0)
        # set the end kernel_tmp_timestamp
        kernel_tmp_times[1] = r_event["timestamp"] + clock_offset
        # create an entry . key is start kernel_tmp_timestamp
        # we add kernel time, kernel name
        kernels[kernel_tmp_times[0]].append(kernel_tmp_times)
        kernels[kernel_tmp_times[0]].append(r_event["name"])
        kernel_tmp_times = [0, 0]


    if "tensorflowTracer:session_start" in name:
        if session_tmp_times != [0, 0]:
            print("error start time session")
            exit(0)
        session_tmp_times[0] = r_event.timestamp
        
    if "tensorflowTracer:session_end" in name:
        if session_tmp_times[1] != 0:
            print("error end time session")
            exit(0)
        session_tmp_times[1] = r_event.timestamp
        sessions.append([session_tmp_times, r_event["count"]])
        session_tmp_times = [0, 0]
    
    
for i in kernels:
    print(i, kernels[i])
    input()

for i in sessions:
    print(i, end=" ")