# analyse CTF traces
# only works for sequential events like hcc kernels, sync operations TF, sessions runs, ...
# All this script consider only TF synchronous GPU operation, as asynchronous
# operations are almost only Tensor copy and reception, and cpu operation don't
# launch GPU kernels

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

# save all the states of the trace
states = []

# define the start and end events we want to analyse
begin_event = 'tensorflowTracer:operation_start'
end_event = 'tensorflowTracer:operation_end'

begin_regex = re.compile(begin_event)
end_regex = re.compile(end_event)
enqueue_regex = re.compile("hsa_runtime:aql_kernel_dispatch_packet_submitted")

# unique id also to link begin and end events together
unique_id = "name"

# list containing temporary State with only start event set, waiting for a 
# corresponding end event
open_state = []

# list of tuple (TF_operation_name, GPU_kernel_name)
kernel_tfop = []

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
    
    # if we reach an enqueue call
    if re.match(enqueue_regex, name):
        # Skip memset kernel as there is no corresponding TF operation
        if "Memset" in r_event["kernel_name"]:
            continue
        # Link with the current TF operation
        if len(open_state) == 0:
            kernel_tfop.append((states[-1].begin_event["name"], r_event["kernel_name"]))
        # Link with the just finished TF operation
        else:
            kernel_tfop.append((open_state[-1].begin_event["name"], r_event["kernel_name"]))
            
        
# sort the State according to their duration
states.sort(key=lambda x: x.timestamps[1] - x.timestamps[0], reverse=True)

# rewrite the trace by changing the tf_name field
print("Start writing the traces")


# Set the output trace
out_path = "/home/pierre/queue_traces"
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

events = defaultdict(list)

# We have a list with all the enqueue call and the corresponding TF operation
# to do the link between TF operation and kernel execution, just use the index
# of the kernel_tfop list and the counter cnt_kernel when iterating over the 
# hcTracer:kernel events
cnt_kernel = 0

for r_event in collection.events:
    name = r_event.name
    event_time = r_event.timestamp
    w_event = btw.Event(event_classes[name])

    fields = r_event.field_list_with_scope(babeltrace.common.CTFScope.EVENT_FIELDS)
    w_event = btw.Event(event_classes[name])

    for f in fields:
        # if hcTracer:kernel_* : fill the grid and groupworker arrays
        if f == "workgroup_size" or f == "grid_size":
            for i in range(3):
                tmp = w_event.payload(f).field(i)
                tmp.value = r_event[f][i]
            continue
        
        # if we have a hcTracer:kernel_ event, get the name of the 
        # corresponding TF operation, and set it in the tf_name field
        # again we need to skip Memset, because there are no corresponding 
        # TF operation
        if f == "tf_name" and "hcTracer:kernel" in name and "Memset" not in r_event["name"]:
            # need to divide by 2, because we deal with start and end events
            # print(int(cnt_kernel/2), len(kernel_tfop), r_event["name"] )
            w_event.payload(f).value = kernel_tfop[int(cnt_kernel/2)][0]
            cnt_kernel += 1
            continue

        w_event.payload(f).value = r_event[f]

    threadId = r_event.field_with_scope("vtid", babeltrace.common.CTFScope.STREAM_EVENT_CONTEXT)
    events[event_time].append([w_event, threadId])

# Append events to the stream
timestamps = list(events.keys())
timestamps.sort()

for timestamp in timestamps:
    clock.time = timestamp
    for i in range(len(events[timestamp])):
        ev = events[timestamp][i][0]
        ev.tid(events[timestamp][i][1])
        # print(timestamp)
        main_stream.append_event(ev)

# Flush the stream
main_stream.flush()
