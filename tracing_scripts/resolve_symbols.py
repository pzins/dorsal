
mapping = {}
base = int("00007f61b8024000", 16)
with open("libSymbols","r") as f:
    lines = f.readlines()
    for line in lines:
        tmp = line.strip().split()
        if not tmp[0][0] == "0":
            continue
        a = int(tmp[0],16)
        # print(a)
        # print(base)
        # print('0x{0:02x}'.format(a+base))
        # exit(0)
        # print(tmp[0], '0x{0:02x}'.format(a+base))
        mapping[a+base] = line.strip()
        
# for i in mapping:
    # print(i, mapping[i])

print("========")
with open("traces_lttng", "r") as f:
    lines = f.readlines()
    for line in lines:
        tmp = line.strip().split()
        adr = int(tmp[12][:-1], 16)
        if adr in mapping:
            print(mapping[adr])
        else:
            print("no")
        # exit(0)
