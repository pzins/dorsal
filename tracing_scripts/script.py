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

# hipTracer
event_classes['function_entry'] = btw.EventClass('hsaTracer:function_entry')
event_classes['function_entry'].add_field(string_fd, 'name')

event_classes['function_exit'] = btw.EventClass('hsaTracer:function_exit')
event_classes['function_exit'].add_field(string_fd, 'name')


# hsaTracer


event_classes['kernel_begin'] = btw.EventClass('hccTracer:kernel_begin')
event_classes['kernel_begin'].add_field(string_fd, 'name')
event_classes['kernel_begin'].add_field(uint64_fd, 'timestamp')


event_classes['kernel_end'] = btw.EventClass('hccTracer:kernel_end')
event_classes['kernel_end'].add_field(string_fd, 'name')
event_classes['kernel_end'].add_field(uint64_fd, 'timestamp')

event_classes['begin'] = btw.EventClass('hipTracer:begin')
event_classes['begin'].add_field(string_fd, 'name')
event_classes['end'] = btw.EventClass('hipTracer:end')
event_classes['end'].add_field(string_fd, 'name')







# Add the input trace to the collection
collection = btr.TraceCollection()
collection.add_trace("/home/pierre/lttng-traces/lkz2-20180209-162642/ust/uid/1000/64-bit", 'ctf')

# Set the output trace
out_path = "/home/pierre/out_traces"
writer = btw.Writer(out_path)

clock = btw.Clock('monotonic')
clock.description = 'Monotonic clock from AMD RCP'
# clock.offset = 1511453049028864041
writer.add_clock(clock)

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

# Create events, based on event classes

init_time = None
events = {}

for r_event in collection.events:
    name = r_event.name.split(':')[-1]
    event_time = r_event.timestamp
    w_event = btw.Event(event_classes[name])

    if name == 'hsa_init':
        init_time = event_time
        w_event = btw.Event(event_classes[name])
        w_event.payload('name').value = r_event['name']
        event_time = r_event['timestamp']
        events[event_time] = [w_event, r_event.field_with_scope("vtid", 3)]

    elif name == 'runtime_shut_down':
        pass

    elif name == 'function_entry':# or name == 'function_exit':
        # w_event.payload('name').value = r_event['name']
        if "hsa_init" == r_event['name']:
            init_time = event_time
            print("OL")
            w_event = btw.Event(event_classes[name])
            w_event.payload('name').value = r_event['name']
            # event_time = r_event['timestamp']
            
            events[event_time] = [w_event, r_event.field_with_scope("vtid", 3)]


    elif name == 'queue_created':
        w_event.payload('agent_handle').value = r_event['agent_handle']
        w_event.payload('queue_id').value = r_event['queue_id']

    elif name == 'queue_destroyed':
        w_event.payload('queue_id').value = r_event['queue_id']

    elif name == 'aql_kernel_dispatch_packet_submitted':
        w_event.payload('packet_id').value = r_event['packet_id']
        w_event.payload('agent_handle').value = r_event['agent_handle']
        w_event.payload('queue_id').value = r_event['queue_id']
        w_event.payload('kernel_object').value = r_event['kernel_object']
        w_event.payload('kernel_name').value = r_event['kernel_name']
    
    elif name == "begin" or name == "end":
        w_event = btw.Event(event_classes[name])
        w_event.payload('name').value = r_event['name']
        events[event_time] = [w_event, r_event.field_with_scope("vtid", 3)]
        
    elif name == 'kernel_begin' or name == 'kernel_end':
        w_event = btw.Event(event_classes[name])
        w_event.payload('name').value = r_event['name']
        w_event.payload('timestamp').value = r_event['timestamp']
        event_time =  1518106715746647446 + r_event['timestamp']
        print(r_event['timestamp'], init_time)

            
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
