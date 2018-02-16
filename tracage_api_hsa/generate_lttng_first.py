# work quite welll except for the first HSA function HSA_Init and HSA_Destroy (need to do manually)

filename = "hsa_table_interface2.cpp"


def getName(l):
    start = l.find("->")
    end = l.find("_fn")
    return l[start+2:end]
    

with open(filename, "r") as f:
    lines = f.readlines()
    outLines = []
    returnType = ""
    cnt = 0
    while cnt < len(lines):
        while cnt < len(lines) and not "HSA_API" in lines[cnt]:
            cnt += 1
        if cnt >= len(lines):
            break
        
        if "deprecated" in lines[cnt]:
            returnType = lines[cnt].split()[3]
        else:
            returnType = lines[cnt].split()[0]

        offset = 0
        while "(" not in lines[cnt+offset]:
            offset += 1
        names = lines[cnt+offset].split()
        for j in names:
            if "(" in j:
                name = j[:j.find("(")]
                break
            
                
        # case same line
        if "return" in lines[cnt]:
            after_accolade = lines[cnt].find("{")+1
            tmp = lines[cnt][:after_accolade]
            core = lines[cnt][after_accolade:].split()[1:][0]
            core += "\ntracepoint(hsaTracer, function_entry, \"" + name + "\");\n"
            core = "\n" + returnType + " tmp = " + core
            tmp += core
            core += "\ntracepoint(hsaTracer, function_exit, \"" + name + "\");\n"
            tmp += "\nreturn tmp;}"
            outLines.append("\n"+tmp)
        else:
            offset = 0
            tmp = ""
            while "return" not in lines[cnt+offset]:
                tmp += lines[cnt+offset]
                offset += 1
            # tmp += "printf(\"=-=-=-=-=-=-=-=-=-=-==-=-=\");"
            tmp += "\ntracepoint(hsaTracer, function_entry, \"" + name + "\");\n"
            if returnType == "void":
                tmp += lines[cnt+offset][lines[cnt+offset].find("return")+7:]
            else:
                tmp += returnType + " tmp = " + lines[cnt+offset][lines[cnt+offset].find("return")+7:]
            offset += 1
            while "}" not in lines[cnt+offset]:
                tmp += lines[cnt+offset]
                offset += 1
            tmp += "\ntracepoint(hsaTracer, function_exit, \"" + name + "\");\n"
            if returnType == "void":
                tmp += "\n}\n"
            else:
                tmp += "return tmp; \n}\n"
            outLines.append("\n"+tmp)
        cnt += 1
        # if "}" in lines[i]:
        #     returnType = ""
        # if "HSA_API" in lines[i]
        # if "{" in lines[i]:
        #     name = ""
        #     if "return" in lines[i]:
        #         name = getName(lines[i])
        #     if name == "":
        #         name = getName(lines[i+1])
        #     lines[i] += "tracepoint(hsaTracer, " + name + ")\n";
        # outLines.append(lines[i])
        # 
with open("out", "w") as out:
    out.writelines(outLines)