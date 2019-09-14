#!/usr/bin/env python

import json, copy

with open("startValue.json",'r') as file:
	startData = json.loads(file.read())
with open("endValue.json",'r') as file:
	endData = json.loads(file.read())
with open("solved.json",'r') as file:
	solvedData = json.loads(file.read())

newData = copy.deepcopy(startData)
unsolved = []

for index in range(0,len(startData["top"])):
	if startData["top"][index] == endData["top"][index]:
		# print("Index {}, {} matches!".format(index, startData["top"][index]))
		newData["top"][index] = solvedData["top"][index]
	else:
		print("Index {}, {} /= {}".format(index, startData["top"][index],endData["top"][index]))
		unsolved.append(("top", index, startData["top"][index]))

for index in range(0,len(startData["middle"])):
	if startData["middle"][index] == endData["middle"][index]:
		# print("Index {}, {} matches!".format(index, startData["middle"][index]))
		newData["middle"][index] = solvedData["middle"][index]
	else:
		print("Index {}, {} /= {}".format(index, startData["middle"][index],endData["middle"][index]))
		unsolved.append(("middle", index, startData["middle"][index]))

for index in range(0,len(startData["bottom"])):
	if startData["bottom"][index] == endData["bottom"][index]:
		# print("Index {}, {} matches!".format(index, startData["bottom"][index]))
		newData["bottom"][index] = solvedData["bottom"][index]
	else:
		print("Index {}, {} /= {}".format(index, startData["bottom"][index],endData["bottom"][index]))
		unsolved.append(("bottom", index, startData["bottom"][index]))

for piece in unsolved:
	found = False
	for index in range(0,len(startData["top"])):
		if piece[2] == endData["top"][index]:
			print("{}: index {} replaced with {}".format(piece[0],piece[1],solvedData["top"][index]))
			newData[piece[0]][piece[1]] = solvedData["top"][index]
			found = True
			break
		if piece[2] == endData["bottom"][index]:
			print("{}: index {} replaced with {}".format(piece[0],piece[1],solvedData["bottom"][index]))
			newData[piece[0]][piece[1]] = solvedData["bottom"][index]
			found = True
			break
	if not found:
		for index in range(0,len(startData["middle"])):
			if piece[2] == endData["middle"][index]:
				print("{}: index {} replaced with {}".format(piece[0],piece[1],solvedData["middle"][index]))
				newData[piece[0]][piece[1]] = solvedData["middle"][index]
				break
	if not found:
		print("PIECES CHANGED! (missing {})".format(piece))
		exit(-1)

with open("consolidated.json",'w') as file:
	file.write(json.dumps({"list": [newData]},indent="  "))



