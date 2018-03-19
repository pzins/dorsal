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
clock_offset = 1519939145097366944 # first computer

# save all the states of the trace
states = []

# define the start and end events we want to analyse
begin_event = "tensorflowTracer:session_start"
end_event = "tensorflowTracer:session_end"

begin_event = 'hccTracer:kernel_begin'
end_event = 'hccTracer:kernel_end'

begin_event = "tensorflowTracer:operation_start"
end_event = "tensorflowTracer:operation_end"

begin_regex = re.compile(begin_event)
end_regex = re.compile(end_event)

# unique id also to link begin and end events together
unique_id = "count"
unique_id = "name"

# list containing temporary State with only start event set, waiting for a 
# corresponding end event
open_state = []

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

for r_event in collection.events:
    name = r_event.name
    
    # begin event
    if re.match(begin_regex, name):
        s = State(r_event)
        open_state.append(s)

    # end event
    if re.match(end_regex, name):
        matching_index = -1
        # find a waiting state
        for i in range(len(open_state)):
            if open_state[i].isMatchingEndEvent(r_event, unique_id):
                open_state[i].setEndEvent(r_event)
                open_state[i].setEndTimestamp(r_event.timestamp)
                matching_index = i
                break
        
        # if no waiting state correspond to an end event. Not possible, so 
        # we have errors
        if matching_index == -1:
            print("Error no matching event, for this end")
            exit(1)
        
        states.append(open_state[matching_index])
        del open_state[matching_index]
        
# sort the State according to their duration
states.sort(key=lambda x: x.timestamps[1] - x.timestamps[0], reverse=True)

# print
for i in states:
    print(i.timestamps, i.begin_event["name"], i.timestamps[1] - i.timestamps[0])
    input()
