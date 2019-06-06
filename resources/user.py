import os
import json
from flask import Flask, request, render_template
from flask_restful import Resource
from test import decode_qrcode
from posttest import getPrizeNum
from db import setData, checkData, getData, getDataBar, getDatabarID
from prize import show_prize
import time

class Index (Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

class Tranditionalcode (Resource):
    def get(self):
        pass

    def post(self):
        year = request.args.get('year')
        month = request.args.get('month')
        code = request.args.get('code')

        YM = str(year) + str(month)

        receipt_prizenum = getPrizeNum(int(year), int(month))
        receipt_prizenum_json = json.loads(receipt_prizenum)
        if(receipt_prizenum_json['msg'] != '無此期別資料'):
            win, money = show_prize(str(code), receipt_prizenum_json)
        else:
            win = -1
            money = 0

        if(checkData('tranditional_code', code) == -1):
            addsql = 'tranditional_code(period, bar_code, win, money)'
            addsqlparams = "VALUES ('%s', '%s', '%s', '%s');" % (YM, code, win, money)
            setData(addsql, addsqlparams)
            print('insert data into database')
        else:
            print('bar_code exist!')

        return code

    def put(self):
        pass

    def delete(self):
        pass

class codeDetail (Resource):
    def get(self):
        id = str(request.args.get('id'))
        detail = getDatabarID(id)
        detail_json = json.dumps(detail)
        detail_json = json.loads(detail_json)
        return detail_json

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

class monthCode (Resource):
    def get(self):
        year = request.args.get('year')
        month = request.args.get('month')
        YM = year+month
        monthCode = getData("bar_code", YM)
        
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
        # print(receipt_prizenum[1])
        receipt_prizenum_json = json.loads(receipt_prizenum)
        # print(receipt_prizenum_json['msg'])

        return receipt_prizenum_json

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
            
            if(data == -1):
                print('decode fail')
                return {
                    'msg' : 'no data'
                }, 200
            
            # if os.path.exists(filename):
            #     os.remove(filename)
                # print('remove img already')
                # insert into database
            # print(data['invDate'])
            # print(data['invPeriod'])
            year = int(data['invPeriod'][0:3])
            month = int(data['invPeriod'][3:])

            receipt_prizenum = getPrizeNum(year, month)
            receipt_prizenum_json = json.loads(receipt_prizenum)
            
            if(receipt_prizenum_json['msg'] != '無此期別資料'):
                win, money = show_prize(str(data['invNum'][2:]), receipt_prizenum_json)
            else:
                win = -1
                money = 0

            # if it is already in database
            # print(data['invNum'][2:])
            # print(len(data['details']))
            if(checkData('bar_code', data['invNum'][2:]) == -1):
            
                addsql = 'bar_code(date, period, prefix_barcode, bar_code, win, money)'
                addsqlparams = "VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (data['invDate'], data['invPeriod'], data['invNum'][0:2], data['invNum'][2:] , win, money)
                setData(addsql, addsqlparams)

                id = getDataBar(data['invNum'][2:])
                # print(id[0][0])
            
                for it in data['details']:
                    addsql = 'receipt_group(group_name, item, price, number, barID)'
                    addsqlparams = "VALUES ('%s', '%s', '%s', '%s', '%s');" % ('食物', it['description'], it['unitPrice'], it['quantity'], id[0][0])
                    # addsqlparams = 'VALUES ("食物", "8888888888", "1", 2000)'
                    setData(addsql, addsqlparams)

                print('insert data into database')
                
            else:
                print('bar_code exist!')

            # print(data)
            return data

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
        data_json = json.loads(data)
        print(data_json)
        return data_json

    def put(self):
        pass

    def delete(self):
        pass

class ItemDetail (Resource):

    def get(self):
        year = request.args.get('year')
        month = request.args.get('month')
        YM = year+month
        item = getData("bar_code", YM)
        tranditional_item = getData("tranditional_code", YM)
        result = []
        result_qr = []
        result_tr = []
        # print(item)
        if(len(item) > 0):
            for it in item:
                describe = getDatabarID(str(it[0]))
                D = {}
                describe_list = []
                describe_dict = {}
                D["Date"] = str(it[1][0:4]) + "/" + str(it[1][4:6]) + "/" + str(it[1][6:8])
                D["Number"] = str(it[3]) + str(it[4])
                D["Win"] = str(it[5])
                
                for des in describe:
                    describe_dict = {}
                    describe_dict["name"] = str(des[2])
                    describe_dict["price"] = str(des[3])
                    describe_list.append(describe_dict)

                D["detail"] = describe_list
                result_qr.append(D)
                # if(count == len(item)-1):


                # print(getDatabarID(str(it[0])))
                # result.append(getDatabarID(str(it[0])))


        if(len(tranditional_item) > 0):
            for tran in tranditional_item:
                T = {}
                T['Number'] = tran[2]
                T['Win'] = tran[3]

                result_tr.append(T)

            result.append(result_qr)
            result.append(result_tr)
            # print(result)
            detail_json = json.dumps(result)
            # print(detail_json)
            result = json.loads(detail_json)
            # print(result)
            return result

            # print(result[0][0][2])
            # print(result[0][0][3])


    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass



