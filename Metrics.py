import os, io, math

def MetricL1(str, NewDataNormal, Weight):
 dist=0
 
 for i, j, w in zip(str, NewDataNormal, Weight):
  if isinstance(i, list)==True:
   dist+=MetricL1(i, j, [w for ii in i])
  else:
   dist+=math.fabs((i-j)*w)

 return dist

def MetricEuclid(str, NewDataNormal, Weight):
 dist=0
 
 for i, j, w in zip(str, NewDataNormal, Weight):
  if isinstance(i, list)==True:
   dist+=math.pow(w*MetricL1(i, j, [w for ii in i]), 2)
  else:
   dist+=math.pow(w*(i-j), 2)
 
 return math.sqrt(dist)
 
def MetricChebyshev(str, NewDataNormal, Weight):
 dist=0

 for i, j, w in zip(str, NewDataNormal, Weight):
  if isinstance(i, list)==True:
   buf=MetricChebyshev(i, j, [w for ii in i])
  else:
   buf=math.fabs(w*(i-j))
  if buf>dist:
   dist=buf

 return dist