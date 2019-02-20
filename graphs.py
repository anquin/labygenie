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

from random import shuffle

class Graph(object):
    def __init__(self, nV):
        self._nV = nV
        self._es = []
        # lists are zero-terminated
        for i in xrange(nV):
            self._es.append([0])

    def getNV(self):
        return self._nV

    def addE(self, a, b):
        if (b not in self._es[a-1]):
            self._es[a-1][-1] = b
            self._es[a-1].append(0)
        if (a not in self._es[b-1]):
            self._es[b-1][-1] = a
            self._es[b-1].append(0)

    def removeE(self, a, b):
        self._es[a-1].remove(b)
        self._es[b-1].remove(a)

    def getEIter(self, v):
        return iter(self._es[v - 1])

    def getNE(self):
        c = 0
        for e in self._es:
            c += len(e) - 1
        return c

    def existE(self, v, w):
        return (w in self._es[v - 1])

    def randomizeEs(self):
        for e in self._es:
            shuffle(e)
            zi = e.index(0)
            e[zi] = e[zi] ^ e[-1]
            e[-1] = e[zi] ^ e[-1]
            e[zi] = e[-1] ^ e[zi]

    def __str__(self):
        s = "G: \n"
        for i in xrange(len(self._es)):
            s += "  " + str(i+1) + ": " + str(self._es[i]) + "\n"
        return s

class GraphWalker(object):
    STATUS_CONTINUE = 0
    STATUS_STOP = 1

    @classmethod
    def dfs(clazz, g, v, funcV, funcE):
        s = []
        t = g.getNV() * [0]
        s.append(v)
        eIter = g.getEIter(v)
        c = 0

        w = eIter.next()

        t[v-1] = 1
        if (funcV != None):
            if (funcV(v) == clazz.STATUS_STOP):
                return s
        while (len(s) > 0):
            while (w != 0):
                if (t[w-1] == 0):
                    c += 1
                    t[w-1] = 1
                    s.append(w)
                    if (funcV != None):
                        if (funcV(w)
                          == clazz.STATUS_STOP):
                            return s
                    if (funcE != None):
                        if (funcE(v, w)
                          == clazz.STATUS_STOP):
                            return s
                    v = w
                    eIter = g.getEIter(v)

                w = eIter.next()
            del s[-1]
            if (len(s)):
                v = s[-1]
            eIter = g.getEIter(v)
            w = eIter.next()
        return s

    @staticmethod
    def _makePath(parents, v):
        path = [v]
        v = parents[v-1]
        while (v != 0):
            path.insert(0, v)
            v = parents[v-1]
        return path

    @classmethod
    def bfs(clazz, g, v, funcV, funcE):
        t = g.getNV() * [0]
        q = []
        path = []
        parents = g.getNV() * [0]

        if (funcV != None):
            if (funcV(v) == clazz.STATUS_STOP):
                return clazz._makePath(parents, v)

        q.append(v)
        t[v-1] = 1
        eIter = g.getEIter(v)
        w = eIter.next()

        while (len(q) != 0):
            while (w != 0):
                if (t[w-1] == 0):
                    parents[w-1] = v
                    t[w-1] = 1
                    q.append(w)
                    if (funcV != None):
                        if (funcV(w) == clazz.STATUS_STOP):
                            return clazz._makePath(parents, w)
                    if (funcE != None):
                        if (funcE(v, w) == clazz.STATUS_STOP):
                            return clazz._makePath(parents, w)
                w = eIter.next()
            del q[0]
            if (len(q)):
                v = q[0]
            eIter = g.getEIter(v)
            w = eIter.next()

        return clazz._makePath(parents, w)

def findPath(g, start, stop):
    def visitV(v):
        if (v == stop):
            return GraphWalker.STATUS_STOP
        return GraphWalker.STATUS_CONTINUE

    return GraphWalker.bfs(g, start, visitV, None)

def findGenTree(g, start):
    genTree = Graph(g.getNV())

    def visitE(v, w):
        genTree.addE(v, w)
        return GraphWalker.STATUS_CONTINUE

    GraphWalker.dfs(g, start, None, visitE)
    return genTree

if __name__ == '__main__':
    g = Graph(7)
    g.addE(1, 2)
    g.addE(1, 4)
    g.addE(1, 6)
    g.addE(2, 3)
    g.addE(2, 5)
    g.addE(3, 4)
    g.addE(5, 7)

    start = 4
    stop = 7
    path = findPath(g, start, stop)

    print str(g)
    print "Path(%d to %d): %s" % (start, stop, str(path))
    path = findPath(g, stop, start)
    print "Path(%d to %d): %s" % (stop, start, str(path))

    print "Generator Tree from %d: %s" \
        % (start, findGenTree(g, start))
