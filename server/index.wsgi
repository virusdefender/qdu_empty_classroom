# coding=utf-8
import json
import sae.kvdb


def import_data():
    
    kv = sae.kvdb.Client()
    
    info = [
        {"campus_name": u"中心校区", "id": "1709",
         "buildings": [{"building_name": u"东12", "id": "2278"},
                       {"building_name": u"博文楼", "id": "1847"},
                       {"building_name": u"博远楼", "id": "1954"},
                       {"building_name": u"博知楼", "id": "1904"},
         ]},
        {"campus_name": u"中心北院", "id": "2348",
         "buildings": [{"building_name": u"教学楼", "id": "2349"}
         ]},
        {"campus_name": u"东校区", "id": "13041",
         "buildings": [{"building_name": u"西院一教", "id": "2706"},
                       {"building_name": u"西院二教", "id": "2748"}
         ]}
    ]
    
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
                        kv.set(key, json.dumps(r))
                    f.close()


def application(environ, start_response):
    start_response('200 ok', [('content-type', 'application/json')])
    try:
        q = environ['QUERY_STRING'].split("=")
        key = q[0]
        value = q[1]
        return json.dumps([key, value])

    except:
        return json.dumps({"status": "error"})
