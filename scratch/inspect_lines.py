with open("/Users/joelduran/Documents/GitHub/MacWaveT2/dashboard-ods.html", "r") as f:
    lines = f.readlines()
for i in range(2945, 2968):
    print(f"{i+1}: {repr(lines[i])}")
