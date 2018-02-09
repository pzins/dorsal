import sys


prefix = "/home/pierre/"

if len(sys.argv) > 1:
    atp_filename = prefix + sys.argv[1]
else:
    atp_filename = prefix + "apitrace.atp"


# helper classes
class Session():
    def __init__(self, start, end):
        self.start = int(start)
        self.end = int(end)
        self.kernels = []

    def __str__(self):
        return "Session: " + str(self.start) + " " + str(self.end) + " " + str(len(self.kernels))
    
    def gpu_usage(self):
        duration = self.end - self.start
        gpu_time = 0
        for i in self.kernels:
            gpu_time += i.end - i.start
        return float(gpu_time / duration) * 100

class Kernel():
    def __init__(self, name, handle, start, end, agentName, agentHandle, index, queueHandle):
        self.name = name
        self.handle = handle
        self.start = int(start)
        self.end = int(end)
        self.agentName = agentName
        self.agentHandle = agentHandle
        self.index = index
        self.queueHandle = queueHandle

    def __str__(self):
        return self.name + " " + str(self.start) + " " + str(self.end) + " " + self.index



# datastructures
SESSIONS = []
KERNELS = []



# parser the ATP trace
with open(atp_filename, "r", encoding="ISO-8859-1") as f:
    lines = f.readlines()
    idx = 0
    
    # go to kernel section
    while not "hsa Kernel Timestamp Output" in lines[idx]:
        idx += 1
        if idx == len(lines):
            print("No kernel section")
            exit(-1)
    
    # pass section name line
    idx += 1
    # read number of kernel line
    number_kernel = int(lines[idx].strip())
    # pass kernel section number of line
    idx += 1
    for i in range(number_kernel):
        elements = lines[idx].strip().split()
        KERNELS.append(Kernel(elements[0], elements[1], elements[2], elements[3], elements[4], elements[5], elements[6], elements[7]))
        idx += 1
    
    # reach perfmarker section name
    # pass the name line
    idx += 1
    # read all the lines until end of file
    while idx < len(lines):
        
        # check session run
        if "DirectSession::Run" in lines[idx]:
            elements = lines[idx].strip().split()
            # just test length to jump thread id and number of line
            if len(elements) > 2:
                # session never overlap => begin1, end1, begin2, end2, ...
                if elements[0] == "clBeginPerfMarker":
                    SESSIONS.append(Session(elements[2], "0")) # create the session, set a temporary end
                elif elements[0] == "clEndPerfMarkerEx":
                    SESSIONS[-1].end = int(elements[1]) # set the real end
        idx += 1
        



# sort
KERNELS.sort(key=lambda x: x.start, reverse=False)
SESSIONS.sort(key=lambda x: x.start, reverse=False)



# link kernels to their corresponding session
# loop over all kernels and gives them to a session
# use session_idx to go over the sessions
session_idx = 0
for i in KERNELS:
    sess = SESSIONS[session_idx] # get the current active session
    
    # check the start of the kernel, but for tensorflow, the end also should be less than the session end
    # because the end of the session wait for all work end
    if i.start <= sess.end:
        sess.kernels.append(i)
    # the kernel belong to the next session
    else:
        session_idx += 1
        sess = SESSIONS[session_idx]
        sess.kernels.append(i)
        
        
        
# compute stats

# GPU usage percentage for each session and a global mean without the first iteration
mean = 0
counter = 0
print("====  GPU USAGE STATS ====")
for i in range(len(SESSIONS)):
    tmp = SESSIONS[i].gpu_usage()
    print("Session (" + str(i) + ") :", tmp)
    # skip first variable init session run, and first session which is really long 
    # due to kernel compilation for the mean computation
    if i > 1:
        mean += tmp
        counter += 1
print("GLOBAL MEAN (" + str(counter) + " sessions) :", mean/counter, "\n\n")

# time between session == python time
print("====  PYTHON LATENCY STATS ====")
for i in range(1, len(SESSIONS)):
    time_between = SESSIONS[i].start - SESSIONS[i - 1].end
    print("Time between session " + str(i-1) + " and " + str(i) + " :", time_between/1000000, "ms")
    mean += time_between
print("GLOBAL MEAN (" + str(counter) + " sessions) :", (mean/(len(SESSIONS)-1))/1000000, "ms")
    