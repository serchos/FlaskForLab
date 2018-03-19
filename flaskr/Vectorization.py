import os
import io

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
	 
def CollectUnKeys(Str, UnKeys):#do beauty recursion
 for i in Str:
  if isinstance(i, list)==False:
   flag=False
  
   for j in UnKeys:
    if i==j:
     flag=True
     break
	
   if flag==False:
    UnKeys.append(i)

  else:
   for k in i:
    flag=False

    for j in UnKeys:
     if k==j:
      flag=True
      break
	
    if flag==False:
     UnKeys.append(k)
 
 flash(UnKeys)
 return UnKeys

def CountKeysInStr(Str, UnKeys):
 UnKeysLen=len(UnKeys)
 CountKeysList=[0 for i in range(0, UnKeysLen)]
 
 for i in Str:
  ind=UnKeys.index(i)
  CountKeysList[ind]=CountKeysList[ind]+1

 return CountKeysList
 
def HashFun(CountKeysList):
 count=1
 HashKeys=[]
 
 for i in CountKeysList: #there wil be some collisions, if number>9
  if i==0:
   buf=0
  else:
   buf=int(str(count)+str(i), 10)
  HashKeys.append(buf)
  count+=1

 return HashKeys
