from config import *

# Helper vars
linesToStrip = []

temperatureFanBlacklist = ["M104", "M106", "M109", "M104","M190"]

# pull all lines out of the file
with open(filePath,"r") as f:
    mainCode = f.readlines()

for line in mainCode:

    # check what mode we're in
    if STRIP_MODE == 1:
        # temperature/fans
        for item in temperatureFanBlacklist:
            if item in line:
                linesToStrip.append(mainCode.index(line))

    #TODO
    #elif STRIP_MODE == 2:
    

# go backwards and remove lines to preserve the indicies
for index in reversed(linesToStrip):
    mainCode.pop(index)

# reconstruct the file string

out = ''.join(mainCode)

# output the stripped file
with open(outputPath,"w") as f:
    f.write(out)