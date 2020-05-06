import numpy as np
import random
import time
from interruptingcow import timeout
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

def init():
    map = np.zeros((6,7), dtype=int)
    district = 1
    startx = random.randint(0, map.shape[0]-1)
    starty = random.randint(0,map.shape[1]-1)
    return map, district, startx, starty

def find_district(map, district, startx, starty):
    while np.count_nonzero(map) < 42:
        map = np.zeros((6,7), dtype=int)
        count = 0
        district = 0
        try:
            with timeout(0.0025, exception=RuntimeError):
                while district < 7:
                    count = 0
                    if map[startx][starty] != 0 and np.count_nonzero(map) < 42:
                        start_list = np.where(map==0)
                        start_list = list(start_list)
                        for i in start_list:
                            random.shuffle(i)
                        startx = start_list[0][0]
                        starty = start_list[1][0]
                    adjacent = [(startx-1, starty), (startx, starty-1), (startx, starty+1), (startx+1, starty)]
                    random.shuffle(adjacent)
                    while count < 7:
                        for a in adjacent:
                            if 0 <= a[0] and abs(a[0]) < map.shape[0] and 0 <= a[1] and abs(a[1]) < map.shape[1]:
                                if map[a[0]][a[1]] == 0:
                                    map[a[0]][a[1]] = district
                                    startx = a[0]
                                    starty = a[1]
                                    adjacent = [(startx-1, starty), (startx, starty-1), (startx, starty+1), (startx+1, starty)]
                                    random.shuffle(adjacent)
                                    break
                        count +=1
                    district += 1
        except RuntimeError:
            pass
    return map

def show(map):
    print(map)
    plt.imshow(map, interpolation = 'nearest')
    plt.yticks([])
    plt.xticks([])
    plt.show()

def perimeter(map):
    perimeter = 0
    area = 7
    for i in range(6):
        for j in range(7):
            if map[i][j] == 1:
                perimeter += (4 - num_of_neighbor(i, j, map))
    print("A/p^2:", area, "/", (perimeter ** 2), "=", area/(perimeter ** 2))

def num_of_neighbor(i, j, map):
    count = 0
    if (i > 0 and map[i - 1][j]==1):
        count +=1
    if (j > 0 and map[i][j - 1]==1):
        count+=1
    if (i < 5 and map[i + 1][j]==1):
        count+=1 
    if (j < 6 and map[i][j + 1]==1):
        count+=1 
    return count

def main():
    while input("Hit enter for a new district or q to quit   ") != "q":
        (map1, district, startx, starty) = init()
        map1 = find_district(map1, district, startx, starty)
        perimeter(map1)
        show(map1)

main()
