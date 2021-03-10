#import pozadovanych knihoven
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import uniform
import queue as q
import random

iters = 6  #pocet iteraci
n = (2 **iters)+1 # velikost zakladni plochy


def getMiddlePoint(grid, a):  # pro kazdy stredovy bod vypocitej perturbaci pro hranicni body
    if (grid[a[0] + a[2]][
        a[1] + a[2]] == 0):  # pokud hranicni body neprosly perturbaci (pocatecni stav) tak jim prirad nahodnou hodnotu
        grid[a[0] + a[2]][a[1] + a[2]] = uniform(-1, 1)
        grid[a[0] - a[2]][a[1] + a[2]] = uniform(-1, 1)
        grid[a[0] + a[2]][a[1] - a[2]] = uniform(-1, 1)
        grid[a[0] - a[2]][a[1] - a[2]] = uniform(-1, 1)

    # vypocitej prumernou hodnotu pro hranicni body a prirad je
    avg = ((grid[a[0] + a[2]][a[1] + a[2]]) + (grid[a[0] - a[2]][a[1] + a[2]]) + (grid[a[0] + a[2]][a[1] - a[2]]) + (
    grid[a[0] - a[2]][a[1] - a[2]])) / 4
    grid[a[0]][a[1]] = avg + uniform(-1, 1)
    grid[a[0] + a[2]][a[1]] = avg + uniform(-1, 1) * a[3]
    grid[a[0]][a[1] + a[2]] = avg + uniform(-1, 1) * a[3]
    grid[a[0] - a[2]][a[1]] = avg + uniform(-1, 1) * a[3]
    grid[a[0]][a[1] - a[2]] = avg + uniform(-1, 1) * a[3]
    # print(grid)
    # print("--------------------------------------------------")


def numberOfIters(n):  # funkce pro navrat poctu iteraci(pocet ctvercu) podle velikosti plochy
    size = (n - 1) ** 2
    number = 0
    var = n - 1
    while (var != 1):
        number += size // (var ** 2)
        var //= 2
    return number


def fractalLand(n, iters):
    grid = np.zeros((n, n))  # vytvorim matici n*n
    # meanGrid = np.zeros((n*n))
    supQ = q.Queue()  # podporujici fronta
    midPoints = q.Queue()  # fronta stredovych bodu jednotlivych ctvercu
    step = ((n - 1) // 2)  # krok
    perturbation = n  # zmena jednotlivych hranicnich bodu postupne snizuji o 2
    supQ.put([step, step, step])  # prvotni stred cele matice n*n
    midPoints.put([step, step, step, perturbation])
    iterations = numberOfIters(n)
    resizeStep = True
    var = 1
    var2 = 0
    # while(supQ.empty() != True):
    while (iterations > 1):
        if (resizeStep == True):
            step = step // 2
            perturbation /= 2
        a = supQ.get()
        if (a[0] + step <= len(grid) - 1):
            supQ.put([a[0] + step, a[1] + step,
                      step])  # do podporove fronty vkladam jednotlive stredy a pro tyhle stredy vkladam dalsi
            supQ.put([a[0] + step, a[1] - step,
                      step])  # stredy podle kroku, takze skacu doleva nahoru doprava nahoru atd. tim dostanu
            supQ.put([a[0] - step, a[1] + step, step])  # vsechny "podctverecky" daneho ctverce
            supQ.put([a[0] - step, a[1] - step, step])
            midPoints.put([a[0] + step, a[1] + step, step, perturbation])
            midPoints.put([a[0] + step, a[1] - step, step, perturbation])
            midPoints.put([a[0] - step, a[1] + step, step, perturbation])
            midPoints.put([a[0] - step, a[1] - step, step, perturbation])
            iterations = iterations - 4
            var2 += 1
        if (var == var2):
            var2 = 0
            resizeStep = True
            var *= 4  # 4 "podctverecky" pro kazdy ctverec takze musim nasobit 4* az po projeti vsech podctverecku zmensuju krok
        else:
            resizeStep = False

    while (midPoints.empty() != True):
        b = midPoints.get()  # vem prvni vlozeny stredovy bod
        getMiddlePoint(grid,
                       b)  # a vloz ho do funkce getMiddlePoint nazev je zavadejici ale pochazi z puvodni implementace
        # tak jsem to uz nemenil :D

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, projection='3d')
    x, y = np.meshgrid(np.arange(n), np.arange(n))
    ax.plot_surface(x, y, grid, rstride=1, cstride=1, cmap=plt.cm.rainbow)
    plt.show()


fractalLand(n, iters)