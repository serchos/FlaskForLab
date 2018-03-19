import sqlite3, os, io, math, re
import Vectorization
import urllib.request

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.utils import secure_filename

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
TabListGl=[]
TabInfo=[]
TabData=[]

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'files'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
 rv = sqlite3.connect(os.path.join(app.root_path+'\\files', 'flaskrflaskr.db'))
 rv.row_factory = sqlite3.Row
 return rv
	
def init_db(SchName): #!!!!!!!!!!!
 with app.app_context():
  db = get_db()
  with app.open_resource(SchName, mode='r') as f:
   db.cursor().executescript(f.read())
  db.commit()
	
if __name__ == '__main__':
    app.run()

	
def get_db():
 if not hasattr(g, 'sqlite_db'):
  g.sqlite_db = connect_db()
 return g.sqlite_db
	
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
	
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            #directory=os.walk(app.root_path+'/files',followlinks=False)
            #return render_template('show_entries.html', directory=directory)
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/ExpHandLoad', methods=['GET', 'POST'])
def ExpHandLoad():
 return render_template('ExpHandLoad.html')


@app.route('/MachLearn', methods=['GET', 'POST'])
def MachLearn():
 db=get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 return render_template('MachLearn.html', TabList=TabList)

	
#Upload Files---------------------------------------------------------	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 		
		
@app.route('/PageForLab1')
def PageForLab1():
 return render_template('PageForLab1.html')	
 
@app.route('/PageForLab2')
def PageForLab2():
 return render_template('PageForLab2.html')	
 
@app.route('/PageForLab3')
def PageForLab3():
 return render_template('PageForLab3.html')	
		
@app.route('/')
def menu():
 return render_template('menu.html')
	
@app.route('/LookBP',  methods = ['GET', 'POST'])
def LookBP():
 db = get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 
 #cur = db.execute('select * from entries order by id desc')
 #entries = cur.fetchall()
 return render_template('LookBP.html', TabList=TabList)
 
@app.route('/LookBP1',  methods = ['GET', 'POST'])
def ExecDataFromTable():
 BPName=request.form['TableChoice']
 db=get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 cur=db.execute('SELECT * FROM {0}'.format(BPName))
 TabData=cur.fetchall()
 return render_template('LookBP.html', TabList=TabList, TabData=TabData)

@app.route('/EditBP',  methods = ['GET', 'POST'])
def EditBP():
 db = get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 return render_template('EditBP.html', TabList=TabList)

@app.route('/TabEdit',  methods = ['GET', 'POST'])
def TabEdit():
 db=get_db()
 BPName=request.form['TableChoice']
 if request.form['TabEdit']=='Удалить':
  db.execute('DROP TABLE {0}'.format(BPName))
 elif request.form['TabEdit']=='Переименовать':
  NewBPName=request.form['NewBPName']
  db.execute('ALTER TABLE {0} RENAME TO {1}'.format(BPName, NewBPName))
  
 elif request.form['TabEdit']=='Работа с данными':
  global BPName
  global TabData
  global TabInfo
  BPName=request.form['TableChoice']
  cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
  TabData=cur.fetchall()
  cur=db.execute('pragma table_info({0})'.format(BPName))
  TabInfo=cur.fetchall()
  return render_template('DataWork.html', TabData=TabData, TabInfo=TabInfo)

 db.commit()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 return render_template('EditBP.html', TabList=TabList)


@app.route('/DataWork',  methods = ['GET', 'POST'])
def DataWork():
 db=get_db()
 global TabInfo
 global TabData

 if request.form['DataEdit']=='Записать столбец':
  NewColName=request.form['NewColName']
  NewColType=request.form['NewColType']
  db.execute('ALTER TABLE {0} ADD COLUMN {1} {2}'.format(BPName, NewColName, NewColType))
  db.commit()
  cur=db.execute('pragma table_info({0})'.format(BPName))
  TabInfo=cur.fetchall()
  cur=db.execute('SELECT * FROM {0}'.format(BPName))
  TabData=cur.fetchall()

 elif request.form['DataEdit']=='Сохранить изменения':#look this shit
  Data=request.form.getlist('DataField')
  Id=request.form.getlist('IdField')
  Column=request.form.getlist('ColumnField')
  AddStr=request.form.getlist('AddStrField')
  DelStr=request.form.getlist('DelStrField')
  #flash(AddStr)
  
  AddColCount=int(request.form['AddColCount'], 10)
 
  for i in range(0, AddColCount):
   NewColName=request.form['AddColName'+str(i)]
   NewColType=request.form['AddColType'+str(i)]
   db.execute('ALTER TABLE {0} ADD COLUMN {1} {2}'.format(BPName, NewColName, NewColType))
  
  db.commit()
  cur=db.execute('pragma table_info({0})'.format(BPName))
  TabInfo=cur.fetchall()

  #Insert Strings In BP
  if len(AddStr)!=0:
   StrNames=','.join(s[1] for s in TabInfo)
   StrParam=','.join('null' for s in range(0, len(TabInfo)-1))

   for id in AddStr:
    StrParam=str(id)+','+StrParam
    db.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(BPName, StrNames, StrParam))

  #Update Strings In BP  
  for id, column, data in zip(Id, Column, Data):
   Col=int(column, 10)
   db.execute('UPDATE {0} SET {1}="{2}" WHERE id={3}'.format(BPName, TabInfo[Col][1], data, id))

  #Delete Strings From BP
  for id in DelStr:
   db.execute('DELETE FROM {0} WHERE id={1}'.format(BPName, id))

  db.commit()
  cur=db.execute('SELECT * FROM {0}'.format(BPName))
  TabData=cur.fetchall()

 elif request.form['DataEdit']=='Отменить изменения':#Make this on JavaScript
  cur=db.execute('SELECT * FROM {0}'.format(BPName))
  TabData=cur.fetchall()

 return render_template('DataWork.html', TabInfo=TabInfo, TabData=TabData)

@app.route('/InputBP',  methods = ['GET', 'POST'])
def AcceptAndCreateScheme():
 ColCount=int(request.form['ColCount'], 10)
 global BPName
 global TabData
 global TabInfo
 BPName=request.form['BPName']
 StrNames=''
 db=get_db()
 
 for i in range(ColCount):
  StrNames=StrNames+', '+request.form['ColName'+str(i)]+' '+request.form['ColType'+str(i)]

 db.execute('CREATE TABLE {0} (id integer primary key autoincrement{1})'.format(BPName, StrNames))
 cur=db.execute('pragma table_info({0})'.format(BPName))
 TabInfo=cur.fetchall()

 if request.form.get('BPFile')!='' and request.form.get('CopyDataToBP')=='on':
  TextFile=io.TextIOWrapper(request.files['BPFile'])
  CopyDataToBP(BPName, TextFile, TabInfo, request.files['BPFile'])

 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()

 return render_template('DataWork.html', TabData=TabData, TabInfo=TabInfo)#Look at this shit
 
def CopyDataToBP(BPName, TextFile, TabInfo, LOL):
 TextStr=TextFile.readlines()
 StrNames=''
 db=get_db()

 if (request.form.get('IdInFile')=='on'):
  StrNames=','.join(Str[1] for Str in TabInfo)
 else:
  StrNames=','.join(Str[1] for Str in TabInfo[1:])

 for Str in TextStr:
  StrParam= re.split("[,; ]+", Str)
  Buf=', '.join('?' for s in StrParam)
  db.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(BPName, StrNames, Buf), StrParam)
  #list(filter(None, re.split("[,; ]+", Str))) #if there is no empty params

 db.commit()
 return 

@app.route('/ShowTab',  methods = ['GET', 'POST'])
def ShowTab():
 db=get_db()
 global BPName
 BPName=request.form['TabList']
 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 cur=db.execute('pragma table_info({0})'.format(BPName))
 TabInfo=cur.fetchall()
 return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo, BPName=BPName)

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

  
def DataExecute(IdList, BPName, ColNames):
 db=get_db()
 DataList=Buf1=[]
 Buf1.extend(IdList)
 Buf2=', '.join(s for s in ColNames) #There must be '?'
 Buf3=', '.join('?' for s in IdList)

 cur=db.execute('SELECT {0} FROM ({1}) WHERE id in ({2})'.format(Buf2, BPName, Buf3), Buf1)
 DataList=cur.fetchall()
 return DataList

def SelectDataExecute(RowsNumber, ColNumber):
 COData = [[0]*(ColNumber-1) for i in range(RowsNumber)]
 COField=request.form.getlist('SelForCol0')
 
 for i in range(1, ColNumber):
  Column=request.form.getlist('SelForCol'+str(i))
  for count, j in enumerate(Column):
   COData[count][i-1]=j

 return COData, COField


@app.route('/GoMachLearn2',  methods = ['GET', 'POST'])
def GoMachLearn2():
 if request.form['Start']=='Старт!':
  return GoMachLearnNew() 
 elif request.form['Start']=='Оптимизировать':
  return DeleteSameParam()
  
@app.route('/OptimizeData',  methods = ['GET', 'POST'])
def OptimizeData():
 db=get_db()

 if request.form['Optimize']=='Оптимизировать':
  RepIdList=DeleteSameParam()
  RepDataList=[]

  for RepId in RepIdList:
   cur=db.execute('SELECT * FROM {0} WHERE id={1} ORDER BY id ASC'.format(BPName, RepId))
   RepDataList.append(list(cur.fetchone()))

 elif request.form['Optimize']=='Удалить':
  RepSelect=request.form.getlist('RepSelect')
  RepDataList=[]
  
  for RepId in RepSelect:
   db.execute('DELETE FROM {0} WHERE id={1}'.format(BPName, RepId))

 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 cur=db.execute('pragma table_info({0})'.format(BPName))
 TabInfo=cur.fetchall()

 return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo, RepDataList=RepDataList, BPName=BPName)
 
 
#@app.route('/GoMachLearn2',  methods = ['GET', 'POST'])
def GoMachLearnNew():   
 db=get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 cur=db.execute('pragma table_info({0})'.format(BPName))
 TabInfo=cur.fetchall()
 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 ColNames=[s[1] for count, s in enumerate(TabInfo) if count>0]
 #ColNames=[s[1] for s in range(1, len(TabInfo))]
 Algol=request.form.get('Algol')
 TSField=request.form.getlist('TSField')
 TSData=DataExecute(TSField, BPName, ColNames)
 RowsNumber=int(request.form['RowsNumber'], 10)
 ColNumber=int(request.form['ColNumber'], 10)
 NeibCount=int(request.form['NeibCount'], 10)
 
 if RowsNumber!=0:
  COData, COField=SelectDataExecute(RowsNumber, ColNumber)
  AlgolMas={'KNN':KNNAlgol}
  AnswerList, MinDistList, YMinDistList, MaxNeibList=AlgolMas[Algol](TSData, COData)
  return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo,
  COData=zip(COField, COData, AnswerList, MaxNeibList), NeibCount=NeibCount, NumPar=4, BPName=BPName)
 else:
  COField=request.form.getlist('COField')
  COData=DataExecute(COField, BPName, ColNames)
  RealAnswerList=DataExecute(COField, BPName, [ColNames[len(ColNames)-1]])
  AlgolMas={'KNN':KNNAlgol}
  AnswerList, MinDistList, YMinDistList, MaxNeibList=AlgolMas[Algol](TSData, COData)
  CountCorAns=0
  for i, j in zip(RealAnswerList, AnswerList):
   if i[0]==j:
    CountCorAns+=1
  Accuracy=round((CountCorAns/len(AnswerList))*100, 2)

  return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo,
  COData=zip(COField, COData, RealAnswerList, AnswerList, MaxNeibList), NeibCount=NeibCount, Accuracy=Accuracy, NumPar=5, BPName=BPName)


@app.route('/GoMachLearn3',  methods = ['GET', 'POST'])
def SavePrecInTable():#RAZOBRATSA. TODAY NEOHOTO
 db=get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 cur=db.execute('pragma table_info({0})'.format(BPName))
 TabInfo=cur.fetchall()
 ColNames=[s[1] for count, s in enumerate(TabInfo) if count>0]
 
 RowsNumber=int(request.form['RowsNumber'], 10)
 ColNumber=int(request.form['ColNumber'], 10)-1
 
 COData, COField=SelectDataExecute(RowsNumber, ColNumber)
 ColNamesStr=', '.join(s for s in ColNames)#NU TAKOE
 
 for str in COData:
  ParamStr=', '.join('"{0}"'.format(s) for s in str)
  cur=db.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(BPName, ColNamesStr, ParamStr))

 db.commit()
 cur=db.execute('SELECT * FROM '+BPName+' ORDER BY id ASC')
 TabData=cur.fetchall()

 return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo, BPName=BPName)

#@app.route('/DeleteSameParam',  methods = ['GET', 'POST'])
def DeleteSameParam():#RAZOBRATSA/ TODAY NEOHOTO
 db=get_db()
 cur=db.execute('pragma table_info('+BPName+')')
 TabInfo=cur.fetchall()
 
 cur=db.execute('SELECT * FROM '+BPName+' ORDER BY id ASC')
 RepIdList=[]
 
 for RowData in cur:
  RowDataLen=len(RowData)
  CondList=[str(i[1]) + '=' + str(j) for i, j in zip(TabInfo, RowData)]
  CondStr=' AND '.join(s for count, s in enumerate(CondList) if count>0 and count<RowDataLen-1)

  cur2=db.execute('SELECT * FROM {0} WHERE {1}'.format(BPName, CondStr))
  BufList=cur2.fetchall()

  if len(BufList)>1:
   for s in BufList:
    flag=False
    for RepId in RepIdList:
     if RepId==s[0]:
      flag=True
      break
	
    if flag==False:
     RepIdList.append(s[0])
 
 return RepIdList

def KNNAlgol(TSData, COData):
 ColCount=len(TSData[0])
 NeibCount=int(request.form['NeibCount'], 10)
 Metric=request.form.get('Metric')
 
 TSDataNormal, UnKeysMat, MEMat, DMat, Y=PrepareForKNN(TSData, ColCount)
 TSDataNormal=list(zip(*TSDataNormal))
 COData=PrepareCOData(COData)
 AnswerList, MinDistList, YMinDistList, MaxNeibList=[], [], [], []

 for s in COData:
  CODataNormal=NormalizeNewData(s, MEMat, DMat, UnKeysMat, ColCount)
  MinDist, YMinDist, IdMinDist=KNN3(TSDataNormal, CODataNormal, NeibCount, Metric, Y)
  Answer, MaxNeib=Voting(MinDist, YMinDist, IdMinDist)
  AnswerList.append(Answer)
  MinDistList.append(MinDist)
  YMinDistList.append(YMinDist)
  MaxNeibList.append(MaxNeib)
 
 return AnswerList, MinDistList, YMinDistList, MaxNeibList

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

def KNN3(TabDataNormal, NewDataNormal, NeibCount, Metric, Y):
 MinDist, YMinDist, IdMinDist=[], [], []
 Left, Right=-1, -1

 for id, str in enumerate(TabDataNormal):
  MetricMas={'MetL1':MetL1,'MetEuclid':MetEuclid,'MetCheb':MetCheb}
  dist=MetricMas[Metric](str, NewDataNormal)

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

def MetL1(str, NewDataNormal):
 dist=0
 
 for i, j in zip(str, NewDataNormal):
  if isinstance(i, list)==True:
   dist+=MetL1(i, j)
  else:
   dist+=math.fabs(i-j)

 return dist
 
def MetEuclid(str, NewDataNormal):
 dist=0
 
 for i, j in zip(str, NewDataNormal):
  if isinstance(i, list)==True:
   dist+=math.pow(MetL1(i, j), 2)
  else:
   dist+=math.pow(i-j, 2)

 return math.sqrt(dist)
 
def MetCheb(str, NewDataNormal):
 dist=0

 for i, j in zip(str, NewDataNormal):
  if isinstance(i, list)==True:
   buf=MetCheb(i,j)
  else:
   buf=math.fabs(i-j)
  if buf>dist:
   dist=buf

 return dist
 
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
 
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
	
