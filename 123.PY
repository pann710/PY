import requests
from bs4 import BeautifulSoup
from pretty_print import pretty_print
import urllib.parse

index = str(input('https://www.ptt.cc/bbs/Food/index.html'))
pages = eval(input('5:'))

not_exist = BeautifulSoup('<a>(本文已被刪除)</a>', 'lxml').a ## '本文已被刪除'的結構不同，自行生成<a>

def get_articles_on_ptt(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml') 
    articles = []

    for i in soup.find_all('div', 'r-ent'):
        meta = i.find('div', 'title').find('a') or not_exist
        articles.append({
            'title': meta.getText().strip(), 
            'push': i.find('div', 'nrec').getText(),
            'date': i.find('div', 'date').getText(),
            'author': i.find('div', 'author').getText(),
        })

    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[1].get('href') 

    return articles, next_link

def get_pages(num): 
    page_url = index
    all_articles = []

    for j in range(num):
        articles, next_link = get_articles_on_ptt(page_url)
        all_articles += articles
        page_url = urllib.parse.urljoin(index, next_link)
    
    return all_articles
data = get_pages(pages)

for k in data: 
    pretty_print(k['push'], k['title'], k['date'], k['author'])

    csv_or_not = input('輸入 y 以匯出成csv檔，輸入其他結束程式：')

if csv_or_not == 'y':
    board = index.split('/')[-2] 
    csv = open('./ptt_%s版_前%d頁.csv'%(board, pages), 'a+', encoding='utf-8') 
    csv.write('推文數,標題,發文日期,作者ID,\n')
    for l in data:
        l['title'] = l['title'].replace(',', '，')
        csv.write(l['push'] + ',' + l['title'] + ',' + l['date'] + ',' + l['author'] + ',\n')
    csv.close()
    print('csv檔案已儲存在您的資料夾中。')
else:
    quit()
