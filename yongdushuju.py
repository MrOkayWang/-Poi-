import requests
import json
import time
import pymysql
import threading
from pandas import DataFrame
def getGaodeTrafficStatus(key,furl,currentTime):
    insert_list = []
    TrafficStatusUrl = furl
    res = requests.get(url=TrafficStatusUrl).content
    res=res.decode("utf-8")
    total_json = json.loads(res)
    print(total_json)
    jsondata = total_json['trafficinfo']['roads']
    currentDate = time.strftime("%Y-%m-%d", time.localtime())
    if any(jsondata):
            for i in jsondata:
              name = i['name']
              status = i['status']
              direction = i['direction']
              evaluation=total_json['trafficinfo']['evaluation']
              df = DataFrame({
                  'p_str': total_json['trafficinfo']['evaluation']
              });

              p_float = df['p_str'].str.strip("%")
              evaluation=p_float
              angle = i['angle']
              speed = i.get('speed')
              if speed is None:
                 speed = None
              lcodes = i['lcodes']
              polyline = i['polyline']
              list = [name, evaluation,status,direction, angle, lcodes, polyline,
                    currentDate, currentTime, speed]
              insert_list.append(list)
            db = pymysql.connect("localhost", "root", "root", "ttt")
            cursor = db.cursor()
            print(len(insert_list))
            for i in insert_list:
             print(len(i))
             if len(i):
                print(
                    "insert into biao(name,evaluation,status,direction,angle,lcodes,polyline, currentDate, currentTime, speed) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))
                print("----------------------------")
                cursor.execute(
                    "insert into biao(name,evaluation,status,direction,angle,lcodes,polyline, currentDate, currentTime, speed) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))
            db.commit()
            db.close()
keyList=[{}]
rectangleList=[]
def pydata():
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    key='bc411bc209882674362f05b90d6167d1'
    rectangle='112.89173,23.17571;112.90443,23.16561'#矩形左上右下坐标；隔开两个坐标
    # location='112.86461,23.51614'#圆形搜索
    # location_arr="[112.86461,23.51614],[112.87079,23.46136],[112.84058,23.41411],[112.94632,23.41159]"
    # radius='5000'#圆形半径
    type='rect'
    if(type=="rect"):
        url='http://restapi.amap.com/v3/traffic/status/rectangle?key='+key+'&rectangle='+rectangle+'&extensions=all'
    else:
        url='http://restapi.amap.com/v3/traffic/status/circle?key='+key+'&location='+location+'&radius='+radius+'&extensions=all'
    getGaodeTrafficStatus(key,url,currentTime);
    timer = threading.Timer(5,pydata)
    timer.start()

if __name__ == "__main__":
    timer = threading.Timer(5,pydata)
    timer.start()
