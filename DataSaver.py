import json, os


def saveScanJson(fileName : str,data):
	i=0
	while os.path.isfile("./backLogs/" + fileName + "_backlog(" + str(i) +").json"):
		i+=1
	else:
		with open("./backLogs/" + fileName + "_backlog(" + str(i) +").json", mode='wt', encoding='utf-8') as myfile:
			myfile.write(json.dumps(data))
		with open(fileName + ".json", mode='wt', encoding='utf-8') as myfile:
			myfile.write(json.dumps(data))

def loadScanJson(fileName : str):
	with open(fileName + ".json", mode='r', encoding='utf-8') as myfile:
		return json.load(myfile)
	