import json
from pprint import pprint
from decimal import *

import babeltrace
import sys
import copy



class Queue:
    def __init__(self):
        self.data = []

    def __str__(self):
        res = "|"
        for i in reversed(self.data):
            res += " " + i + " >"
        return res + ">"
    def push(self, element):
        self.data.append(element)
    def pull(self):
        return self.data.pop(0)
    def checkPull(self, element):
        if len(self.data) < 1:
            return 0
        return (element in self.data[0])
    def last(self):
        if len(self.data) < 1:
            return 0
        return self.data[0]

# get the trace path from the first command line argument
trace_path = "/home/pierre/lttng-traces/ol-20171024-191352"
trace_path = "/home/pierre/lttng-traces/lkz-20171024-181405"
trace_path = "/home/pierre/lttng-traces/coco-20171025-184307"


trace_collection = babeltrace.TraceCollection()
trace_collection.add_traces_recursive(trace_path, 'ctf')
queue_size = 0
queue = Queue()
miss = []

test = 0
counters = [0, 0, 0]

def inc_counter(ss):
    if "kernel" in ss:
        counters[0] += 1
    elif "write" in ss:
        counters[1] += 1
    elif "read" in ss:
        counters[2] += 1

for i in trace_collection.events:
    while queue.last() in miss:
        print("OL")
        queue.pull()
    if i.name == "ocl:kernel_queued":
        inc_counter("kernel")
        queue.push("kernel " + str(counters[0]))
        # queue.push(i["kernel_name"])
    elif i.name == "ocl:write_buffer_queued":
        inc_counter("write_buffer")
        queue.push("write_buffer " + str(counters[1]))
    elif i.name == "ocl:read_buffer_queued":
        inc_counter("read_buffer")
        queue.push("read_buffer " + str(counters[2]))

    elif i.name == "ocl:kernel_submitted":
        # if queue.checkPull("SYCL"):
        if queue.checkPull("kernel"):
            queue.pull()
        else:
            miss.append("kernel " + str(counters[0]))
            print("ADD ", "kernel " + str(counters[0]))
            test = 1

    elif i.name == "ocl:write_buffer_submitted":
        if queue.checkPull("write_buffer"):
            queue.pull()
        else:
            miss.append("write_buffer " + str(counters[1]))
            print("ADD ", "write_buffer " + str(counters[1]))
            test = 1

    elif i.name == "ocl:read_buffer_submitted":
        if queue.checkPull("read_buffer"):
            queue.pull()
        else:
            miss.append("read_buffer " + str(counters[2]))
            print("ADD ", "read_buffer " + str(counters[2]))
            test = 1

    dbg_str = i.name
    if "kernel" in dbg_str:
        dbg_str += " " + str(counters[0])
    elif "write" in dbg_str:
        dbg_str += " " + str(counters[1])
    elif "read" in dbg_str:
        dbg_str += " " + str(counters[2])
    print(dbg_str)
    print(str(i.timestamp), end=" ")
    print(queue)
    # if test:
    #     r = input()
    #     if r == "c":
    #         test = 0
print(miss)
print("Order problem:", len(miss))
