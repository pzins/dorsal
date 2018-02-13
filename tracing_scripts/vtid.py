out_path = "/home/pierre/out_traces"
out_metadata = []
with open(out_path + "/metadata", "r") as f:
    lines = f.readlines()
    for i in lines:
        if "vtid" in i and "_vtid" not in i:
            i = i.replace("vtid", "_vtid")
        out_metadata.append(i)

with open(out_path + "/metadata", "w") as f:
    f.writelines(out_metadata)