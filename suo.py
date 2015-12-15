import kuokka
from timeit import default_timer as timer
import numpy as np

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
#   [0,1,1]]
   [7,1,3,2,1,1]]

starttime=timer()
itercount=1
riveja=len(K)
sarakkeita=len(T)

print "riveja %s, sarakkeita %s" % (riveja,sarakkeita)
#print "K"
#print K

blockrows=kuokka.Positio(K,sarakkeita)
#print 'alustetut minimikertoimet'
#print blockrows.kerroin

#print blockrows.rowvalues()
#for value in grid.rowvalues():
#  print kuokka.decToBin(value)

gridvalues=kuokka.Grid(blockrows,T)
gridvalues.printgrid()


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

iterate(24,len(gridvalues.blockrows.K[24])-1,gridvalues)

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
