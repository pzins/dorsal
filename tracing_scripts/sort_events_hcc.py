
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
clock_offset = 1523055627781584997 # third computer
clock_offset = 1523380531878303029 # first computer
save_barrier_time = 0
cnt_incoherent_barrier = 0

init_time = 0
pool_memory_allocate_events = {}

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

    # save pool_memory_allocate events
    if "hsaTracer:pool_memory_allocate" in name:
        pool_memory_allocate_events[r_event["ptr"]] = [r_event["size"], r_event["handle"]]
    if "hsaTracer:pool_memory_free" in name:
        if r_event["ptr"] in pool_memory_allocate_events:
            w_event.payload("size").value = pool_memory_allocate_events[r_event["ptr"]][0] * -1
            w_event.payload("handle").value = pool_memory_allocate_events[r_event["ptr"]][1]

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

hc_kernels = []
hc_copy = []
hc_barrier = []

with open("/home/pierre/tf_examples/hc_out", "r") as f:
    lines = f.readlines()
    for l in lines:
        if l[:7] == "profile":
            fields = l.split(";")
            element_type = fields[0].split()[-1]
            name = fields[1].strip()
            duration = float(fields[2].split()[0])
            start = int(fields[3]) + clock_offset
            end = int(fields[4]) + clock_offset
            id_ = fields[5]
            if "kernel" in element_type:
                hc_kernels.append([name, duration, start, end, id_])
            if "barrier" in element_type:
                hc_barrier.append([name, duration, start, end, id_])
            if "copy" in element_type:
                size_bytes = int(fields[6].split()[0])
                size_mb = float(fields[7].split()[0])
                bandwith = float(fields[8].split()[0])
                hc_copy.append([element_type, name, duration, start, end, size_bytes, size_mb, bandwith])




threadId = 181818
for i in hc_kernels:
    w_event = btw.Event(event_classes["hccTracer:kernel2_begin"])
    w_event.payload("cat").value = "hcc"
    w_event.payload("name").value = i[0]
    w_event.payload("tf_name").value = ""
    w_event.payload("id").value = i[4]
    w_event.payload("timestamp").value = i[2]
    events[i[2]].append([w_event, threadId])

    w_event = btw.Event(event_classes["hccTracer:kernel2_end"])
    w_event.payload("cat").value = "hcc"
    w_event.payload("name").value = i[0]
    w_event.payload("tf_name").value = ""
    w_event.payload("id").value = i[4]
    w_event.payload("timestamp").value = i[3]
    events[i[3]].append([w_event, threadId])

for i in hc_barrier:
    w_event = btw.Event(event_classes["hccTracer:barrier2_begin"])
    w_event.payload("cat").value = "hcc"
    w_event.payload("name").value = i[0]
    w_event.payload("id").value = i[4]
    w_event.payload("timestamp").value = i[2]
    events[i[2]].append([w_event, threadId])

    w_event = btw.Event(event_classes["hccTracer:barrier2_end"])
    w_event.payload("cat").value = "hcc"
    w_event.payload("name").value = i[0]
    w_event.payload("id").value = i[4]
    w_event.payload("timestamp").value = i[3]
    events[i[3]].append([w_event, threadId])

for i in hc_copy:
    if i[0] == "copy":
        w_event_begin = btw.Event(event_classes["hccTracer:async_memcpy2_begin"])
        w_event_end = btw.Event(event_classes["hccTracer:async_memcpy2_end"])
    else:
        w_event_begin = btw.Event(event_classes["hccTracer:async_memcpyslo2_begin"])
        w_event_end = btw.Event(event_classes["hccTracer:async_memcpyslo2_end"])

    w_event_begin.payload("cat").value = "hcc"
    w_event_begin.payload("name").value = i[1]
    w_event_begin.payload("timestamp").value = i[4]
    w_event_begin.payload("size_bytes").value = i[5]
    w_event_begin.payload("size_megabytes").value = i[6]
    w_event_begin.payload("throughput").value = i[7]
    events[i[3]].append([w_event_begin, threadId])

    w_event_end.payload("cat").value = "hcc"
    w_event_end.payload("name").value = i[1]
    w_event_end.payload("timestamp").value = i[4]
    w_event_end.payload("size_bytes").value = i[5]
    w_event_end.payload("size_megabytes").value = i[6]
    w_event_end.payload("throughput").value = i[7]
    events[i[4]].append([w_event_end, threadId])

# Append events to the stream
timestamps = list(events.keys())
timestamps.sort()

for timestamp in timestamps:
    clock.time = timestamp
    for i in range(len(events[timestamp])):
        ev = events[timestamp][i][0]
        # print(timestamp)
        ev.tid(events[timestamp][i][1])
        main_stream.append_event(ev)

# Flush the stream
main_stream.flush()
