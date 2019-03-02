#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"This script is intended for testing purposes"

from bot.analyze import process, go_back, touch

print("Possible input:",
      "ID - begin",
      "ID N - add N points",
      "bID - go back", sep='\n')
while True:
    data = input("> ").split()
    if len(data) == 2:
        uid = int(data[0])
        points = float(data[1])
        result = process(uid, points, send=False)
    elif data[0][0] == 'b':
        uid = int(data[0][1:])
        result = go_back(uid, send=False)
    else:
        uid = int(data[0])
        result = touch(uid, send=False)
    print(result)
