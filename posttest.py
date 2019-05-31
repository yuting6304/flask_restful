import requests
import json


def getPrizeNum(year, month):
	URL='https://api.einvoice.nat.gov.tw/PB2CAPIVAN/invapp/InvApp'
	#?version=0.2&action=QryWinningList&invTerm=10606&appID=EINV4201904296869
	my_data = {
		'version':'0.2',
		'action' :'QryWinningList',
		'appID' : 'EINV4201904296869'
	}

	if(month < 10):
		my_data['invTerm'] = str(year) + '0' + str(month)
	else:
		my_data['invTerm'] = str(year) + str(month)
	r = requests.post(URL,data = my_data)
	# print(r.status_code)
	# print(r.text)
	return r.text
