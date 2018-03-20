# script used to generate graph, representing the flow of operations
# output file can be visualized with sigmaJS
class Outputs:
    
    def __init__(self, node):
        self.node = node
        self.succ = []
    
    def add_succ(self, node):
        self.succ.append(node)
    
    def is_null(self):
        return len(self.succ) == 0

    def __str__(self):
        tmp = ""
        for i in self.succ:
            tmp += " " + i
        return self.node + " => " + tmp
    
graph = []
all_nodes = []

with open("out", "r") as f:
    lines = f.readlines()
    for idx in range(len(lines)):
        if "PropagateOutputs" in lines[idx]:
            name = lines[idx-1].split()[-1]
            o = Outputs(name)
            
            if name not in all_nodes:
                all_nodes.append(name)
                
            idx += 1
            while lines[idx][0] == " ":
                tmp_name = lines[idx].strip()
                
                if tmp_name not in all_nodes:
                    all_nodes.append(tmp_name)
                
                o.add_succ(tmp_name)
                idx += 1
            if not o.is_null():
                graph.append(o)
        idx += 1
        

for i in graph:
    print(i)

edges = []
link_id_node = {}


with open("graph", "w") as f:
    cnt = 0
    st = ""
    for i in all_nodes:
        st += "{" + "\n"
        st += "\"id\": \"n" + str(cnt) + "\"," + "\n"
        st += "\"label\": \"" + i + "\"," + "\n"
        st += "\"x\": " + str(cnt//3) + "," + "\n"
        st += "\"y\": " + str(cnt%3) + "," + "\n"
        st += "\"size\": 3" + "\n"
        st += "}"
        if cnt != len(all_nodes)-1:
            st += ","
        st += "\n"
        link_id_node[i] = "n" + str(cnt)
        cnt += 1 
    
    f.write("{\"nodes\": [" + "\n")
    f.write(st + "\n")
    f.write("], \"edges\": [" + "\n")
    
    stop = False
    st = ""
    cnt_edge = 0
    for i in graph:
        if i.node == "_SOURCE":
            if stop:
                break
            stop = True
        for j in i.succ:
            st += "{" + "\n"
            st += "\"id\": \"e" + str(cnt_edge) + "\"," + "\n"
            st += "\"source\": \"" + link_id_node[i.node] + "\","  + "\n"
            st += "\"target\": \"" + link_id_node[j] + "\"" + "\n"
            st += "},"
            cnt_edge += 1
    st = st[:-1] + "\n"
    f.write(st)
    f.write("]}")
    
"""
{
  "id": "n1",
  "label": "Another node",
  "x": 3,
  "y": 1,
  "size": 2
},


{
  "id": "e0",
  "source": "n0",
  "target": "n1"
},
"""