import sys
import json


# init env file...
env = {}
with open('env.json') as json_data:
	env = json.load(json_data)
	sys.path.append(env["model"]["path"])

