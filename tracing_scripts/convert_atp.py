"""
convert ATP traces to CTF format
hsa API Trace Output and hsa Timestamp Output should be combined to get the API call
and the associated timestamp. They are split into thread sections. For each section
the lines in API Trace correspond to the lines in Timestamp.
One HSA API event should generate 2 ctf events : 1 entry + 1 exit
 
hsa Kernel Timestamp Output : no thread section. Just need to create 2 ctf events for 1
HSA Kernel event (begin + end)

Perfmarker Output : they are in separate files, 1 for each thread.
Already begin and end event => direct conversion into ctf event
"""

KERNEL_TID = 171717
DATA_TRANSFER_GPU_CPU = 171718
DATA_TRANSFER_CPU_GPU = 171719
DATA_TRANSFER_GPU_GPU = 171720
DATA_TRANSFER_CPU_CPU = 171721


import re
import sys
import pdb
import time

import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import tempfile
import codecs

# check arguments
if len(sys.argv) < 2:
    print("Usage : python3 convert_atp.py MAIN_TRACE.atp MARKER_TRACE_1 MARKER_TRACE_2 ...")
    exit(0)

# temporary directory holding the CTF trace
trace_path = tempfile.mkdtemp()
trace_path = "/home/pierre/out_ctf_mlp"
trace_path = "/home/pierre/out_ctf_cnn" # reserve for the use case cnn 1 iteration slow
trace_path = "/home/pierre/out_ctf_test_py"
trace_path = "/home/pierre/out_ctf"
print('trace path: {}'.format(trace_path))

# INITIALIZE CTF WRITER

writer = btw.Writer(trace_path)
# create one default clock and register it to the writer
clock = btw.Clock('monotonicO')
clock.description = 'Monotonic clock from AMD RCP'
clock.offset = 1511453049028864041
writer.add_clock(clock)

writer.add_environment_field("hostname", "pierre-tensorflow")
writer.add_environment_field("domain", "ust")
writer.add_environment_field("tracer_name", "lttng-ust")
writer.add_environment_field("tracer_major", 2)
writer.add_environment_field("tracer_minor", 7)

# create one default stream class and assign our clock to it
stream_class = btw.StreamClass('main_stream')
stream_class.clock = clock

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
event_classes = {}
event_classes["hsa_event:entry"] = btw.EventClass('hsa_event:entry')
event_classes["hsa_event:exit"] = btw.EventClass('hsa_event:exit')
event_classes["hsa_kernel:begin"] = btw.EventClass('hsa_kernel:begin')
event_classes["hsa_kernel:end"] = btw.EventClass('hsa_kernel:end')
event_classes["perfmarker:begin"] = btw.EventClass('perfmarker:begin')
event_classes["perfmarker:end"] = btw.EventClass('perfmarker:end')
event_classes["data_transfer:begin"] = btw.EventClass('data_transfer:begin')
event_classes["data_transfer:end"] = btw.EventClass('data_transfer:end')

# Add field for each event class
event_classes["hsa_event:entry"].add_field(string_fd, "name")
event_classes["hsa_event:entry"].add_field(string_fd, "args")
event_classes["hsa_event:entry"].add_field(string_fd, "result")
event_classes["hsa_event:entry"].add_field(uint32_fd, "api_type")

event_classes["hsa_event:exit"].add_field(string_fd, "name")
event_classes["hsa_event:exit"].add_field(string_fd, "args")
event_classes["hsa_event:exit"].add_field(string_fd, "result")
event_classes["hsa_event:exit"].add_field(uint32_fd, "api_type")


event_classes["hsa_kernel:begin"].add_field(string_fd, "name")
event_classes["hsa_kernel:begin"].add_field(string_fd, "handle")
event_classes["hsa_kernel:begin"].add_field(string_fd, "agentName")
event_classes["hsa_kernel:begin"].add_field(string_fd, "agentHandle")
event_classes["hsa_kernel:begin"].add_field(uint32_fd, "index")
event_classes["hsa_kernel:begin"].add_field(uint32_fd, "queueHandle")

event_classes["hsa_kernel:end"].add_field(string_fd, "name")
event_classes["hsa_kernel:end"].add_field(string_fd, "handle")
event_classes["hsa_kernel:end"].add_field(string_fd, "agentName")
event_classes["hsa_kernel:end"].add_field(string_fd, "agentHandle")
event_classes["hsa_kernel:end"].add_field(uint32_fd, "index")
event_classes["hsa_kernel:end"].add_field(uint32_fd, "queueHandle")

event_classes["perfmarker:begin"].add_field(string_fd, "name")
event_classes["perfmarker:begin"].add_field(string_fd, "category")
event_classes["perfmarker:end"].add_field(string_fd, "name")
event_classes["perfmarker:end"].add_field(string_fd, "category")

event_classes["data_transfer:begin"].add_field(string_fd, "name")
event_classes["data_transfer:begin"].add_field(uint64_fd, "size")
event_classes["data_transfer:end"].add_field(string_fd, "name")
event_classes["data_transfer:end"].add_field(uint64_fd, "size")



# Add event classes to the stream
stream_class.add_event_class(event_classes["hsa_event:entry"])
stream_class.add_event_class(event_classes["hsa_event:exit"])
stream_class.add_event_class(event_classes["hsa_kernel:begin"])
stream_class.add_event_class(event_classes["hsa_kernel:end"])
stream_class.add_event_class(event_classes["perfmarker:begin"])
stream_class.add_event_class(event_classes["perfmarker:end"])
stream_class.add_event_class(event_classes["data_transfer:begin"])
stream_class.add_event_class(event_classes["data_transfer:end"])


# modify metadata (no more needed)
# # change timestamp_begin and timestamp_end into 64
# f = babeltrace.writer.StructureFieldDeclaration()
# f.add_field(uint64_fd, "timestamp_begin")
# f.add_field(uint64_fd, "timestamp_end")
# f.add_field(uint32_fd, "content_size")
# f.add_field(uint32_fd, "packet_size")
# f.add_field(uint32_fd, "events_discarded")
# stream_class.packet_context_type = f

# Add a custom uint16_t field in the stream's packet context
# packet_context_type = stream_class.packet_context_type
# packet_context_type.add_field(uint32_fd, "cpu_id")
# stream_class.packet_context_type = packet_context_type

# 
# # doesn't do anything
# g = babeltrace.writer.StructureFieldDeclaration()
# g.add_field(uint64_fd, "timestamp")
# g.add_field(uint32_fd, "id")
# stream_class.event_header_type = g



# CLASSES FOR HSA PARSING AND CTF WRITING

# create ctf event entry and exit from 1 association of event hsa_api and hsa_timestamp
def create_ctf_api_event_from_hsa(hsa_api, hsa_timestamp):
    ctf_event_entry = CTF_hsa_api_entry(hsa_api.name, hsa_timestamp.begin, hsa_api.result, hsa_api.args, hsa_timestamp.api_type, hsa_api.tid)
    ctf_event_exit = CTF_hsa_api_exit(hsa_api.name, hsa_timestamp.end, hsa_api.result, hsa_api.args, hsa_timestamp.api_type, hsa_api.tid)
    
    ctf_data_transfer_begin = 0
    ctf_data_transfer_end = 0
    
    # if api event is a memory copy, we add a data transfer event
    if hsa_api.src_agent != "" and hsa_api.dst_agent != "" and hsa_timestamp.transferBegin != -1 and hsa_timestamp.transferEnd != -1:
        ctf_data_transfer_begin = CTF_data_transfer_begin(hsa_timestamp.transferBegin, hsa_api.src_agent, hsa_api.dst_agent, hsa_api.transfer_size)
        ctf_data_transfer_end = CTF_data_transfer_end(hsa_timestamp.transferEnd, hsa_api.src_agent, hsa_api.dst_agent, hsa_api.transfer_size)
        
    return ctf_event_entry, ctf_event_exit, ctf_data_transfer_begin, ctf_data_transfer_end

class CTF_hsa_api_entry():
    def __init__(self, name, timestamp, result, args, api_type, tid):
        self.name = name
        self.timestamp = timestamp
        self.api_type = api_type
        self.result = result
        self.args = args
        self.tid = tid
    
    def getEvent(self):
        global event_classes, debug
        ev = btw.Event(event_classes["hsa_event:entry"])
        ev.payload("name").value = self.name
        ev.payload("args").value = self.args
        ev.payload("result").value = self.result
        ev.payload("api_type").value = self.api_type
        return ev, self.timestamp, self.tid
    
class CTF_hsa_api_exit():
    def __init__(self, name, timestamp, result, args, api_type, tid):
        self.name = name
        self.timestamp = timestamp
        self.api_type = api_type
        self.result = result
        self.args = args
        self.tid = tid
    
    def getEvent(self):
        global event_classes
        ev = btw.Event(event_classes["hsa_event:exit"])
        ev.payload("name").value = self.name
        ev.payload("args").value = self.args
        ev.payload("result").value = self.result
        ev.payload("api_type").value = self.api_type
        return ev, self.timestamp, self.tid


class CTF_data_transfer_begin():
    def __init__(self, timestamp, src_agent, dst_agent, size):
        self.timestamp = timestamp
        self.src_agent = src_agent
        self.dst_agent = dst_agent
        self.size = size
    
    def getEvent(self):
        global event_classes
        ev = btw.Event(event_classes["data_transfer:begin"])
        ev.payload("name").value = "datatransfer " + self.size
        ev.payload("size").value = int(self.size)
        if "gfx803" in self.src_agent and "gfx803" not in self.dst_agent:
            tid = DATA_TRANSFER_GPU_CPU
        elif "gfx803" not in self.src_agent and "gfx803" in self.dst_agent:
            tid = DATA_TRANSFER_CPU_GPU
        elif "gfx803" in self.src_agent and "gfx803" in self.dst_agent:
            tid = DATA_TRANSFER_GPU_GPU
        else:
            tid = DATA_TRANSFER_CPU_CPU
        return ev, self.timestamp, tid

class CTF_data_transfer_end():
    def __init__(self, timestamp, src_agent, dst_agent, size):
        self.timestamp = timestamp
        self.src_agent = src_agent
        self.dst_agent = dst_agent
        self.size = size
    
    def getEvent(self):
        global event_classes
        ev = btw.Event(event_classes["data_transfer:end"])
        ev.payload("name").value = "datatransfer " + self.size
        ev.payload("size").value = int(self.size)
        if "gfx803" in self.src_agent and "gfx803" not in self.dst_agent:
            tid = DATA_TRANSFER_GPU_CPU
        elif "gfx803" not in self.src_agent and "gfx803" in self.dst_agent:
            tid = DATA_TRANSFER_CPU_GPU
        elif "gfx803" in self.src_agent and "gfx803" in self.dst_agent:
            tid = DATA_TRANSFER_GPU_GPU
        else:
            tid = DATA_TRANSFER_CPU_CPU
        return ev, self.timestamp, tid

class HSA_API():
    def __init__(self, string, tid):
        self.tid = tid
        self.regex = re.compile("""(.*) = (.* )(\(.*)""")
        self.regex_no_return = re.compile("""(.* )(\(.*)""")
        self.regex_mem_copy_async = re.compile(""".*?dst_agent.*?name=(.+?)}.*?src_agent.*?name=(.+?)};size=(\d+).*""")
        
        self.src_agent = ""
        self.dst_agent = ""
        self.transfer_size = -1
        
        res = self.regex.search(string)
        if not res:
            # regex no return
            res = self.regex_no_return.search(string)
            if not res:
                print("Error HSA_API regex :", string)
                exit(0)
            else:
                g = res.groups()
                self.result = ""
                self.name = g[0]
                self.args = g[1]
                
                # if mem copy
                res = self.regex_mem_copy_async.search(self.args)
                if res:
                    g = res.groups()
                    self.dst_agent = g[0]
                    self.src_agent = g[1]
                    self.transfer_size = g[2]

                    
        else:
            # regex normal
            g = res.groups()
            self.result = g[0]
            self.name = g[1]
            self.args = g[2]
            
            # if mem copy
            res = self.regex_mem_copy_async.search(self.args)
            if res:
                g = res.groups()
                self.dst_agent = g[0]
                self.src_agent = g[1]
                self.transfer_size = g[2]
        
        # not good but didn't find other solution
        if not all(ord(char) < 128 for char in self.args):
            self.args = "invalid arguments characters"


class HSA_Timestamp():
    def __init__(self, line):
        tmp = line.strip().split()
        self.api_type = int(tmp[0])
        self.name = tmp[1]
        self.begin = int(tmp[2])
        self.end = int(tmp[3])
        self.transferBegin = -1
        self.transferEnd = -1
        if len(tmp) > 4:
            self.transferBegin = int(tmp[4])
            self.transferEnd = int(tmp[5])
        




# create ctf kernel begin and end from a HSA kernel
def create_CTF_HSA_Kernel_event(hsa_kernel):
    ctf_kernel_begin = CTF_kernel_begin(hsa_kernel.name, hsa_kernel.handle, hsa_kernel.begin, hsa_kernel.agentName, hsa_kernel.agentHandle, hsa_kernel.index, hsa_kernel.queueHandle)
    ctf_kernel_end = CTF_kernel_end(hsa_kernel.name, hsa_kernel.handle, hsa_kernel.end, hsa_kernel.agentName, hsa_kernel.agentHandle, hsa_kernel.index, hsa_kernel.queueHandle)
    return ctf_kernel_begin, ctf_kernel_end

class CTF_kernel_begin():
    def __init__(self, name, handle, timestamp, agentName, agentHandle, index, queueHandle):
        self.name = name
        self.handle = handle
        self.timestamp = timestamp
        self.agentName = agentName
        self.agentHandle = agentHandle
        self.index = index
        self.queueHandle = queueHandle

    def getEvent(self):
        global event_classes
        ev = btw.Event(event_classes["hsa_kernel:begin"])
        ev.payload("name").value = self.name
        ev.payload("handle").value = self.handle
        ev.payload("agentName").value = self.agentName
        ev.payload("agentHandle").value = self.agentHandle
        ev.payload("index").value = self.index
        ev.payload("queueHandle").value = self.queueHandle
        return ev, self.timestamp, KERNEL_TID
    
    
class CTF_kernel_end():
    def __init__(self, name, handle, timestamp, agentName, agentHandle, index, queueHandle):
        self.name = name
        self.handle = handle
        self.timestamp = timestamp
        self.agentName = agentName
        self.agentHandle = agentHandle
        self.index = index
        self.queueHandle = queueHandle

    def getEvent(self):
        global event_classes
        ev = btw.Event(event_classes["hsa_kernel:end"])
        ev.payload("name").value = self.name
        ev.payload("handle").value = self.handle
        ev.payload("agentName").value = self.agentName
        ev.payload("agentHandle").value = self.agentHandle
        ev.payload("index").value = self.index
        ev.payload("queueHandle").value = self.queueHandle
        return ev, self.timestamp, 171717

class HSA_Kernel():
    def __init__(self, string):
        tmp = string.strip().split()
        self.name = tmp[0]
        self.handle = tmp[1]
        self.begin = int(tmp[2])
        self.end = int(tmp[3])
        self.agentName = tmp[4]
        self.agentHandle = tmp[5]
        self.index = int(tmp[6])
        self.queueHandle = int(tmp[7])


class Perfmarker():
    def __init__(self, string, tid):
        self.tid = int(tid)
        tmp = string.strip().split()
        self.marker_type = tmp[0]
        self.category = ""
        self.name = ""
        if "Begin" in self.marker_type:
            self.name = tmp[1]
            self.timestamp = int(tmp[2])
            self.category = tmp[3]
        else:
            self.timestamp = int(tmp[1])
            if "Ex" in self.marker_type:
                self.name = tmp[2]
                self.category = tmp[3]

    def getEvent(self):
        global event_classes
        if "Begin" in self.marker_type:
            event = btw.Event(event_classes["perfmarker:begin"])
            event.payload("name").value = self.name
            event.payload("category").value = self.category
        else:
            event = btw.Event(event_classes["perfmarker:end"])
            event.payload("name").value = self.name
            event.payload("category").value = self.category
        return event, self.timestamp, self.tid


# datastructures to read HSA
# contain hsa api events
hsa_api_dic = {}
# contain hsa timestamp events
hsa_timestamp_dic = {}

# contain perfmarkers events
perfmarker_dic = {}


# contain kernels ctf events (begin and end)
ctf_kernels = []
# contain ctf hsa api events
ctf_api_dic = {}
# contain data transfers event
data_transfer_vector = []


# 

# parse main ATP file
with open(sys.argv[1], "r", errors='backslashreplace') as f:
    lines = f.readlines()
    idx = 0
    
    # idx reach hsa API Trace Output line
    while "=====" not in lines[idx]:
        idx += 1
    
    # read all hsa API Trace Output, stop when idx reach hsa timestamp
    # pass section line
    idx += 1
    while "=====" not in lines[idx]:
        # idx point to the thread id
        # read tid and number of lines
        tid = int(lines[idx].strip())
        idx += 1
        nb_lines = int(lines[idx].strip())
        tmp = []
        for i in range(nb_lines):
            idx += 1
            tmp.append(HSA_API(lines[idx], tid))
            
        # save all the traces for 1 thread id and add into the dict
        hsa_api_dic[tid] = tmp
        
        # next thread
        idx += 1

    # read all hsa timestamp
    # pass section line
    idx += 1
    while "=====" not in lines[idx]:
        # idx point to the thread id
        # read tid and number of lines
        tid = int(lines[idx].strip())
        idx += 1
        nb_lines = int(lines[idx].strip())
        tmp = []
        for i in range(nb_lines):
            idx += 1
            tmp.append(HSA_Timestamp(lines[idx]))
        # save all the traces for 1 thread id and add into the dict
        hsa_timestamp_dic[tid] = tmp
        
        # next thread
        idx += 1

    # read nb of kernels lines
    # pass section line
    idx += 1
    nb_lines = int(lines[idx].strip())
    for i in range(nb_lines):
        idx += 1
        # from 1 hsa kerne event, create 2 ctf kernels event (begin and end)
        ctf_kernel_begin, ctf_kernel_end = create_CTF_HSA_Kernel_event(HSA_Kernel(lines[idx]))
        ctf_kernels.append(ctf_kernel_begin)
        ctf_kernels.append(ctf_kernel_end)
    idx += 1

# parse perfmarkers files
for filename in sys.argv[2:]:
    with open(filename, "r") as f:
        tid = filename.replace(".", "_").split("_")[1]
        lines = f.readlines()
        tmp = []
        # read perfmarker
        for line in lines:
            tmp.append(Perfmarker(line, tid))
        # save all the traces for 1 thread id and add into the dict
        perfmarker_dic[tid] = tmp


# check that hsa_timestamp_dic and hsa_api_dic are coherent
hsa_event_ok = True
if len(hsa_api_dic) != len(hsa_timestamp_dic):
    hsa_event_ok = False
for i in hsa_api_dic:
    if i not in hsa_timestamp_dic:
        hsa_event_ok = False
        break
    else:
        for i in hsa_api_dic:
            if len(hsa_api_dic[i]) != len(hsa_timestamp_dic[i]):
                hsa_event_ok = False
                break
if hsa_event_ok:
    print("hsa events are ok")
else:
    print("Error traces hsa api and hsa timestamp are different")
    exit(-1)


# create ctf hsa api event from hsa_api and hsa_timestamp
# link calls in hsa_api with the corresponding timestamp in hsa_timestamp
# and create one event for the entry and one for the exit
for i in hsa_api_dic:
    tmp = []
    for j in range(len(hsa_api_dic[i])):
        ctf_event_begin, ctf_event_end, ctf_data_transfer_begin, ctf_data_transfer_end = \
                                            create_ctf_api_event_from_hsa(hsa_api_dic[i][j], hsa_timestamp_dic[i][j])
        tmp.append(ctf_event_begin)
        tmp.append(ctf_event_end)
        if ctf_data_transfer_begin != 0 and ctf_data_transfer_end != 0:
            data_transfer_vector.append(ctf_data_transfer_begin)
            data_transfer_vector.append(ctf_data_transfer_end)
    ctf_api_dic[i] = tmp


# combine all traces in a list and sort
all_events = []

# append api events
for i in ctf_api_dic:
    all_events.extend(ctf_api_dic[i])

# append kernel events
all_events.extend(ctf_kernels)
# append perfmarkers events
for i in perfmarker_dic:
    all_events.extend(perfmarker_dic[i])

# append data transfer
all_events.extend(data_transfer_vector)

# sort
all_events.sort(key=lambda x: x.timestamp, reverse=False)
# for i in all_events:
#     print(i.name, i.timestamp)
#     input()

# create our single stream
st = writer.create_stream(stream_class)

# write the ctf
counter = 0
for i in all_events:
    ev, tp, tid = i.getEvent()
    ev.tid(tid)
    clock.time = tp
    st.append_event(ev)
    if counter > 10000:
        st.flush()
        st = writer.create_stream(stream_class)
        counter = 0
    counter += 1

st.flush()