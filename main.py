import multiprocessing
import time
import mouse
from PIL import ImageGrab
import keyboard
from multiprocessing import Process,queues
import psutil
global closed
closed = 0
mouseduration =0.1
started = 0

def inputs():
      global paused
      paused = 0
      print("o data")
      while closed == 0:
            print("inputs")
            if keyboard.read_key() == "c":
                  closed = 1
            if keyboard.read_key() == "p":
                  if paused == 1:
                        paused = 0
                  else:
                        paused = 1
                  print(paused)
                  while paused == 0:
                        print("P")


def game():
      pixels = ImageGrab.grab(bbox=())
      startingy = -1
      a = pixels.getbbox()
      screenwidth = a[2]
      screenheight = a[3]
      for i in range (0,screenwidth):
            for j in range(0,screenheight):
                  if pixels.getpixel((i,j))==(74, 117, 44) and startingy==-1:
                        startingx=i
                        startingy=j
      squaresy=0
      squaresx=0
      lineheight=0
      linewidth=0
      color=(162, 209, 73)
      color2=(166,214,74)
      m=startingy
      pixels = ImageGrab.grab(bbox=())
      startingpixel = pixels.getpixel((startingx, m))

      while startingpixel==(74, 117, 44):
            startingpixel = pixels.getpixel((startingx, m))
            m += 1
      startingy=m
      pixely=startingpixel
      pixelx=startingpixel

      while pixely[1]>pixely[0] and pixely[1]>pixely[2]:
            pixely=pixels.getpixel((startingx,m))
            lineheight+=1
            if (color==(170, 215, 81) and pixely==(162, 209, 73)) or (pixely==(170, 215, 81) and color==(162, 209, 73)):
                  color=pixely
                  squaresy+=1

            if(color2==(166,214,74) and pixely==(174,220,82)) or (color2==(174,220,82) and pixely==(166,214,74)):
                  color2 = pixely
                  squaresy += 1
            m+=1
      incrementy=lineheight//squaresy
      m=startingx

      while pixelx[1]>pixelx[0] and pixelx[1]>pixelx[2]:
            pixelx=pixels.getpixel((m,startingy+3))
            linewidth+=1
            if (color==(170, 215, 81) and pixelx==(162, 209, 73)) or (pixelx==(170, 215, 81) and color==(162, 209, 73)):
                  color=pixelx
                  squaresx+=1

            if(color2==(166,214,74) and pixelx==(174,220,82)) or (color2==(174,220,82) and pixelx==(166,214,74)):
                  color2 = pixelx
                  squaresx += 1
            m+=1
      incrementx=linewidth//squaresx

      print(linewidth,squaresx)
      print(lineheight-1, squaresy)

      startingx-=1

      printat=""
      while closed == 0:
            matrice = [[0] * squaresy for i in range(0, squaresx)]
            vecini = [[0] * squaresy for i in range(0, squaresx)]
            flagsaround = [[0] * squaresy for i in range(0, squaresx)]
            for tilex in range(0,squaresx):
                  for tiley in range(0,squaresy):
                        colored=False
                        for j in range(int(startingy + tiley * incrementy), int(startingy + (tiley+1) * incrementy)):
                              for i in range(int(startingx + tilex * incrementx),int(startingx + (tilex + 1) * incrementx)):
                                    pixel=pixels.getpixel((i,j))
                                    if tilex==11 and tiley==19:
                                          print(pixel)
                                    if pixel[0]==119 and pixel[1]==0 and pixel[2]==162:
                                          matrice[tilex][tiley] = 4
                                          colored = True
                                          #print("purple", tilex,tiley)
                                    elif pixel[0]==0 and pixel[1]<=110 and pixel[2]//100==2:
                                          matrice[tilex][tiley] = 1
                                          colored = True
                                          #print("blue", tilex,tiley)
                                    elif pixel[0]==210 and pixel[1]+ pixel[2]<100:
                                          matrice[tilex][tiley] = 3
                                          colored = True
                                          #print("red", tilex, tiley)
                                    elif pixel[1]<140 and pixel[0]==pixel[2]==0:
                                          matrice[tilex][tiley]=2
                                          colored=True
                                          #print("Green",tilex,tiley,i,j,pixel)
                        if colored == False and (pixels.getpixel((int(startingx + (tilex + 1) * incrementx) - 3,
                                                                  int(startingy + (tiley + 1) * incrementy) - 3)) == (
                                                 215, 184, 153) or pixels.getpixel((int(startingx + (
                                tilex + 1) * incrementx) - 3, int(startingy + (tiley + 1) * incrementy) - 3)) == (
                                                 229, 194, 159)):
                              matrice[tilex][tiley] = 99
                        elif matrice[tilex][tiley]==0:
                              if tilex!=squaresx-1:
                                    vecini[tilex+1][tiley]+=1
                                    if tiley!=0:
                                          vecini[tilex + 1][tiley - 1] += 1
                              if tiley!=squaresy-1:
                                    vecini[tilex][tiley+1] += 1
                                    if tilex!=0:
                                          vecini[tilex - 1][tiley+1] += 1
                                    if tilex!=squaresx-1:
                                          vecini[tilex + 1][tiley+1] += 1
                              if tilex != 0:
                                    vecini[tilex - 1][tiley] += 1
                                    if tiley!=0:
                                          vecini[tilex - 1][tiley - 1] += 1
                              if tiley != 0:
                                    vecini[tilex][tiley - 1] += 1
            for tilex in range(0,squaresx):
                  for tiley in range(0,squaresy):
                        if matrice[tilex][tiley]==vecini[tilex][tiley]:
                              print(tilex,tiley)
                              if tilex!=squaresx-1 and matrice[tilex+1][tiley]==0 :
                                    matrice[tilex+1][tiley]="f"
                                    mouse.move(startingx+int(incrementx*(tilex+3/2)),startingy+(incrementy*(tiley+1/2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='right')
                              if tilex!=0 and matrice[tilex-1][tiley]==0 :
                                    matrice[tilex - 1][tiley] ="f"
                                    mouse.move(startingx+int(incrementx * (tilex -1 / 2)),startingy+ int(incrementy * (tiley + 1 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='right')
                              if tiley!=squaresy-1 and matrice[tilex][tiley+1]==0 :
                                    matrice[tilex][tiley+1] ="f"
                                    mouse.move(startingx+int(incrementx * (tilex + 1 / 2)),startingy+ int(incrementy * (tiley + 3 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='right')
                              if tiley!=0 and matrice[tilex][tiley-1]==0 :
                                    matrice[tilex][tiley - 1] ="f"
                                    mouse.move(startingx+int(incrementx * (tilex + 1 / 2)), startingy+int(incrementy * (tiley -1 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='right')
                              if tiley!=squaresy-1 and tilex!=squaresx-1 and matrice[tilex+1][tiley+1]==0 :
                                    matrice[tilex+1][tiley + 1] ="f"
                                    mouse.move(startingx+int(incrementx * (tilex + 3 / 2)), startingy+int(incrementy * (tiley + 3 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='right')
                              if tiley!=0 and tilex!=squaresx-1 and matrice[tilex+1][tiley-1]==0 :
                                    matrice[tilex+1][tiley - 1] ="f"
                                    mouse.move(startingx+int(incrementx * (tilex + 3 / 2)), startingy+int(incrementy * (tiley -1/ 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='right')
                              if tiley!=squaresy-1 and tilex!=0 and matrice[tilex-1][tiley+1]==0 :
                                    matrice[tilex-1][tiley + 1] ="f"
                                    mouse.move(startingx+int(incrementx * (tilex -1 / 2)), startingy+int(incrementy * (tiley + 3 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='right')
                              if tiley!=0 and tilex!=0 and matrice[tilex-1][tiley-1]==0 :
                                    matrice[tilex-1][tiley - 1] ="f"
                                    mouse.move(startingx+int(incrementx * (tilex -1 / 2)), startingy+int(incrementy * (tiley -1 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='right')
            for tilex in range(0,squaresx):
                  for tiley in range(0,squaresy):
                        if matrice[tilex][tiley]=="f":
                              if tilex != squaresx - 1:
                                    flagsaround[tilex + 1][tiley] += 1
                                    if tiley != 0:
                                          flagsaround[tilex + 1][tiley - 1] += 1
                              if tiley != squaresy - 1:
                                    flagsaround[tilex][tiley + 1] += 1
                                    if tilex != 0:
                                          flagsaround[tilex - 1][tiley + 1] += 1
                                    if tilex != squaresx - 1:
                                          flagsaround[tilex + 1][tiley + 1] += 1
                              if tilex != 0:
                                    flagsaround[tilex - 1][tiley] += 1
                                    if tiley != 0:
                                          flagsaround[tilex - 1][tiley - 1] += 1
                              if tiley != 0:
                                    flagsaround[tilex][tiley - 1] += 1
            for tilex in range(0,squaresx):
                  for tiley in range(0,squaresy):
                        if matrice[tilex][tiley]!="f" and matrice[tilex][tiley]!=0 and flagsaround[tilex][tiley]>=matrice[tilex][tiley]:
                              if tilex!=squaresx-1 and matrice[tilex+1][tiley]==0 :
                                    mouse.move(startingx+int(incrementx*(tilex+3/2)),startingy+(incrementy*(tiley+1/2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='left')
                              if tilex!=0 and matrice[tilex-1][tiley]==0 :
                                    mouse.move(startingx+int(incrementx * (tilex -1 / 2)),startingy+ int(incrementy * (tiley + 1 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='left')
                              if tiley!=squaresy-1 and matrice[tilex][tiley+1]==0 :
                                    mouse.move(startingx+int(incrementx * (tilex + 1 / 2)),startingy+ int(incrementy * (tiley + 3 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='left')
                              if tiley!=0 and matrice[tilex][tiley-1]==0 :
                                    mouse.move(startingx+int(incrementx * (tilex + 1 / 2)), startingy+int(incrementy * (tiley -1 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='left')
                              if tiley!=squaresy-1 and tilex!=squaresx-1 and matrice[tilex+1][tiley+1]==0 :
                                    mouse.move(startingx+int(incrementx * (tilex + 3 / 2)), startingy+int(incrementy * (tiley + 3 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='left')
                              if tiley!=0 and tilex!=squaresx-1 and matrice[tilex+1][tiley-1]==0 :
                                    mouse.move(startingx+int(incrementx * (tilex + 3 / 2)), startingy+int(incrementy * (tiley -1/ 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='left')
                              if tiley!=squaresy-1 and tilex!=0 and matrice[tilex-1][tiley+1]==0 :
                                    mouse.move(startingx+int(incrementx * (tilex -1 / 2)), startingy+int(incrementy * (tiley + 3 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='left')
                              if tiley!=0 and tilex!=0 and matrice[tilex-1][tiley-1]==0 :
                                    mouse.move(startingx+int(incrementx * (tilex -1 / 2)), startingy+int(incrementy * (tiley -1 / 2)),absolute=True, duration=mouseduration)
                                    mouse.click(button='left')

            print(printat)
            print(startingx,startingy,incrementx,incrementy)
            print(matrice)
            print(vecini)
            print(vecini)

if __name__ == '__main__':
      game()

      """
      #green (0, >100, 0)
      #purple (119,0,162)
      #albatru(0,99,22ceva)
      #rosu(210,<100)
      #browndark (215, 184, 153)
      #brownlight (229, 194, 159)
      #break for in for
      """


