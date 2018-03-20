import re
import pdb

import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import tempfile

# CTF

# temporary directory holding the CTF trace
trace_path = tempfile.mkdtemp()
trace_path = "/home/pierre/outout"

print('trace path: {}'.format(trace_path))

# our writer
writer = btw.Writer(trace_path)

# create one default clock and register it to the writer
clock = btw.Clock('my_clock')
clock.description = 'this is my clock'
writer.add_clock(clock)

# create one default stream class and assign our clock to it
stream_class = btw.StreamClass('my_stream')
stream_class.clock = clock

uint64_fd = btw.IntegerFieldDeclaration(64)
uint64_fd.signed = False

huint64_fd = btw.IntegerFieldDeclaration(64)
huint64_fd.base = babeltrace.writer.IntegerBase.HEX
huint64_fd.signed = False

string_fd = btw.StringFieldDeclaration()
event_classes = {}
event_classes["hsa_trace"] = btw.EventClass('hsa_trace')
event_classes["hsa_timestamp"] = btw.EventClass('hsa_timestamp')
event_classes["hsa_kernel"] = btw.EventClass('hsa_kernel')
event_classes["perfmarker"] = btw.EventClass('perfmarker')

event_classes["hsa_trace"].add_field(string_fd, "result")
event_classes["hsa_trace"].add_field(string_fd, "name")
event_classes["hsa_trace"].add_field(string_fd, "args")


event_classes["hsa_timestamp"].add_field(uint64_fd, "API_type")
event_classes["hsa_timestamp"].add_field(string_fd, "name")
event_classes["hsa_timestamp"].add_field(uint64_fd, "begin")
event_classes["hsa_timestamp"].add_field(uint64_fd, "end")


event_classes["hsa_kernel"].add_field(string_fd, "name")
event_classes["hsa_kernel"].add_field(string_fd, "handle")
event_classes["hsa_kernel"].add_field(uint64_fd, "begin")
event_classes["hsa_kernel"].add_field(uint64_fd, "end")
event_classes["hsa_kernel"].add_field(string_fd, "agentName")
event_classes["hsa_kernel"].add_field(string_fd, "agentHandle")
event_classes["hsa_kernel"].add_field(uint64_fd, "index")
event_classes["hsa_kernel"].add_field(uint64_fd, "queueHandle")


event_classes["perfmarker"].add_field(string_fd, "name")
event_classes["perfmarker"].add_field(string_fd, "markerName")
event_classes["perfmarker"].add_field(string_fd, "type")
event_classes["perfmarker"].add_field(uint64_fd, "timestamp")



stream_class.add_event_class(event_classes["hsa_trace"])
stream_class.add_event_class(event_classes["hsa_timestamp"])
stream_class.add_event_class(event_classes["hsa_kernel"])
stream_class.add_event_class(event_classes["perfmarker"])


#============================

class Section():
    def __init__(self):
        self.data = []
        self.threadID = 0
        self.num_elements = 0
    def __str__(self):
        return self.data[0].__str__() + " \n" + self.data[-1].__str__()

    def size(self):
        return len(data)

class HSA_API():
    def __init__(self, string):
        self.regex = re.compile("""(.*) = (.* )(\(.*)""")
        self.regex_no_return = re.compile("""(.* )(\(.*)""")
        res = self.regex.search(string)
        if not res:
            res = self.regex_no_return.search(string)
            if not res:
                print("Error HSA_API regex :", string)
                exit(0)
            else:
                g = res.groups()
                self.result = ""
                self.name = g[0]
                self.args = g[1]
        else:
            g = res.groups()
            self.result = g[0]
            self.name = g[1]
            self.args = g[2]

    def __str__(self):
        return self.result + " " + self.name + " " + self.args

    def getEvent(self):
        global event_classes
        event = btw.Event(event_classes["hsa_trace"])
        event.payload("result").value = self.result
        event.payload("name").value = self.name
        event.payload("args").value = "self.args"
        return event


class HSA_Timestamp():
    def __init__(self, line):
        tmp = line.strip().split()
        self.API_type = int(tmp[0])
        self.name = tmp[1]
        self.begin = int(tmp[2])
        self.end = int(tmp[3])

    def __str__(self):
        return str(self.API_type) + " " + self.name + " " + str(self.begin) + " " + str(self.end)

    def getEvent(self):
        global event_classes
        event = btw.Event(event_classes["hsa_timestamp"])
        event.payload("API_type").value = self.API_type
        event.payload("name").value = self.name
        event.payload("begin").value = self.begin
        event.payload("end").value = self.end
        return event

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

    def __str__(self):
        return self.name + " " + str(self.begin) + " " + str(self.end) + " " + str(self.index)
    def output(self):
        return self.name + " " + self.handle + " " + str(self.begin) + " " + str(self.end) + " " + self.agentName + " " + self.agentHandle + " " + str(self.index) + " " + str(self.queueHandle) + "\n"

    def getEvent(self):
        global event_classes
        event = btw.Event(event_classes["hsa_kernel"])
        event.payload("name").value = self.name
        event.payload("handle").value = self.handle
        event.payload("begin").value = self.begin
        event.payload("end").value = self.end
        event.payload("agentName").value = self.agentName
        event.payload("agentHandle").value = self.agentHandle
        event.payload("index").value = self.index
        event.payload("queueHandle").value = self.queueHandle
        return event

class Perfmarker():
    def __init__(self, string):
        tmp = string.strip().split()
        self.name = tmp[0]
        self.marker_name = ""
        if "clBeginPerfMarker" in tmp:
            self.type = "begin"
            self.timestamp = int(tmp[2])
            self.marker_name = tmp[3]
        else:
            self.type = "end"
            self.timestamp = int(tmp[1])


    def __str__(self):
        return self.type + " " + str(self.timestamp) + " " + self.marker_name

    def getEvent(self):
        global event_classes
        event = btw.Event(event_classes["perfmarker"])
        event.payload("name").value = self.name
        event.payload("markerName").value = self.marker_name
        event.payload("type").value = self.type
        event.payload("timestamp").value = self.timestamp
        return event


string = "HSA_STATUS_SUCCESS = hsa_agent_get_info ( agent={handle=24240912,name=Intel(R)&nbsp;Core(TM)&nbsp;i7-4770&nbsp;CPU&nbsp;&#64;&nbsp;3.40GHz};attribute=HSA_AGENT_INFO_DEVICE;value=[HSA_DEVICE_TYPE_CPU] )"

"""
pr chaque section :
faire un loop while qui lit ttes les lignes d'un thread
en testant si next line contains ==== or not
si not juste continue, et ça reprendra avec la new section ds le if "====" du d2but

comme ça apres le if "=====", on get tte la section en un coup même si pls threads

chaque pqrtir specifique à un thread est consid comme une section à part je pense
ds ts les cas il suffira de tester le type de la section puisque si pls section d'un même type, elles se suivent forcement

un fois que j'ai une list avec ttes les section il faudra comprendre le format CTF et utiliser le writer de babeltrace
"""



sections = []
curr_section = -1
with open("apitrace_new.atp", "r") as f:
    lines = f.readlines()
    idx = 0
    while "=====" not in lines[idx]:
        idx += 1
    while idx < len(lines):
        line = lines[idx]
        if "=====" in line:
            if "hsa API Trace" in line:
                section_type = "hsa_api"
            elif "hsa Timestamp" in line:
                section_type = "hsa_timestamp"
            elif "hsa Kernel Timestamp" in line:
                section_type = "hsa_kernel_timestamp"
            elif "Perfmarker" in line:
                section_type = "perfmarker"
            else:
                print("Wrong section type")
                exit(0)
            idx += 1
            while idx < len(lines) and "=====" not in lines[idx]:
                # pdb.set_trace()
                sections.append(Section())
                curr_section += 1
                if "hsa Kernel" not in lines[idx-1]:
                    threadID = lines[idx]
                    idx += 1
                num_entries = int(lines[idx].strip())
                if section_type == "hsa_api":
                    for j in range(1,num_entries+1):
                        sections[curr_section].data.append(HSA_API(lines[idx+j]))
                    idx += num_entries + 1
                elif section_type == "hsa_timestamp":
                    for j in range(1,num_entries+1):
                        sections[curr_section].data.append(HSA_Timestamp(lines[idx+j]))
                    idx += num_entries + 1
                elif section_type == "hsa_kernel_timestamp":
                    for j in range(1,num_entries+1):
                        sections[curr_section].data.append(HSA_Kernel(lines[idx+j]))
                    idx += num_entries + 1
                elif section_type == "perfmarker":
                    num_entries = len(lines) - idx
                    for j in range(1,num_entries):
                        sections[curr_section].data.append(Perfmarker(lines[idx+j]))
                    idx += num_entries
                    print(idx)
                else:
                    print("Wrong section_type")
                    exit(0)


# # create our single stream
stream = writer.create_stream(stream_class)


counter = 0
for i in sections:
    for j in i.data:
        event = j.getEvent()
        stream.append_event(event)
        if counter > 1000:
            stream.flush()
            stream = writer.create_stream(stream_class)
            counter = 0

        counter += 1


# flush the stream
# stream.flush()
