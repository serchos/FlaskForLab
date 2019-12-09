import os, io, math, random, sqlite3
from Metrics import MetricL1, MetricEuclid, MetricChebyshev
from ExtractionAlgorithms import PrepareForKNN
from flask import flash

'''
def KMeans(TabData, ClusterCount, Metric, Weight, PrimCent): 
 TabDataNormal, UnKeysMat, MEMat, DMat, Y=PrepareForKNN(TabData, len(TabData[0]))
 TabDataNormal.pop(0)
 TabDataNormal=list(zip(*TabDataNormal))
 mu1=PrimaryCenter(TabDataNormal, Y, ClusterCount, Metric, Weight, PrimCent)
 TotalDist1, TotalDist2=-1, -1

 while True:
  ClusterList=CreateClusterList(TabDataNormal, mu1, Metric, Weight)
  if TotalDist1==-1:
   TotalDist1=TotalDistance(ClusterList, mu1)
  
  mu2=[]

  for Cluster in ClusterList:
   center=CenterOfMass(Cluster)
   mu2.append(center)
  
  TotalDist2=TotalDistance(ClusterList, mu2)
  
  if TotalDist2>=TotalDist1:
   break
  else:
   TotalDist1=TotalDist2
   mu1=mu2[:]

 mu=CloseToCenterOfMass(ClusterList, mu1, Metric, Weight)
 id=GetIdOfCenterMass(TabData, TabDataNormal, mu)
 
 id.sort()
 id1 = [e for i,e in enumerate(id) if e not in id[:i]]
 return id1, mu
 #ClearTabData(TabDataNormal, mu)
'''
def KMeans2(TabData, ClusterCount, Metric, Weight, PrimCent): 
 TabDataNormal, UnKeysMat, MEMat, DMat, Y=PrepareForKNN(TabData, len(TabData[0]))
 TabDataNormal.pop(0)
 TabDataNormal=list(zip(*TabDataNormal))
 mu1=PrimaryCenter(TabDataNormal, Y, ClusterCount, Metric, Weight, PrimCent)
 
 Default=[]
 for i in TabDataNormal[0]:
  if isinstance(i, list)==True:
   Default.append([0 for ii in i])
  else:
   Default.append(0)

 while True:
  ClusterList=CreateClusterList(TabDataNormal, mu1, Metric, Weight)
  mu2=[]
  #print('0: {0}  1: {1}  2: {2}  3: {3}  4: {4}'. format(len(ClusterList[0]), len(ClusterList[1]), len(ClusterList[2]), len(ClusterList[3]), len(ClusterList[4])))
  
  for Cluster in ClusterList:
   center=CenterOfMass(Cluster, Default)
   mu2.append(center)
  
  if (mu1==mu2):
   break
  else:
   mu1=mu2[:]

 mu=CloseToCenterOfMass(ClusterList, mu1, Metric, Weight)
 OptTabData=GetOptimizedTabData(TabData, TabDataNormal, mu)
 
 return OptTabData
'''
def Classification(TabData, Metric, Weight, Similarity):
 Id=[Str[0] for Str in TabData]
 TabDataNormal, UnKeysMat, MEMat, DMat, Y=PrepareForKNN(TabData, len(TabData[0]))
 TabDataNormal.pop(0)
 TabDataNormal=list(zip(*TabDataNormal))
 
 for i, Str1 in enumerate(TabDataNormal):
  ClosePrecId=[]
  for j, Str2 in enumerate(TabDataNormal):
   if i!=j:
    dist=globals()[Metric](Str1, Str2, Weight)
    if dist<=Similarity:
     ClosePrecId.append(j)
  
  for id in list(reversed(ClosePrecId)):
   TabDataNormal.pop(id)
   Id.pop(id)

 return Id
'''
def Classification2(TabData, Metric, Weight, Similarity):
 TabDataNormal, UnKeysMat, MEMat, DMat, Y=PrepareForKNN(TabData, len(TabData[0]))
 TabDataNormal = list(TabDataNormal)
 TabData = list(TabData)
 TabDataNormal.pop(0)
 TabDataNormal=list(zip(*TabDataNormal))
 
 for i, Str1 in enumerate(TabDataNormal):
  PartTabDataNormal=(TabDataNormal)[i+1:]
  for j, Str2 in enumerate(PartTabDataNormal):
   dist=globals()[Metric](Str1, Str2, Weight)
   if dist<=Similarity:
    PartTabDataNormal.pop(j)
    TabDataNormal.pop(i+1+j)
    TabData.pop(i+1+j)
 
 return TabData

 
 
 
def TimurAlgorithm(TabData):
 IdTab=[Str[0] for Str in TabData]
 TabDataNormal, UnKeysMat, MEMat, DMat, Y=PrepareForKNN(TabData, len(TabData[0]))
 TabDataNormal.pop(0)
 #TabDataNormal=list(zip(*TabDataNormal))
 
 Id, d=[], {}
 
 for y in Y:
  if d.get(y)==None:
   d[y]=len(d)
   
 ClusterList=[[] for i in range(0, len(d))]
 
 for i, y in enumerate(Y):
  ClusterList[d.get(y)].append(i)

 for Column in TabDataNormal:
  for ClNum, Cluster in enumerate(ClusterList):
   #flash('------'+str(ClNum)+'------')
   max, min, idmax, idmin=Column[Cluster[0]], Column[Cluster[0]], Cluster[0], Cluster[0]
   for i in Cluster:
    if Column[i]>max:
     max=Column[i]
     idmax=i
    if Column[i]<min:
     min=Column[i]
     idmin=i
   #flash('IdMax: '+str(idmax)+'   Max: '+str(max))
   #flash('IdMin: '+str(idmin)+'   Min: '+str(max))
   Id.append(IdTab[idmax])
   Id.append(IdTab[idmin])
 
 Id.sort()
 Id1 = [e for i,e in enumerate(Id) if e not in Id[:i]]
 return Id1

def TimurAlgorithm2(TabData):
 OptTabData, Id=[], {} 
 TabDataNormal, UnKeysMat, MEMat, DMat, Y=PrepareForKNN(TabData, len(TabData[0]))
 TabDataNormal.pop(0)
 
 ClusterList={}
 
 for i, y in enumerate(Y):
  if ClusterList.get(y)==None:
   ClusterList[y]=[i]
  else:
   ClusterList[y].append(i)

 for key in ClusterList.keys():
  Cluster=ClusterList[key]
  for Column in TabDataNormal:
   min, max=Column[Cluster[0]], Column[Cluster[0]]
   idmin, idmax=Cluster[0], Cluster[0] 
   for i in Cluster[1:]:
    if Column[i]<min:
     min=Column[i]
     idmin=i
    elif Column[i]>max:
     max=Column[i]
     idmax=i

   Id[idmin], Id[idmax]=idmin, idmax

 for id in sorted(Id.keys()):
  OptTabData.append(TabData[id])

 return OptTabData

 
 
#--------------------PrimaryCentersOfClusters---------------------
def PrimaryCenter(TabDataNormal, Y, ClusterCount, Metric, Weight, PrimCent):
 Center={'Forgy': Forgy2(TabDataNormal, ClusterCount, Metric, Weight), 
		 'RandomPartitioning': RandomPartitioning(TabDataNormal, ClusterCount), 
		 'AnswerPartitioning': AnswerPartitioning(TabDataNormal, Y, ClusterCount)
		}
 return Center[PrimCent]
 
def Forgy(TabDataNormal, ClusterCount, Metric, Weight):
 rmu, mu=[], []
 
 for i in range(0, ClusterCount):
  flag=True
  while flag==True:
   r=random.randint(0, len(TabDataNormal)-1)
   flag=False
   for rmuel in rmu:
    if r==rmuel:
     flag=True
     break
  rmu.append(r)
  
 for i in rmu:
  mu.append(TabDataNormal[i])
 
 EmptyCluster=True
 
 while EmptyCluster==True:
  EmptyCluster=False
  ClusterList=CreateClusterList(TabDataNormal, mu, Metric, Weight)
  for i, Cluster in enumerate(ClusterList):
   if Cluster==[]:
    EmptyCluster, flag=True, True
    while flag==True:
     r=random.randint(0, len(TabDataNormal)-1)
     flag=False
     for rmuel in rmu:
      if r==rmuel:
       flag=True
       break
    rmu[i]=r
    mu[i]=TabDataNormal[r]

 return mu

def Forgy2(TabDataNormal, ClusterCount, Metric, Weight):
 EmptyCluster, mu=True, []

 while EmptyCluster==True:
  rmu, mu=[], []
  EmptyCluster=False 
  for i in range(0, ClusterCount):
   flag=True
   while flag==True:
    r=random.randint(0, len(TabDataNormal)-1)
    flag=False
    for rmuel in rmu:
     if r==rmuel:
      flag=True
      break
   rmu.append(r)
  for i in rmu:
   mu.append(TabDataNormal[i])
  
  ClusterList=CreateClusterList(TabDataNormal, mu, Metric, Weight)
  
  for Cluster in ClusterList:
   if Cluster==[]:
    EmptyCluster=True
    break

 return mu
 
def RandomPartitioning(TabDataNormal, ClusterCount):
 ClusterList=[[] for i in range(0, ClusterCount)]
 EmptyCluster=True

 while EmptyCluster==True:
  for Str in TabDataNormal:
   r=random.randint(0, ClusterCount-1)
   ClusterList[r].append(Str)
  
  EmptyCluster=False
  for Cluster in ClusterList:
   if Cluster==[]:
    EmptyCluster=True
    ClusterList=[[] for i in range(0, ClusterCount)]
    break
 
 mu=[]
 
 for Cluster in ClusterList:
  mu.append(CenterOfMass(Cluster, 0))

 return mu

def AnswerPartitioning(TabDataNormal, Y, ClusterCount):
 ClusterList=[[] for i in range(0, ClusterCount)]
 d={}
 
 for y in Y:
  if d.get(y)==None:
   d[y]=len(d)
  
 if len(d)==ClusterCount:
  
  for Str, y in zip(TabDataNormal, Y):
   ClusterList[d.get(y)].append(Str)
   
 elif len(d)<ClusterCount:
 
  for Str, y in zip(TabDataNormal, Y):
   ClusterList[d.get(y)].append(Str)
  
  for i, j in zip(range(len(d), ClusterCount), range(0, ClusterCount-len(d))):
    for k in range(0, math.floor(len(ClusterList[j])/2)):
     Str=ClusterList[j].pop()
     ClusterList[i].append(Str)

 elif len(d)>ClusterCount: 
  for Str, y in zip(TabDataNormal, Y):
   i=d.get(y)
   if i>=ClusterCount:
    r=random.randint(0, ClusterCount-1)
    ClusterList[r].append(Str)
   else:
    ClusterList[i].append(Str)

 mu=[]

 return mu
  
#-----------------------------------------------------------------------

#-----------------------Help K-Mean Functions---------------------------
def CreateClusterList(TabDataNormal, mu, Metric, Weight):
 ClusterList=[[] for i in mu]
 for i, stri in enumerate(TabDataNormal):
  mindist, minmu=-1, -1
  
  for j, strj in enumerate(mu):
   dist=globals()[Metric](stri, strj, Weight)
   if (mindist==-1) or (dist<mindist and dist!=0):
    mindist=dist
    minmu=j
  
  ClusterList[minmu].append(stri)

 return ClusterList
 
def CenterOfMass(Cluster, Default):#Сделать рекурсивно. возможно применить транспонировние
 sum=[]
 if Cluster!=[]:
  for i in Cluster[0]:
   if isinstance(i, list)==True:
    buf=[]
    for ii in i:
     buf.append(0)
    sum.append(buf)
   else:
    sum.append(0)

  for Str in Cluster:
   for i, x in enumerate(Str):
    if isinstance(x, list)==True:
     for ii, xx in enumerate(x):
      sum[i][ii]=sum[i][ii]+xx
    else:
     sum[i]=sum[i]+x
	
  ClusterLen=len(Cluster)
   
  for i, s in enumerate(sum):
   if isinstance(s, list)==True:
    for ii, ss in enumerate(s):
     sum[i][ii]=sum[i][ii]/ClusterLen
   else:
    sum[i]=sum[i]/ClusterLen
 else:
  sum=Default[:]
  
 return sum
 
'''
def CenterOfMass(Cluster): Старая версия
 sum=[0 for i in Cluster[0]]

 for Str in Cluster:
  for i, x in enumerate(Str):
   sum[i]=sum[i]+x
	
 ClusterLen=len(Cluster)
  
 for i in range(0, len(sum)):#check without range only for
  sum[i]=sum[i]/ClusterLen
 return sum
'''
 
def TotalDistance(ClusterList, mu):
 TotalDistance=0
 for Cluster, muel in zip(ClusterList, mu):
  for Str in Cluster:
   for s, m in zip(Str, muel):
    if isinstance(s, list)==True:
     PartDistance=0
     for ss, mm in zip(s, m):
      PartDistance+=(ss-mm)*(ss-mm)
     TotalDistance+=math.sqrt(PartDistance)
    else:
     TotalDistance+=(s-m)*(s-m)
 
 return TotalDistance
 
''' 
def TotalDistance(ClusterList, mu):старая версия
 TotalDistance=0
 for Cluster, muel in zip(ClusterList, mu):
  for Str in Cluster:
   buf=[]
   for s, m in zip(Str, muel):
    buf.append(s-m)
   for x in buf:
    TotalDistance=TotalDistance+x*x
 return TotalDistance
'''
 
def CloseToCenterOfMass(ClusterList, mu, Metric, Weight):
 newmu=[]
 
 for Cluster in ClusterList:
  if Cluster!=[]:
   mindist, minmu=-1, 0
   for Str, muel in zip(enumerate(Cluster), mu):
    dist=globals()[Metric](Str[1], muel, Weight)
    if mindist==-1 or dist<mindist:
     mindist=dist
     minmu=Str[0]
   newmu.append(Cluster[minmu])

 return newmu
 
#-----------------------------------------------------------------------
''' 
def ClearTabData(TabDataNormal, mu):
 db=get_db()

 for i, Str in enumerate(TabDataNormal):
  flag=False
  for muel in mu:
   if Str==muel:
    flag=True
    break
  if flag==False:
   db.execute('DELETE FROM {0} WHERE id={1}'.format(BPName, TabData[i][0]))
'''
def GetIdOfCenterMass(TabData, TabDataNormal, mu):
 id=[]
 for i, Str in enumerate(TabDataNormal):
  for j, muel in enumerate(mu):
   if Str==muel:
    id.append(TabData[i][0])
    mu.pop(j)
    break
 return id
 
def GetOptimizedTabData(TabData, TabDataNormal, mu):
 OptTabData=[]
 print('Длина mu: {0}'.format(len(mu)))
 
 for muel in mu:
  for i, Str in enumerate(TabDataNormal):
   if muel==Str:
    OptTabData.append(TabData[i])
    break

 print('Длина опт: {0}'.format(len(OptTabData)))

 return OptTabData