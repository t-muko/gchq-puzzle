import numpy as np
import re
import array
import threading

import Tkinter as tk

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
        #print "line %s palikka %s min %s, max %s" % (line, palikka,self.minpositio(line,palikka),self.maxpositio(line,palikka))
        for ispossible in range(self.minpositio(line,palikka),self.maxpositio(line,palikka)+1):
          #print ispossible
          palikkapos.append(ispossible)
        #print palikkapos
        posrow.append(palikkapos)
      self.possibleRowPos.append(posrow)
      #print self.possibleRowPos
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

  def checkBlockChain(self):
    # Make sure that min position of a block does not overlap with min position of the previous block.

    for line in range(0,len(self.possibleRowPos)):
      for blockidx in range(1,len(self.possibleRowPos[line])):
        #print "before up run %s" % self.possibleRowPos[line][blockidx],
        self.possibleRowPos[line][blockidx]=[i for i in self.possibleRowPos[line][blockidx] if
                                               i > min(self.possibleRowPos[line][blockidx-1])+self.K[line][blockidx-1]]

        #print "after up run %s" % self.possibleRowPos[line][blockidx]

    for line in range(0,len(self.possibleRowPos)):
      #print "line %s" % line,
      for blockidx in range((len(self.possibleRowPos[line])-2),0-1,-1):
        #print "before down run %s" % self.possibleRowPos[line][blockidx]
        self.possibleRowPos[line][blockidx]=[i for i in self.possibleRowPos[line][blockidx] if
                                               i < max(self.possibleRowPos[line][blockidx+1])-self.K[line][blockidx]]
        #print "after down run %s" % self.possibleRowPos[line][blockidx]






  def rowvalues(self):
    values=[]

    for rowidx,row in enumerate(self.kerroin):
      rowsum=0
      for idx,kerroin in enumerate(row):
        rowsum=rowsum+(pow(2,self.K[rowidx][idx-1])-1)*pow(2,self.kerroin[rowidx][idx-1])
      values.append(rowsum)
    return values

  def printFreedoms(self,direction,verbose='detail'):
    permutations=1
    for lineidx,line in enumerate(self.possibleRowPos):
      for blockidx,block in enumerate(line):
        permutations=permutations*len(block)
        if (len(block)>1 & (verbose=='detail')):
          print "Line (%s) %s, block %s has got %s possible locations %s" % (direction,lineidx,blockidx,len(block), self.possibleRowPos[lineidx][blockidx])
    print "Total %s permutations." % permutations

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
      #print "dir %s: line %s, pos %s, len %s. White constraint found under the block." % (direction,line,position,length)
      #print 'white constraints and test line'
      #print whiteConstraints[line].astype(int)
      #print self.posLenToBinArray(position,length)
      return False
    # 2. Check that there are no black blobs at the ends
    if position>0:
      if np.any(np.logical_and(self.posLenToBinArray(position-1,1), blackConstraints[line])):
        #print "dir %s: line %s, pos %s, len %s. Pos>0. Black blob before block." % (direction,line,position,length)
        #print 'black constraints and test line'
        #print blackConstraints[line].astype(int)
        #print self.posLenToBinArray(position,length)
        return False
    if position<np.shape(whiteConstraints)[0]:
      if np.any(np.logical_and(self.posLenToBinArray(position+length,1), blackConstraints[line])):
        #print "dir %s: line %s, pos %s, len %s. pos less than max. Blob after block." % (direction,line,position,length)
        #print 'black constraints and test line'
        #print blackConstraints[line].astype(int)
        #print self.posLenToBinArray(position,length)
        return False
    # All tests passed, so it must be True!
    #print "dir %s: line %s, pos %s, len %s. No constraints found." % (direction,line,position,length)
    return True

  def setCommonBlobs(self,direction,line,possiblePos,length):
    commonBlobs=np.ones(np.shape(self.whiteConstraints)[0])

    for pos in possiblePos:
      commonBlobs=np.logical_and(self.posLenToBinArray(pos,length),commonBlobs)

    if (direction>0):
      tempGrid=np.transpose(self.blackConstraints)
      tempGrid[line]=np.logical_or(tempGrid[line],commonBlobs)
      self.blackConstraints=np.transpose(tempGrid)

    else:
      self.blackConstraints[line]=np.logical_or(self.blackConstraints[line],commonBlobs)

  def whiteBridge(self,direction,line):
    if (direction>0):
      # Working on columns
      possiblepos=self.blockcols.possibleRowPos[line]
      K=self.blockcols.K[line]
    else:
      # working on rows
      possiblepos=self.blockrows.possibleRowPos[line]
      K=self.blockrows.K[line]

    for blockidx in range(0,len(possiblepos)-1):
      # set white constraints on every square in between end of previous block on its maximum position and
      # next block on its minimum position
      for whiteBlob in range(max(possiblepos[blockidx])+K[blockidx],
                             min(possiblepos[blockidx+1])):
        if (direction>0):
          self.whiteConstraints[whiteBlob][line]=1
        else:
          self.whiteConstraints[line][whiteBlob]=1

  def freezeBlock(self,direction,line,blockno,position):

    #Extend the block with white constraints to both directions unless we are just in the edge
    if (direction>0):
      # Working on columns
      length=self.blockcols.K[line][blockno]
      # Only one position left
      self.blockcols.possibleRowPos[line][blockno]=[position]
      #print "Freezing columns..."
      if position>0:
        #We are above lower boundary, so can extend down
        self.whiteConstraints[position-1][line]=1

      if position<self.maxrowid-length+1:
        # If below high edge, extend up
        self.whiteConstraints[position+length][line]=1

    else:
      # Working on rows
      length=self.blockrows.K[line][blockno]
      # Only one position left
      self.blockrows.possibleRowPos[line][blockno]=[position]
      #print "Freezing rows..."
      if position>0:
        #We are above lower boundary, so can extend down
        self.whiteConstraints[line][position-1]=1

      if position<self.maxrowid-length+1:
        # If below high edge, extend up
        self.whiteConstraints[line][position+length]=1

    # set black blobs for the block
    self.setCommonBlobs(direction,line,[position],length)

  def vampireSlayer(self,direction,line,reverse=0):
    # Find a white-black transition, which must mark a start of a block. Try to identify this block
    # based on possible starting points. If it is possible for only one block, this must be our vampire.
    # Eliminate it
    if (direction>0):
      # working on columns
      whiteConstraints=np.transpose(self.whiteConstraints)
      blackConstraints=np.transpose(self.blackConstraints)
      blocklines=self.blockcols
      if (reverse>0):
        whiteConstraints=np.fliplr(np.transpose(self.whiteConstraints))
        blackConstraints=np.fliplr(np.transpose(self.blackConstraints))
    else:
      # working on rows
      whiteConstraints=self.whiteConstraints
      blackConstraints=self.blackConstraints
      blocklines=self.blockrows
      if (reverse>0):
        whiteConstraints=np.fliplr(self.whiteConstraints)
        blackConstraints=np.fliplr(self.blackConstraints)

    # start from the edge of the grid i.e. "white"
    previousBlobIsWhite=1

    # Buffy checks all blobs
    for buffy in range(0,len(whiteConstraints[0])):
      if previousBlobIsWhite & blackConstraints[line][buffy]:
        # Transition point. This may be a vampire! Try to identify him
        # check how many blocks have got this as starting point. If only one, this must be it!

        blocksWithVampire=[]

        if (reverse>0):
          # Buffy is walking backwards. We are at the end point of possible block.

          realEndPoint=len(whiteConstraints[0])-1-buffy
          print "reversebuffy %s, realEndPoint %s" % (buffy, realEndPoint)
          print blackConstraints[line].astype(int)
          print whiteConstraints[line].astype(int)
          for blockno,startPointArray in enumerate(blocklines.possibleRowPos[line]):
            if (realEndPoint-blocklines.K[line][blockno]+1) in startPointArray:
              # Buffy found a vampire on this block
              blocksWithVampire.append(blockno)

        else:
          # normal direction
          realStartingPoint=buffy
          # Check how many blocks have been seen staring from here. Store those block numbers in an array
          for blockno,startPointArray in enumerate(blocklines.possibleRowPos[line]):
            if realStartingPoint in startPointArray:
              # Buffy found a vampire on this block
              blocksWithVampire.append(blockno)

        if (len(blocksWithVampire)==1):
          # Only one vampire found. Slay him, unless he is already dead
          if (len(blocklines.possibleRowPos[line][blocksWithVampire[0]])>1):
            if (reverse>0):
              realStartingPoint=realEndPoint-blocklines.K[line][blocksWithVampire[0]]+1

            print blocksWithVampire
            print blocklines.possibleRowPos[line][blocksWithVampire[0]]
            print "Buffy slaying a vampire in dir %s, line %s, block %s, position %s, rev %s" % (direction,line,blocksWithVampire[0],realStartingPoint,reverse)
            #print blocklines.possibleRowPos[line][blocksWithVampire[0]]
            self.freezeBlock(direction,line,blocksWithVampire[0],realStartingPoint-blocklines.K[line][blocksWithVampire[0]]+1)

      # Store the current white blob for the next round
      previousBlobIsWhite=whiteConstraints[line][buffy]

  def walkFromBoundary(self,direction,line,reverse=0):
    # We need a state machine.
    # State 0: We are against the boundary AND we know our block. White block maintains this state.
    # State 1: We have got an ongoing black blob, we know our block and we do have hard boundary behind.
    # Another black dot maintains this state. We can set the block when getting into this state.
    # State 2: We have got e white blob after state 1. This is an end of a known block.
    # State 3: We have got an empty blob. Still within lenght of a block from the last hard boundary.
    # State $:
    if (direction>0):
      whiteConstraints=np.transpose(self.whiteConstraints)
      blackConstraints=np.transpose(self.blackConstraints)
      if (reverse>0):
        whiteConstraints=np.flipud(np.transpose(self.whiteConstraints))
        blackConstraints=np.flipud(np.transpose(self.blackConstraints))
    else:
      whiteConstraints=self.whiteConstraints
      blackConstraints=self.blackConstraints
      if (reverse>0):
        whiteConstraints=np.fliplr(np.transpose(self.whiteConstraints))
        blackConstraints=np.fliplr(np.transpose(self.blackConstraints))

    hardStartPos=0
    blockno=0
    backAgainstBoundary=True
    walkingInThedark=False
    partialBlockBits=[]

    for walker in range(0,len(whiteConstraints[0])):

      if whiteConstraints[line][walker]:
        if walkingInThedark:
          if walker-hardStartPos==self.blockcols.K[line][blockno]:
            # This must be part of assumed current block located between white blobs.
            # we can freeze this!
            pass

        else:
          # we haven't walked in the dark. Just pass
          pass

        # Good. Blob is a white constraint
        backAgainstBoundary=True
        hardStartPos=walker+1
        walkingInThedark=False
        continue



      # With white constraint, we never get this far. So it is either back or blank

      if (blackConstraints[line][walker]==1) & (walkingInThedark==False):
        # this is a black blob
        # Test if we are on a ongoing block or at the start of a new one

        if backAgainstBoundary & (hardStartPos==walker):
          # This must be the first blob of the block after hard boundary. Next one can't
          backAgainstBoundary=False

          # We can freeze this block!
          if (direction>0):
            if (len(self.blockcols.possibleRowPos[line][blockno])>1):
              # This is block has not been frozen yet. Freeze now.
              print "Walker freezing COLUMN line %s, block no %s at position %s," % (line,blockno, walker)
              print "Possible positions: %s" % self.blockcols.possibleRowPos[line][blockno]
              self.freezeBlock(direction,line,blockno,walker)
            # read constraints again
            whiteConstraints=np.transpose(self.whiteConstraints)
            blackConstraints=np.transpose(self.blackConstraints)
            backAgainstBoundary=0 # We could be anywhere after freezing the block.
          else:
            if (len(self.blockrows.possibleRowPos[line][blockno])>1):
              # This is block has not been frozen yet. Freeze now.
              print "Walker freezing ROW line %s, block no %s at position %s," % (line,blockno,walker)
              print "Possible positions: %s" % self.blockrows.possibleRowPos[line][blockno]
              self.freezeBlock(direction,line,blockno,walker)
            # read constraints again
            whiteConstraints=self.whiteConstraints
            blackConstraints=self.blackConstraints
            backAgainstBoundary=0 # We could be anywhere after freezing the block.

          blockno=blockno+1

          # carry on... i.e. start again


        else:
          # existing ongoing blob... Back still against something
          continue

      else:

        # It's hopeless Mr Frodo. We are lost. We have got an empty block or even more...
        # One last change... We can try to walk in the dark until we find a black block before our current
        # block runs out. If it does, we loose count of blocks and abort (break)
        walkingInThedark=True
        if walker-hardStartPos>1:
          # this is our second step
          backAgainstBoundary=False


        # Still good. Hoping for a black blob
        if (blackConstraints[line][walker]==1):
          # bingo! We have got a black blob. No idea if this is belonging to the current block. Test that next.
          # Store the position anyway.
          partialBlockBits.append(walker)



        break




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



class Graphics(threading.Thread):
  def __init__(self,grid):
    threading.Thread.__init__(self)
    self.grid=grid
    self.start()
    self.scale=2
    self.offset=140
    self.gridBlobs=np.zeros([25,25],dtype='int')

  def callback(self):
    self.root.quit()

  def run(self):
    self.root = tk.Tk()
    self.root.protocol("WM_DELETE_WINDOW", self.callback)
    self.canvas = tk.Canvas(self.root, width=255*self.scale+self.offset, height=250*self.scale+self.offset)
    self.canvas.pack()
    label = tk.Label(self.root, text="Hello World")
    label.pack()
    for idx,line in enumerate(self.grid.blockrows.K):
      self.canvas.create_text(20,10+idx*10*self.scale+self.offset,text=line,anchor="w")

    for idx,line in enumerate(self.grid.blockcols.K):
      self.canvas.create_text((10+idx*10*self.scale+self.offset,5), text="\n".join([str(x) for x in line]), anchor="n")

    for i in range(10,250,10):
      self.canvas.create_line(i*self.scale+self.offset, 0*self.scale+self.offset, i*self.scale+self.offset, 250*self.scale+self.offset, fill="grey")
      self.canvas.create_line(0*self.scale+self.offset, i*self.scale+self.offset, 250*self.scale+self.offset, i*self.scale+self.offset, fill="grey")


    for row in range(0,25):
      for col in range(0,25):
        self.gridBlobs[row][col]=self.foo=self.canvas.create_rectangle(  (0+10*col)*self.scale+self.offset,(0+10*row)*self.scale+self.offset,
                                 (10+10*col)*self.scale+self.offset, (10+10*row)*self.scale+self.offset,fill='grey')


    self.root.mainloop()

  def test(self):
    self.canvas.create_rectangle(  0,   0, 150, 150, fill="yellow")
    self.canvas.create_rectangle(100,  50, 250, 100, fill="orange", width=5)
  def test2(self):
    self.canvas.create_rectangle( 50, 100, 150, 200, fill="green", outline="red", width=3)
    self.canvas.create_rectangle(125,  25, 175, 190, fill="purple", width=0)

  def lightBlock(self,line,col,colour):
    #self.canvas.create_rectangle(  (0+10*col)*self.scale+self.offset,(0+10*line)*self.scale+self.offset,
    #                             (10+10*col)*self.scale+self.offset, (10+10*line)*self.scale+self.offset,fill=colour)
    self.canvas.itemconfig(self.gridBlobs[line][col], fill=colour)


  def drawBlockFreedom(self,linemin,linemax,colmin,colmax,no=3,color='yellow'):
    if (linemin==linemax):
      self.canvas.create_line((0+10*colmin)*self.scale+self.offset,(no*1.5+10*linemin)*self.scale+self.offset,
                            (0+10*colmax)*self.scale+self.offset, (no*1.5+10*linemax)*self.scale+self.offset,fill=color,arrow=tk.BOTH,tag='arrow')
    else:
      self.canvas.create_line((no*1.5+10*colmin)*self.scale+self.offset,(0+10*linemin)*self.scale+self.offset,
                            (no*1.5+10*colmax)*self.scale+self.offset, (0+10*linemax)*self.scale+self.offset,fill=color,arrow=tk.BOTH,tag='arrow')


  def showGrid(self):
    #self.canvas.create_rectangle(100,  50, 250, 100, fill="orange", width=5)
    for row,line in enumerate(self.grid.blackConstraints):
      for col,bit in enumerate(line):
        if bit:
          self.lightBlock(row,col,'black')
      for row,line in enumerate(self.grid.whiteConstraints):
        for col,bit in enumerate(line):
          if bit:
            self.lightBlock(row,col,'white')
    #self.showFreedom()

  def showFreedom(self):
    for row,line in enumerate(self.grid.blockrows.possibleRowPos):
      for blockno,blockpossibility in enumerate(line):
        self.drawBlockFreedom(row,row,min(blockpossibility),max(blockpossibility),blockno,'yellow')
    for row,line in enumerate(self.grid.blockcols.possibleRowPos):
      for blockno,blockpossibility in enumerate(line):
        self.drawBlockFreedom(min(blockpossibility),max(blockpossibility),row,row,blockno,'red')
