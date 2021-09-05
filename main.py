import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

img = plt.imread("7.png")

def convert(list):
    return tuple(map(tuple, list))

def generateHeatmap(): 
    a = [[1410,870],[1411,870],[1323,832],[1336,854],[1335,854],[1323,832],[1410,869],[1409,869],[1334,854],[1408,869],[1333,854],[1323,827]]
    b = convert(a)

    img = plt.imread("7.png")
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.hist2d(b)

    plt.show()


if __name__ == "__main__":
    generateHeatmap()