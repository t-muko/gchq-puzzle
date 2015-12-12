import numpy as np
import re

#from pythonds.basic.stack import Stack

#def divideBy2(decNumber):
#  remstack = Stack()

#  while decNumber > 0:
#    rem = decNumber % 2
#    remstack.push(rem)
#    decNumber = decNumber // 2
#  binString = ""
#  while not remstack.isEmpty():
#    binString = binString + str(remstack.pop())

#  return binString

#print(divideBy2(42))

#def pystybinToDec(grid,position):
#print (2%2)

def decToBin(n):
    if n==0: return ''
    else:
#        return decToBin(n/2) + str(n%2)
        return str(n%2) + decToBin(n/2)
# Big endian, please
#print decToBin(24)

def binToDec(binarray):
  decimal = 0
  for digit in binarray:
    decimal = decimal*2 + int(digit)
  return decimal

#print binToDec([1,1,1,1])

#def palikkaLoop(grid,rivi,K,palikkano,positio):
#  for testpositio in range(positio.minmax(rivi,palikkano))
#    positio[rivi,palikkano]=testpositio



class Positio:
  # A class to store start positions for each block in the grid shade puzzle.
  # Start position has to be larger than the lenght of previous blocks and spaces
  # When creating an object, the positions are initialised to their minimum values
  # Inputs, Block lenght definition array K, lenght of the row rowlenght
#    for row in range(1,(len(self.K)+1)):
  # K array ja positioarray ovat ykkosindeksoituja
  # Rivit nollaindeksoituja
  # Positiot nollaindeksoituja
  def __init__(self,Kin,rowlenght):
    self.rowlenght=rowlenght
    self.K=Kin
    self.kerroin=[]
    # Alustetaan palikkakertoimet K:n mukaan
    for row in range(0,(len(self.K))):
      kerroinrivi=[0]
      for palikka in range(1,(len(self.K[row]))):
        kerroinrivi.append(self.minpositio(row,palikka))
      self.kerroin.append(kerroinrivi)

  def minpositio(self,row,palikkano):
    minpos=0
    #print "minimipositio riville %s, palikalle %s" % (row,palikkano)
    for i in range(1,palikkano):
      minpos=minpos+self.K[row][i]
    minpos=minpos+palikkano-1
    return minpos

  def maxpositio(self,row,palikkano):
    maxpos=0
    for i in range(palikkano,len(self.K)-1):
      maxpos=maxpos+self.K[rivi][i]
    maxpos=maxpos+len(self.K[rivi])-i-1
    return maxpos

  def rowvalues(self):
    values=[]

    for rowidx,row in enumerate(self.kerroin):
      rowsum=0
      for idx,kerroin in enumerate(row):
        rowsum=rowsum+(pow(2,self.K[rowidx][idx])-1)*pow(2,self.kerroin[rowidx][idx])
      values.append(rowsum)
    return values

class Grid:
  def __init__(self,rowvalues,T):
    #print rowvalues
    #rowlength=len(T)
    self.T=T
    self.grid=np.zeros((len(rowvalues),len(T)),dtype="bool_")
    for rowidx,row in enumerate(rowvalues):
      self.decToRow(row,rowidx)

  def decToRow(self,n,rowno,colno=0):
    #print "converting row %s, %s:%s bit %s" % (n,rowno,colno,str(n%2))
    if n==0: return ''
    else:
        self.grid[rowno,colno]=n%2
        self.decToRow(n/2,rowno,colno+1)
        return

  def printgrid(self):
    print self.grid.astype(int)

  def testColumn(self,col):
    # transpose the grid, convert bit row to a string and do regexp match on it
    testcolumn=re.sub("[^0-1]","", str(self.grid.transpose().astype(int)[col]))
    #    #re.match("0*1{2}0+1{3}", "000110111000")
    regstring="0*"
    n=len(self.T[col])
    for idx,blocklen in enumerate(self.T[col]):
      regstring=regstring+('1{%s}' % str(blocklen))
      if idx<n-1:
        regstring=regstring+('0+')
    print testcolumn
    print regstring
    print re.match(regstring,testcolumn)

