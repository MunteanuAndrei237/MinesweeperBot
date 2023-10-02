import time
import mouse
from PIL import ImageGrab
import keyboard
import copy

global closed
import sys

sys.setrecursionlimit(15000)
# Set global variables; you can modify the mouse speed and pause time (the value is in seconds)
closed = 0
mouseduration = 0.1
pauseTime = 0.1


def play():
    # Get the screen pixels and calculate the box, the starting x and y, the number of squares and their width/height
    pixels = ImageGrab.grab(bbox=())
    startingy = -1
    screenwidth = pixels.getbbox()[2]
    screenheight = pixels.getbbox()[3]
    for i in range(0, screenwidth):
        for j in range(0, screenheight):
            if pixels.getpixel((i, j)) == (74, 117, 44) and startingy == -1:
                startingx = i
                startingy = j
    squaresy = 0
    squaresx = 0
    lineheight = 0
    linewidth = 0
    color = (162, 209, 73)
    color2 = (166, 214, 74)
    m = startingy
    startingpixel = pixels.getpixel((startingx, m))

    while startingpixel == (74, 117, 44):
        startingpixel = pixels.getpixel((startingx, m))
        m += 1
    startingy = m
    pixely = startingpixel
    pixelx = startingpixel

    while pixely[1] > pixely[0] and pixely[1] > pixely[2]:
        pixely = pixels.getpixel((startingx, m))
        lineheight += 1
        if (color == (170, 215, 81) and pixely == (162, 209, 73)) or (
                pixely == (170, 215, 81) and color == (162, 209, 73)):
            color = pixely
            squaresy += 1

        if (color2 == (166, 214, 74) and pixely == (174, 220, 82)) or (
                color2 == (174, 220, 82) and pixely == (166, 214, 74)):
            color2 = pixely
            squaresy += 1
        m += 1
    incrementy = lineheight // squaresy
    m = startingx

    while pixelx[1] > pixelx[0] and pixelx[1] > pixelx[2]:
        pixelx = pixels.getpixel((m, startingy + 3))
        linewidth += 1
        if (color == (170, 215, 81) and pixelx == (162, 209, 73)) or (
                pixelx == (170, 215, 81) and color == (162, 209, 73)):
            color = pixelx
            squaresx += 1

        if (color2 == (166, 214, 74) and pixelx == (174, 220, 82)) or (
                color2 == (174, 220, 82) and pixelx == (166, 214, 74)):
            color2 = pixelx
            squaresx += 1
        m += 1

    incrementx = linewidth // squaresx

    # Vector for neighbors of every square
    neighbourvector = [[0, 1], [1, 0], [-1, 0], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]

    # Function that verifies the validity of a neighbor square
    def valid(xcoord, ycoord):
        if xcoord >= 0 and ycoord >= 0 and xcoord < squaresx and ycoord < squaresy:
            return True
        return False

    flagsaround = [[0] * squaresy for i in range(0, squaresx)]

    # Function that modifies the vector flagsaround
    def flagsmodifyvectors(sqx, sqy):
        for movement in neighbourvector:
            if valid(sqx + movement[0], sqy + movement[1]):
                flagsaround[sqx + movement[0]][sqy + movement[1]] += 1

    startingx -= 1
    gamevector = [[0] * squaresy for i in range(0, squaresx)]
    numbervector = [[0] * squaresy for i in range(0, squaresx)]
    # Press in the top left corner to start the gameloop
    mouse.move(startingx + 2, startingy + 2, absolute=True, duration=mouseduration)
    mouse.click(button='left')
    mouse.move(startingx + 2, startingy + 2, absolute=True, duration=mouseduration)
    while closed == 0:
        gamedone = True
        pixels = ImageGrab.grab(bbox=())
        neighbours = [[0] * squaresy for i in range(0, squaresx)]
        oldgamevector = copy.deepcopy(gamevector)

        # We read the game box and modify the gamevector (0 for grass 99 for brown f for flag and numbers for numbers)
        # We also add the modify the neighbours vector to check how many empty squares and flag squares are nearby
        for tilex in range(0, squaresx):
            for tiley in range(0, squaresy):
                colored = False
                for j in range(int(startingy + tiley * incrementy),
                               int(startingy + (tiley + 1) * incrementy)):
                    for i in range(int(startingx + tilex * incrementx),
                                   int(startingx + (tilex + 1) * incrementx)):
                        pixel = pixels.getpixel((i, j))
                        if pixel[0] == 0 and pixel[1] <= 110 and pixel[2] // 100 == 2:
                            gamevector[tilex][tiley] = 1
                            numbervector[tilex][tiley] = 1
                            colored = True
                        elif pixel[1] < 140 and pixel[0] == pixel[2] == 0:
                            gamevector[tilex][tiley] = 2
                            numbervector[tilex][tiley] = 1
                            colored = True
                        elif pixel[0] == 210 and pixel[1] + pixel[2] < 100:
                            gamevector[tilex][tiley] = 3
                            numbervector[tilex][tiley] = 1
                            colored = True
                        elif pixel[0] > 116 and pixel[0] < 122 and pixel[2] == 162:
                            gamevector[tilex][tiley] = 4
                            numbervector[tilex][tiley] = 1
                            colored = True
                        elif pixel[0] > 252 and pixel[1] > 133 and pixel[2] == 0:
                            gamevector[tilex][tiley] = 5
                            numbervector[tilex][tiley] = 1
                            colored = True
                        elif pixel[0] < 5 and pixel[2] > 164 and pixel[2] < 171:
                            gamevector[tilex][tiley] = 6
                            numbervector[tilex][tiley] = 1
                            colored = True
                        elif pixel[0] < 71 and pixel[1] < 70 and pixel[2] < 70:
                            gamevector[tilex][tiley] = 7
                            numbervector[tilex][tiley] = 1
                            colored = True
                            # print("NEGRU7")

                if colored == False and (pixels.getpixel((int(startingx + (tilex + 1) * incrementx) - 3,
                                                          int(startingy + (tiley + 1) * incrementy) - 3)) == (
                                                 215, 184, 153) or pixels.getpixel((int(startingx + (
                        tilex + 1) * incrementx) - 3, int(startingy + (tiley + 1) * incrementy) - 3)) == (
                                                 229, 194, 159)):
                    gamevector[tilex][tiley] = 99
                elif gamevector[tilex][tiley] == 0 or gamevector[tilex][tiley] == "f":
                    if gamevector[tilex][tiley] == 0:
                        gamedone = False
                    for movement in neighbourvector:
                        if valid(tilex + movement[0], tiley + movement[1]):
                            neighbours[tilex + movement[0]][tiley + movement[1]] += 1
        if gamedone == True:
            break
        # if the number of neighbors is equal to the number written on the square then we can add flags around, modifying the flagsaround vector
        for tilex in range(0, squaresx):
            for tiley in range(0, squaresy):
                if gamevector[tilex][tiley] == neighbours[tilex][tiley]:
                    for movement in neighbourvector:
                        if valid(tilex + movement[0], tiley + movement[1]) and gamevector[tilex + movement[0]][
                            tiley + movement[1]] == 0:
                            gamevector[tilex + movement[0]][tiley + movement[1]] = "f"
                            mouse.move(startingx + int(incrementx * (tilex + movement[0] + 1 / 2)),
                                       startingy + int(incrementy * (tiley + movement[1] + 1 / 2)),
                                       absolute=True, duration=mouseduration)
                            mouse.click(button='right')
                            flagsmodifyvectors(tilex + movement[0], tiley + movement[1])
        # if we have more flags around a square which has a number written on it that means there are no more bombs nearby so we can dig in the grass(0) tiles
        for tilex in range(0, squaresx):
            for tiley in range(0, squaresy):
                if numbervector[tilex][tiley] == 1 and flagsaround[tilex][tiley] >= gamevector[tilex][tiley]:
                    for movement in neighbourvector:
                        if valid(tilex + movement[0], tiley + movement[1]) and gamevector[tilex + movement[0]][
                            tiley + movement[1]] == 0:
                            mouse.move(startingx + int(incrementx * (tilex + movement[0] + 1 / 2)),
                                       startingy + int(incrementy * (tiley + movement[1] + 1 / 2)),
                                       absolute=True, duration=mouseduration)
                            mouse.click(button='left')
        # if the trivial approach does not work, we try to use backtracking by checking chains of "exposed squares" and filling them with flag combinations
        # after we get al the working combinations, we add them and see which spots do not contain any flags.That means there are no bombs and we can dig them
        tried = []
        while oldgamevector == gamevector:
            grasssquares = []
            exposedsquares = []
            foruse = []
            currentexposedsquare = [0, 0, 0]
            # we get the chains of exposed squares and the "grass" squares around them
            for tilex in range(0, squaresx):
                for tiley in range(0, squaresy):
                    if numbervector[tilex][tiley] == 1 and gamevector[tilex][tiley] - flagsaround[tilex][
                        tiley] > 0 and [tilex, tiley] not in tried:
                        currentexposedsquare = [tilex, tiley, gamevector[tilex][tiley] - flagsaround[tilex][tiley]]
                        exposedsquares.append(currentexposedsquare)
                        foruse.append(currentexposedsquare)
                        tried.append([tilex, tiley])
                        break;
                if currentexposedsquare != [0, 0, 0]:
                    break;
            while foruse != []:
                currentexposedsquare = foruse[0]
                for movement in neighbourvector:
                    if valid(currentexposedsquare[0] + movement[0], currentexposedsquare[1] + movement[1]) and \
                            gamevector[currentexposedsquare[0] + movement[0]][
                                currentexposedsquare[1] + movement[1]] == 0 and [currentexposedsquare[0] + movement[0],
                                                                                 currentexposedsquare[1] + movement[
                                                                                     1]] not in grasssquares:
                        grasssquares.append(
                            [currentexposedsquare[0] + movement[0], currentexposedsquare[1] + movement[1]])
                        for movement2 in neighbourvector:
                            if valid(currentexposedsquare[0] + movement[0] + movement2[0],
                                     currentexposedsquare[1] + movement[1] + movement2[1]) and \
                                    numbervector[currentexposedsquare[0] + movement[0] + movement2[0]][
                                        currentexposedsquare[1] + movement[1] + movement2[1]] == 1 \
                                    and [currentexposedsquare[0] + movement[0] + movement2[0],
                                         currentexposedsquare[1] + movement[1] + movement2[1],
                                         gamevector[currentexposedsquare[0] + movement[0] + movement2[0]][
                                             currentexposedsquare[1] + movement[1] + movement2[1]] -
                                         flagsaround[currentexposedsquare[0] + movement[0] + movement2[0]][
                                             currentexposedsquare[1] + movement[1] + movement2[
                                                 1]]] not in exposedsquares:
                                exposedsquares.append([currentexposedsquare[0] + movement[0] + movement2[0],
                                                       currentexposedsquare[1] + movement[1] + movement2[1],
                                                       gamevector[currentexposedsquare[0] + movement[0] + movement2[0]][
                                                           currentexposedsquare[1] + movement[1] + movement2[1]] -
                                                       flagsaround[
                                                           currentexposedsquare[0] + movement[0] + movement2[0]][
                                                           currentexposedsquare[1] + movement[1] + movement2[1]]])
                                foruse.append([currentexposedsquare[0] + movement[0] + movement2[0],
                                               currentexposedsquare[1] + movement[1] + movement2[1]])
                                tried.append([currentexposedsquare[0] + movement[0] + movement2[0],
                                              currentexposedsquare[1] + movement[1] + movement2[1]])
                foruse.pop(0)
            # here we define the possible bombs,which is the sum of all working combination of flags and bkt squares so the prograsm doest't eat too much memory
            bktsquares = []
            for exposedsq in exposedsquares:
                bktsquares.append([exposedsq[0], exposedsq[1]])
            possiblebombs = [0] * len(grasssquares)

            # we define the bkt function ,path represents a series of 0s and 1s, 0 for no flag and 1 for flag
            def backtrack(path=[]):
                if len(path) == len(grasssquares):
                    temporaryflags = [0] * len(exposedsquares)
                    for airsq in grasssquares:
                        if path[grasssquares.index(airsq)] == 1:
                            for movement in neighbourvector:
                                if [airsq[0] + movement[0], airsq[1] + movement[1]] in bktsquares:
                                    temporaryflags[
                                        bktsquares.index([airsq[0] + movement[0], airsq[1] + movement[1]])] += 1
                    solved = True
                    # if the flags we placed dont satisfy every bkt square (bringing their unknown bombs to exactly 0) then we do not add the solution to the sum of all working combination
                    for i in range(0, len(temporaryflags)):
                        if temporaryflags[i] != exposedsquares[i][2]:
                            solved = False
                    if solved == True:
                        for i in range(0, len(possiblebombs)):
                            possiblebombs[i] += path[i]
                    return

                for value in [0, 1]:
                    path.append(value)
                    backtrack(path)
                    path.pop()

            backtrack([])
            # if there are squares that have no bomb in all working combination,then it means we can dig it
            for i in range(0, len(possiblebombs)):
                if possiblebombs[i] == 0:
                    oldgamevector = []
                    mouse.move(startingx + int(incrementx * (grasssquares[i][0] + 1 / 2)),
                               startingy + int(incrementy * (grasssquares[i][1] + 1 / 2)), absolute=True,
                               duration=mouseduration)
                    mouse.click(button='left')

        time.sleep(pauseTime)


if __name__ == '__main__':
    # if we press p we start the play function, c for closing the program
    while closed == 0:
        if keyboard.read_key() == "p":
            play()
            break
        if keyboard.read_key() == "c":
            closed = 1
