# compute stats from the trace
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
directory = "/home/pierre/dev/tensorflow-profiler/results"
collection.add_trace(directory, 'ctf')
clock_offset = 1519157918746548550 # first computer


# map : key / list
# to save all operations for each threads
operations = defaultdict(list)

for r_event in collection.events:
    name = r_event.name
    # save all operations event depending on their threadID
    if "operation" in name and "operation_sync" in r_event["cat"] and "gpu" in r_event["cat"]:
        operations[r_event.field_with_scope("vtid", babeltrace.common.CTFScope.STREAM_EVENT_CONTEXT)].append(r_event)

# list containing execution time for each operations for each threadID
all_ops = []

# iterate on all the threadID
for i in operations:
    # map : key / list 
    # to save all the execution time for each operation
    # list because an operation can be executed several time over the total program execution
    ops = defaultdict(list)
    
    cnt = 0
    # assume that we have alternated start/end events
    while cnt < len(operations[i])-1:
        name = operations[i][cnt]["name"]
        duration = operations[i][cnt+1]["timestamp"] - operations[i][cnt]["timestamp"]
        ops[name].append(duration)
        cnt += 2
    # save the results for 1 threadID into the global results
    all_ops.append(ops)
    
# just print the max time for each operation for the first threadID
for i in all_ops[0]:
    max_time = max(all_ops[0][i])
    print(i, max_time)
        