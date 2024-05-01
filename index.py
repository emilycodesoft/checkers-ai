#import needed functions
import turtle
from CheckersGame import CheckersGame
from utils import logToConsole

gameTitle = "pyCheckers v1.00"

#setup output window
wn = turtle.Screen()
wn.setup(0.95, 0.95)
wn.tracer(0,0)
turtle.speed("fastest")
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
    logToConsole("Main Program Loop Ended")
    game.showStatistics()
    return
    #announce end of main program loop

main()