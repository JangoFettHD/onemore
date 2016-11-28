import random


def giveInitPlayerPosition(arr, players):
    x = -1
    y = -1

    print(1 < x < (len(arr) - 2) > y > 1)
    print([x, y] in [])

    while not (0 < x < (len(arr) - 1) > y > 0) and not ([x, y] in []):
        x = int(random.uniform(1, (len(arr)-2)))
        y = int(random.uniform(1, (len(arr)-2)))
        print(x, y)

    return [x, y]


print(giveInitPlayerPosition([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 0))
