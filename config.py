# I/O paths
filePath = "tests/2Cubes.gcode"

outputPath = "tests/output.gcode"



# Mode Settings.

# Debug enable/disable
DEBUG = True

# Stripping settings, 1 for temperature/fans, 2 for extrusion, 3 for everything
STRIP_MODE = 3

# Motors to knock out if on modes 2 or 3
# Options are "X", "Y", "Z" and "E"
knockoutAxes = ["Y","Z","E"]