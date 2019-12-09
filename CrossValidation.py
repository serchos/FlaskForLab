import os, io, math, random
from Metrics import MetricL1, MetricEuclid, MetricChebyshev
from flask import flash
from ExtractionAlgorithms import KNNAlgorithm
 
def KFoldCV(TabData, K, NeibCount, Metric, Weight):
 #TabData=Shuffle(TabData)
 IntPart, FractPart=len(TabData)//K, len(TabData)%K
 Index, Acc=0, 0

 for i in range(0, K):
  COCount=IntPart
  if FractPart!=0:
   COCount+=1
   FractPart-=1

  TSData, COData, RealAnswerList=TabData, [], []
  
  # for i in range(Index, Index+COCount):
   # COData.append(TSData.pop(i))
   
   
  TSData=TabData[:Index]+TabData[Index+COCount:]
  COData=TabData[Index:Index+COCount]
  #for i in range()
   
  for Str in COData:
   RealAnswerList.append(Str[len(Str)-1])
  
  AnswerList, MinDistList, YMinDistList, MaxNeibList=KNNAlgorithm(TSData, COData, NeibCount, Metric, Weight)
  Acc+=Accuracy(AnswerList, RealAnswerList)
  Index+=COCount
  
 Acc=round(Acc/K, 2)
 return Acc
   
def HoldOutCV(TabData, Percent, N, NeibCount, Metric, Weight):
 #TabData=Shuffle(TabData)
 CODataLen=len(TabData)-math.floor(len(TabData)*(Percent*0.01))
 Acc=0
 
 for n in range(0,N):
  TSData, COData, RealAnswerList=TabData[:], [], []

  for i in range(0, CODataLen):
   r=random.randint(0, (len(TSData)-1))
   COData.append(TSData.pop(r))

  for Str in COData:
   RealAnswerList.append(Str[len(Str)-1])
  
  AnswerList, MinDistList, YMinDistList, MaxNeibList=KNNAlgorithm(TSData, COData, NeibCount, Metric, Weight)
  Acc+=Accuracy(AnswerList, RealAnswerList)
  
 Acc=round(Acc/N, 2)

 return Acc

def Shuffle(TabData):
 Count=len(TabData)  
  
 for i in range(0, Count-1):
  r=random.randint(i+1, Count-1)
  buf=TabData[i]
  TabData[i]=TabData[r]
  TabData[r]=buf
  
 return TabData
  
def Accuracy(AnswerList, RealAnswerList):
 CountCorAns=0
 for i, j in zip(RealAnswerList, AnswerList):
  if i==j:
    CountCorAns+=1

 Acc=round((CountCorAns/len(AnswerList))*100, 2)
 return Acc 
 