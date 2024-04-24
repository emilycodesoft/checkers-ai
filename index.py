#import needed functions
import turtle
from CheckersGame import CheckersGame
from utils import logToConsole

gameTitle = "pyCheckers v1.00"

#setup output window
wn = turtle.Screen()
wn.setup(width = 1200, height = 700)
# wn.bgcolor("black")
wn.tracer(0,0)
wn.title(gameTitle)


def main():

    logToConsole("Program Starting...")
    logToConsole("Running Game: ",gameTitle)
    #creates game instance
    game = CheckersGame(wn)

    #attach mouseEvent to click
    wn.onclick(game.mouseEvent)

    #begin main program loop
    logToConsole("Mouse Event attatched to window")
    logToConsole("Beginning Main Program Loop...\n")
    wn.mainloop()

    #announce end of main program loop
    logToConsole("Main Program Loop Ended")

main()