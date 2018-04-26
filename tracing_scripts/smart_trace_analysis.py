#!/usr/bin/python3
import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import sys
import time
import os
import operator
import argparse

# parse arguments
parser = argparse.ArgumentParser(description="Compute statistics")
parser.add_argument("--trace", help="set the input trace", required=True)
parser.add_argument("--graph", help="set the TensorFlow graph file", required=True)
parser.add_argument("--output", help="set the output csv file")
args = parser.parse_args()

if args.output == None:
    outfile = "latencies.csv"
else:
    outfile = args.output

from tracing_events_classes import event_classes
from collections import defaultdict
# Add the input trace to the collection
collection = btr.TraceCollection()

# Set the input traces
path = args.trace
if path[-1] == "/":
    path = path[:-1]
collection.add_trace(path, 'ctf')


events = defaultdict(list)
output = ["session id;operation;latency;nb inputs\n"]
skip_sessions = [1, 2]

# loop for each session except the first two
# first is usually : variable initialization
# second is usually biased beause of GPU initialization, ...
for session_ite in range(1,10):
    if session_ite in skip_sessions:
        continue
    operations_start = {}
    operations_end = {}
    nb_session_run = 0
    session_run_analysis = session_ite
    record = False


    # get all the operation start and end in 2 lists
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
    assert(len(operations_start) == len(operations_end))

    # get all the inputs for each TensorFlow operations in a dict ops_inputs
    ops_inputs = defaultdict(list)
    current_op = ""
    with open(args.graph, "r") as f:
        lines = f.readlines()
        for l in lines:
            if "name:" in l:
                current_op = l.split()[-1][1:-1]
            
            if "input:" in l:
                if current_op == "":
                    print("error")
                    exit(-1)
                ops_inputs[current_op].append(l.split()[-1][1:-1])

    # for each TensorFlow operations, check all the inputs and get the one which
    # ends the last. Compute the difference with the start of the current 
    # TensorFlow operation to get the latency
    ops_latencies = {}
    for i in ops_inputs:
        last_ready = 0
        for j in ops_inputs[i]:
            # check if the input is a TensorFlow operation
            # in some cases it is not
            if j in operations_end:
                tmp = operations_end[j]
                if tmp > last_ready:
                    last_ready = tmp
        if i in operations_start and last_ready > 0:
            ops_latencies[i] = max(0, operations_start[i] - last_ready)
        
    res = (sorted(ops_latencies.items(), key=operator.itemgetter(1), reverse=True))
    for e in res:
        # output.append(str(session_ite) + ";" + e + ";" + str(ops_latencies[e]) + "\n")
        output.append(str(session_ite) + ";" + e[0] + ";" + str(e[1]) + ";" + str(len(ops_inputs[e[0]])) + "\n")

    output.append("\n")


with open("output.csv", "w") as f:
    f.writelines(output)