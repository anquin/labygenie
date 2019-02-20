#!/usr/bin/python

# Copyright (C) 2016 Andre Q. Barbosa

# This file is part of Labygenie.

# Labygenie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from graphs import Graph
from graphs import GraphWalker
from graphs import findGenTree
from graphs import findPath

from random import random

class Labirynth(object):
    def __init__(self, tree, w, h, start, end):
        self._tree = tree
        self._w = w
        self._h = h
        self._start = start
        self._end = end

    def getGraph(self):
        return self._tree

    def getStart(self):
        return self._start

    def getEnd(self):
        return self._end

    def __str__(self):
        l = []
        for y in xrange(2 * self._h + 1):
            y = []
            l.append(y)
            for x in xrange(2 * self._w + 1):
                y.append('#')

        nV = self._tree.getNV()

        import sys
        for i in xrange(nV):
            for j in xrange(nV):
                x = (1 + (j % self._w) * 2)
                y = (1 + (j / self._w) * 2)
                l[y][x] = ' '
                if (self._tree.existE(i+1, j+1)):
                    #print "(%d, %d) (%d, %d)" % (i, j, x, y)
                    if (j == (i + 1)):
                        l[y][x - 1] = ' '
                    elif (j == (i - 1)):
                        l[y][x + 1] = ' '
                    elif (j > i):
                        l[y-1][x] = ' '
                    else:
                        l[y+1][x] = ' '


        startlin = 1 + ((self._start - 1) / self._w * 2)
        startcol = 1 + ((self._start - 1) % self._w * 2)
        endlin = 1 + ((self._end - 1) / self._w * 2)
        endcol = 1 + ((self._end - 1) % self._w * 2)
        l[startlin][startcol] = 'S'
        l[endlin][endcol] = 'E'

        #print "start: %d, end: %d" % (self._start, self._end)

        s = ""
        for lin in l:
            for col in lin:
                s += col
            s += "\n"
        return s

def makeGrid(x, y):
    nV = x * y
    g = Graph(nV);
    for j in xrange(1, y + 1):
        linBeg = (j - 1) * x + 1
        for i in xrange(x):
            if (i < (x - 1)):
                g.addE(linBeg + i, linBeg + i + 1)
            if (j != y):
                g.addE(linBeg + i, linBeg + i + x)

    return g

def generateLabirynth(x, y):
    g = makeGrid(x, y)
    startDfs = (int)(random() * g.getNV())
    g.randomizeEs()
    tree = findGenTree(g, startDfs)

    es = []
    for i in xrange(tree.getNV()):
        es.append([])
    leaves = []

    def visitE(v, w):
        if (w not in es[v-1]):
            es[v-1].append(w)
        if (v not in es[w-1]):
            es[w-1].append(v)
        return GraphWalker.STATUS_CONTINUE

    GraphWalker.dfs(tree, startDfs, None, visitE)

    i = 1
    for e in es:
        if (len(e) == 1):
            leaves.append(i)
        i += 1
    print "LEAVES: ", leaves
    endIdx = (int)(random() * len(leaves))
    end = leaves[endIdx]
    del leaves[endIdx]
    start = leaves[(int)(random() * len(leaves))]

    if (len(findPath(tree, start, end)) == 0):
        raise Exception("Cannot generate labirynth: End is unreachable!\n"
                        + str(tree) + "\nstart: " + str(start) + "\nend: " + str(end))

    return Labirynth(tree, x, y, start, end)

if __name__ == '__main__':
    x = 34
    y = 15
    labirynth = generateLabirynth(x, y)
    labstr = str(labirynth)
    #print labstr

    solution = findPath(labirynth.getGraph(),
                        labirynth.getStart(),
                        labirynth.getEnd())
    labarr = list(labstr)
    prevV = 0
    for v in solution:
        pos = 2*x+3 + (((v-1)/x)*2*x)*2 + ((v-1)/x*4) + (((v-1)%x))*2
        if (labarr[pos] == ' '):
            labarr[pos] = '.'
        if (prevV != 0):
            if (prevV == v + 1):
                labarr[pos + 1] = '.'
            elif (prevV == v - 1):
                labarr[pos - 1] = '.'
            elif (prevV < v):
                labarr[pos-(x*2+3)+1] = '.'
            else:
                labarr[pos+(x*2+3)-1] = '.'
        prevV = v
    print "".join(labarr)

    #print "Solution: \n", solution
