import logging as lg
import os

# Establish common file path for all debugging logs/documentation:
currDir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory is: {currDir}")
debugDir = os.path.join(currDir, 'logs')

if not os.path.isdir(debugDir):
    os.mkdir(debugDir)
    print("No debug log directory. Creating one now.")

class DebugClient:
   def ToDebugPath(filename):
       logPath = os.path.join(debugDir,filename)
       return logPath