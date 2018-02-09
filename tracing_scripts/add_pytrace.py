import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw

path = "/home/pierre/"


trace_path = path + "lttng-traces/auto-20171206-150358"

# get offset by reading trace metadata file
metadata_file = trace_path + "/ust/uid/1000/64-bit/metadata"
with open(metadata_file, "r", errors='ignore') as f:
    lines = f.readlines()
    for l in lines:
        if "offset =" in l:
            offset = int(l.strip().split()[-1][:-1])
            break

# init ctf babeltrace reader
trace_collection = babeltrace.TraceCollection()
trace_collection.add_traces_recursive(trace_path, 'ctf')

first_event = True
with open(path + "apitrace.atp", "a") as f:
    for i in trace_collection.events:
        
        # before writing event into atp, we need to add the tid and the nb of lines
        if first_event == True:
            f.write("69\n")
            f.write(str(len(list(trace_collection.events))) + "\n")
            first_event = False
        
        name = i.get("msg")
        type_name = "python::session::run"
        # 2 cases : begin marker or end marker
        if "begin" in name:
            f.write("clBeginPerfMarker " + name + " " + str(i.timestamp - offset) + " " + type_name + "\n")
        else:
            f.write("clEndPerfMarkerEx " + str(i.timestamp - offset) + " " + name + " " + type_name + "\n")





# # old version working with output of babeltrace (really bad) or with lttng instrumentation without lttng
# lttng = True
# if not lttng:
#     with open(path + "apitrace.atp", "a") as f:
#         with open(path + "pytraces", "r") as g:
#             lines = g.readlines()
#             for line in lines:
#                 tmp = line.strip().split(":")
#                 name = tmp[2]
#                 time =int(float(tmp[3])*1000000000)
#                 type_name = "python::session:run"
#                 if "begin" in name:
#                     name = name.split(".")[0]
#                     f.write("clBeginPerfMarker " + name + " " + str(time) + " " + type_name + "\n")
#                 else:
#                     name = name.split(".")[0]
#                     f.write("clEndPerfMarkerEx  " + str(time) + " " + name + " " + type_name + "\n")
# else:
#     with open(path + "apitrace.atp", "a") as f:
#         with open(path + "pytraces_lttng", "r") as g:
#             lines = g.readlines()
#             for line in lines:
#                 tmp = line.strip().split()
#                 name = tmp[16][1:-2]
#                 time = float(tmp[0][1:-2])*1000000000
#                 # change after computer reboot
#                 ref = 1510585966028949806
#                 time = int(time - ref)
#                 type_name = "python::session:run"
#                 if "begin" in name:
#                     name = name.split(".")[0]
#                     f.write("clBeginPerfMarker " + name + " " + str(time) + " " + type_name + "\n")
#                 else:
#                     name = name.split(".")[0]
#                     f.write("clEndPerfMarkerEx  " + str(time) + " " + name + " " + type_name + "\n")
