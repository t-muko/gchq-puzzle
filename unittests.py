import unittest
import kuokka
import array
import numpy as np
import time


class TestGrid(unittest.TestCase):



  @classmethod
  def setUpClass(cls):

    K=[[7,3,1,1,7],
     [1,1,2,2,1,1],
     [1,3,1,3,1,1,3,1],
     [1,3,1,1,6,1,3,1],
     [1,3,1,5,2,1,3,1],
     [1,1,2,1,1],
     [7,1,1,1,1,1,7],
     [3,3],
     [1,2,3,1,1,3,1,1,2],
     [1,1,3,2,1,1],
     [4,1,4,2,1,2],
     [1,1,1,1,1,4,1,3],
     [2,1,1,1,2,5],
     [3,2,2,6,3,1],
     [1,9,1,1,2,1],
     [2,1,2,2,3,1],
     [3,1,1,1,1,5,1],
     [1,2,2,5],
     [7,1,2,1,1,1,3],
     [1,1,2,1,2,2,1],
     [1,3,1,4,5,1],
     [1,3,1,3,10,2],
     [1,3,1,1,6,6],
     [1,1,2,1,1,2],
     [7,2,1,2,5]]

    T=[[7,2,1,1,7],
     [1,1,2,2,1,1],
     [1,3,1,3,1,3,1,3,1],
     [1,3,1,1,5,1,3,1],
     [1,3,1,1,4,1,3,1],
     [1,1,1,2,1,1],
     [7,1,1,1,1,1,7],
     [1,1,3],
     [2,1,2,1,8,2,1],
     [2,2,1,2,1,1,1,2],
     [1,7,3,2,1],
     [1,2,3,1,1,1,1,1],
     [4,1,1,2,6],
     [3,3,1,1,1,3,1],
     [1,2,5,2,2],
     [2,2,1,1,1,1,1,2,1],
     [1,3,3,2,1,8,1],
     [6,2,1],
     [7,1,4,1,1,3],
     [1,1,1,1,4],
     [1,3,1,3,7,1],
     [1,3,1,1,1,2,1,1,4],
     [1,3,1,4,3,3],
     [1,1,2,2,2,6,1],
     [7,1,3,2,1,1]]

    blockrows=kuokka.Positio(K,24)
    blockcols=kuokka.Positio(T,24)

    cls._grid=kuokka.Grid(blockrows,blockcols)
    #self.UI=kuokka.Graphics(cls._grid)
    #time.sleep(1)


    cls._grid.whiteConstraints[0][8]=1
    cls._grid.blackConstraints[0][9]=1

  @classmethod
  def tearDownClass(cls):
    cls._grid=None

class testBuffy(TestGrid):
  def printLine(self,line):
    print unittest.TestCase.id(self)
    print "Whites %s " % self._grid.whiteConstraints[0].astype(int)
    print "Blacks %s " % self._grid.blackConstraints[0].astype(int)
    print "possibleRowPos %s" % self._grid.blockrows.possibleRowPos[0][1]
    print

  def test_common_blobs(self):
#    super(TestGrid, cls).setUpClass()
    print self._grid.blockrows.possibleRowPos[0][0]

    time.sleep(1)
    self.printLine(0)
    self._grid.setCommonBlobs(0,0,self._grid.blockrows.possibleRowPos[0][1],3)
    self.printLine(0)

    #self.UI.showGrid()

  def test_buffy_one_forward_transition_at_3(self):
    self._grid=self._grid
    self.printLine(0)
    self._grid.vampireSlayer(0,0)
    self.printLine(0)

  def test_whiteBridge(self):
    self._grid.whiteBridge(0,0)
    self.printLine(0)

  def test_freezeBlock(self):
    self.grid=self._grid
    self.grid.freezeBlock(0,0,1,9)
    self.printLine(0)


if __name__ == '__main__':
    unittest.main()
