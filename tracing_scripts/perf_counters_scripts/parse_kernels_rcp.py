# no more used, everything merge into read_kernels.py
# create csv file from RCP perf counter file and ctf traces

from datetime import datetime

out = []
values = []
with open("kernels", "r") as f:
    lines = f.readlines()
    for line in lines:
        # elements = line.split(",")
        split_line = line.split("_gfx803")
        name = split_line[0].replace("&nbsp;", " ").replace("&comma;", ",")
        out.append(name)
        values.append(split_line[1:])

data = []
with open("out2", "r") as f:
    lines = f.readlines()
    out_index = 0
    for i in range(min(len(lines),  len(out))):
        name = lines[out_index].split("|")[1].strip() 
        res =  name in out[i]
        print(res)
        if res == False:
            out_index += 1
            name = lines[out_index].split("|")[1].strip() 
            res =  name in out[i]
            if res == False:
                exit(-1)
        # data.append(lines[out_index].strip() + "|" + out[i].strip() + "| " + "".join(values[i]).replace(",", "|"))
        timestamp = int(lines[out_index].split("|")[0])
        dt = datetime.fromtimestamp(timestamp//1000000000)
        s = dt.strftime('%Y-%m-%d %H:%M:%S')
        s += '.' + str(int(timestamp % 1000000000)).zfill(9)
        
        data.append(s + " | " + out[i].strip() + "".join(values[i]).replace(",", "|"))
        out_index += 1
    
names = "Timestamp | Method | ExecutionOrder | ThreadID | GlobalWorkSize | WorkGroupSize | LocalMemSize | VGPRs | SGPRs | Wavefronts | VALUInsts | SALUInsts | VFetchInsts | SFetchInsts | VWriteInsts | FlatVMemInsts | FlatLDSInsts | FetchSize | WriteSize | CacheHit \n"
data.insert(0, names)
        
with open("parsed_kernels", "w") as f:
    f.writelines(data)