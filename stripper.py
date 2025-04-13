from config import *

# Helper vars
linesToStrip = []

splicer = []
latch = 0
currentLine = 0

temperatureFanBlacklist = ["M104", "M106", "M109", "M104","M190"]

# Set to true to strip all of the gcode, otherwise the code will ignore the preheat/start routine
startupComplete = False

# pull all lines out of the file
with open(filePath,"r") as f:
    mainCode = f.readlines()

# Main line-wise loop
for line in mainCode:

    # Check for slicer profile-implemented flag indicating end of startup sequence
    if "; (GhostPrint Flag) END STARTUP" in line and startupComplete == False:
        startupComplete = True

        # If we hit start sequence and Z axis is disabled, raise it so as to not drag nozzle on bed

        if("Z" in knockoutAxes):
            print("Inserting Z axis")
            mainCode.insert(currentLine, "G1 Z2 F1000")
            #mainCode.pop(currentLine + 1)

    # Main splicing and stuff
    if startupComplete:

        if STRIP_MODE == 1:
            # temperature/fans
            for item in temperatureFanBlacklist:
                if item in line:
                    linesToStrip.append(mainCode.index(line))

        elif STRIP_MODE == 2:
            # motor knockouts
            if "G1" in line:
                
                splicer = list(line)

                for i in range(len(splicer)):
                    for Axis in knockoutAxes:
                        if splicer[i] == Axis:
                            latch = 1

                    if splicer[i] == " " and latch == 1:
                        latch = 0

                    if latch == 1:
                        splicer[i] = ""

            mainCode[mainCode.index(line)] = ''.join(splicer)
            print("".join(splicer))

        elif STRIP_MODE == 3:
            # temperature/fans
            for item in temperatureFanBlacklist:
                if item in line:
                    linesToStrip.append(mainCode.index(line))

            # then knock out motor codes
            # motor knockouts
            if "G1" in line:
                
                splicer = list(line)

                for i in range(len(splicer)):
                    for Axis in knockoutAxes:
                        if splicer[i] == Axis:
                            latch = 1

                    if splicer[i] == " " and latch == 1:
                        latch = 0

                    if latch == 1:
                        splicer[i] = ""

            mainCode[mainCode.index(line)] = ''.join(splicer)
            #print("".join(splicer))
            

        else:
            print("Invalid strip mode")
        
    currentLine += 1


# reconstruct the file string
print("Starting compression to file")
if STRIP_MODE == 1 or STRIP_MODE == 3:
    # go backwards and remove lines to preserve the indicies
    for index in reversed(linesToStrip):
        mainCode.pop(index)

out = ''.join(mainCode)

print("Attempting to write to file")
# output the stripped file
with open(outputPath,"w") as f:
    f.write(out)