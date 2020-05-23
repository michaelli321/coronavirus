import matplotlib.pyplot as plt
import random
import threading
import math

# def printit():
#   threading.Timer(5.0, printit).start()
#   print "Hello, World!"
#
# printit()

xPoints = []
yPoints = []

def addToPlot(x, y):
    global xPoints, yPoints
    xPoints += [x]
    yPoints += [y]

def plot():
    global xPoints, yPoints

    plt.plot(xPoints, yPoints, 'r.')
    plt.axis([0, 100, 0, 100])

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

if __name__=="__main__":
    for i in range(1059):
        x, y = 1000 * random.random(), 1000 * random.random()
        # for i in range(len(xPoints)):
        #     if distance(x, y, xPoints[i], yPoints[i]) < 6:
        #         color = 'g'
        #     else:
        #         color = 'r'
        addToPlot(x, y)

    for i in range(1):
        for i in range(10):
            addToPlot(random.randint(0, 100), random.randint(0, 100))
        plot()
        plt.show()
        # plt.pause(5)
