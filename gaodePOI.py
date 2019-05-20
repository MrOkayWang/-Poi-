from urllib.parse import quote
from urllib import request
import json
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
 
# TODO

# amap_web_key = '1ec3875364ca8c23846130690b530749'
amap_web_key = '3b6d95c5e26e64caf10780497b3d93da'#此处需要添加高德API密钥，申请个很简单
filename = r'sah.xls'
cityname = "聊城"                #可以修改，不同的地区查找不同地区的poi
classfiled = "网吧"              #可修改，查找不同类型的poi
 
poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"
 
 
# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        result = json.loads(result)  # 将字符串转换为json
        if result['status'] is not '1':
            return
        if len(result['pois']) < 25:
            hand(poilist, result)
            write_to_excel(poilist, cityname, keywords)
            break
        hand(poilist, result)
        if i == 1:
            write_to_excel(poilist, cityname, keywords)
        else:
            contact_read_excel(poilist)
        i = i + 1
    return poilist
 
 
# 追加数据到excel中
def contact_read_excel(poilist):
    rexcel = open_workbook(filename)  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
    # print('原有的行', rows)
    for i in range(len(poilist)):
        table.write(rows + i, 0, poilist[i]['id'])
        table.write(rows + i, 1, poilist[i]['name'])
        table.write(rows + i, 2, poilist[i]['location'])
        table.write(rows + i, 3, poilist[i]['address'])      #添加部分
        table.write(rows + i, 4, poilist[i]['tel'])         #添加部分
    excel.save(filename)  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
 
 
# 数据写入excel
def write_to_excel(poilist, cityname, classfield):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)
    # 第一行(列标题)
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'name')
    sheet.write(0, 2, 'location')
    sheet.write(0, 3, 'address')         #添加部分
    sheet.write(0, 4, 'tel')             #添加部分
    for i in range(len(poilist)):
        sheet.write(i + 1, 0, poilist[i]['id'])
        sheet.write(i + 1, 1, poilist[i]['name'])
        sheet.write(i + 1, 2, poilist[i]['location'])
        sheet.write(i + 1, 3, poilist[i]['address'])        #添加部分
        sheet.write(i + 1, 4, poilist[i]['tel'])               #添加部分
    book.save(filename)
 
 
# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])
 
 
# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data
 
 
# 获取城市分类数据
pois = getpois(cityname, classfiled)
 
print('写入成功')
