# coding=utf-8
import sae.kvdb
import json

from info import info

kv = sae.kvdb.Client()

for campus in info:
    for building in campus["buildings"]:
        for week in range(1, 21):
            for week_day in range(1, 8):
                file_name = campus["id"] + "." + building["id"] + "." + str(week) + "." + str(week_day) + ".json"
                f = open("data/" + file_name, "r")
                data = json.loads(f.read())
                for t in [1, 3, 5, 7, 9]:
                    r = []
                    key = campus["id"] + "." + building["id"] + "." + str(week) + "." + str(week_day) + "." + str(t / 2 + 1)
                    for room in data:
                        r.append((room[0], room[t]))
                    print "-----"
                    print key
                    print r
                    kv.set(key, json.dumps(r))
                f.close()