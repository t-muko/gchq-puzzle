import numpy as np
import re

def decToBin(n):
    if n==0: return ''
    else:
#        return decToBin(n/2) + str(n%2)
        return str(n%2) + decToBin(n/2)
# Big endian, please

def binToDec(binarray):
  decimal = 0
  for digit in binarray:
    decimal = decimal*2 + int(digit)
  return decimal


class Positio:
  # A class to store start positions for each block in the grid shade puzzle.
  # Start position has to be larger than the lenght of previous blocks and spaces
  # When creating an object, the positions are initialised to their minimum values
  # Inputs, Block lenght definition array K, lenght of the row rowlenght
  # Everything is zero indexed

  def __init__(self,Kin,rowlenght):
    self.rowlenght=rowlenght
    self.K=Kin
    self.kerroin=[]
    self.possibleRowPos=[]
    self.possibleColPos=[]

    # Alustetaan palikkakertoimet K:n mukaan
    for row in range(0,(len(self.K))):
      kerroinrivi=[]
      posrow=[]
      for palikka in range(0,(len(self.K[row]))):
        kerroinrivi.append(self.minpositio(row,palikka))
        palikkapos=[]
        print "row %s min %s, max %s" % (row,self.minpositio(row,palikka),self.maxpositio(row,palikka))
        for ispossible in range(self.minpositio(row,palikka),self.maxpositio(row,palikka)+1):
          palikkapos.append(ispossible)
        posrow.append(palikkapos)
      self.kerroin.append(kerroinrivi)
      self.possibleRowPos.append(posrow)
#    print "kertoimet"
#    print self.kerroin
#    print "possilbes"
#    print self.possibleRowPos

  def minpositio(self,row,palikkano):
#    print "minimipositio riville %s, palikalle %s" % (row,palikkano),
    if (palikkano>0):
      minpos=0
      # Palikoiden yhteispituus plus yksi
      # Nollapalikan minimi on aina nolla
      for i in range(0,palikkano):
        minpos=minpos+self.K[row][i]+1
    else:
      # first block. Always zero
#      print 0
      return 0
#    print minpos
    return minpos

  def maxpositio(self,row,palikkano):
    # Maksimipalikkapositio on rivin pituus miinus palikoiden yhteismitta mukaanlukien palikka itse
    # plus palikoiden maara miinus yksi, paitsi jos on viimeinen palikka, niin silloin voi menna loppuun asti
    # Lasketaan siis kaikkien muiden paitsi viimeisen palikan mitat plus yksi yhteen ja sitten viela viimeinen
    # palikka.
    maxpos=self.rowlenght
    # Viimeisen palikan mitta otetaan pois aina, mutta koska alkupaikka on ekan ruuudun alla, lisataan yksi
    maxpos=maxpos-self.K[row][len(self.K[row])-1]+1
    for i in range(palikkano,len(self.K[row])-1):
      maxpos=maxpos-self.K[row][i]-1
    return maxpos

  def resetRowToMin(self,row):
    for palikka in range(0,(len(self.K[row]))):
      self.kerroin[row][palikka]=self.minpositio(row,palikka)


  def rowvalues(self):
    values=[]

    for rowidx,row in enumerate(self.kerroin):
      rowsum=0
      for idx,kerroin in enumerate(row):
        rowsum=rowsum+(pow(2,self.K[rowidx][idx-1])-1)*pow(2,self.kerroin[rowidx][idx-1])
      values.append(rowsum)
    return values

class Grid:
  def __init__(self,blockrows,T):
    #print rowvalues
    #rowlength=len(T)
    self.T=T
    self.blockrows=blockrows
    self.grid=np.zeros((len(blockrows.rowvalues()),len(T)),dtype="bool_")
    self.blackConstraints=np.zeros((len(blockrows.rowvalues()),len(T)),dtype="bool_")
    self.whiteConstraints=np.zeros((len(blockrows.rowvalues()),len(T)),dtype="bool_")

    # Given constraints:
    self.blackConstraints[3]=[0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0]
    self.blackConstraints[8]=[0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0]
    self.blackConstraints[16]=[0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0]
    self.blackConstraints[21]=[0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0]
    for rowidx,row in enumerate(blockrows.rowvalues()):
      self.decToRow(row,rowidx)
    self.binWghArray=np.zeros(len(T))
    self.binWghArray=pow(2,np.arange(1,len(T),1))
    print self.blackConstraints.astype(int)

  def decToRow(self,n,rowno,colno=0):
    #print "converting row %s, value %s, col %s bit %s" % (rowno,n,colno,str(n%2))
    # make an array with numbers 0-24 and raise two to that power
    binWghArray=pow(2,np.arange(0,25,1))

#    if n==0: return ''
#    else:
#        self.grid[rowno,colno]=n%2
#        self.decToRow(n/2,rowno,colno+1)
    # divide the number to be converted with binary weighed array. Take modulo 2 of that to create a binary array
    self.grid[rowno]=(n/binWghArray)%2
    return

  def updateRow(self,row):
    #print "Updating row %s, value %s" % (row,self.blockrows.rowvalues()[row])
    #print self.blockrows.kerroin[row]
    self.decToRow(self.blockrows.rowvalues()[row],row)

  def printgrid(self):
    print self.grid.astype(int)

  def testColumn(self,col):
    # transpose the grid, convert bit row to a string and do regexp match on it
    testcolumn=re.sub("[^0-1]","", str(self.grid.transpose().astype(int)[col]))
    #    #re.match("0*1{2}0+1{3}", "000110111000")
    regstring="0*"
    n=len(self.T[col])
    for idx,blocklen in enumerate(self.T[col]):
      if idx>0:
        regstring=regstring+('1{%s}' % str(blocklen))
        if idx<n-1:
          regstring=regstring+('0+')
#    print testcolumn
#    print regstring
    return bool(re.match(regstring,testcolumn))

