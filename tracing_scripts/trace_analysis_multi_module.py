# analyse CTF traces
# only works for sequential events like hcc kernels, sync operations TF, sessions runs, ...

#!/usr/bin/python3
import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import re
import argparse

# parse arguments
parser = argparse.ArgumentParser(description="Compute statistics")
parser.add_argument("--trace", help="set the input trace", required=True)
parser.add_argument("--output", help="set the output csv file")
args = parser.parse_args()


if args.output == None:
    outfile = "stats.csv"
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



# represent one Analysis : like tf operations, hcc kernels, session runs, ...
class Module():
    def __init__(self, name, begin, end, unique_id):
        self.name = name
        # begin and end event regex
        self.begin_event = re.compile(begin)
        self.end_event = re.compile(end)
        
        # unique id to do the link between start and end events
        self.unique_id = unique_id
        
        # will contain all the states from the trace
        self.states = []
        # list containing temporary State with only start event set, waiting for a 
        # corresponding end event
        self.open_state = []
    def states_size(self):
        return len(self.states)
        
# Represent a State from ctf events
class State():
    def __init__(self):
        self.begin_event = 0
        self.end_event = 0
        self.timestamps = [0, 0]
        self.session = 0
    def __init__(self, begin_ev):
        self.begin_event = begin_ev
        self.end_event = 0
        self.timestamps = [begin_ev.timestamp, 0]
        self.session = 0
    def setSession(self, sess):
        self.session = sess
    def setBeginEvent(self, ev):
        self.begin_event = ev
    def setEndEvent(self, ev):
        self.end_event = ev
    def setBeginTimestamp(self, tt):
        self.timestamps[0] = tt
    def setEndTimestamp(self, tt):
        self.timestamps[1] = tt
    def isMatchingEndEvent(self, end_event, unique_id):
        if self.begin_event == 0:
            return False
        return self.begin_event[unique_id] == end_event[unique_id]        

# define the modules we want
modules = [
            Module("sessions", "tensorflowTracer:session_start", "tensorflowTracer:session_end", "count"),
            Module("kernels", "hcTracer:kernel_begin", "hcTracer:kernel_end", "name"),
            Module("operations", "tensorflowTracer:operation_start", "tensorflowTracer:operation_end", "name")
          ]

# loop over the events
for r_event in collection.events:
    name = r_event.name
    # loop over the modules
    for mod in modules:
        # begin test of the module
        if re.match(mod.begin_event, name):
            s = State(r_event)
            s.setSession(modules[0].states_size() + 1)
            mod.open_state.append(s)

        # end test of the module
        if re.match(mod.end_event, name):
            matching_index = -1
            # find a waiting state
            for i in range(len(mod.open_state)):
                if mod.open_state[i].isMatchingEndEvent(r_event, mod.unique_id):
                    mod.open_state[i].setEndEvent(r_event)
                    mod.open_state[i].setEndTimestamp(r_event.timestamp)
                    mod.open_state[i].setSession(modules[0].states_size() + 1)
                    matching_index = i
                    break
        
            # if no waiting state correspond to an end event. Not possible, so 
            # we have errors
            if matching_index == -1:
                print("Error no matching event, for this end")
                exit(1)
            
            mod.states.append(mod.open_state[matching_index])
            del mod.open_state[matching_index]

# sort the State according to their duration for each module
for mod in modules:
    mod.states.sort(key=lambda x: x.timestamps[1] - x.timestamps[0], reverse=True)



skip_sessions = [1, 2]
with open(outfile, "w") as f:
    # print
    f.write("begin_timestamp;end_timestamp;name;duration;session\n")
    for mod in modules:
        f.write("\n\n")
        for i in mod.states:
            if i.session in skip_sessions:
                continue
            if "kernels" in mod.name:
                f.write(str(i.timestamps[0]) + ";" + str(i.timestamps[1]) + ";"\
                        + i.begin_event["tf_name"] + ";" + str(i.timestamps[1]\
                        - i.timestamps[0]) + ";" + str(i.session) + "\n")
                # print(i.timestamps, i.begin_event["tf_name"], i.timestamps[1] - i.timestamps[0])
            else:
                f.write(str(i.timestamps[0]) + ";" + str(i.timestamps[1]) + ";"\
                        + i.begin_event["name"] + ";" + str(i.timestamps[1] - \
                        i.timestamps[0]) + ";" + str(i.session) + "\n")
                # print(i.timestamps, i.begin_event["name"], i.timestamps[1] - i.timestamps[0])
            # input()
