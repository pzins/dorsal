import sys


if len(sys.argv) < 2:
    print("Usage : python3 merge_marker.py MAIN_TRACE MARKER_TRACE_1 MARKER_TRACE_2 ...")
    exit(-1)



with open(sys.argv[1], "a") as f:
    f.write("=====Perfmarker Output=====\n")
    
    for filename in sys.argv[2:]:
        with open(filename, "r") as ff:
            tid = filename.replace(".", "_").split("_")[1]
            lines = ff.readlines()
            f.write(str(tid) + "\n")
            f.write(str(len(lines)) + "\n")
            for line in lines:
                if line[-1] == '\n':
                    f.write(line)
                else:
                    f.write(line + '\n')
