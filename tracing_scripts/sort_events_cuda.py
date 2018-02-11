#!/usr/bin/python3
import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import sys
from collections import defaultdict

# Create field declarations

# Field declarations
uint64_fd = btw.IntegerFieldDeclaration(64)
uint64_fd.signed = False

uint32_fd = btw.IntegerFieldDeclaration(32)
uint32_fd.signed = False

huint64_fd = btw.IntegerFieldDeclaration(64)
huint64_fd.base = babeltrace.writer.IntegerBase.HEX
huint64_fd.signed = False

string_fd = btw.StringFieldDeclaration()

# Create event classes

def event_classes_factory():
    other_event_class = btw.EventClass('hsa_runtime:other_event')
    other_event_class.add_field(string_fd, 'name')
    return other_event_class

event_classes = {}

# cuptiTracer
event_classes['cuptiTracer:runtime_api_entry'] = btw.EventClass('cuptiTracer:runtime_api_entry')
event_classes['cuptiTracer:runtime_api_entry'].add_field(uint64_fd, 'timestamp')
event_classes['cuptiTracer:runtime_api_entry'].add_field(uint64_fd, 'is_ready')

event_classes['cuptiTracer:runtime_api_exit'] = btw.EventClass('cuptiTracer:runtime_api_exit')
event_classes['cuptiTracer:runtime_api_exit'].add_field(uint64_fd, 'timestamp')
event_classes['cuptiTracer:runtime_api_exit'].add_field(uint64_fd, 'is_ready')

event_classes['cuptiTracer:driver_api_entry'] = btw.EventClass('cuptiTracer:driver_api_entry')
event_classes['cuptiTracer:driver_api_entry'].add_field(uint64_fd, 'timestamp')
event_classes['cuptiTracer:driver_api_entry'].add_field(uint64_fd, 'is_ready')

event_classes['cuptiTracer:driver_api_exit'] = btw.EventClass('cuptiTracer:driver_api_exit')
event_classes['cuptiTracer:driver_api_exit'].add_field(uint64_fd, 'timestamp')
event_classes['cuptiTracer:driver_api_exit'].add_field(uint64_fd, 'is_ready')

event_classes['cuptiTracer:kernel_begin'] = btw.EventClass('cuptiTracer:kernel_begin')
event_classes['cuptiTracer:kernel_begin'].add_field(string_fd, 'name')
event_classes['cuptiTracer:kernel_begin'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:kernel_end'] = btw.EventClass('cuptiTracer:kernel_end')
event_classes['cuptiTracer:kernel_end'].add_field(string_fd, 'name')
event_classes['cuptiTracer:kernel_end'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:memcpy_begin'] = btw.EventClass('cuptiTracer:memcpy_begin')
event_classes['cuptiTracer:memcpy_begin'].add_field(string_fd, 'name')
event_classes['cuptiTracer:memcpy_begin'].add_field(string_fd, 'details')
event_classes['cuptiTracer:memcpy_begin'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:memcpy_end'] = btw.EventClass('cuptiTracer:memcpy_end')
event_classes['cuptiTracer:memcpy_end'].add_field(string_fd, 'name')
event_classes['cuptiTracer:memcpy_end'].add_field(string_fd, 'details')
event_classes['cuptiTracer:memcpy_end'].add_field(uint64_fd, 'timestamp')

# tensorflowTracer
event_classes['tensorflowTracer:process_entry'] = btw.EventClass('tensorflowTracer:process_entry')
event_classes['tensorflowTracer:process_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:process_exit'] = btw.EventClass('tensorflowTracer:process_exit')
event_classes['tensorflowTracer:process_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:inline_ready_entry'] = btw.EventClass('tensorflowTracer:inline_ready_entry')
event_classes['tensorflowTracer:inline_ready_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:inline_ready_exit'] = btw.EventClass('tensorflowTracer:inline_ready_exit')
event_classes['tensorflowTracer:inline_ready_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:push_succ_entry'] = btw.EventClass('tensorflowTracer:push_succ_entry')
event_classes['tensorflowTracer:push_succ_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:push_succ_exit'] = btw.EventClass('tensorflowTracer:push_succ_exit')
event_classes['tensorflowTracer:push_succ_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:push_succ_exit'].add_field(uint64_fd, 'is_ready')

event_classes['tensorflowTracer:session_start'] = btw.EventClass('tensorflowTracer:session_start')
event_classes['tensorflowTracer:session_start'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:session_end'] = btw.EventClass('tensorflowTracer:session_end')
event_classes['tensorflowTracer:session_end'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:operation_start'] = btw.EventClass('tensorflowTracer:operation_start')
event_classes['tensorflowTracer:operation_start'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:operation_end'] = btw.EventClass('tensorflowTracer:operation_end')
event_classes['tensorflowTracer:operation_end'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:allocate_chunk_entry'] = btw.EventClass('tensorflowTracer:allocate_chunk_entry')
event_classes['tensorflowTracer:allocate_chunk_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:allocate_chunk_exit'] = btw.EventClass('tensorflowTracer:allocate_chunk_exit')
event_classes['tensorflowTracer:allocate_chunk_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:allocate_raw_internal_entry'] = btw.EventClass('tensorflowTracer:allocate_raw_internal_entry')
event_classes['tensorflowTracer:allocate_raw_internal_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:allocate_raw_internal_exit'] = btw.EventClass('tensorflowTracer:allocate_raw_internal_exit')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:deallocate_raw_internal_entry'] = btw.EventClass('tensorflowTracer:deallocate_raw_internal_entry')
event_classes['tensorflowTracer:deallocate_raw_internal_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:deallocate_raw_internal_exit'] = btw.EventClass('tensorflowTracer:deallocate_raw_internal_exit')
event_classes['tensorflowTracer:deallocate_raw_internal_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:do_create_entry'] = btw.EventClass('tensorflowTracer:do_create_entry')
event_classes['tensorflowTracer:do_create_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:do_create_exit'] = btw.EventClass('tensorflowTracer:do_create_exit')
event_classes['tensorflowTracer:do_create_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:cleanup_entry'] = btw.EventClass('tensorflowTracer:cleanup_entry')
event_classes['tensorflowTracer:cleanup_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:cleanup_exit'] = btw.EventClass('tensorflowTracer:cleanup_exit')
event_classes['tensorflowTracer:cleanup_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:gpu_bfc_alloc_entry'] = btw.EventClass('tensorflowTracer:gpu_bfc_alloc_entry')
event_classes['tensorflowTracer:gpu_bfc_alloc_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:gpu_bfc_alloc_exit'] = btw.EventClass('tensorflowTracer:gpu_bfc_alloc_exit')
event_classes['tensorflowTracer:gpu_bfc_alloc_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:gpu_device_compute_entry'] = btw.EventClass('tensorflowTracer:gpu_device_compute_entry')
event_classes['tensorflowTracer:gpu_device_compute_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:gpu_device_compute_entry'].add_field(uint64_fd, 'is_ready')
event_classes['tensorflowTracer:gpu_device_compute_exit'] = btw.EventClass('tensorflowTracer:gpu_device_compute_exit')
event_classes['tensorflowTracer:gpu_device_compute_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:gpu_device_compute_exit'].add_field(uint64_fd, 'is_ready')




# Add the input trace to the collection
collection = btr.TraceCollection()
collection.add_trace("/home/pierre/lttng-traces/all-20180210-223215/ust/uid/1000/64-bit", 'ctf')

# Set the output trace
out_path = "/home/pierre/dev/out_traces"
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
events = {}

for r_event in collection.events:
    name = r_event.name
    event_time = r_event.timestamp
    w_event = btw.Event(event_classes[name])

    if "hsaTracer" in name or "hipTracer" in name or "tensorflowTracer" in name:
        if "push_succ_exit" in name or "gpu_device_compute" in name:
            w_event = btw.Event(event_classes[name])
            w_event.payload('name').value = r_event['name']
            w_event.payload('is_ready').value = r_event['is_ready']
        else:
            w_event = btw.Event(event_classes[name])
            w_event.payload('name').value = r_event['name']
            # print("tf  ", event_time)

    elif "cuptiTracer" in name:
        if "api" in name:
            w_event = btw.Event(event_classes[name])
            w_event.payload('is_ready').value = r_event['is_ready']
            w_event.payload('timestamp').value = r_event['timestamp']
            event_time = r_event['timestamp']
            # print("cupti   ", r_event['timestamp'])


        elif "kernel" in name:
            w_event = btw.Event(event_classes[name])
            w_event.payload('name').value = r_event['name']
            w_event.payload('timestamp').value = r_event['timestamp']
            event_time = r_event['timestamp']*1000
        elif "memcpy" in name:
            w_event = btw.Event(event_classes[name])
            w_event.payload('name').value = r_event['name']
            w_event.payload('details').value = r_event['details']
            w_event.payload('timestamp').value = r_event['timestamp']
            event_time = r_event['timestamp']*1000

    events[event_time] = [w_event, r_event.field_with_scope("vtid", 3)]

    # else:
        # w_event.payload('name').value = name
# Append events to the stream
timestamps = list(events.keys())
timestamps.sort()

for timestamp in timestamps:
    clock.time = timestamp
    ev = events[timestamp][0]
    ev.tid(events[timestamp][1])
    main_stream.append_event(ev)
    # input()

# Flush the stream
main_stream.flush()
