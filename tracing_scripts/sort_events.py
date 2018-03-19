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



# Add the input trace to the collection
collection = btr.TraceCollection()
directory = "/home/pierre/lttng-traces"
path = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)
# path = "/home/pierre/lttng-traces/tensorflow-20180312-101756"
collection.add_trace(path + "/ust/uid/1000/64-bit", 'ctf')

# Set the output trace
out_path = "/home/pierre/out_traces"
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
clock_offset = 1520551794904150339 # first computer
save_barrier_time = 0
cnt_incoherent_barrier = 0

init_time = 0
for r_event in collection.events:
    name = r_event.name
    event_time = r_event.timestamp
    w_event = btw.Event(event_classes[name])

    fields = r_event.field_list_with_scope(babeltrace.common.CTFScope.EVENT_FIELDS)
    w_event = btw.Event(event_classes[name])

    for f in fields:
        # print(name, f, r_event[f])
        if r_event[f] == "hsa_init":
            init_time = event_time

        # if hccTracer:kernel_* : fill the grid and groupworker arrays
        if f == "workgroup_size" or f == "grid_size":
            for i in range(3):
                tmp = w_event.payload(f).field(i)
                tmp.value = r_event[f][i]
            continue

        w_event.payload(f).value = r_event[f]

    if "hsa_runtime:kernel" in name:
        if init_time == 0:
            print("Error, hsa_init not called before kernel")
            exit(0)
        event_time = r_event["timestamp"] + init_time

    if "hccTracer:kernel" in name or "hccTracer:async" in name or "hccTracer:barrier" in name:
        event_time = r_event["timestamp"] + clock_offset
        if save_barrier_time == 0:
            save_barrier_time = r_event["timestamp"]
        if "barrier" in name:
            # if time between last barrier and this barrier time (start or end) we skip it
            if abs(r_event["timestamp"] - save_barrier_time) > 1000000000 * 120:
                print("barrier incoherent time")
                cnt_incoherent_barrier += 1
                continue
            save_barrier_time = r_event["timestamp"]



    # organize threads
    threadId = r_event.field_with_scope("vtid", babeltrace.common.CTFScope.STREAM_EVENT_CONTEXT)

    # if "grpcTracer:test" in name:
        # threadId = 1111

    # if "RecvTensor" in name:
    #     threadId = 1111
    # elif "grpc" in name:
    #     continue
    # do not change vtid
    # events[event_time-1519157918746548549] = [w_event, threadId]
    if event_time in events:
        print("timestamp already exists")
        cntol += 1

    events[event_time].append([w_event, threadId])
    continue

    if "tensorflowTracer:session" in name or "tensorflowTracer:process" in name or "tensorflowTracer:inline_ready" in name or "tensorflowTracer:push_succ" in name:
        threadId = 1
    elif "operation" in name:
        if "gpu" in r_event["placement"]:
            if "async" not in name:
                threadId = 31
            else:
                threadId = 32
        else:
            if "async" not in name:
                threadId = 21
            else:
                threadId = 22
    elif "hsaTracer" in name:
        threadId = 4
    elif "hipTracer" in name:
        threadId = 5
    elif "hccTracer" in name:
        if "unpinned_memory_engine_copy" in name:
            threadId = 6
        else:
            threadId = 7
    elif "alloc" in name:
        threadId = 8
    elif "tensorflowTracer:do_create" in name or "tensorflowTracer:cleanup" in name:
        threadId = 9
    elif "grpcTracer" in name:
        if "RecvTensor" in name:
            threadId = 98
        elif "GetStatus" in r_event["name"]:
            threadId = 90
        elif "RegisterGraph" in r_event["name"]:
            threadId = 91
        elif "DeregisterGraph" in r_event["name"]:
            threadId = 92
        elif "RunGraph" in r_event["name"]:
            threadId = 93
        elif "CleanupGraph" in r_event["name"]:
            threadId = 94
        elif "CleanupAll" in r_event["name"]:
            threadId = 95
        elif "Logging" in r_event["name"]:
            threadId = 96
        elif "Tracing" in r_event["name"]:
            threadId = 97
        else:
            threadId = 99
    else:
        threadId = 99999

    events[event_time] = [w_event, threadId]
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
