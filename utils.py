from datetime import datetime
import os

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

#checks to see if coordinates (x, y) are on the board
def onGrid(x,y):
    if((x in range(8)) and (y in range(8))):
        return True
    else:
        return False


#prints a log string to the console
def logToConsole(*strings):
    dt = datetime.today()
    print("<%02i/%02i/%04i" % (dt.month,dt.day,dt.year),end=" ")
    print("%02i:%02i:%02i>" % (dt.hour,dt.minute,dt.second),end=" ")
    for string in strings:
        print(string,end="")
    print()