#!/usr/bin/env python

'''
@package gieldomat
'''

import os

class Dane:
    d = "0000-00-00"
    o = 0.00
    h = 0.00
    l = 0.00
    c = 0.00
    ss  = 0
    s10 = 0.00
    s15 = 0.00

def sygnaly(d, fi):
    i = 0
    l = len(d) - 1
    
    txt = ""
    if (d[l].o < d[l].s10 and d[l].c > d[l].s10):
        txt = "SMA10 - sygnal kupna "+ str(d[l].d) + " " + str(d[l].c) + " " + str(d[l].s10) + "\n"

    if (d[l].o < d[l].s15 and d[l].c > d[l].s15):
       txt = txt + "SMA15 - sygnal kupna " + str(d[l].d) + " " + str(d[l].c) + " " + str(d[l].s15) + "\n"
    
    if (d[l].o > d[l].s10 and d[l].c < d[l].s10):
        txt = txt + "SMA10 - sygnal sprzedazy "+ str(d[l].d) + " " + str(d[l].c) + " " + str(d[l].s10) + "\n"

    if (d[l].o > d[l].s15 and d[l].c < d[l].s15):
        txt = txt + "SMA15 - sygnal sprzedazy "+ str(d[l].d) + " " + str(d[l].c) + " " + str(d[l].s15) + "\n"

    if (txt != ""):
        with open("out/raport.txt", 'a') as f_:
            f_.write("   " + fi + "\n")
            f_.write(" \n")
            f_.write(txt)
            f_.write("============================================================\n")

def calcSMA(dane):
    i = 0
    sum10 = 0
    sum15 = 0
    for d in dane:
        if (i < 10):
            sum10 = sum10 + d.c
        if (i < 15):
            sum15 = sum15 + d.c

        if (i >= 10):
            d.s10 = sum10 / 10 
            sum10 = sum10 - dane[i-10].c
            sum10 = sum10 + d.c
        
        if (i >= 15):
            d.s15 = sum15 / 15 
            sum15 = sum15 - dane[i-15].c
            sum15 = sum15 + d.c

        i = i + 1;


    return dane

# odczyt danych z pliku
#==========================================================
def readData(file):
    print("Przetwarzam " + file)
 
    with  open("data/"+file, 'r') as f:
        content = f.read().splitlines();
    
    i = 0
    ceny = []
    for line in content: # files are iterablei
        if i > 0:
            l = line.split(',')
            dane = Dane()
            dane.d = l[0]
            dane.o = float(l[1])
            dane.h = float(l[2])
            dane.l = float(l[3])
            dane.c = float(l[4])
            ceny.append(dane)
        i = i + 1

    calcSMA(ceny)
    sygnaly(ceny, file)

# main function
#==========================================================
def main():
    for file in os.listdir("data"):
        if (file.endswith(".csv") or file.endswith(".txt")):
            readData(file)



main()

