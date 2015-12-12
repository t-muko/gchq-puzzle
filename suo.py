import kuokka
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



riveja=len(K)
sarakkeita=len(T)

print "riveja %s, sarakkeita %s" % (riveja,sarakkeita)
print "K"
print K

blockrows=kuokka.Positio(K,sarakkeita)
#print 'alustetut minimikertoimet'
#print grid.kerroin
#print grid.rowvalues()
#for value in grid.rowvalues():
#  print kuokka.decToBin(value)

gridvalues=kuokka.Grid(blockrows,T)
gridvalues.printgrid()

#for test in range(sarakkeita):
#  gridvalues.testColumn(test)


def iterate(row,blockno,gridvalues):
  # Kukin blokki voi liikkua edellisen blockin perasta seuraavaan blockin alkuun miinus pituus miinus yksi
  # asti tai rivin loppuun miinus pituus
  if blockno == 0:
    print "Zeroblock"
    currminpos=0
  else:
    currminpos=gridvalues.blockrows.kerroin[row][blockno-1]+1+gridvalues.blockrows.K[row][blockno-1]
  if blockno < len(gridvalues.blockrows.K[row])-1:
    currmaxpos=gridvalues.blockrows.kerroin[row][blockno+1]-1-gridvalues.blockrows.K[row][blockno]
  else:
    currmaxpos=sarakkeita-gridvalues.blockrows.K[row][blockno]

  print 'min %s, max %s' % (currminpos,currmaxpos)

  #range is upper limit exclusive
  for currpos in range(currminpos,currmaxpos+1):
    gridvalues.blockrows.kerroin[row][blockno]=currpos
    gridvalues.updateRow(row)
    gridvalues.printgrid()
  if blockno > 0:
    iterate(row,blockno-1,gridvalues)

iterate(24,5,gridvalues)
