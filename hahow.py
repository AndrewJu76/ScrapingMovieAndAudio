import requests as req
from openpyxl import load_workbook, Workbook

wb = Workbook()
ws = wb.active

title = ['课名','作者','价格','预购价','贩售数']
ws.append(title)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:157.0) Gecko/20100101 Firefox/157.0'
}

for index in range(71): #70
    url = 'https://api.hahow.in/api/products/search?limit=24&mixedResults=true&page='
    url += str(index)
    url+= '&sort=TRENDING'
    # print(url)
    r = req.get(url,headers=header)
    print(r)
    root_json = r.json()

    # print(root_json["data"]['productData']['products'])
    for data in root_json["data"]['productData']['products']:
        course = []
        try:
            course.append(data['product']['title'])
            course.append(data['product']['owner']['name'])
            course.append(data['product']['price'])
            course.append(data['product']['preOrderedPrice'])
            course.append(data['product']['numSoldTickets'])
            # print(data['product']['_id'])
            # print(data['product']['title'])
            # print(data['product']['owner']['name'])
            # print(data['product']['price'])
            # print(data['product']['preOrderedPrice'])
            # print(data['product']['numSoldTickets'])
        except:
            print('something in web is wrong')
            continue

        try:
            ws.append(course)
        except:
            print('something in execl is wrong')
            continue
wb.save('hahowcourselist.xlsx')
