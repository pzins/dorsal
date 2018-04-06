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
from cbid_cuda import correlation_cbid


# Add the input trace to the collection
collection = btr.TraceCollection()
directory = "/home/pierre/lttng-traces"
path = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)

collection.add_trace(path + "/ust/uid/1000/64-bit", 'ctf')

# Set the output trace
out_path = "/home/pierre/out_traces"
writer = btw.Writer(out_path)

clock = btw.Clock('monotonic')
clock.description = 'Monotonic clock from AMD RCP'
# clock.offset = 1511453049028864041
writer.add_clock(clock)

writer.add_environment_field("hostname", "pierre")
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

# Create events, based on event classes

init_time = None
cntol = 0
events = defaultdict(list)


driver_dic, runtime_dic = correlation_cbid()

for r_event in collection.events:
    name = r_event.name
    event_time = r_event.timestamp
    w_event = btw.Event(event_classes[name])

    fields = r_event.field_list_with_scope(babeltrace.common.CTFScope.EVENT_FIELDS)
    w_event = btw.Event(event_classes[name])


    for f in fields:
        # print(name, f, r_event[f])
        w_event.payload(f).value = r_event[f]


    if "cuptiTracer:kernel" in name or "cuptiTracer:memcpy" in name:
        event_time = r_event["timestamp"] * 1000

    if "cuptiTracer:runtime" in name:
        w_event.payload("name").value = runtime_dic[r_event["name"]]
        event_time = r_event["timestamp"]
    if "cuptiTracer:driver" in name:
        w_event.payload("name").value = driver_dic[r_event["name"]]
        event_time = r_event["timestamp"]


    # organize threads
    threadId = r_event.field_with_scope("vtid", babeltrace.common.CTFScope.STREAM_EVENT_CONTEXT)

    if event_time in events:
        print("timestamp already exists")
        cntol += 1

    events[event_time].append([w_event, threadId])
    continue


    # organize threads
    threadId = r_event.field_with_scope("vtid", babeltrace.common.CTFScope.STREAM_EVENT_CONTEXT)
    if "tensorflowTracer:session" in name:
        threadId = 1000
    elif "tensorflowTracer:process" in name:
        threadId = 1001
    elif "tensorflowTracer:inline_ready" in name:
        threadId = 1002
    elif "tensorflowTracer:push_succ" in name:
        threadId = 1003

    elif "operation" in name:
        if "gpu" in r_event["placement"]:
            if "async" not in name:
                threadId = 2000
            else:
                threadId = 2001
        else:
            if "async" not in name:
                threadId = 2003
            else:
                threadId = 2002
    elif "cuptiTracer" in name:
        if "driver" in name:
            threadId = 3000
        elif "runtime" in name:
            threadId = 3001
        elif "kernel" in name:
            threadId = 3002
        else: #memcpy
            threadId = 3003
    elif "tensorflowTracer:do_create" in name or "tensorflowTracer:cleanup" in name:
        threadId = 4000
    else:
        threadId = 5000

    events[event_time] = [w_event, threadId]



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
