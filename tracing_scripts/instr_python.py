import lttngust
import logging
import re
import sys

start_tracing_element = "python_instrument"
start_tracing_element = "tf.Session"

if len(sys.argv) < 2:
    print("Please specify a python file to instrument")
    exit(1)

ext = ".py"
name = sys.argv[1]
if sys.argv[1][-2:] == "py":
    name = sys.argv[1][:-3]
    
filename = name + ext
output_filename = name + "_instr" + ext
print(filename, output_filename)

def get_indent(line):
    # compute indentation
    tmp = line.split(" ")
    s = 0
    for i in tmp:
        if i == '':
            s += 1
    return s

def is_profiling_line(l):
    if len(line) <= 1 or "#" in line or "if" in line or "for" in line:
        return False
    return True

def init_logging(l):
    tmp = []
    spaces = " "*get_indent(l)
    tmp.append(spaces + "logging.basicConfig()\n")
    tmp.append(spaces + "logger = logging.getLogger('my-logger')\n")
    tmp.append(l)
    return tmp


def wrap_line(l, indent):
    spaces = " "*indent
    tmp = []
    st = l.strip().replace(" ", "_")
    tmp.append(spaces + "logger.info('begin:" + st + "')\n")
    if '\n' not in l:
        l += "\n"    
    tmp.append(l)
    tmp.append(spaces + "logger.info('end:" + st + "')\n")
    return tmp
output_script = []

session_start = False
import_done = False

with open(filename, "r") as f:
    lines = f.readlines()
    for line in lines:
        if not import_done and "import" not in line:
            output_script.append("import lttngust\n")
            output_script.append("import logging\n")
            import_done = True
            
        if start_tracing_element in line:
            output_script.extend(init_logging(line))
            session_start = True
        
        elif session_start and is_profiling_line(line):
            output_script.extend(wrap_line(line, get_indent(line)))
        
        else:
            if '\n' not in line:
                line += "\n"
            output_script.append(line)
 
open(output_filename, 'w').writelines(output_script)
