#!/usr/bin/env python

import os
from datetime import datetime


class Dane:
    d = "0000-00-00"
    o = 0.00
    h = 0.00
    l = 0.00
    c = 0.00


def saveDane(dane, file):
    with open("data/"+file, 'w') as f_:
        for d in dane:
            f_.write(str(d.d.year) + "-" +
                     str(d.d.month) + "-" +
                     str(d.d.day) + "," +
                     str(d.o) + ","+
                     str(d.h) + "," +
                     str(d.l) + "," +
                     str(d.c) + "\n")

def readData(file):
    print("Generuje " + file)

    with  open("download/pl/"+file, 'r') as f:
        content = f.read().splitlines();

    pr_date = None
    date    = None

    op = 0
    mx = 0
    mi = 999999
    cl = 0

    i = 0
    ceny = []
    for line in content: # files are iterablei
        if (i>0):
            l = line.split(',')

            if (date != None):
                pr_date = date
            else:
                op = float(l[1])

            date = datetime.strptime(l[1], '%Y%m%d')

            if (pr_date != None and date.month != pr_date.month):
                nm = Dane()
                nm.d = pr_date
                nm.o = op
                nm.h = mx
                nm.l = mi
                nm.c = cl
                ceny.append(nm)

                op = float(l[2])
                mx = 0
                mi = 999999


            cl = float(l[5])
            if (float(l[3]) > mx):
                mx = float(l[3])

            if (float(l[4]) < mi):
                mi = float(l[4])

        i = i + 1

    nm = Dane()
    nm.d = date
    nm.o = op
    nm.h = mx
    nm.l = mi
    nm.c = cl
    ceny.append(nm)

    saveDane(ceny, file)

# main function
#==========================================================
def main():
    for file in os.listdir("download/pl"):
        if file.endswith(".txt"):
            readData(file)

main()
