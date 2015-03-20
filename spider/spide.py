# coding=utf-8
import time
import json
import re

import requests

from thread_pool import ThreadPool


class Spider(object):
    def __init__(self):
        self.cookies = {}
        self.r = re.compile(
            u'<tr style="display:" id="tr\d+"[^>]*?>\s*<td>([^<]*?)</td>[\s\S]+?<tr align="center" >[\s\S]+?<tr align="center" >\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>')

    def request(self, url, data):
        return requests.post(url, data=data, cookies=self.cookies)

    def craw(self, campus, building, week, week_day):
        #time.sleep(3)
        data = {"aid": campus, "buildingid": building, "room": "-1", "whichweek": week, "week": week_day}
        try:
            html = self.request("http://jw.qdu.edu.cn/academic/teacher/teachresource/roomschedule_week.jsdo",
                                data).content
            # print html
        except Exception as e:
            print e
            print campus, building, week, week_day
            return None
        content = self.r.findall(html)
        rooms = []
        for item in content:
            l = []
            for i in range(0, len(item)):
                c = item[i].decode("gb2312")
                if i == 0:
                    l.append(c)
                else:
                    if c[0] == "&":
                        l.append(0)
                    else:
                        l.append(1)
            rooms.append(l)
        f = open("data/" + campus + "." + building + "." + week + "." + week_day + ".json", "w")
        f.write(json.dumps(rooms))
        f.close()
        print "finish: week:" + week + " week_day:" + week_day
        return "success"

'''
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
    '''
if __name__ == "__main__":
    s = Spider()
    s.cookies = {"JSESSIONID": "246D37FBEB5AC630D8A24FEDBF04A485.TAC1;"}
    # s.craw("1709", "2278", "3", "3")
    pool = ThreadPool(size=20)
    pool.start()

    for week in range(1, 21):
        for week_day in range(1, 8):
            print "start week:" + str(week) + " week_day:" + str(week_day)
            pool.append_job(s.craw, "1709", "1783", str(week), str(week_day))
    pool.join()