import sqlite3, os, io, math, re, random
import Vectorization
import urllib.request

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.utils import secure_filename
from Metrics import MetricL1, MetricEuclid, MetricChebyshev
from ImprovingEfficiencyAlgorithms import KMeans, Classification, TimurAlgorithm
from ExtractionAlgorithms import KNNAlgorithm
from CrossValidation import KFoldCV, HoldOutCV, Shuffle

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
TabListGl=[]
TabInfo, TabData=[], []
TabDescrData, DescriptionTabInfo=[], []

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

if __name__ == '__main__':
 app.run()
	
	
def init_db(SchName): #!!!!!!!!!!!
 with app.app_context():
  db = get_db()
  with app.open_resource(SchName, mode='r') as f:
   db.cursor().executescript(f.read())
  db.commit()

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
def ExecDataFromTable(): #показать содержимое таблички
 BPName=request.form['TableChoice']
 db=get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 cur=db.execute('SELECT * FROM {0}'.format(BPName))
 TabData=cur.fetchall()
 cur=db.execute('pragma table_info({0})'.format(BPName))
 TabInfo=cur.fetchall()
 for i in TabList:
  if i[1] == BPName + 'Description':
   cur2 = db.execute('SELECT * FROM {0}'.format(BPName+'Description'))
   TabDescrData = cur2.fetchall()
   cur2=db.execute('pragma table_info({0})'.format(BPName+'Description'))
   DescriptionTabInfo=cur2.fetchall()
   return render_template('LookBP.html', TabList=TabList, TabData=TabData, TabDescrData=TabDescrData, TabInfo = TabInfo, DescriptionTabInfo=DescriptionTabInfo )
 return render_template('LookBP.html', TabList=TabList, TabData=TabData, TabInfo = TabInfo)

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
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 if request.form['TabEdit']=='Удалить':
  db.execute('DROP TABLE {0}'.format(BPName))
  for i in TabList:
   if i[1] == BPName + 'Description':
    db.execute('DROP TABLE {0}'.format(BPName + 'Description'))
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
  for i in TabList:
   if i[1] == BPName + 'Description':
    cur2 = db.execute('SELECT * FROM {0}'.format(BPName+'Description'))
    TabDescrData = cur2.fetchall()
    cur2=db.execute('pragma table_info({0})'.format(BPName+'Description'))
    DescriptionTabInfo=cur2.fetchall()
    return render_template('DataWork.html', TabData=TabData, TabDescrData=TabDescrData, 
	TabInfo = TabInfo, DescriptionTabInfo=DescriptionTabInfo )
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
 
 elif request.form['DataEdit']=='Повысить эффективность':
  ImprovingEfficiency()
  cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
  TabData=cur.fetchall()
  cur=db.execute('pragma table_info({0})'.format(BPName))
  TabInfo=cur.fetchall()

 return render_template('DataWork.html', TabInfo=TabInfo, TabData=TabData)

@app.route('/InputBP',  methods = ['GET', 'POST'])
def AcceptAndCreateScheme(): # создание таблицы в бп
 ColCount=int(request.form['ColCount'], 10) # преобразовать в int в десятичной системе
 global BPName, TabInfo, TabData
 global DescriptionBPName, DescriptionTabInfo, TabDescrData
 BPName=request.form['BPName']
 DescriptionBPName = BPName + 'Description'
 StrNames = ''
 StrDescNames = ''
 StrParamNames = ''
 StrDescriptions = ''
 StrTypes = ''
 StrRangeFrom = ''
 StrRangeTo = ''
 StrWeights = ''
 StrUnits = ''
 Description_Str_Names = ''
 db=get_db()
 # flash(ColCount)
 # return render_template('ExpHandLoad.html')
 for i in range(0,ColCount):
  StrNames = StrNames+', '+request.form['ColName'+str(i)]+' '+request.form['ColType'+str(i)] # str - переводит строку в id
 Description_Str_Names = ', '+ 'Параметр' + ' ' + 'text' + ', ' + 'Описание' + ' ' + 'text' + ', '+ 'Тип' + ' ' + 'text' + ', ' + 'Единицы_измерения' + ' ' + 'text' + ', ' + 'Диапазон_от' + ' ' + 'real' + ', ' + 'Диапазон_до' + ' ' + 'real' + ', ' + 'Вес' + ' ' + 'real'
 for i in range(0,ColCount-1):
  StrParamNames = StrParamNames + ', ' + request.form['ColName' + str(i)]
  StrDescriptions = StrDescriptions + ', ' + request.form['DescriptionName'+str(i)]
  StrTypes = StrTypes + ', ' + request.form['ColType' + str(i)]
  StrUnits = StrUnits + ', ' + request.form['ColUnit' + str(i)] #todo
  StrRangeFrom = StrRangeFrom + ', ' + request.form['RangeFrom' + str(i)]
  StrRangeTo = StrRangeTo + ', ' + request.form['RangeTo' + str(i)]
  StrWeights = StrWeights + ', ' + request.form['ColWeights' + str(i)]
 StrDescNames = 'Параметр' + ', ' + 'Описание' + ', ' + 'Тип' + ', ' + 'Единицы_измерения' + ', ' + 'Диапазон_от' + ', ' + 'Диапазон_до' + ', ' + 'Вес'
  #Description_Str_Names = ', ' + request.form['ColName'+str(i)] + ' ' + request.form['ColType' + str(i)] + ' ' + request.form['ColWeights' +str(i)] + ' ' + request.form['RangeFrom' + str(i)] + ' ' + request.form['RangeTo' + str(i)] + ' ' + request.form['ColUnit' + str(i)]+ ' ' + request.form['DescriptionName' + str(i)] 
 db.execute('CREATE TABLE {0} (id integer primary key autoincrement{1})'.format(BPName, StrNames))
 db.execute('CREATE TABLE {0} (id integer primary key autoincrement{1})'.format(DescriptionBPName, Description_Str_Names))
 cur=db.execute('pragma table_info({0})'.format(BPName))
 cur_2 = db.execute('pragma table_info({0})'.format(DescriptionBPName))
 TabInfo = cur.fetchall()
 DescriptionTabInfo = cur_2.fetchall()
 if request.form.get('BPFile')!='' and request.form.get('CopyDataToBP')=='on':
  TextFile=io.TextIOWrapper(request.files['BPFile'])
  CopyDataToBP(BPName, TextFile, TabInfo, request.files['BPFile'])
 CopyDataToDescriptionTable(DescriptionBPName, StrDescNames, StrParamNames, StrDescriptions, StrTypes, StrUnits, StrRangeFrom, StrRangeTo, StrWeights, ColCount)
 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 cur_2 = db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(DescriptionBPName))
 TabData=cur.fetchall()
 TabDescrData = cur_2.fetchall()
 return render_template('DataWork.html', TabData=TabData, TabInfo=TabInfo, TabDescrData=TabDescrData, DescriptionTabInfo=DescriptionTabInfo) # TabDescrData=TabDescrData, DescriptionTabInfo=DescriptionTabInfo
 
def CopyDataToDescriptionTable(DescriptionBPName, StrDescNames ,StrParamNames, StrDescriptions, StrTypes, StrUnits, StrRangeFrom, StrRangeTo, StrWeights, ColCount):
 db=get_db()
 ParamNames_mas = StrParamNames[2:].split(', ')
 Descriptions_mas = StrDescriptions[2:].split(', ')
 Types_mas = StrTypes[2:].split(', ')
 Units_mas = StrUnits[2:].split(', ')
 RangeFrom_mas = StrRangeFrom[2:].split(', ')
 RangeTo_mas = StrRangeTo[2:].split(', ')
 Weights_mas = StrWeights[2:].split(', ')
 # flash(StrDescNames)
 for i in range(0,ColCount-1):
  mas_param = ParamNames_mas[i] + ', ' + Descriptions_mas[i]+ ', ' + Types_mas[i]+', ' + Units_mas[i]+', ' + RangeFrom_mas[i]+', ' + RangeTo_mas[i]+', ' + Weights_mas[i]
  mas_param_spl = mas_param.split(', ')
  Buf=', '.join('?' for s in mas_param_spl)
  # flash(mas_param)
  db.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(DescriptionBPName, StrDescNames, Buf), mas_param_spl)
 db.commit()
 return
def CopyDataToBP(BPName, TextFile, TabInfo, LOL): #если данные в таблице взяли из файла
 TextStr=TextFile.readlines()
 StrNames=''
 db=get_db()

 if (request.form.get('IdInFile')=='on'):
  StrNames=','.join(Str[1] for Str in TabInfo)
 else:
  StrNames=','.join(Str[1] for Str in TabInfo[1:]) #начиная с 1 элемента
 for Str in TextStr:
  StrParam= re.split("[,; ]+", Str)
  Buf=', '.join('?' for s in StrParam)
  # flash(StrParam)
  db.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(BPName, StrNames, Buf), StrParam)
  #list(filter(None, re.split("[,; ]+", Str))) #if there is no empty params
 db.commit()
 return 
##################################################################

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


@app.route('/GoMachLearn',  methods = ['GET', 'POST'])
def GoMachLearn():
 if request.form['Start']=='Старт!':
  return ExtractionAlgorithms() 
 elif request.form['Start']=='Оптимизировать':
  return DeleteSameParam()
 elif request.form['Start']=='Подобрать!':
  return PickingNeibCount()
  
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
 
def ExtractionAlgorithms():
 ExtractAlgol=request.form.get('ExtractionAlgorithm')

 if ExtractAlgol=='KNN':
  return KNNAlgorithmExtraction()
 else:
  pass
  
def KNNAlgorithmExtraction():
 db=get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 cur=db.execute('pragma table_info({0})'.format(BPName))
 TabInfo=cur.fetchall()
 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 cur=db.execute('SELECT * FROM {0}Description ORDER BY id ASC'.format(BPName))
 TabDescrData=cur.fetchall()
 
 if request.form.get('WeightOn')=='on':
  Weight=[Str[7] for Str in TabDescrData]
 else:
  Weight=[1 for Str in TabDescrData]
  
 #flash(Weight)
 ColNames=[s[1] for count, s in enumerate(TabInfo) if count>0]
 TSField=request.form.getlist('TSField')
 TSData=DataExecute(TSField, BPName, ColNames)
 RowsNumber, ColNumber=int(request.form['RowsNumber'], 10), int(request.form['ColNumber'], 10)
 NeibCount=int(request.form['NeibCount'], 10)
 Metric=request.form.get('Metric')
  
 if RowsNumber!=0:
  COData, COField=SelectDataExecute(RowsNumber, ColNumber)
  AnswerList, MinDistList, YMinDistList, MaxNeibList=KNNAlgorithm(TSData, COData, NeibCount, Metric, Weight)
  #COData=zip(COField, COData, AnswerList, MaxNeibList)
  #NumPar=4
  return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo,
  COData=zip(COField, COData, AnswerList, MaxNeibList), NeibCount=NeibCount, NumPar=4, BPName=BPName)
 else:
  COField=request.form.getlist('COField')
  COData=DataExecute(COField, BPName, ColNames)
  RealAnswerList=DataExecute(COField, BPName, [ColNames[len(ColNames)-1]])
  AnswerList, MinDistList, YMinDistList, MaxNeibList=KNNAlgorithm(TSData, COData, NeibCount, Metric, Weight)
  CountCorAns=0
  for i, j in zip(RealAnswerList, AnswerList):
   if i[0]==j:
    CountCorAns+=1
  Accuracy=round((CountCorAns/len(AnswerList))*100, 2)

  return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo,
  COData=zip(COField, COData, RealAnswerList, AnswerList, MaxNeibList), NeibCount=NeibCount, 
  Accuracy=Accuracy, NumPar=5, BPName=BPName)

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
 
@app.route('/logout')
def logout():
 session.pop('logged_in', None)
 flash('You were logged out')
 return redirect(url_for('show_entries'))

def ImprovingEfficiency():
 Method=request.form.get('ImpEffAlgorithm')
 db=get_db()
 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 cur=db.execute('SELECT * FROM {0}Description ORDER BY id ASC'.format(BPName))
 TabDescrData=cur.fetchall()
 #if request.form.get('WeightOn')=='on':
 Weight=[Str[7] for Str in TabDescrData]
 #else:
  #Weight=[1 for Str in TabDescrData]

 if Method=='KMeans':
  ClusterCount=int(request.form['ClusterCount'], 10)
  Metric=request.form.get('Metric')
  PrimCent=request.form.get('PrimaryCenter')
  Id, mu=KMeans(TabData, ClusterCount, Metric, Weight, PrimCent)

 elif Method=='Classification':
  Similarity1=float(request.form['Similarity'])
  Metric=request.form.get('Metric')
  Id=Classification(TabData, Metric, Weight, Similarity1)

 elif Method=='TimurAlgorithm':
  Id=TimurAlgorithm(TabData)
 
 if len(Id)==0:
  db.execute('DELETE FROM {0}'.format(BPName))
 else:
  Buf=', '.join('?' for id in Id)
  db.execute('DELETE FROM {0} WHERE id NOT IN ({1})'.format(BPName, Buf), Id)
 
def CrossValidation(NeibCount):
 db=get_db()
 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 Method=request.form.get('CrossValidation')
 Metric=request.form.get('CVMetric')
 cur=db.execute('SELECT * FROM {0}Description ORDER BY id ASC'.format(BPName))
 TabDescrData=cur.fetchall()
 
 if request.form.get('WeightOn')=='on':
  Weight=[Str[7] for Str in TabDescrData]
 else:
  Weight=[1 for Str in TabDescrData] 
 Acc=0
 
 if Method=='KFoldCV':
  BlockCount=int(request.form['BlockCount'], 10)
  Acc=KFoldCV(TabData, BlockCount, NeibCount, Metric, Weight)
  
 elif Method=='HoldOutCV':
  PercentTS=int(request.form['PercentTS'], 10)
  IterationCount=int(request.form['IterationCount'], 10)
  Acc=HoldOutCV(TabData, PercentTS, IterationCount, NeibCount, Metric, Weight)
  
 elif Method=='LOOCV':
  Acc=KFoldCV(TabData, len(TabData), NeibCount, Metric, Weight)

 return Acc
 
def PickingNeibCount(): 
 db=get_db()
 cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 TabList=cur.fetchall()
 cur=db.execute('pragma table_info({0})'.format(BPName))
 TabInfo=cur.fetchall()
 cur=db.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 MaxAcc, MaxNeibCount=-1, 0
 TabData=Shuffle(TabData)
 TabData=Shuffle(TabData)
 TabData=Shuffle(TabData)
 a, b=1, 18
 AccList=[a,b]
 
 for NeibCount in range (a, b):
  Acc=CrossValidation(NeibCount)
  #flash('Accuracy: {0}   Count: {1}'.format(Acc, NeibCount))
  AccList.append(Acc)
  if Acc>=MaxAcc:
   MaxAcc=Acc
   MaxNeibCount=NeibCount
 
 #flash(MaxNeibCount)
 #flash(MaxAcc)
 return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo, BPName=BPName, AccList=AccList, MaxAcc=MaxAcc, MaxNeibCount=MaxNeibCount)