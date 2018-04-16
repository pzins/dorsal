#!/usr/bin/python3
import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import sys
from tracing_events_classes import event_classes
from collections import defaultdict
import time
import os
from collections import defaultdict
import operator



# Add the input trace to the collection
# Add the input trace to the collection
collection = btr.TraceCollection()
directory = "/home/pierre/out_traces"
collection.add_trace(directory, 'ctf')

# Set the output trace
out_path = "/home/pierre/out_traces_trash"
writer = btw.Writer(out_path)

# Clock
clock = btw.Clock('monotonic')
clock.description = 'Monotonic clock from AMD RCP'
writer.add_clock(clock)

# Environment
writer.add_environment_field("hostname", "pierre-tensorflow")
writer.add_environment_field("domain", "ust")
writer.add_environment_field("tracer_name", "lttng-ust")
writer.add_environment_field("tracer_major", 2)
writer.add_environment_field("tracer_minor", 7)

# Create stream class
main_stream_class = btw.StreamClass('main_stream')
main_stream_class.clock = clock

# Create stream
for event_class in event_classes.values():
    main_stream_class.add_event_class(event_class)
main_stream = writer.create_stream(main_stream_class)

cntol = 0
events = defaultdict(list)

# clock_offset = 1518196357777395130 # second computer
clock_offset = 1523458334781392755 # third computer
clock_offset = 1523380531878303029 # first computer

output = []

for session_ite in range(2,10):

    operations_start = {}
    operations_end = {}
    nb_session_run = 0
    session_run_analysis = session_ite
    record = False



    for r_event in collection.events:
        name = r_event.name
        event_time = r_event.timestamp
        if name == "tensorflowTracer:session_start":
            nb_session_run += 1
            if nb_session_run == session_run_analysis and record == False:
                record = True
        if record and name == "tensorflowTracer:session_end":
            record = False
        
        if record:
            if "operation_end" in name:
                operations_end[r_event["name"]] = event_time
            if "operation_start" in name:
                operations_start[r_event["name"]] = event_time



    ops_inputs = defaultdict(list)
    current_op = ""
    with open("/home/pierre/tf_examples/train.pbtxt", "r") as f:
        lines = f.readlines()
        for l in lines:
            if "name:" in l:
                current_op = l.split()[-1][1:-1]
            
            if "input:" in l:
                if current_op == "":
                    print("error")
                    exit(-1)
                ops_inputs[current_op].append(l.split()[-1][1:-1])

    ops_latencies = {}

    for i in ops_inputs:
        
        
        last_ready = 0
        for j in ops_inputs[i]:
            if j in operations_end:
                tmp = operations_end[j]
                if tmp > last_ready:
                    last_ready = tmp
        if i in operations_start and last_ready > 0:
            ops_latencies[i] = max(0, operations_start[i] - last_ready)
        
    # res = (sorted(ops_latencies.items(), key=operator.itemgetter(1), reverse=False))
    for e in ops_latencies:
        output.append(str(session_ite) + ";" + str(ops_latencies[e]) + "\n")
    # print(res)


with open("output.csv", "w") as f:
    f.writelines(output)