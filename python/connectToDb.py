import pymysql
import pymongo


'''
  Connections to mySQL DB
'''

def cities():
  db = pymysql.connect(host='localhost', user='root', password='Ma1r3ad2015*%', db='world', cursorclass=pymysql.cursors.DictCursor)

  sql = """ select * from city limit 15 """

  with db:
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def population(compare,pop):      
  db = pymysql.connect(host='localhost', user='root', password='Ma1r3ad2015*%', db='world', cursorclass=pymysql.cursors.DictCursor)
  
  if (compare == '>'):
    sql = """ select * from city where population > %s """
  elif (compare == '<'):
    sql = """ select * from city where population < %s """
  elif (compare == '='):
    sql = """ select * from city where population = %s """

  with db:
    cursor = db.cursor()
    cursor.execute(sql,(pop))
    return cursor.fetchall()

def addCity(newCityName,countryCode,district,population):
  db = pymysql.connect(host='localhost', user='root', password='Ma1r3ad2015*%', db='world', cursorclass=pymysql.cursors.DictCursor)

  sql = "INSERT INTO city (Name,CountryCode,District,Population) VALUES (%s, %s, %s, %s)"

  with db:
    try:
      cursor = db.cursor()
      cursor.execute(sql,(newCityName,countryCode,district,population))
      db.commit()
    except pymysql.err.IntegrityError as e: 
      print('***ERROR***: Countrycode {} does not exist'.format(countryCode))
    except pymysql.err.InternalError as e:
      print(e)
    except Exception as e:
      print(e)

def countryNames(countryName):
  db = pymysql.connect(host='localhost', user='root', password='Ma1r3ad2015*%', db='world', cursorclass=pymysql.cursors.DictCursor)

  sql = """ select * from country where name like %s """

  with db:
    cursor = db.cursor()
    cursor.execute(sql,('%'+countryName+'%'))
    return cursor.fetchall()

def countryPopulations(compare,pop):
  db = pymysql.connect(host='localhost', user='root', password='Ma1r3ad2015*%', db='world', cursorclass=pymysql.cursors.DictCursor)
  
  if (compare == '>'):
    sql = """ select * from country where population > %s """
  elif (compare == '<'):
    sql = """ select * from country where population < %s """
  elif (compare == '='):
    sql = """ select * from country where population = %s """

  with db:
    cursor = db.cursor()
    cursor.execute(sql,(pop))
    return cursor.fetchall()


'''
  Connections to MongoDB
'''

myclient = None
def createConnection():
  global myclient
  myclient = pymongo.MongoClient(host='localhost', port=27017)
  myclient.admin.command('ismaster')

def connectMongo(): 
  if(not myclient):
    try:
      createConnection()  
    except Exception as e:
      print('Error - could not connect - ', e)

def engineSize(size):
  connectMongo()
  #print('input ',type(size))
  mongoDb = myclient['dbfinalproject']
  collection = mongoDb['docs']
  query = {"car.engineSize": size}
  documents = collection.find(filter=query)
  return documents
  
def addCar(carId,regNumber,engineSize2):
  connectMongo()
  #print('carId ',type(carId))
  #print('regNumber ',type(regNumber))
  #print('engineSize2 ',type(engineSize2))
  print(carId,regNumber,engineSize2)
  mongoDb = myclient['dbfinalproject']
  collection = mongoDb['docs']
  query = {"car": {"engineSize": engineSize2, "reg": regNumber}, "_id":carId}
  collection.insert_one(query)

