# -*- coding: utf-8 -*-  
import os, sys, string  
from decimal import *
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb

class DBSaver:
    def __init__(self, host = "localhost", user='root',passwd='123456',db='web_data',charset='UTF8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.perf_attr = ['unloadEventStart', 'unloadEventEnd',\
        'redirectStart', 'redirectEnd', 'fetchStart', 'domainLookupStart', \
        'domainLookupEnd', 'connectStart', 'secureConnectionStart', 'connectEnd', 'requestStart',\
        'responseStart', 'responseEnd', 'domLoading', 'domInteractive', \
        'domContentLoadedEventStart', 'domContentLoadedEventEnd', \
        'domComplete', 'loadEventStart', 'loadEventEnd']

        self.res_attr = [
            'test_id', 'resource_id', 'name', 'entryType', 'startTime',\
            'duration', 'initiatorType', 'redirectStart', 'redirectEnd',\
            'fetchStart', 'domainLookupStart', 'domainLookupEnd',\
            'connectStart', 'connectEnd', 'secureConnectionStart',\
            'requestStart', 'responseStart', 'responseEnd', 'transferSize',\
            'nextHopProtocol', 'type', 'workerStart', 'encodedBodySize',\
            'decodedBodySize', 'unloadEventStart', 'unloadEventEnd',\
            'domContentLoadedEventStart', 'domContentLoadedEventEnd',\
            'loadEventStart', 'loadEventEnd', 'domInteractive', 'domComplete',\
            'redirectCount']

    def save(self, url, perf, res):
        conn = None
        try:  
            conn = MySQLdb.connect(host=self.host, user = self.user,
                passwd = self.passwd, db = self.db, charset='UTF8')

        except Exception, e:  
            return False, e

        # 获取cursor对象来进行操作  
        cursor = conn.cursor()

        sql = "insert into performance(url,"
        for item in self.perf_attr:
            sql += item + ','
        sql = sql[:-1] + ')'
        sql += " values('" + url + "'," #+ "%d,"*19 + "%d)" + 
        for item in self.perf_attr:
            sql += str(perf[item]) + ","
        sql = sql[:-1] + ")"



        try:
            cursor.execute(sql)
        except Exception, e:
            self.rollback(cursor, conn)
            return False, e

        sql = "select LAST_INSERT_ID();"
        try:
          cursor.execute(sql)
        except Exception, e:
            self.rollback(cursor, conn)
            return False, e
        alldata = cursor.fetchall()
        index = alldata[0][0]

        res_count = len(res)
        

        # index, i + 1
        
        for i in xrange(res_count):

            sql = "insert into resource("
            for item in self.res_attr:
                sql += item + ","
            sql = sql[:-1] + ")"

            sql += " values("

            res_attr_dic = {}
            for item in self.res_attr:
                res_attr_dic[item] = None
            res_attr_dic['test_id'] = str(index)
            res_attr_dic['resource_id'] = str(i + 1)
            res_attr_dic['name'] = "'" + res[i]['name'] + "'"
            res_attr_dic['entryType'] = "'" + res[i]['entryType'] + "'"
            res_attr_dic['startTime'] = "%.10f" %res[i]['startTime']
            res_attr_dic['duration'] = "%.10f" %res[i]['duration']
            res_attr_dic['initiatorType'] = "'" + res[i]['initiatorType'] + "'"
            res_attr_dic['redirectStart'] = "%.10f" %res[i]['redirectStart']
            res_attr_dic['redirectEnd'] = "%.10f" %res[i]['redirectEnd']
            res_attr_dic['fetchStart'] = "%.10f" %res[i]['fetchStart']
            res_attr_dic['domainLookupStart'] = "%.10f" %res[i]['domainLookupStart']
            res_attr_dic['domainLookupEnd'] = "%.10f" %res[i]['domainLookupEnd']
            res_attr_dic['connectStart'] = "%.10f" %res[i]['connectStart']
            res_attr_dic['connectEnd'] = "%.10f" %res[i]['connectEnd']
            res_attr_dic['secureConnectionStart'] = "%.10f" %res[i]['secureConnectionStart']
            res_attr_dic['requestStart'] = "%.10f" %res[i]['requestStart']
            res_attr_dic['responseStart'] = "%.10f" %res[i]['responseStart']
            res_attr_dic['responseEnd'] = "%.10f" %res[i]['responseEnd']

            # 不一定存在的属性
            if 'transferSize' in res[i]:
                res_attr_dic['transferSize'] = "%d" %res[i]['transferSize']
            if 'nextHopProtocol' in res[i]:
                res_attr_dic['nextHopProtocol'] = "'" + res[i]['nextHopProtocol'] + "'"
            if 'type' in res[i]:
                res_attr_dic['type'] = "'" + res[i]['type'] + "'"
            if 'workerStart' in res[i]:
                res_attr_dic['workerStart'] = "%.10f" %res[i]['workerStart']
            if 'encodedBodySize' in res[i]:
                res_attr_dic['encodedBodySize'] = "%d" %res[i]['encodedBodySize']
            if 'decodedBodySize' in res[i]:
                res_attr_dic['decodedBodySize'] = "%d" %res[i]['decodedBodySize']

            if 'unloadEventStart' in res[i]:
                res_attr_dic['unloadEventStart'] = "%.10f" %res[i]['unloadEventStart']
            if 'unloadEventEnd' in res[i]:
                res_attr_dic['unloadEventEnd'] = "%.10f" %res[i]['unloadEventEnd']
            if 'domContentLoadedEventStart' in res[i]:
                res_attr_dic['domContentLoadedEventStart'] = "%.10f" %res[i]['domContentLoadedEventStart']
            if 'domContentLoadedEventEnd' in res[i]:
                res_attr_dic['domContentLoadedEventEnd'] = "%.10f" %res[i]['domContentLoadedEventEnd']
            if 'loadEventStart' in res[i]:
                res_attr_dic['loadEventStart'] = "%.10f" %res[i]['loadEventStart']
            if 'loadEventEnd' in res[i]:
                res_attr_dic['loadEventEnd'] = "%.10f" %res[i]['loadEventEnd']
            if 'domInteractive' in res[i]:
                res_attr_dic['domInteractive'] = "%.10f" %res[i]['domInteractive']
            if 'domComplete' in res[i]:
                res_attr_dic['domComplete'] = "%.10f" %res[i]['domComplete']
            if 'redirectCount' in res[i]:
                res_attr_dic['redirectCount'] = "%d" %res[i]['redirectCount']
            for item in self.res_attr:
                if res_attr_dic[item] != None:
                    sql += res_attr_dic[item] + ","
                else:
                    sql += "NULL" + ","

            sql = sql[:-1] + ")"
            #print sql
            try:
                cursor.execute(sql)
            except Exception, e:
                self.rollback(cursor, conn)
                return False, e


        cursor.close()  
        conn.commit()
        conn.close()

        return True, None

    def rollback(self, cursor, conn):
        try:
            cursor.close()
            conn.rollback()
            conn.close()
        except:
            pass

def test():
    t = DBSaver()
    pref = {"unloadEventStart": 0, "domLoading": 1495106462767, "fetchStart": 1495106461081, "responseStart": 1495106462690, "loadEventEnd": 1495106463517, "connectStart": 1495106461081, "domainLookupStart": 1495106461081, "redirectStart": 0, "domContentLoadedEventEnd": 1495106463221, "requestStart": 1495106462201, "secureConnectionStart": 0, "connectEnd": 1495106461081, "navigationStart": 1495106460845, "loadEventStart": 1495106463512, "domInteractive": 1495106463214, "domContentLoadedEventStart": 1495106463214, "redirectEnd": 0, "domainLookupEnd": 1495106461081, "unloadEventEnd": 0, "responseEnd": 1495106462769, "domComplete": 1495106463512}
    res = [{"startTime": 0, "initiatorType": "navigation", "unloadEventStart": 0, "fetchStart": 235.11, "duration": 2671.135, "responseStart": 1844.66, "loadEventEnd": 2671.135, "transferSize": 29135, "connectStart": 235.11, "domainLookupStart": 235.11, "redirectStart": 0, "domContentLoadedEventEnd": 2375.385, "requestStart": 1355.7050000000002, "type": "navigate", "secureConnectionStart": 0, "connectEnd": 235.11, "redirectCount": 0, "workerStart": 0, "decodedBodySize": 102058, "loadEventStart": 2666.9300000000003, "encodedBodySize": 28096, "entryType": "navigation", "domInteractive": 2368.675, "domContentLoadedEventStart": 2368.82, "redirectEnd": 0, "name": "http://www.baidu.com/", "domainLookupEnd": 235.11, "unloadEventEnd": 0, "responseEnd": 1923.1950000000002, "domComplete": 2666.83}]
    res = [{"startTime": 0, "initiatorType": "navigation", "unloadEventStart": 0, "fetchStart": 235.11, "duration": 2671.135, "responseStart": 1844.66, "loadEventEnd": 2671.135, "transferSize": 29135, "connectStart": 235.11, "domainLookupStart": 235.11, "redirectStart": 0, "domContentLoadedEventEnd": 2375.385, "requestStart": 1355.7050000000002, "type": "navigate", "secureConnectionStart": 0, "connectEnd": 235.11, "redirectCount": 0, "workerStart": 0, "decodedBodySize": 102058, "loadEventStart": 2666.9300000000003, "encodedBodySize": 28096, "entryType": "navigation", "domInteractive": 2368.675, "domContentLoadedEventStart": 2368.82, "redirectEnd": 0, "name": "http://www.baidu.com/", "domainLookupEnd": 235.11, "unloadEventEnd": 0, "responseEnd": 1923.1950000000002, "domComplete": 2666.83, "toJSON": {}}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 8190, "redirectEnd": 0, "name": "http://www.baidu.com/img/bd_logo1.png", "responseStart": 2090.28, "startTime": 1950.43, "domainLookupEnd": 1950.43, "connectEnd": 1950.43, "requestStart": 1957.9, "initiatorType": "img", "responseEnd": 2094.91, "workerStart": 0, "decodedBodySize": 7877, "fetchStart": 1950.43, "duration": 144.4799999999998, "encodedBodySize": 7877, "toJSON": {}, "entryType": "resource", "connectStart": 1950.43, "domainLookupStart": 1950.43}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 1016, "redirectEnd": 0, "name": "http://www.baidu.com/img/baidu_jgylogo3.gif", "responseStart": 2433.3150000000005, "startTime": 1950.565, "domainLookupEnd": 1950.565, "connectEnd": 1950.565, "requestStart": 1959.1850000000002, "initiatorType": "img", "responseEnd": 2433.9000000000005, "workerStart": 0, "decodedBodySize": 705, "fetchStart": 1950.565, "duration": 483.3350000000005, "encodedBodySize": 705, "toJSON": {}, "entryType": "resource", "connectStart": 1950.565, "domainLookupStart": 1950.565}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/jquery/jquery-1.10.2.min_65682a2.js", "responseStart": 0, "startTime": 1950.6900000000003, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "script", "responseEnd": 2155.155, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 1950.6900000000003, "duration": 204.46499999999992, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/home/img/qrcode/zbios_efde696.png", "responseStart": 0, "startTime": 1969.2300000000002, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "css", "responseEnd": 2115.17, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 1969.2300000000002, "duration": 145.93999999999983, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/global/img/icons_5859e57.png", "responseStart": 0, "startTime": 1969.3950000000002, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "css", "responseEnd": 2144.425, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 1969.3950000000002, "duration": 175.02999999999997, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/global/js/all_async_search_a2c362b.js", "responseStart": 0, "startTime": 2175.8700000000003, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "script", "responseEnd": 2315.545, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 2175.8700000000003, "duration": 139.67499999999973, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/plugins/every_cookie_a70bc15.js", "responseStart": 0, "startTime": 2178.75, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "script", "responseEnd": 2225.0350000000003, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 2178.75, "duration": 46.28500000000031, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/home/js/nu_instant_search_08089ad.js", "responseStart": 0, "startTime": 2344.0950000000003, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "script", "responseEnd": 2365.5000000000005, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 2344.0950000000003, "duration": 21.4050000000002, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/global/img/quickdelete_33e3eb8.png", "responseStart": 0, "startTime": 2352.565, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "css", "responseEnd": 2384.0000000000005, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 2352.565, "duration": 31.4350000000004, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/plugins/swfobject_0178953.js", "responseStart": 0, "startTime": 2356.885, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "script", "responseEnd": 2485.655, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 2356.885, "duration": 128.76999999999998, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/soutu/js/tu_329aca4.js", "responseStart": 0, "startTime": 2357.1400000000003, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "script", "responseEnd": 2384.2850000000003, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 2357.1400000000003, "duration": 27.144999999999982, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/sug/js/bdsug_async_97a395d.js", "responseStart": 0, "startTime": 2365.8700000000003, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "script", "responseEnd": 2486.05, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 2365.8700000000003, "duration": 120.17999999999984, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}, {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 0, "redirectEnd": 0, "name": "http://s1.bdstatic.com/r/www/cache/static/soutu/css/soutu.css", "responseStart": 0, "startTime": 2387.6850000000004, "domainLookupEnd": 0, "connectEnd": 0, "requestStart": 0, "initiatorType": "link", "responseEnd": 2664.2750000000005, "workerStart": 0, "decodedBodySize": 0, "fetchStart": 2387.6850000000004, "duration": 276.59000000000015, "encodedBodySize": 0, "toJSON": {}, "entryType": "resource", "connectStart": 0, "domainLookupStart": 0}]

    res, e = t.save("aaa", pref, res)
    if res == False:
        print e
#import json
if __name__ == '__main__':
    test()
    '''
    res = [{"startTime": 0, "initiatorType": "navigation", "unloadEventStart": 0, "fetchStart": 235.11, "duration": 2671.135, "responseStart": 1844.66, "loadEventEnd": 2671.135, "transferSize": 29135, "connectStart": 235.11, "domainLookupStart": 235.11, "redirectStart": 0, "domContentLoadedEventEnd": 2375.385, "requestStart": 1355.7050000000002, "type": "navigate", "secureConnectionStart": 0, "connectEnd": 235.11, "redirectCount": 0, "workerStart": 0, "decodedBodySize": 102058, "loadEventStart": 2666.9300000000003, "encodedBodySize": 28096, "entryType": "navigation", "domInteractive": 2368.675, "domContentLoadedEventStart": 2368.82, "redirectEnd": 0, "name": "http://www.baidu.com/", "domainLookupEnd": 235.11, "unloadEventEnd": 0, "responseEnd": 1923.1950000000002, "domComplete": 2666.83}]
    b = 89988.9999999999999
    a = json.dumps(b)
    c = {'a':8888.123456789123456789}
    print json.dumps(c)
    print a 
    '''




