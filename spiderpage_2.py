import requests
from bs4 import BeautifulSoup
import pandas as pd

#构造出一个DataFrame类型的数据
#构造一个字典
# info = {
#     'name':['wang','liu','zhang'],
#     'sex':['F','M','F']
# }



header = {
    'referer':'https://scrape.center/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
}

movie_info = {'电影名称':[],'类型':[],'国家':[],'时长':[],'上映时间':[],'分数':[]}

for page in range(1,11):
    response = requests.get('https://ssr1.scrape.center/page/%d' %page,headers=header,verify=False)
    soup = BeautifulSoup(response.text,'html.parser')
    result = soup.find_all(name='div',class_='p-h el-col el-col-24 el-col-xs-9 el-col-sm-13 el-col-md-16')

    for i in range(len(result)):
        movie_info['电影名称'].append(result[i].h2.string)
        btn_list = result[i].find_all(name='button',class_='el-button category el-button--primary el-button--mini')
        movie_type = ''
        for btn in btn_list:
            movie_type += btn.span.string + ','
        movie_info['类型'].append(movie_type)

        info_list = result[i].find_all(name='div',class_='m-v-sm info')
        span_list = info_list[0].find_all(name='span')
        movie_info['国家'].append(span_list[0].string)
        movie_info['时长'].append(span_list[2].string)
        # movie_info['上映时间'].append(info_list[1].span.string)
        span_list = info_list[1].find_all(name='span')
        if len(span_list) > 0:
            movie_info['上映时间'].append(info_list[1].span.string)
        else:
            movie_info['上映时间'].append('')

        score = soup.find_all(name='p',class_='score m-t-md m-b-n-sm')
        movie_info['分数'].append(score[i].string.strip())

data = pd.DataFrame(movie_info)
data.to_excel('movieinfo.xlsx',index=False)