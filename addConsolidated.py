#!/usr/bin/env python

import json

with open("moves.json",'r') as file:
	moves = json.loads(file.read())
with open("consolidated.json",'r') as file:
	consolidated = json.loads(file.read())

moves["list"].append(consolidated["list"][0])

with open("moves.json",'w') as file:
	file.write(json.dumps(moves,indent="  ",sort_keys=True))