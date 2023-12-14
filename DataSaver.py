import json


def saveScanJson(fileName : str,data):
	with open(fileName, mode='wt', encoding='utf-8') as myfile:
		myfile.write(json.dumps(data))

def loadScanJson(fileName : str):
	with open(fileName, mode='r', encoding='utf-8') as myfile:
		return json.load(myfile)
	