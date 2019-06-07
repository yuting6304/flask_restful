import MySQLdb
from warnings import filterwarnings

def dbConnection():
    db = MySQLdb.connect(host="localhost", user="pl", password="123", db="receipt", charset="utf8")
    return db

def dbInit():
    filterwarnings('ignore', category = MySQLdb.Warning)

    db = dbConnection()
    cursor = db.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS bar_code(id INT NOT NULL AUTO_INCREMENT, date CHAR(10) NOT NULL , period CHAR(10) NOT NULL ,prefix_barcode CHAR(2) NOT NULL, bar_code CHAR(20) NOT NULL, win CHAR(10) NOT NULL, money char(20) NOT NULL, PRIMARY KEY(id)) DEFAULT CHARSET=utf8")
    cursor.execute("CREATE TABLE IF NOT EXISTS tranditional_code(id INT NOT NULL AUTO_INCREMENT, period CHAR(10) NOT NULL , bar_code CHAR(20) NOT NULL, win CHAR(10) NOT NULL, money char(20) NOT NULL, PRIMARY KEY(id)) DEFAULT CHARSET=utf8")
    cursor.execute("CREATE TABLE IF NOT EXISTS Mtranditional_code(id INT NOT NULL AUTO_INCREMENT, period CHAR(10) NOT NULL , bar_code CHAR(20) NOT NULL, win CHAR(10) NOT NULL, money char(20) NOT NULL, PRIMARY KEY(id)) DEFAULT CHARSET=utf8")    
    cursor.execute("CREATE TABLE IF NOT EXISTS receipt_group(id INT NOT NULL AUTO_INCREMENT, group_name CHAR(30) NOT NULL, item CHAR(30) NOT NULL, price CHAR(30) NOT NULL, number CHAR(30) NOT NULL, PRIMARY KEY(id), barID CHAR(30) NOT NULL) DEFAULT CHARSET=utf8")

    db.close()
    print('[MySQL]: Table had been created')


def checkData(table_name, target):
    find_target = 0
    db = dbConnection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM " + table_name)
    result = cursor.fetchall()

    for record in result:
        if str(target) in str(record):
            # print(record)
            find_target = 1
            break
    
    db.close()

    if(find_target == 1):
        return 1
    else:
        return -1

def setData(addsql, addsqlparams):
    # example : 
    # addsql = bar_code(bar_code, win, money)
    # addsqlparams = VALUES ("8888888888", "1", 2000)


    db = dbConnection()
    cursor = db.cursor()

    cursor.execute('INSERT INTO ' + addsql + ' ' + addsqlparams + ';')

    db.commit()
    db.close()

def deleteData(table_name, option):
    # example : 
    # table_name = bar_code
    # option = bar_code = "8888888888"

    db = dbConnection()
    cursor = db.cursor()

    cursor.execute('DELETE FROM ' + table_name + ' WHERE ')
    db.commit()
    db.close()

def updateData(table_name, addsqlparams):
    db = dbConnection()
    cursor = db.cursor()

    cursor.execute('UPDATE ' + table_name + ' SET ' + addsqlparams)
    db.commit()
    db.close()


def getData (table_name, date) :
    db = dbConnection ()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM " + table_name + " WHERE period = " + date)
    result = cursor.fetchall()
    db.close()
    return result

def getDataBar (bar_code) :
    db = dbConnection ()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM bar_code WHERE bar_code = " + bar_code)
    result = cursor.fetchall()
    db.close()
    # print(result)
    return result

def getDatabarID (id) :
    db = dbConnection ()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM receipt_group WHERE barID=" + id)
    result = cursor.fetchall()
    db.close()
    # print(result)
    return result
