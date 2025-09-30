import requests
from bs4 import BeautifulSoup
import hashlib
import time
import os

def createSign(r):
    r += '0b50b02fd0d73a9c4c8c3a781c30845f'
    return hashlib.md5(r.encode('utf8')).hexdigest()

header = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
}
keyword = input('请输入关键字:')
# keyword = '胡彦斌'
response = requests.get('https://music.91q.com/search?word=%s' % keyword,headers=header)

soup = BeautifulSoup(response.text,'html.parser')
page_tags = soup.find_all(name='li',class_='number')
total_page = 0
if len(page_tags) == 0:
    total_page = 1
else:
    total_page = int(page_tags[-1].string)

for cur_page in range(1,total_page + 1):
    word = keyword
    appid = '16073360'
    timestamp = str(int(time.time()))

    r = 'appid=16073360&pageNo=%d&pageSize=20&timestamp=%s&type=1&word=%s' % (cur_page,timestamp,word)
    sign = createSign(r)

    params = {
        'sign' : sign,
        'appid': appid,
        'word': word,
        'timestamp':timestamp,
        'type': '1',
        'pageNo': str(cur_page),
        'pageSize': '20'
    }

    response = requests.get('https://music.91q.com/v1/search', params=params)
    song_info = response.json()
    # print(song_info)

    for track in song_info['data']['typeTrack']:
        TSID = track['TSID']
        song_name = track['title']
        singer_name = ''
        for singer in track['artist']:
            singer_name += singer['name']+' '

        r = 'TSID='+TSID+'&appid=16073360&timestamp='+timestamp
        sign = createSign(r)
        params = {
            'sign': sign,
            'appid': appid,
            'timestamp': timestamp,
            'TSID': TSID
        }
        response = requests.get('https://music.91q.com/v1/song/tracklink', params=params)
        info = response.json()
        #print(response.json())

        if 'path' in info['data']:
            print(info['data']['path'])
            response = requests.get(info['data']['path'])
            try:
                if not os.path.exists('./music'):
                    os.mkdir('./music')
                with open('./music/%s+%s.mp3' % (singer_name,song_name),'wb') as f:
                    f.write(response.content)
                print('下载完毕')
            except:
                print('文件名出错,已经跳过')

