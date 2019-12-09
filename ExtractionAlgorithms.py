import os, io, math, random, Vectorization
from Metrics import MetricL1, MetricEuclid, MetricChebyshev
from flask import flash

#--------------------------KNN Algorithm----------------------------
def KNNAlgorithm(TSData, COData, NeibCount, Metric, Weight):
 ColCount=len(TSData[0])
 # flash(TSData[0][0])
 TSDataNormal, UnKeysMat, MEMat, DMat, Y=PrepareForKNN(TSData, ColCount)
 TSDataNormal=list(zip(*TSDataNormal))
 COData=PrepareCOData(COData)
 AnswerList, MinDistList, YMinDistList, MaxNeibList=[], [], [], []

 for s in COData:
  CODataNormal=NormalizeNewData(s, MEMat, DMat, UnKeysMat, ColCount)
  MinDist, YMinDist, IdMinDist=KNN(TSDataNormal, CODataNormal, NeibCount, Metric, Weight, Y)
  Answer, MaxNeib=Voting(MinDist, YMinDist, IdMinDist)
  AnswerList.append(Answer)
  MinDistList.append(MinDist)
  YMinDistList.append(YMinDist)
  MaxNeibList.append(MaxNeib)
 
 return AnswerList, MinDistList, YMinDistList, MaxNeibList
 
def KNN(TabDataNormal, NewDataNormal, NeibCount, Metric, Weight, Y):
 MinDist, YMinDist, IdMinDist=[], [], []
 Left, Right=-1, -1
 MetricMas={'MetricL1':MetricL1,'MetricEuclid':MetricEuclid,'MetricChebyshev':MetricChebyshev}
 
 for id, str in enumerate(TabDataNormal):
  dist=MetricMas[Metric](str, NewDataNormal, Weight)

  if len(MinDist)<NeibCount:
   if Left==-1:
    Left, Right=dist, dist
    LeftPos, RightPos=0, 0
   elif dist<Left:
    Left=dist
    LeftPos=id
   elif dist>Right:
    Right=dist
    RightPos=id
	
   MinDist.append(dist)
   YMinDist.append(Y[id])
   IdMinDist.append(id)
  else:
   if dist<=Left:
    Left=dist
    LeftPos=RightPos
 
   if (dist<=Left) or (Left<dist and dist<Right):
    MinDist[RightPos]=dist
    YMinDist[RightPos]=Y[id]
    IdMinDist[RightPos]=id

    Right, RightPos=MinDist[0], 0
    
    for count, i in enumerate(MinDist):#Maybe here we need float
     if i>Right:
      Right=i
      RightPos=count

 return MinDist, YMinDist, IdMinDist
 
def Voting(MinDist, YMinDist, IdMinDist):
 max=0

 for y1 in YMinDist:
  count=0
  for y2 in YMinDist:#I can decrease count
   if y1==y2:
    count+=1
  if count>max:
   max=count
   Answer=y1

 return Answer, max 
#-----------------------------------------------------------------------------
#------------------------------Help Functions---------------------------------
def PrepareCOData(COData):
 NewCOData=[]

 for i in COData:
  BufList=[]
  for j in i:
   if isinstance(j, list)==False and IsFloat(j)==False:
    BufList.append([j])
   else:
    BufList.append(j)
  NewCOData.append(BufList)	

 return NewCOData

def NormalizeNewData(NewData, MEMat, DMat, UnKeysMat, ColCount):
 count=0
 NewDataNormal=[]
 
 for  s, ME, D in zip(NewData, MEMat, DMat):
  if IsFloat(s)==False:
   CountKeysData=Vectorization.CountKeysInStr(s, UnKeysMat[count])
   NewDataNormal.append(NoLineNormal2(CountKeysData, ME, D))
   count+=1
  else:
   if D!=0:
    NewDataNormal.append(1/(math.exp((-0.3)*((float(s)-float(ME))/math.sqrt(float(D))))+1))#OBEDINIT
   else:
    NewDataNormal.append(1/(math.exp((-0.3)*(float(s)-float(ME)))+1))#OBEDINIT
 
 return NewDataNormal
 
def PrepareForKNN(TabData, ColCount):
 TabDataNormal, UnKeysMat, Y, MEMat, DMat=[], [], [], [], []
 
 for CurCol in range(0, ColCount-1):
  ColData, ColDataNormal=[], []

  for s in TabData:
   buf=s[CurCol]
   if isinstance(s[CurCol], list)==False and IsFloat(s[CurCol])==False:
    buf=[buf]
   ColData.append(buf)
  
  #Y=ColData#ERES AND KOSTIL
  if IsFloat(ColData[0])==False:
   UnKeys=Vectorization.CollectUnKeys(ColData, [])
   UnKeysMat.append(UnKeys)
   ME, D=[], []

   for s in ColData:
    CountKeysData=Vectorization.CountKeysInStr(s, UnKeys)
    ME=FindMinMaxListME(CountKeysData, ME, len(ColData))

   for s in ColData:
    CountKeysData=Vectorization.CountKeysInStr(s, UnKeys)
    D=FindMinMaxListD(CountKeysData, ME, D, len(ColData))

   for s in ColData:
    CountKeysData=Vectorization.CountKeysInStr(s, UnKeys)
    ColDataNormal.append(NoLineNormal2(CountKeysData, ME, D))

  else:
   ME=FindMinMax2ME(ColData)
   D=FindMinMax2D(ColData, ME)
   ColDataNormal=NoLineNormal2(ColData, ME, D)

  MEMat.append(ME)
  DMat.append(D)
  TabDataNormal.append(ColDataNormal)

 for s in TabData:
  Y.append(s[ColCount-1]) 
  
 return TabDataNormal, UnKeysMat, MEMat, DMat, Y

def IsFloat(value):
 try:
  float(value)
  return True
 except ValueError:
  return False
 except TypeError:
  return False
  
def IsInt(value):
 try:
  int(value, 10)
  return True
 except ValueError:
  return False
 except TypeError:
  return False
  
def FindMinMax2ME(ColData):
 n=len(ColData)
 ME=0

 for s in ColData:
  ME+=s*(1/n)
 
 return ME

def FindMinMax2D(ColData, ME):
 n=len(ColData)
 D=0

 for s in ColData:
  D+=(1/n)*math.pow((s-ME), 2)

 return D
 
def FindMinMaxListME(VecData, MEList, n):
 if MEList==[]:
  MEList=[0 for i in VecData]

 for count, s in enumerate(VecData):
  MEList[count]+=s*(1/n)

 return MEList
 
def FindMinMaxListD(VecData, MEList, DList, n):
 if DList==[]:
  DList=[0 for i in VecData]

 for count, s in enumerate(VecData):
  DList[count]+=(1/n)*math.pow((s-MEList[count]), 2)

 return DList

def NoLineNormal2(ColData, ME, D):
 ColDataNormal=[]
 
 if isinstance(ME, list)==False: 
  #try:
   for s in ColData:
    if D!=0:
     ColDataNormal.append(1/(math.exp((-0.3)*((s-ME)/math.sqrt(D)))+1))
    else:
     ColDataNormal.append(1/(math.exp((-0.3)*(s-ME))+1))
    #ColDataNormal.append(1/(math.exp((-0.3)*(s/Cent-1))+1))
  #except:
   #import sys
   #import ipdb
   #tb = sys.exc_info()[2]
   #ipdb.post_mortem(tb)
 else:
  for i, me, d in zip(ColData, ME, D):
   if d!=0:
    ColDataNormal.append(1/(math.exp((-0.3)*((i-me)/math.sqrt(d)))+1))
   else:
    ColDataNormal.append(1/(math.exp((-0.3)*(i-me))+1))

 return ColDataNormal
#-----------------------------------------------------------------------