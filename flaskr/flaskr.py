import os, io, math, re, random
import Vectorization
import urllib.request
import json
import cgi
import tempfile

from flask import Flask, request, session, g, escape, redirect, url_for, abort, render_template, flash, make_response, send_file
from werkzeug.utils import secure_filename
from Metrics import MetricL1, MetricEuclid, MetricChebyshev
from ImprovingEfficiencyAlgorithms import KMeans2, Classification2, TimurAlgorithm2
from ExtractionAlgorithms import KNNAlgorithm
from CrossValidation import KFoldCV, HoldOutCV, Shuffle
from flaskext.mysql import MySQL
#from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_sslify import SSLify
#from flask.ext.session import Session
#from flask_login import current_user, login_user
#from app.models import User


DEBUG = True
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'LabSCT'
app.config['MYSQL_DATABASE_PASSWORD'] = 'RomanProveril1'
app.config['MYSQL_DATABASE_DB'] = 'LabSCT$table_storage'
app.config['MYSQL_DATABASE_HOST'] = 'LabSCT.mysql.pythonanywhere-services.com'
app.config['SECRET_KEY']='development key'
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.debug = True
mysql = MySQL(app)
mysql.init_app(app)
sslify = SSLify(app)

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

global BPName
global TabData
global TabInfo

TabListGl=[]
TabInfo, TabData=[], []

def get_db():
 if not hasattr(g, 'conn'):
  g.conn = connect_db()
 return g.conn



def connect_db():
 conn = mysql.connect()
 return conn

@app.teardown_appcontext
def close_db(error):
 if hasattr(g, 'conn'):
  g.conn.close()

if __name__ == '__main__':
 app.run()


def init_db(SchName): #!!!!!!!!!!!
 with app.app_context():
  db = get_db()
  with app.open_resource(SchName, mode='r') as f:
   db.cursor().executescript(f.read())
  db.commit()

class ServerError(Exception):pass
@app.route('/login', methods=['GET', 'POST'])
def login():
 return render_template('login.html')
@app.route('/loginRequest', methods=['POST'])
def loginRequest():
 conn=get_db()
 cur = conn.cursor()
 user_name = request.values.get('login')
 user_pass = request.values.get('pass')
 secret_word = request.values.get('secretWord')
 print(len(secret_word))
 if 'username' in session:
  return redirect(url_for('MainPage'))
 try:
  cur.execute('SELECT COUNT(1) FROM users WHERE user_name = \'{}\';'.format(user_name))
  if not cur.fetchone()[0]:
   abort(404)
  if len(secret_word) == 0:
   cur.execute('SELECT user_pass FROM users WHERE user_name = \'{}\' limit 1;'.format(user_name))
   print('golubi letyat2')
   hash_pass = cur.fetchone()[0]
   print(hash_pass)
   user_pass_b = user_pass.encode('utf-8')
   if md5(user_pass_b).hexdigest() == hash_pass:
    #session['logged_in'] = True
    session['username'] = user_name
    return redirect(url_for('MainPage'))
   abort(404)
  else:
   cur.execute('SELECT user_secret_word FROM users WHERE user_name = \'{}\' limit 1;'.format(user_name))
   secret_word_from_query = cur.fetchall()[0]
   if secret_word_from_query == secret_word:
    session['username'] = user_name
    #session['logged_in'] = True
    return redirect(url_for('MainPage'))
   abort(404)
 except:
  abort(404)
 return 'OK'

@app.route('/registration', methods=['POST'])
def registration():
 conn=get_db()
 cur = conn.cursor()
 user_name = request.values.get('login')
 user_pass = request.values.get('pass')
 secret_word = request.values.get('secretWord')
 try:
  if len(user_name) > 32:
   abort(404)
  cur.execute("SELECT COUNT(1) FROM users WHERE user_name = \'{}\';".format(user_name))

  if cur.fetchone()[0]:
   #raise ServerError('Имя пользователя уже занято')
   abort(404)
  user_pass_b = user_pass.encode('utf-8') # perevodim v bayts
  password_form_hash = md5(user_pass_b).hexdigest()
  print(password_form_hash)
  print('INSERT INTO users SET user_name = \'{0}\', user_pass = \'{1}\', user_rights = \'user\', user_secret_word=\'{2}\';'.format(user_name,password_form_hash,secret_word))
  cur.execute('INSERT INTO users SET user_name = \'{0}\', user_pass = \'{1}\', user_rights = \'user\', user_secret_word=\'{2}\';'.format(user_name,password_form_hash,secret_word))
  conn.commit()
  return redirect(url_for('login'))
 except:
  abort(404)
 return 'OK'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('MainPage'))


@app.route('/ExpHandLoad', methods=['GET', 'POST'])
def ExpHandLoad():
 if 'username' not in session:
  return redirect(url_for('login'))
 return render_template('ExpHandLoad.html')


@app.route('/MachLearn', methods=['GET', 'POST'])
def MachLearn():
 if 'username' not in session:
  return redirect(url_for('login'))
 conn=get_db()
 cur = conn.cursor()
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='LabSCT$table_storage'\
				                             and table_name NOT LIKE '%Description' and table_name NOT LIKE 'users'")
 TabList=cur.fetchall()
 return render_template('MachLearn.html', TabList=TabList)


#Upload Files---------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def MainPage():
 if 'username' not in session:
  return redirect(url_for('login'))
 username_session = escape(session['username']).capitalize()
 return render_template('MainPage.html', session_user_name=username_session)

#новая для представления
#@app.route('/')
#def MainPage():
# return render_template('MainPage.html')

#переделал
@app.route('/LookBP',  methods = ['GET', 'POST'])
def LookBP():
 if 'username' not in session:
  return redirect(url_for('login'))
 conn = get_db()
 cur = conn.cursor()
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='LabSCT$table_storage' and table_name NOT LIKE '%Description' and table_name NOT LIKE 'users'")
 TabList=[Tab[0] for Tab in cur.fetchall()]
 return render_template('LookBP.html', TabList=TabList)

 #переделал
@app.route('/EditBP',  methods = ['GET', 'POST'])
def EditBP():
 if 'username' not in session:
  return redirect(url_for('login'))
 conn = get_db()
 cur = conn.cursor()
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='LabSCT$table_storage'\
				                             and table_name NOT LIKE '%Description' and table_name NOT LIKE 'users'")
 TabList=[Tab[0] for Tab in cur.fetchall()]
 return render_template('EditBP.html', TabList=TabList)

# @app.route('/LookBP',  methods = ['GET', 'POST'])
# def LookBP():
 # db = get_db()
 # cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 # TabList=cur.fetchall()

 # buf=[row for row in TabList[0]]

 # flash(TabList)
 # return render_template('LookBP.html', TabList=TabList)
#----------------------------
 #edit

@app.route('/LookBPRequest',  methods = ['GET'])
def LookBPRequest():
 conn = get_db()
 cur = conn.cursor()
 BPName=request.args.get('TableChoice')
 Id=int(request.args.get('Id'), 10)
 if (Id==-1):
  cur.execute("SELECT COUNT(*) FROM {0}".format(BPName))
  TotalCount=cur.fetchone()[0]
  #print(TotalCount)
  to_json={'TotalCount':TotalCount}
 else:
  CountStr=int(request.args.get('CountStr'), 10)
  cur.execute("SELECT COUNT(*) FROM {0} WHERE id>={1} AND id<{2}".format(BPName, Id, (Id+CountStr)))
  CurCount=cur.fetchone()[0]
  cur.execute("SELECT * FROM {0} WHERE id>={1} AND id<{2}".format(BPName, Id, (Id+CountStr)))
  TabData=cur.fetchall()
  to_json={'Id':Id, 'CurCount':CurCount, 'TabData':TabData}
  if (Id==0):
   cur.execute('DESCRIBE {0}'.format(BPName))
   TabInfo=cur.fetchall()
   cur.execute('DESCRIBE {0}'.format(BPName+'Description'))
   DescrTabInfo=cur.fetchall()
   cur.execute("SELECT * FROM {0}".format(BPName+'Description'))
   DescrTabData=cur.fetchall()
   #print(DescrTabData)
   to_json={'Id':Id, 'CurCount':CurCount, 'TabData':TabData, 'TabInfo':TabInfo, 'DescrTabData':DescrTabData, 'DescrTabInfo':DescrTabInfo}
 return json.dumps(to_json)

@app.route('/DeleteBP',  methods = ['POST'])
def DeleteBP():
 conn = get_db()
 cur = conn.cursor()
 BPChoice=json.loads(request.values.get('BPChoice'))
 for BPName in BPChoice.values():
  cur.execute("DROP TABLE {0}".format(BPName))
  cur.execute("DROP TABLE {0}".format(BPName + 'Description'))

 conn.commit()
 return 'OK'
 #все редактирование ?
@app.route('/EditBPRequest',  methods = ['POST'])
def EditBPRequest():
 conn = get_db()
 cur = conn.cursor()
 BPName=request.values.get('TableChoice')
 cur.execute('DESCRIBE {0}'.format(BPName))
 TabInfo=cur.fetchall()
 buf_types= []
 #dlya strok
 for tabinf in TabInfo[1:]:
  buf_types.append(tabinf[1])
 Operation=request.values.get('Operation')

 if (Operation=='Delete'):
  Data=json.loads(request.values.get('JsonObj'))
  for Id in Data:
   cur.execute('DELETE FROM {0} WHERE id={1}'.format(BPName, Id))
  to_json={'Status': 'OK!'}
 elif Operation=='DeleteAll':
  cur.execute('DELETE FROM {0}'.format(BPName))
  to_json={'Status': 'OK!'}
 elif Operation=='Insert':
  CountStr=int(request.values.get('Count'), 10)
  RowId=[]
  for i in range(0, CountStr):
   cur.execute('INSERT INTO {0} () VALUES()'.format(BPName))
   cur.execute('SELECT last_insert_id()')
   RowId.append(cur.fetchone()[0])
  to_json={'LastInsertRowId': RowId}
 elif Operation=='Update':
  Data=json.loads(request.values.get('JsonObj'))
  cur.execute('UPDATE {0} SET {1}="{2}" WHERE id={3}'.format(BPName, Data['ColName'], Data['Value'], Data['Id']))
  to_json={'Status': 'OK!'}
 elif Operation=='RenameColumn':
  Data=json.loads(request.values.get('JsonObj'))
  #db.execute('ALTER TABLE {0} RENAME COLUMN {1} TO {2}'.format(BPName, Data['ColName'], Data['Value']))
  to_json={'Status': 'OK!'}
 elif Operation=='Load From File':
  file=request.files['ImportBPFile']
  LastId=-1
  cur.execute("SELECT COUNT(*) FROM {0}".format(BPName))
  TotalCountBeforeInsert=cur.fetchone()[0]
  for line in file:
   line=re.sub("[\n\r]", "", line.decode('UTF-8'))
   data=re.split("[(,\s)(;\s),;\s]", line)
   #Buf=','.join('?' for d in data)
   Buf=''
   for j,data_type in enumerate(data):
    if buf_types[j] == 'varchar(255)':
     Buf += '\'{}\', '.format(data_type)
    else:
     Buf += '{}, '.format(data_type)
   Buf = Buf[0:len(Buf)-2]
   #Buf=','.join(d for d in data)
   #cur.execute('INSERT INTO {0} VALUES(null, {1})'.format(BPName, Buf), data)
   #print(Buf)
   #print('INSERT INTO {0} VALUES(null, {1})'.format(BPName, Buf))
   cur.execute('INSERT INTO {0} VALUES(null, {1})'.format(BPName, Buf))
   if LastId==-1:
    #cur.execute("SELECT LAST_INSERT_ROWID()")
    cur.execute("SELECT last_insert_id()")
    LastId=cur.fetchone()[0]

  cur.execute("SELECT COUNT(*) FROM {0}".format(BPName))
  TotalCountAfterInsert=cur.fetchone()[0]
  #print(TotalCountBeforeInsert)
  #print(TotalCountAfterInsert)
  #print(LastId)
  to_json={'TCBI': TotalCountBeforeInsert, 'TCAI': TotalCountAfterInsert, 'LastId': LastId}

 conn.commit()
 return json.dumps(to_json)
# mysql +
@app.route('/ExportToFile',  methods = ['POST'])
def ExportToFile():
 conn = get_db()
 cur = conn.cursor()
 BPName=request.form['HiddenTableChoice']
 tfile=tempfile.TemporaryFile()
 FileName=BPName
 #print(request.form['ExportToFile'])

 if request.form['ExportToFile']=='Экспорт БП':
  cur.execute("SELECT COUNT(*) FROM {0}".format(BPName))
  TotalCount, Id, CountStr=cur.fetchone()[0], 1, 5000

  while (Id<=TotalCount):
   cur.execute("SELECT * FROM {0} WHERE id>={1} AND id<{2}".format(BPName, Id, (Id+CountStr)))
   TabData=cur.fetchall()

   for Str in TabData:
    buf=','.join(str(Col) for Col in Str)+'\n'
    tfile.write(buf.encode("utf-8"))

   Id+=CountStr

 elif request.form['ExportToFile']=='Экспорт тестовой выборки':
  TestSample=request.form['HiddenTestSample']
  cur.execute('SELECT * FROM {0} WHERE id IN ({1})'.format(BPName, TestSample))
  TabData=cur.fetchall()

  for Str in TabData:
   buf=','.join(str(Col) for Col in Str)+'\n'
   tfile.write(buf.encode("utf-8"))

  FileName+='TestSample'

 elif request.form['ExportToFile']=='Экспорт обучающей выборки':
  TestSample=request.form['HiddenTestSample']
  cur.execute("SELECT COUNT(*) FROM {0}".format(BPName))
  TotalCount, Id, CountStr=cur.fetchone()[0], 1, 5000

  while (Id<=TotalCount):
   cur.execute("SELECT * FROM {0} WHERE id>={1} AND id<{2} AND id NOT IN ({3})".format(BPName, Id, (Id+CountStr), TestSample))
   TabData=cur.fetchall()

   for Str in TabData:
    buf=','.join(str(Col) for Col in Str)+'\n'
    tfile.write(buf.encode("utf-8"))

   Id+=CountStr

  FileName+='TrainSample'

 tfile.seek(0)
 return send_file(tfile, attachment_filename="{0}.csv".format(FileName), as_attachment=True, mimetype='text/csv')

 # исправил майsql +
@app.route('/RenameBP',  methods = ['POST'])
def RenameBP():
 conn = get_db()
 cur = conn.cursor()
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='LabSCT$table_storage'\
				                             and table_name NOT LIKE '%Description' and table_name NOT LIKE 'users'")
 OldBPNames=[BP[0] for BP in cur.fetchall()]
 NewBPNames=json.loads(request.values.get('NewBPNames'))
 for OldBPName, key in zip(OldBPNames,  range(0, len(NewBPNames))):
  try:
   cur.execute('ALTER TABLE {0} RENAME TO {1}'.format(OldBPName, NewBPNames.get(str(key))))
   cur.execute('ALTER TABLE {0}Description RENAME TO {1}Description'.format(OldBPName, NewBPNames.get(str(key))))
  except mysql.OperationalError:
   pass

 return 'OK'

 #----------------------------------------------------

@app.route('/LookBP1',  methods = ['GET', 'POST'])
def ExecDataFromTable(): #показать содержимое таблички
 BPName=request.form['TableChoice']
 flash('SELECT * FROM {0}'.format(BPName))
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

# @app.route('/EditBP',  methods = ['GET', 'POST'])
# def EditBP():
 # db = get_db()
 # cur=db.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
 # TabList=cur.fetchall()
 # return render_template('EditBP.html', TabList=TabList)

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
 conn = get_db()
 db = conn.cursor()
 global TabInfo
 global TabData

 if request.form['DataEdit']=='Записать столбец':
  NewColName=request.form['NewColName']
  NewColType=request.form['NewColType']
  db.execute('ALTER TABLE {0} ADD COLUMN {1} {2}'.format(BPName, NewColName, NewColType))
  db.commit()
  db.execute('DESCRIBE table_info({0})'.format(BPName))
  TabInfo=cur.fetchall()
  db.execute('SELECT * FROM {0}'.format(BPName))
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
  db.execute('DESCRIBE table_info({0})'.format(BPName))
  TabInfo=cur.fetchall()

  #Insert Strings In BP
  if len(AddStr)!=0:
   StrNames=','.join(s[1] for s in TabInfo if s[1]!='id')
   StrParam=','.join('null' for s in range(0, len(TabInfo)-1))

   #print(StrNames)
   #print(StrParam)
   for id in AddStr:
    #StrParam=str(id)+','+StrParam
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
  flash(len(TabData))
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
 conn = get_db()
 cur = conn.cursor()
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

 #print(StrNames)
  #Description_Str_Names = ', ' + request.form['ColName'+str(i)] + ' ' + request.form['ColType' + str(i)] + ' ' + request.form['ColWeights' +str(i)] + ' ' + request.form['RangeFrom' + str(i)] + ' ' + request.form['RangeTo' + str(i)] + ' ' + request.form['ColUnit' + str(i)]+ ' ' + request.form['DescriptionName' + str(i)]
 cur.execute('CREATE TABLE {0} (id integer primary key AUTO_INCREMENT{1})'.format(BPName, StrNames))
 cur.execute('CREATE TABLE {0} (id integer primary key AUTO_INCREMENT{1})'.format(DescriptionBPName, Description_Str_Names))
 cur.close()

 conn1 = get_db()
 cur_1 = conn1.cursor()
 conn2 = get_db()
 cur_2 = conn2.cursor()
 cur_1.execute('DESCRIBE {0}'.format(BPName))
 cur_2.execute('DESCRIBE {0}'.format(DescriptionBPName))
 TabInfo = cur_1.fetchall()
 DescriptionTabInfo = cur_2.fetchall()
 if request.form.get('BPFile')!='' and request.form.get('CopyDataToBP')=='on':
  TextFile=io.TextIOWrapper(request.files['BPFile'])
  CopyDataToBP(BPName, TextFile, TabInfo, request.files['BPFile'])
 #cur_2.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{0}'".format(DescriptionBPName)) #типы столбцов
 cur_2.execute("show columns from {0}".format(DescriptionBPName))
 descr_values = [Row[1] for Row in cur_2.fetchall()]
 print(descr_values)
 #print(COLUMN_NAME)
 #print(showtab)
# print("------------------------------------------------------")

 CopyDataToDescriptionTable(DescriptionBPName, StrDescNames, StrParamNames, StrDescriptions, StrTypes, StrUnits, StrRangeFrom, StrRangeTo, StrWeights, ColCount, descr_values)
 cur_1.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 cur_2.execute('SELECT * FROM {0} ORDER BY id ASC'.format(DescriptionBPName))
 TabData=cur_1.fetchall()
 TabDescrData = cur_2.fetchall()
 return render_template('DataWork.html', TabData=TabData, TabInfo=TabInfo, TabDescrData=TabDescrData, DescriptionTabInfo=DescriptionTabInfo) # TabDescrData=TabDescrData, DescriptionTabInfo=DescriptionTabInfo

def CopyDataToDescriptionTable(DescriptionBPName, StrDescNames ,StrParamNames, StrDescriptions, StrTypes, StrUnits, StrRangeFrom, StrRangeTo, StrWeights, ColCount, DescrTabInfTypes):
 #cur=get_db()
 conn=get_db()
 cur=conn.cursor()
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
  DescrTabInfTypesNew = DescrTabInfTypes[1:]
  print(DescrTabInfTypesNew)
  Buf=''
  #print(DescrTabInfTypesNew)
  #print(mas_param_spl)
  for j in range(0,len(mas_param_spl)-1):
   if DescrTabInfTypesNew[j] == 'text':
    Buf += "\'{}\', ".format(mas_param_spl[j])
   else:
    Buf += '{}, ' .format(mas_param_spl[j])
  Buf += mas_param_spl[len(mas_param_spl)-1]
  # flash(mas_param)
  print('INSERT INTO {0} ({1}) VALUES ({2})'.format(DescriptionBPName, StrDescNames, Buf))
  cur.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(DescriptionBPName, StrDescNames, Buf))
 #db.commit()
 conn.commit()
 return

def CopyDataToBP(BPName, TextFile, TabInfo, LOL): #если данные в таблице взяли из файла
 TextStr=TextFile.readlines()
 StrNames=''
 conn = get_db()
 db = conn.cursor()
 buf_types= []

 #dlya strok
 for tabinf in TabInfo[1:]:
  buf_types.append(tabinf[1])

 if (request.form.get('IdInFile')=='on'):
  StrNames=','.join(Str[0] for Str in TabInfo)
 else:
  StrNames=','.join(Str[0] for Str in TabInfo[1:]) #начиная с 1 элемента
 for Str in TextStr:
 #for i,Str in enumerate(TextStr):
  StrParam= re.split("[,; ]+", Str)
  #Buf=', '.join('?' for s in StrParam)
  Buf=''
  for j,str_type in enumerate(StrParam):
   if buf_types[j] == 'varchar(255)':
    Buf += '\'{}\', '.format(str_type)
   else:
    Buf += '{}, '.format(str_type)
  Buf = Buf[0:len(Buf)-2]
  #Buf=', '.join(s for s in StrParam)
  #print(Buf)
  #print('INSERT INTO {0} ({1}) VALUES ({2})'.format(BPName, StrNames, Buf))
  db.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(BPName, StrNames, Buf))
  #list(filter(None, re.split("[,; ]+", Str))) #if there is no empty params
 conn.commit()
 return
##################################################################

@app.route('/ShowTab',  methods = ['GET', 'POST'])
def ShowTab():
 conn=get_db()
 cur = conn.cursor()
 global BPName
 BPName=request.form['TabList']
 cur.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 #print(TabData)
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='table_storage'\
				                             and table_name NOT LIKE '%Description' and table_name NOT LIKE 'users'")
 TabList=cur.fetchall()
 cur.execute('DESCRIBE {0}'.format(BPName)) #поправить
 TabInfo=cur.fetchall()
 #print(TabInfo)
 return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo, BPName=BPName)

'''
def DataExecute(IdList, BPName, ColNames):
 db=get_db()
 DataList=Buf1=[]
 Buf1.extend(IdList)
 Buf2=', '.join(s for s in ColNames) #There must be '?'
 Buf3=', '.join('?' for s in IdList)

 cur=db.execute('SELECT {0} FROM ({1}) WHERE id in ({2})'.format(Buf2, BPName, Buf3), Buf1)
 DataList=cur.fetchall()
 return DataList


'''
def SelectDataExecute(RowsNumber, ColNumber):
 COData = [[0]*(ColNumber-1) for i in range(RowsNumber)]
 COField=request.form.getlist('SelForCol0')

 for i in range(1, ColNumber):
  Column=request.form.getlist('SelForCol'+str(i))
  for count, j in enumerate(Column):
   COData[count][i-1]=j

 return COData, COField

def DataExecute(IdList, BPName, ColNames):
 conn = get_db()
 cur = conn.cursor()
 DataList, Buf1=[], []
 Buf1.extend(IdList)
 GG=200

 if len(IdList)>GG:
  count, nex=0, 0
  Buf2=', '.join(s for s in ColNames) #There must be '?'
  while count<len(IdList):
   if (len(IdList)-count)>=GG:
    nex=GG
   else:
    nex=len(IdList)-count

   Buf3=[]
   #Buf3=', '.join('?' for i in range(0, nex)) edit by Ser
   Buf3=', '.join(IdList[i] for i in range(count, count+nex))
   #print(Buf3)
   #cur.execute('SELECT {0} FROM ({1}) WHERE id in ({2})'.format(Buf2, BPName, Buf3), IdList[count:count+nex])
   cur.execute('SELECT {0} FROM ({1}) WHERE id in ({2})'.format(Buf2, BPName, Buf3))
   DataList.extend(cur.fetchall())

   count+=nex
 else:
  Buf2=', '.join(s for s in ColNames) #There must be '?'
  #Buf3=', '.join('?' for s in IdList)
  Buf3 =  ', '.join(s for s in IdList)
  #cur.execute('SELECT {0} FROM ({1}) WHERE id in ({2})'.format(Buf2, BPName, Buf3), Buf1)
  cur.execute('SELECT {0} FROM ({1}) WHERE id in ({2})'.format(Buf2, BPName, Buf3))
  DataList=cur.fetchall()

 return DataList


@app.route('/GoMachLearn',  methods = ['GET', 'POST'])
def GoMachLearn():
 if request.form['Start']=='Начать классификацию':
  return ExtractionAlgorithms()
 elif request.form['Start']=='Оптимизировать':
  return DeleteSameParam()
 elif request.form['Start']=='Начать кросс-валидацию':
  return PickingNeibCount()

@app.route('/OptimizeData',  methods = ['GET', 'POST'])
def OptimizeData():
 conn = get_db()
 cur = conn.cursor()

 if request.form['Optimize']=='Оптимизировать':
  RepIdList=DeleteSameParam()
  RepDataList=[]

  for RepId in RepIdList:
   cur.execute('SELECT * FROM {0} WHERE id={1} ORDER BY id ASC'.format(BPName, RepId))
   RepDataList.append(list(cur.fetchone()))

 elif request.form['Optimize']=='Удалить':
  RepSelect=request.form.getlist('RepSelect')
  RepDataList=[]

  for RepId in RepSelect:
   cur.execute('DELETE FROM {0} WHERE id={1}'.format(BPName, RepId))

 cur.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='LabSCT$table_storage'")
 TabList=cur.fetchall()
 cur.execute('DESCRIBE {0}'.format(BPName))
 TabInfo=cur.fetchall()
 return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo, RepDataList=RepDataList, BPName=BPName)

def ExtractionAlgorithms():
 ExtractAlgol=request.form.get('ExtractionAlgorithm')

 if ExtractAlgol=='KNN':
  return KNNAlgorithmExtraction()
 else:
  pass

def KNNAlgorithmExtraction():
 conn=get_db()
 cur = conn.cursor()
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='LabSCT$table_storage'\
				                             and table_name NOT LIKE '%Description'  and table_name NOT LIKE 'users'")
 TabList=cur.fetchall()
 cur.execute('DESCRIBE {0}'.format(BPName))
 TabInfo=cur.fetchall()
 cur.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 cur.execute('SELECT * FROM {0}Description ORDER BY id ASC'.format(BPName))
 TabDescrData=cur.fetchall()

 if request.form.get('WeightOn')=='on':
  Weight=[Str[7] for Str in TabDescrData]
 else:
  Weight=[1 for Str in TabDescrData]

 #flash(Weight)
 ColNames=[s[0] for count, s in enumerate(TabInfo) if count>0]
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
 conn = get_db()
 cur = conn.cursor()
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='LabSCT$table_storage'\
				                             and table_name NOT LIKE '%Description'  and table_name NOT LIKE 'users'")
 TabList=cur.fetchall()
 cur.execute('DESCRIBE {0}'.format(BPName))
 TabInfo=cur.fetchall()
 ColNames=[s[0] for count, s in enumerate(TabInfo) if count>0]

 RowsNumber=int(request.form['RowsNumber'], 10)
 ColNumber=int(request.form['ColNumber'], 10)-1

 COData, COField=SelectDataExecute(RowsNumber, ColNumber)
 ColNamesStr=', '.join(s for s in ColNames)#NU TAKOE

 for str in COData:
  ParamStr=', '.join('"{0}"'.format(s) for s in str)
  cur.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(BPName, ColNamesStr, ParamStr))

 conn.commit()
 cur.execute('SELECT * FROM '+BPName+' ORDER BY id ASC')
 TabData=cur.fetchall()

 return render_template('MachLearn.html', TabData=TabData, TabList=TabList, TabInfo=TabInfo, BPName=BPName)

#@app.route('/DeleteSameParam',  methods = ['GET', 'POST'])
def DeleteSameParam():#RAZOBRATSA/ TODAY NEOHOTO
 conn = get_db()
 cur = conn.cursor()
 cur.execute('DESCRIBE {0}'.format(BPName))
 TabInfo=cur.fetchall()

 cur.execute('SELECT * FROM '+BPName+' ORDER BY id ASC')
 RepIdList=[]

 for RowData in cur:
  RowDataLen=len(RowData)
  CondList=[str(i[1]) + '=' + str(j) for i, j in zip(TabInfo, RowData)]
  CondStr=' AND '.join(s for count, s in enumerate(CondList) if count>0 and count<RowDataLen-1)

  cur2 = conn.cursor()
  cur2.execute('SELECT * FROM {0} WHERE {1}'.format(BPName, CondStr))
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

# @app.route('/logout')
# def logout():
 # session.pop('logged_in', None)
 # flash('You were logged out')
 # return redirect(url_for('show_entries'))

@app.route('/OptimizationBP',  methods = ['POST'])
def OptimizationBP():
 conn = get_db()
 cur = conn.cursor()
 BPName=request.values.get('TableChoice')
 OptArr=json.loads(request.values.get('JsonObj'))
 #print(BPName)
 cur.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 cur.execute('SELECT * FROM {0}Description ORDER BY id ASC'.format(BPName))
 DescrTabData=cur.fetchall()
 Weight=[Str[7] for Str in DescrTabData]

 if OptArr['OptAlgol']=='Classification':
  OptTabData=Classification2(TabData[:], OptArr['ClassMetric'], Weight, float(OptArr['ClassSimilarity']))
 elif OptArr['OptAlgol']=='KMeans':
  OptTabData=KMeans2(TabData, int(OptArr['KMClusterCount'], 10), OptArr['KMMetric'], Weight, OptArr['KMPrimaryCenter'])
 elif OptArr['OptAlgol']=='TimurAlgorithm':
  OptTabData=TimurAlgorithm2(TabData[:])
 '''
 if len(OptTabData)!=0:
  for Str in TabData:
   if (len(OptTabData)==0 or Str[0]!=OptTabData[0][0]):
    db.execute('DELETE FROM {0} WHERE id={1}'.format(BPName, Str[0]))
   else:
    OptTabData.pop(0)
 '''

 if len(OptTabData)!=0:
  #print(','.join(str(Str[0]) for Str in OptTabData))
  cur.execute('DELETE FROM {0} WHERE id NOT IN ({1})'.format(BPName, ','.join(str(Str[0]) for Str in OptTabData)))

 conn.commit()
 return 'Success'



def ImprovingEfficiency():
 Method=request.form.get('ImpEffAlgorithm')
 conn = get_db()
 cur = conn.cursor()
 cur.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 cur.execute('SELECT * FROM {0}Description ORDER BY id ASC'.format(BPName))
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
  cur.execute('DELETE FROM {0}'.format(BPName))
 else:
  IdDel, i=[], 0

  for Str in TabData:
   #flash('Str: {0}   Id: {1}'.format(Str[0], Id[i]))
   if (len(Id)!=0):
    if Str[0]!=Id[0]:
     IdDel.append(Str[0])
    else:
     Id.pop(0)
   else:
    IdDel.append(Str[0])

  DeleteFromBP(IdDel, BPName)
  #Buf=', '.join('?' for id in Id)
  #db.execute('DELETE FROM {0} WHERE id NOT IN ({1})'.format(BPName, Buf), Id)

def DeleteFromBP(IdList, BPName):
 conn = get_db()
 cur = conn.cursor()
 GG=200

 if len(IdList)>GG:
  count, nex=0, 0
  while count<len(IdList):
   if (len(IdList)-count)>=GG:
    nex=GG
   else:
    nex=len(IdList)-count

   Buf=[]
   Buf=', '.join('?' for i in range(0, nex))
   cur.execute('DELETE FROM {0} WHERE id IN ({1})'.format(BPName, Buf), IdList[count:count+nex])
   count+=nex
 else:
  Buf=', '.join('?' for s in IdList)
  cur.execute('DELETE FROM {0} WHERE id IN ({1})'.format(BPName, Buf), IdList)



def CrossValidation(NeibCount):
 conn = get_db()
 cur = conn.cursor()
 cur.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
 TabData=cur.fetchall()
 Method=request.form.get('CrossValidation')
 Metric=request.form.get('CVMetric')
 cur.execute('SELECT * FROM {0}Description ORDER BY id ASC'.format(BPName))
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
 conn = get_db()
 cur = conn.cursor()
 cur.execute("SELECT table_name FROM information_schema.tables where table_schema='LabSCT$table_storage'\
				                             and table_name NOT LIKE '%Description' and table_name NOT LIKE 'users'")
 TabList=cur.fetchall()
 cur.execute('DESCRIBE {0}'.format(BPName))
 TabInfo=cur.fetchall()
 cur.execute('SELECT * FROM {0} ORDER BY id ASC'.format(BPName))
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