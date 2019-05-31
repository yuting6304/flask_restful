import os
import json
from flask import Flask, request
from flask_restful import Resource
from test import decode_qrcode
from posttest import getPrizeNum
from db import setData, checkData, getData, getDataBar, getDatabarID
from prize import show_prize 


class Index (Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

class codeDetail (Resource):
    def get(self):
        id = str(request.args.get('id'))
        detail = getDatabarID(id)
        return detail

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

class monthCode (Resource):
    def get(self):
        date = request.args.get('date')
        monthCode = getData(date)
        return monthCode

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

# use getPrizeNum(year, month) from posttest.py
class Detail (Resource):

    def get(self):
        year = int(request.args.get('year'))
        month = int(request.args.get('month'))
        receipt_prizenum = getPrizeNum(year, month)
        receipt_prizenum_json = json.loads(receipt_prizenum)
        return {
            'msg' : receipt_prizenum_json
        }
    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass



class QRcode (Resource):
    def get(self):
        pass

    def post(self):
        
        file = request.files['image']
        if file.filename == '':
            print('no image')
            return {
                'msg' : 'no data'
            }
        else:
            filename = 'image.jpg'
            file.save(filename)
            data = decode_qrcode(filename)
            
            if os.path.exists(filename):
                os.remove(filename)
                print('remove img already')
                # insert into database

            # print(data['invPeriod'])
            prize_num = str(data['invNum'][2:])
            year = int(data['invPeriod'][0:3])
            month = int(data['invPeriod'][3:])
            receipt_prizenum = getPrizeNum(year, month)
            receipt_prizenum_json = json.loads(receipt_prizenum)
            
            win, money = show_prize(prize_num, receipt_prizenum_json)
            # print(data['invNum'][2:])
            if(checkData('bar_code', data['invNum'][2:]) == -1):
            
                addsql = 'bar_code(period, bar_code, win, money)'
                addsqlparams = "VALUES ('%s', '%s', '%s', '%s');" % (data['invPeriod'], data['invNum'][2:] , win, money)
                setData(addsql, addsqlparams)
                id = getDataBar(data['invNum'][2:])
                print(id[0][0])
                addsql = 'receipt_group(group_name, item, price, number, barID)'
                addsqlparams = "VALUES ('%s', '%s', '%s', '%s', '%s');" % ('食物', data['details'][0]['description'], data['details'][0]['unitPrice'], data['details'][0]['quantity'], id[0][0])
                # addsqlparams = 'VALUES ("食物", "8888888888", "1", 2000)'
                setData(addsql, addsqlparams)

                print('insert data into database')
                
            else:
                print('bar_code exist!')

            return {
                'msg' : data
            }, 200

    def put(self):
        pass

    def delete(self):
        pass


class Prize (Resource):
    def get(self):
        pass

    def post(self):
        year = request.args.get('year')
        month = request.args.get('month')
        data = getPrizeNum(int(year), int(month))
        print(data)
        return {
            'msg' : data
        }, 200

    def put(self):
        pass

    def delete(self):
        pass
