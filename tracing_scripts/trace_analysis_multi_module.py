# analyse CTF traces
# only works for sequential events like hcc kernels, sync operations TF, sessions runs, ...

#!/usr/bin/python3
import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
from tracing_events_classes import event_classes
from collections import defaultdict
import re

# Add the input trace to the collection
collection = btr.TraceCollection()
directory = "/home/pierre/out_traces"
collection.add_trace(directory, 'ctf')
clock_offset = 1523311163488553312 # first computer

# represent one Analysis : like tf operations, hcc kernels, session runs, ...
class Module():
    def __init__(self, begin, end, unique_id):
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
        
# Represent a State from ctf events
class State():
    def __init__(self):
        self.begin_event = 0
        self.end_event = 0
        self.timestamps = [0, 0]
    def __init__(self, begin_ev):
        self.begin_event = begin_ev
        self.end_event = 0
        self.timestamps = [begin_ev.timestamp, 0]
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
modules =   [
            Module("tensorflowTracer:session_start", "tensorflowTracer:session_end", "count"),
            Module("hccTracer:kernel2_begin", "hccTracer:kernel_end", "name"),
            Module("tensorflowTracer:operation_start", "tensorflowTracer:operation_end", "name")
            ]


# loop over the events
for r_event in collection.events:
    name = r_event.name
    
    # loop over the modules
    for mod in modules:
        # begin test of the module
        if re.match(mod.begin_event, name):
            s = State(r_event)
            mod.open_state.append(s)

        # end test of the module
        if re.match(mod.end_event, name):
            matching_index = -1
            # find a waiting state
            for i in range(len(mod.open_state)):
                if mod.open_state[i].isMatchingEndEvent(r_event, mod.unique_id):
                    mod.open_state[i].setEndEvent(r_event)
                    mod.open_state[i].setEndTimestamp(r_event.timestamp)
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

# print
for mod in modules:
    for i in mod.states:
        print(i.timestamps, i.begin_event["name"], i.timestamps[1] - i.timestamps[0])
        input()
