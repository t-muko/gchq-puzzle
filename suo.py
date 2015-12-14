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

K=[[0,7,3,1,1,7],
   [0,1,1,2,2,1,1],
   [0,1,3,1,3,1,1,3,1],
   [0,1,3,1,1,6,1,3,1],
   [0,1,3,1,5,2,1,3,1],
   [0,1,1,2,1,1],
   [0,7,1,1,1,1,1,7],
   [0,3,3],
   [0,1,2,3,1,1,3,1,1,2],
   [0,1,1,3,2,1,1],
   [0,4,1,4,2,1,2],
   [0,1,1,1,1,1,4,1,3],
   [0,2,1,1,1,2,5],
   [0,3,2,2,6,3,1],
   [0,1,9,1,1,2,1],
   [0,2,1,2,2,3,1],
   [0,3,1,1,1,1,5,1],
   [0,1,2,2,5],
   [0,7,1,2,1,1,1,3],
   [0,1,1,2,1,2,2,1],
   [0,1,3,1,4,5,1],
   [0,1,3,1,3,10,2],
   [0,1,3,1,1,6,6],
   [0,1,1,2,1,1,2],
   [0,7,2,1,2,5]]

T=[[0,7,2,1,1,7],
   [0,1,1,2,2,1,1],
   [0,1,3,1,3,1,3,1,3,1],
   [0,1,3,1,1,5,1,3,1],
   [0,1,3,1,1,4,1,3,1],
   [0,1,1,1,3,1,1],
   [0,7,1,1,1,1,1,7],
   [0,1,1,3],
   [0,2,1,2,1,8,2,1],
   [0,2,2,1,2,1,1,1,2],
   [0,1,7,3,2,1],
   [0,1,2,3,1,1,1,1,1],
   [0,4,1,1,2,6],
   [0,3,3,1,1,1,3,1],
   [0,1,2,5,2,2],
   [0,2,2,1,1,1,1,1,2,1],
   [0,1,3,3,2,1,8,1],
   [0,6,2,1],
   [0,7,1,4,1,1,3],
   [0,1,1,1,1,4],
   [0,1,3,1,3,7,1],
   [0,1,3,1,1,1,2,1,1,4],
   [0,1,3,1,4,3,3],
   [0,1,1,2,2,2,6,1],
#   [0,1,1]]
   [0,7,1,3,2,1,1]]

starttime=timer()
itercount=0
riveja=len(K)
sarakkeita=len(T)

print "riveja %s, sarakkeita %s" % (riveja,sarakkeita)
#print "K"
#print K

blockrows=kuokka.Positio(K,sarakkeita)
#print 'alustetut minimikertoimet'
#print grid.kerroin
#print grid.rowvalues()
#for value in grid.rowvalues():
#  print kuokka.decToBin(value)

gridvalues=kuokka.Grid(blockrows,T)
#gridvalues.printgrid()


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

  if blockno == 1:
    # eka blokki. Voi olla alussa.
    #print "Zeroblock"
    currminpos=0
  else:
    currminpos=gridvalues.blockrows.kerroin[row][blockno-1]+1+gridvalues.blockrows.K[row][blockno-1]

  # maksimipositio:
  if blockno < len(gridvalues.blockrows.K[row])-1:
    currmaxpos=gridvalues.blockrows.kerroin[row][blockno+1]-1-gridvalues.blockrows.K[row][blockno]
  else:
    # Viimeinen blokki
    currmaxpos=sarakkeita-gridvalues.blockrows.K[row][blockno]+1

  #print 'row %s block %s current min %s, max %s' % (row,blockno,currminpos,currmaxpos)
  #print gridvalues.blockrows.K[row]


  #range is upper limit exclusive
  for currpos in range(currminpos,currmaxpos+1):
    gridvalues.blockrows.kerroin[row][blockno]=currpos
    gridvalues.updateRow(row)
    #print "row %s, itercount %s" % (row,itercount)
    #print "%s iterations per second" % (itercount/(timer()-starttime))
    #gridvalues.printgrid()
    # Limit printing
    if row >-1:
      print "row %s, itercount %s" % (row,itercount)
      print "%s iterations per second" % (itercount/(timer()-starttime))
      gridvalues.printgrid()

      #print gridvalues.blockrows.kerroin

    testAll(gridvalues)

    # If not the first row, iterate previous row after every move
    if row > 0:
      # Kunkin siirron jalkeen resetoidaan edellinen rivi ja iteroidaan myos se
      gridvalues.blockrows.resetRowToMin(row-1)
      iterate(row-1,len(gridvalues.blockrows.K[row-1])-1,gridvalues)

  # Jos edella on viela blokkeja, iteroidaan nekin
    if blockno > 1:
      iterate(row,blockno-1,gridvalues)



iterate(2,len(gridvalues.blockrows.K[1])-1,gridvalues)
#gridvalues.printgrid()
