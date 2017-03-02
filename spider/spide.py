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
            u'<tr style="display:" id="tr\d+"[^>]*?>\s*<td>([^<]*?)</td>[\s\S]+?<tr align="center" >[\s\S]+?<tr align="center" >\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)[\s\S]*?(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)[\s\S]*?(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>\s*'
            u'<td[^>]*?>(?:<a href="#" title="[^"]*?"><font color="#\w+">|)([\s\S]*?)(?:</font></a>|)</td>')

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
        with open("data/" + campus + "." + building + "." + week + "." + week_day + ".json", "w") as f:
            f.write(json.dumps(rooms))
        print "finish: week:" + week + " week_day:" + week_day
        return "success"


if __name__ == "__main__":
    s = Spider()
    s.cookies = {"JSESSIONID": "8B7DA565F71772D37B04170241A757A8.TAB2;"}
    pool = ThreadPool(size=20)
    pool.start()

    for week in range(1, 21):
        for week_day in range(1, 8):
            print "start week:" + str(week) + " week_day:" + str(week_day)
            # 请自行确定info.py中的校区id和教学楼id是正确的
            # 然后按照info.py中的数据修改校区和教学楼id
            pool.append_job(s.craw, "1709", "1783", str(week), str(week_day))
    pool.join()