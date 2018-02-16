# no working very well
filename = "hsa_table_interface.cpp"


def getName(l):
    start = l.find("->")
    end = l.find("_fn")
    return l[start+2:end]
    

with open(filename, "r") as f:
    lines = f.readlines()
    outLines = []
    return_type = ""
    for i in range(len(lines)):
        line = lines[i]
        if "HSA_API" in line:
            if "deprecated" in line:
                return_type = line.split()[3]
            else:
                return_type = line.split()[0]
        
        elif return_type != "":
            if "return" in line:
                print("------", line)
                tp_entry = "tracepoint(hsaTracer, function_entry, \"" + getName(line) + "\");\n"
                if return_type == "void":
                    call = "".join(line.split()[1:]) + "\n"
                else:
                    call = return_type + " tmp = " + "".join(line.split()[1:]) + "\n"

                offset = 1
                while "}" not in lines[i+offset]:
                    call += lines[i]
                    offset += 1
                tp_exit = "tracepoint(hsaTracer, function_exit, \"" + getName(line) + "\");\n"
                line = tp_entry + call + tp_exit  + "\n"
                if return_type != "void":
                    line += "return tmp;\n"
                    return_type = ""
        else:
            print(":",line)
        outLines.append(line)
with open("out", "w") as out:
    out.writelines(outLines)