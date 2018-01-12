#import sys for command-line reading, pandas for csv reading, Predictor to predict closing price for time t
import sys
import pandas as pd
from Predictor import Predictor

def main():
    #read the arguments from the command line, excluding Assessment.py
    args = sys.argv[1:]
    #if the user provides us with no time t via the command line
    if len(args) == 0:
        #define the error strings
        errorStrings = ["Give a command line argument denoting time t.", "Example Command: python Assessment.py 5, 10, 100, 1000"]
        #print the error strings
        printIt(errorStrings)
        return

    #otherwise, instantiate the predictor class
    predictor = Predictor()
    #for each argument provided via the command line
    for arg in args:
        #make sure the argument has no errors
        if( noErrorsInArg(arg) ):
            #get the int version of the arg
            t = int(arg)
            #predict the closing price for day t
            interval = 30
            testOutcome = predictor.getPredictionForDay(t, interval)
            printIt(testOutcome)

def noErrorsInArg(s):
    #try to convert the string to an int
    try:
        #get int version of string
        t = int(s)
        #if time t <= 0, there is no data for us to predict
        if t <= 0:
            printIt("Number must be positive integer, not " + s)
            return False
        #get the data of the cvs file
        data = pd.read_csv("EZA_Daily.csv")
        #if the number wants a time t too large for the data set
        if t >= len(data.index):
            #this is an issue
            printIt("Number too large. Last t of data set is: " + str( len(data.index) ) )
            return False

        #all checks are passed, return true
        return True

    #if number cannot be converted to an int, return false
    except ValueError:
        printIt(s + " is not a positive integer.")
        return False

#The following method prints a string or list of strings in the desired format
def printIt(strings):
        print
        print "*"*60

        if type(strings) == str:
            print strings

        if type(strings) == list:
            for string in strings:
                print string

        print "*"*60
        print

#run the main method
if __name__ == "__main__":
    main()
