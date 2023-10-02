import os

filename = "test.txt"

with open(filename) as f:
	lines = f.readlines()
	for line in lines:
		if "world" in line:
			print(line)
