import json
from pprint import pprint
from decimal import *

import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import tempfile
import pdb

# mapping address resolution
# ==============================================================================
mapping = {}
# base = int("00007effe17e6000", 16) # base address of the process
base = int("00007f020a7a8000", 16) # base address of the process


# read library symbols
with open("libSymbols","r") as f:
    lines = f.readlines()
    for line in lines:
        tmp = line.strip().split()
        # if it doesn't start with an address continue next
        if not tmp[0][0] == "0":
            continue
        # get the address
        a = int(tmp[0],16)
        
        # print(a)
        # print(base)
        # print('0x{0:02x}'.format(a+base))
        # print(tmp[0], '0x{0:02x}'.format(a+base))
        # print(line)
        # add the line in mapping with the address as key
        
        # if a+base in mapping:
            # print("ERASE", line)
        mapping[a+base] = line.strip()
        
# for i in mapping:
#     if "Process" in mapping[i]:
#         print(i, mapping[i])
#     input(2)
# exit(0)
# ==============================================================================




# prepare ctf writer
# ==============================================================================
# temporary directory holding the CTF trace
trace_path = tempfile.mkdtemp()
trace_path = "/home/pierre/outout"
print('trace path: {}'.format(trace_path))


# our writer
writer = btw.Writer(trace_path)

# create one default clock and register it to the writer
clock = btw.Clock('my_clock')
clock.description = 'Monotonic clock from AMD RCP'
clock.offset = 1511359944029031455
writer.add_clock(clock)

writer.add_environment_field("hostname", "pierre-tensorflow")
writer.add_environment_field("domain", "ust")
writer.add_environment_field("tracer_name", "lttng-ust")
writer.add_environment_field("tracer_major", 2)
writer.add_environment_field("tracer_minor", 7)

# create one default stream class and assign our clock to it
stream_class = btw.StreamClass('my_stream')
stream_class.clock = clock

uint64_fd = btw.IntegerFieldDeclaration(64)
uint64_fd.signed = False

huint64_fd = btw.IntegerFieldDeclaration(64)
huint64_fd.base = babeltrace.writer.IntegerBase.HEX
huint64_fd.signed = False

string_fd = btw.StringFieldDeclaration()
string_fd.encoding = babeltrace.common.CTFStringEncoding.UTF8

function_entry_class = btw.EventClass('lttng_ust_cyg_profile:func_entry')
function_entry_class.add_field(string_fd, "name")
function_entry_class.add_field(huint64_fd, "addr")
function_entry_class.add_field(huint64_fd, "call_site")
function_entry_class.add_field(uint64_fd, "cpu_id")

function_exit_class = btw.EventClass('lttng_ust_cyg_profile:func_exit')
function_exit_class.add_field(string_fd, "name")
function_exit_class.add_field(huint64_fd, "addr")
function_exit_class.add_field(huint64_fd, "call_site")
function_exit_class.add_field(uint64_fd, "cpu_id")

stream_class.add_event_class(function_entry_class)
stream_class.add_event_class(function_exit_class)
stream = writer.create_stream(stream_class)
# ==============================================================================

# ctf reader + write the new one
# ==============================================================================
# get the trace path from the first command line argument
# trace_path = "/home/pierre/lttng-traces/auto-20171116-182928"
trace_path = "/home/pierre/lttng-traces/finstrument-20171122-155917"

trace_collection = babeltrace.TraceCollection()
trace_collection.add_traces_recursive(trace_path, 'ctf')

cnt = 0
for i in trace_collection.events:
    
    # create the right Event
    if "entry" in i.name:
        event = btw.Event(function_entry_class)
    else:
        event = btw.Event(function_exit_class)
    # add payload
    event.payload("addr").value = i.get("addr")
    event.payload("call_site").value = i.get("call_site")
    
    # check if the address is resolved
    if i.get("addr") in mapping:
        event.payload("name").value = mapping[i.get("addr")]
    else:
        event.payload("name").value = "ERROR"
    event.payload("cpu_id").value = i.get("cpu_id")

    clock.time = i.timestamp
    event.tid(i.get("vtid"))
    stream.append_event(event)

    # stop before the end, otherwise too long
    if cnt > 100000:
        break
    cnt += 1
    
    
# write the new trace
stream.flush()                   