import kuokka
import array
from timeit import default_timer as timer
import numpy as np
import time

#from kuokka import positio
#import numpy as np
#rivit = np.array([
#  [7,3,1,1,7],
#  [1,1,2,2,1,1]
#    ])


#grid_dec=np.array([[2], [7], [23]], dtype=np.uint16)
#np.unpackbits(grid_dec, axis=1)
#np.packbits(rivit, axis=1)
#K=[[0,1,3,2,4],[0,1,1],[0,1,1,1,3,2]]

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
   [1,1,1,3,1,1],
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

starttime=timer()
itercount=1
riveja=len(K)-1
sarakkeita=len(T)-1



#print "riveja %s, sarakkeita %s" % (riveja,sarakkeita)
#print "K"
#print K

blockrows=kuokka.Positio(K,sarakkeita)
blockcols=kuokka.Positio(T,riveja)
#print "suo %s " % blockcols.maxidx
#print 'alustetut minimikertoimet'
#print blockrows.kerroin

#print blockrows.rowvalues()
#for value in grid.rowvalues():
#  print kuokka.decToBin(value)

grid=kuokka.Grid(blockrows,blockcols)
#print grid.checkIfBlockFits(0,21,0,5)
#print grid.checkIfBlockFits(0,21,0,4)
#grid.freezeBlock(0,3,2,3)
#grid.setCommonBlobs(0,0,[0,1,2],7)
UI=kuokka.Graphics(grid)
time.sleep(2)
#grid.printgrid()
#print blockrows.possibleRowPos[0][0]

def rowinduction():
  for lineidx, line in enumerate(blockrows.possibleRowPos):
    for blockidx,block in enumerate(line):
      grid.setCommonBlobs(0,lineidx,block,blockrows.K[lineidx][blockidx])
      #UI.showGrid()
      stillpossible=array.array('i')
      for posidx,position in enumerate(block):

        # if position is still possible, add it to the new possible position array
        if (grid.checkIfBlockFits(0,lineidx,position,blockrows.K[lineidx][blockidx])):
          stillpossible.append(position)

#        print "before"
#        print blockrows.possibleRowPos[lineidx][blockidx]
        # save the new possible rows array
        blockrows.possibleRowPos[lineidx][blockidx]=stillpossible
#        print "after"
#        print blockrows.possibleRowPos[lineidx][blockidx]

      # if we have got only one possible position left, the block can be freezed
      if len(stillpossible)==1:
        lastpos=blockrows.possibleRowPos[lineidx][blockidx]
        #print "last position: %s" % lastpos
        #print "Row %s, position %s, lenght %s is frozen" % (lineidx,lastpos[0],blockrows.K[lineidx][blockidx])
        grid.freezeBlock(0,lineidx,lastpos[0],blockrows.K[lineidx][blockidx])

def colinduction():
  for lineidx, line in enumerate(blockcols.possibleRowPos):
    for blockidx,block in enumerate(line):
      grid.setCommonBlobs(1,lineidx,block,blockcols.K[lineidx][blockidx])

      stillpossible=array.array('i')
      for posidx,position in enumerate(block):

        # if position is still possible, add it to the new possible position array
        if (grid.checkIfBlockFits(1,lineidx,position,blockcols.K[lineidx][blockidx])):
          stillpossible.append(position)

        # save the new possible rows array
        blockcols.possibleRowPos[lineidx][blockidx]=stillpossible
        #UI.showGrid()

      # if we have got only one possible position left, the block can be freezed
      if len(stillpossible)==1:
        lastpos=blockcols.possibleRowPos[lineidx][blockidx]
        #print "last position: %s" % lastpos
        #print "Col %s, position %s, lenght %s is frozen" % (lineidx,lastpos[0],blockcols.K[lineidx][blockidx])
        grid.freezeBlock(1,lineidx,lastpos[0],blockcols.K[lineidx][blockidx])

UI.showGrid()
#time.sleep(1)
#grid.freezeBlock(0,6,7,blockrows.K[6][0])

for i in range(0,30):
  print "ROUND %s" % i
  rowinduction()
#  UI.showGrid()
  colinduction()
  UI.showGrid()
  for line in range(0,25):
    grid.walkFromBoundary(0,line)
  UI.showGrid()
  for line in range(0,25):
    grid.walkFromBoundary(1,line)
  UI.showGrid()
  #grid.printgrid()
#  blockrows.printFreedoms('row','no')
#  blockcols.printFreedoms('Col','no')
#print blockcols.possibleRowPos


def testAll(gridvalues,sarakkeita=26):
  overallResult=True
  global itercount
  itercount=itercount+1

  if (np.array_equal(np.dot(gridvalues.grid,np.ones(sarakkeita-1)),K)):
    for test in range(sarakkeita):
      overallResult=gridvalues.testColumn(test)
      if overallResult==False:
        #print "Test fail at col %s" % test
        break
    if overallResult==True:
      print "Yeee!"
      gridvalues.printgrid()

def iterate(row,blockno,gridvalues):
  # Kukin blokki voi liikkua edellisen blockin perasta seuraavaan blockin alkuun miinus pituus miinus yksi
  # asti tai rivin loppuun miinus pituus
  # kunkin blockin liikutuksen jalkeen iteroidaan kaikki aiemmat rivit ennen kuin siirretaan taas blockia.
  # Jos blockia siirretaan, niin aiemmat rivit resetoidaan
  # Block numero on ykkosindeksoitu


  #for resetrow in range(row):
    #print "reset row %s" % row

  # etsitaan palikan liikkumavara

  if blockno == 0:
    # eka blokki. Voi olla alussa.
    #print "Zeroblock"
    currminpos=0
  else:
    currminpos=gridvalues.blockrows.kerroin[row][blockno-1]+gridvalues.blockrows.K[row][blockno-1]+1
    #print currminpos
  # maksimipositio:
  if blockno < len(gridvalues.blockrows.K[row])-1:
    #print row,blockno
    currmaxpos=gridvalues.blockrows.kerroin[row][blockno+1]-1-gridvalues.blockrows.K[row][blockno]+1
  else:
    # Viimeinen blokki
    #print row,blockno
    currmaxpos=sarakkeita-gridvalues.blockrows.K[row][blockno]+1

  #print 'row %s block %s current min %s, max %s' % (row,blockno,currminpos,currmaxpos)
  #print gridvalues.blockrows.K[row]


  #range is upper limit exclusive
  for currpos in range(currminpos,currmaxpos):
    gridvalues.blockrows.kerroin[row][blockno]=currpos
    gridvalues.updateRow(row)
    #print "row %s, itercount %s" % (row,itercount)
    #print "%s iterations per second" % (itercount/(timer()-starttime))
    #gridvalues.printgrid()
    # Limit printing
    if row >99:
      print "row %s, itercount %s" % (row,itercount)
      print "%s iterations per second" % (itercount/(timer()-starttime))
      #print gridvalues.blockrows.kerroin
      #gridvalues.printgrid()

      #print gridvalues.blockrows.kerroin

    testAll(gridvalues)

    # If not the first row, iterate previous row after every move
    if row > 0:
      # Kunkin siirron jalkeen resetoidaan edellinen rivi ja iteroidaan myos se
      gridvalues.blockrows.resetRowToMin(row-1)
      iterate(row-1,len(gridvalues.blockrows.K[row-1])-1,gridvalues)

  # Jos edella on viela blokkeja, iteroidaan nekin
    if blockno > 0:
      iterate(row,blockno-1,gridvalues)

#iterate(24,len(gridvalues.blockrows.K[24])-1,gridvalues)

#rowiters=[]

#for row in range(0,25):
#  itercount=1
#  starttime=timer()
#  iterate(row,len(gridvalues.blockrows.K[row])-1,gridvalues)
#  print "row %s, itercount %s, " % (row,itercount-len(gridvalues.blockrows.K[row])),
#  print "%s iterations per second" % (itercount/(timer()-starttime))
#  rowiters.append(itercount-len(gridvalues.blockrows.K[row]))
#gridvalues.printgrid()

#totiters=1

#for n in range(0,25):
#  totiters=totiters*rowiters[n]

#print "Total iterations: %s " % totiters

#UI.showGrid()
#UI.test2()
