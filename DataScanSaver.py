


def saveScanTxt(data):
	with open('scanData.txt', mode='wt', encoding='utf-8') as myfile:
		myfile.write('\n'.join(data))