import numpy as np
import re
import array

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
    self.maxidx=(len(Kin)-1)

    self.possibleRowPos=[]
    self.possibleColPos=[]
    #print Kin

    # Alustetaan palikkakertoimet K:n mukaan
    for row in range(0,(len(self.K))):
      kerroinrivi=array.array('i')
      for palikka in range(0,(len(self.K[row]))):
        kerroinrivi.append(self.minpositio(row,palikka))
      self.kerroin.append(kerroinrivi)

    # Alustetaan mahdolliset positiot jokaiselle palikalle
    for line in range(0,(len(self.K))):
      posrow=[]
      for palikka in range(0,(len(self.K[line]))):
        palikkapos=array.array('i')
        print "line %s palikka %s min %s, max %s" % (line, palikka,self.minpositio(line,palikka),self.maxpositio(line,palikka))
        for ispossible in range(self.minpositio(line,palikka),self.maxpositio(line,palikka)+1):
          print ispossible
          palikkapos.append(ispossible)
        #print palikkapos
        posrow.append(palikkapos)
      self.possibleRowPos.append(posrow)
      print self.possibleRowPos
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
  def __init__(self,blockrows,blockcols):
    #print rowvalues
    #rowlength=len(T)
    self.blockrows=blockrows
    self.blockcols=blockcols
    #print "gridissa"
    self.maxrowid = self.blockrows.maxidx
    self.maxcolid = self.blockcols.maxidx

    self.grid=np.zeros((self.maxrowid+1,self.maxcolid+1),dtype="bool_")
    self.blackConstraints=np.zeros((self.blockrows.maxidx+1,self.blockcols.maxidx+1),dtype="bool_")
    self.whiteConstraints=np.zeros((self.blockrows.maxidx+1,self.blockcols.maxidx+1),dtype="bool_")

    # Given constraints:
    self.blackConstraints[3]=[0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0]
    self.blackConstraints[8]=[0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0]
    self.blackConstraints[16]=[0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0]
    self.blackConstraints[21]=[0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0]
    for rowno,rowvalue in enumerate(self.blockrows.rowvalues()):
      self.grid[rowno]=self.decToBinArray(rowvalue)
    self.binWghArray=np.zeros(self.blockcols.maxidx+1)
    self.binWghArray=pow(2,np.arange(1,self.blockcols.maxidx+1,1))
    #print self.blackConstraints.astype(int)

  def posLenToValue(self,position,lenght):
    return (pow(2,lenght)-1)*pow(2,position)


  def decToBinArray(self,n):
    #print "converting row %s, value %s, col %s bit %s" % (rowno,n,colno,str(n%2))
    # make an array with numbers 0-24 and raise two to that power
    binWghArray=pow(2,np.arange(0,25,1))

#    if n==0: return ''
#    else:
#        self.grid[rowno,colno]=n%2
#        self.decToRow(n/2,rowno,colno+1)
    # divide the number to be converted with binary weighed array. Take modulo 2 of that to create a binary array
    #self.grid[rowno]=(n/binWghArray)%2
    return (n/binWghArray)%2

  def posLenToBinArray(self,position,lenght):
    return self.decToBinArray((pow(2,lenght)-1)*pow(2,position))

  def updateRow(self,row):
    #print "Updating row %s, value %s" % (row,self.blockrows.rowvalues()[row])
    #print self.blockrows.kerroin[row]
    self.grid[row]=self.decToBinArray(self.blockrows.rowvalues()[row])


  def checkIfBlockFits(self,direction,line,position,length):
    # if playing with columns, transpose the constraint matrices
    if direction:
      whiteConstraints=np.transpose(self.whiteConstraints)
      blackConstraints=np.transpose(self.blackConstraints)
    else:
      whiteConstraints=self.whiteConstraints
      blackConstraints=self.blackConstraints
    # 1. Check that there are no white blobs under the block
    if np.any(np.logical_and(self.posLenToBinArray(position,length), whiteConstraints[line])):
      return False
    # 2. Check that there are no black blobs at the ends
    if position>0:
      if np.any(np.logical_and(self.posLenToBinArray(position-1,1), blackConstraints[line])):
        return False
    if position<np.shape(whiteConstraints)[0]:
      if np.any(np.logical_and(self.posLenToBinArray(position+length,1), blackConstraints[line])):
        return False
    # All tests passed, so it must be True!
    return True

  def setCommonBlobs(self,direction,line,possiblePos,length):
    commonBlobs=np.ones(np.shape(self.whiteConstraints)[0])

    for pos in possiblePos:
      commonBlobs=np.logical_and(self.posLenToBinArray(pos,length),commonBlobs)

    if direction:
      tempGrid=np.transpose(elf.blackConstraints)
      tempGrid[line]=np.logical_or(tempGrid[line],commonBlobs)
      self.blackConstraints=np.transpose(tempGrid)

    else:
      self.blackConstraints[line]=np.logical_or(self.blackConstraints[line],commonBlobs)


  def freezeBlock(self,direction,line,position,length):
    # set black blobs and Extend the block to both directions unless we are just in the edge and enter white constraints
    self.setCommonBlobs(direction,line,[position],length)
    if direction:
      # Working on columns
      if position>0:
        #We are above lower boundary, so can extend down
        self.whiteConstraints[position-1][line]=1

      if position<self.maxrowid-length+1:
        # If below high edge, extend up
        self.whiteConstraints[position+length][line]=1

    else:
      # Working on rows
      if position>0:
        #We are above lower boundary, so can extend down
        self.whiteConstraints[line][position-1]=1

      if position<self.maxrowid-length+1:
        # If below high edge, extend up
        self.whiteConstraints[line][position+length]=1


  def printgrid(self):
    print "Test grid:"
    print self.grid.astype(int)
    print "White contraints:"
    print self.whiteConstraints.astype(int)
    print "Black contraints:"
    print self.blackConstraints.astype(int)

  def testColumn(self,col):
    # transpose the grid, convert bit row to a string and do regexp match on it
    testcolumn=re.sub("[^0-1]","", str(self.grid.transpose().astype(int)[col]))
    #    #re.match("0*1{2}0+1{3}", "000110111000")
    regstring="0*"
    n=len(self.blockcol.K[col])
    for idx,blocklen in enumerate(self.blockcol.K[col]):
      if idx>0:
        regstring=regstring+('1{%s}' % str(blocklen))
        if idx<n-1:
          regstring=regstring+('0+')
#    print testcolumn
#    print regstring
    return bool(re.match(regstring,testcolumn))

