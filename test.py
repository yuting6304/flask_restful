from pyzbar.pyzbar import decode
from PIL import Image
import requests
import json

def GetDetail(CodeData):
	UUID='B1B5EEAF-DBB9-484C-AF7F-BC3160DAF1E9'
	URL='https://api.einvoice.nat.gov.tw/PB2CAPIVAN/invapp/InvApp'
#input string type is "byte"
	CodeData = str(CodeData)
	Number_str = CodeData[2:12]
	year = CodeData[12:15]
	month = CodeData[15:17]
	day = CodeData[17:19]
	even_month = round(int(month)/2)*2
	Term_str = year + "%02d"%even_month #format
	# print(Term_str)
	Date_str = str(int(year)+1911) + '/' + month + '/' + day
	# print(Date_str)
	Random_str = CodeData[19:23]
	SellerID_str = CodeData[47:55]
	Encrypt_str = CodeData[55:79]
	# print(Random_str)
	# print(SellerID_str)
	# print(Encrypt_str)
	detail_data = {
		'version':'0.5',
		'type'   :'QRCode',
		'invNum' : Number_str,
		'action' :'qryInvDetail',
		'generation':'V2',
		'invTerm' : Term_str,#yyymm
		'invDate' : Date_str,#yyyy/MM/dd
		'encrypt' : Encrypt_str,#if qrcode ,needed
		'sellerID': SellerID_str,#if qrcode ,needed
		'UUID':UUID,
		'randomNumber':Random_str,
		'appID':'EINV4201904296869'
	}
	r = requests.post(URL,data = detail_data)
	# print(r.status_code)
	test = json.loads(r.text)
	# print(test)

	return test

def decode_qrcode(img):
	result = decode(Image.open(img))
	print(result[1].data)
	for text in result:
		tt = text.data.decode("utf-8")

	return GetDetail(result[1].data)

