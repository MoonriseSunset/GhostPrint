from config import *

# Helper vars
linesToStrip = []

temperatureFanBlacklist = ["M104", "M106", "M109", "M104","M190"]
movementBlacklist = ["G1"]

# Set to true to strip all of the gcode, otherwise the code will ignore the preheat/start routine
startupComplete = True

# pull all lines out of the file
with open(filePath,"r") as f:
    mainCode = f.readlines()

# Main line-wise loop
for line in mainCode:

    if "; (GhostPrint Flag) END STARTUP" in line:
        startupComplete = True

    if startupComplete:

        if STRIP_MODE == 1:
            # temperature/fans
            for item in temperatureFanBlacklist:
                if item in line:
                    linesToStrip.append(mainCode.index(line))

            # go backwards and remove lines to preserve the indicies
            for index in reversed(linesToStrip):
                mainCode.pop(index)

        elif STRIP_MODE == 2:
            knockOut = []
            # motor knockouts
            for item in movementBlacklist:
                if item in line:
                    
                    # check for calls to the requested axes
                    for axis in knockoutAxes:

                        # find the start and end index for where we need to remove
                        startIndex = line.find(axis)
                        endIndex = line.find(" ", startIndex)

                        if endIndex == -1:
                            endIndex = len(line)

                        line = line[:startIndex] + line[endIndex:]

            
            knockOut.append(line)


        #TODO
        elif STRIP_MODE == 3:
            # flag fan and temperature codes
            for item in movementBlacklist:
                if item in line:
                    linesToStrip.append(mainCode.index(line))

            # then knock out motor codes
            

        else:
            print("Invalid strip mode")





# reconstruct the file string
if STRIP_MODE == 1:
    out = ''.join(mainCode)

elif STRIP_MODE == 2:
    out = ''.join(knockOut)

# output the stripped file
with open(outputPath,"w") as f:
    f.write(out)