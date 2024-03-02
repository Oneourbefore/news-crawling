#크롤링시 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import sys
import requests

def translate_text_ko_to_en(text): # 번역 API 네이버 파파고 
    Client_ID='****'
    Client_Secret='****'
    Source_Lang='ko' #ko
    Target_Lang='en' #en 

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        f'X-Naver-Client-Id': Client_ID,
        f'X-Naver-Client-Secret': Client_Secret,
    }

    data = f'source={Source_Lang}&target={Target_Lang}&text={text}'.encode()

    response = requests.post('https://openapi.naver.com/v1/papago/n2mt', headers=headers, data=data)
    translated_text = response.json()['message']['result']['translatedText']
    return translated_text

# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
#입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num+1
    else:
        return num+9*(num-1)

# 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)

def makeUrl(search, start_pg, end_pg):
    if start_pg == end_pg:
        start_page = makePgNum(start_pg)
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(start_page)
        print("생성url: ", url)
        return url
    else:
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
            urls.append(url)
        print("생성url: ", urls)
        return urls    

# html에서 원하는 속성 추출하는 함수 만들기 (기사, 추출하려는 속성값)
def news_attrs_crawler(articles,attrs):
    attrs_content=[]
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

# ConnectionError방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

#html생성해서 기사크롤링하는 함수 만들기(url): 링크를 반환
def articles_crawler(url):
    #html 불러오기
    original_html = requests.get(i,headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")

    url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    url = news_attrs_crawler(url_naver,'href')
    return url


#####뉴스크롤링 시작#####

search = input("검색할 키워드를 입력해주세요:")
page = int(1) 
page2 = int(2)


# naver url 생성
url = makeUrl(search,page,page2)

#뉴스 크롤러 실행
news_titles = []
news_url =[]
# news_contents =[]
news_dates = []
news_image_url=[]
for i in url:
    url = articles_crawler(url)
    news_url.append(url)


def makeList(newlist, content):
    for i in content:
        for j in i:
            newlist.append(j)
    return newlist

    
#제목, 링크, 내용 담을 리스트 생성
news_url_1 = []

#1차원 리스트로 만들기(내용 제외)
makeList(news_url_1,news_url)

#NAVER 뉴스만 남기기
final_urls = []
for i in tqdm(range(len(news_url_1))):
    if "news.naver.com" in news_url_1[i]:
        final_urls.append(news_url_1[i])
    else:
        pass

# 뉴스 내용 크롤링

for i in tqdm(final_urls):
    #각 기사 html get하기
    news = requests.get(i,headers=headers)
    news_html = BeautifulSoup(news.text,"html.parser")
    # 뉴스 제목 가져오기
    title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
    #ct > div.media_end_head.go_trans > div.media_end_head_title
    #title_area
    #img_a1
    #img_a1
    
    if title == None:
        title = news_html.select_one("#content > div.end_ct > div > h2")
    #dic_area
    #newsct_article
    # 뉴스 본문 가져오기
    # content = news_html.select("article#dic_area")
    # if content == []:
    #     content = news_html.select("#articeBody")

    image = news_html.select("img#img1")
    if image == []:
        image=['none']
    
    # 이미지 URL 가져오기

    # 기사 텍스트만 가져오기
    # list합치기
    # content = ''.join(str(content))

    # html태그제거 및 텍스트 다듬기
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1, repl='', string=str(title))
    if image!=['none']:
        pattern_img = r'data-src="(.*?)"'
        image[0]=str(image[0])
        match = re.search(pattern_img, image[0])
        if match is not None:
            data_src = match.group(1)
            news_image_url.append(data_src)
        else:
            news_image_url.append('none')

    else:
        news_image_url.append('해당 기사는 사진이 없습니다.')

    # content = re.sub(pattern=pattern1, repl='', string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    # content = content.replace(pattern2, '')


    # headers = {
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # f'X-Naver-Client-Id': Client_ID,
    # f'X-Naver-Client-Secret': Client_Secret,
    # }
    # Text=title
    # data = f'source={Source_Lang}&target={Target_Lang}&text={Text}'.encode()

    # response = requests.post('https://openapi.naver.com/v1/papago/n2mt', headers=headers, data=data)
    # news_titles.append(response.json()['message']['result']['translatedText'])
    news_titles.append(title)
    # news_contents.append(content)

    try:
        html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
        news_date = html_date.attrs['data-date-time']
    except AttributeError:
        news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
        news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
    # 날짜 가져오기
    news_dates.append(news_date)

###데이터 프레임으로 만들기###
import pandas as pd
from fuzzywuzzy import fuzz
news_df = pd.DataFrame({'date': news_dates, 'title': news_titles, 'link': final_urls,  'image_url': news_image_url})

news_df = news_df.drop_duplicates(keep='first', ignore_index=True)
# '해당 기사는 사진이 없습니다.'를 포함한 행 제거
news_df = news_df[news_df['image_url'] != '해당 기사는 사진이 없습니다.']

# 검색어와 기사 제목 간의 유사도 측정하여 정렬
search_similarity = lambda x: fuzz.token_set_ratio(search, x)
news_df['search_similarity'] = news_df['title'].apply(search_similarity)
news_df = news_df.sort_values(by='search_similarity', ascending=False).reset_index(drop=True)

# 데이터프레임 저장
now = datetime.datetime.now() 
real_use5_df=news_df[:5]
real_use5_df = real_use5_df.copy()
real_use5_df['title'] = real_use5_df['title'].apply(lambda x: x.strip()) # 공백 없애기 -> 파파고 api 사용을 위한 전처리 
real_use5_df['title'] = real_use5_df['title'].apply(translate_text_ko_to_en) # api호출해서 번역 실행하기 , 현재 title에 적용함
#news_df.to_csv('{}_{}.csv'.format(search, now.strftime('%Y%m%d_%H시%M분%S초')), encoding='utf-8-sig', index=False)
real_use5_df.to_json('{}_{}.json'.format(search, now.strftime('%Y%m%d_%H시%M분%S초')), orient='records', force_ascii=False)
