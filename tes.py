import requests
from bs4 import BeautifulSoup
import json

# 전처리 함수 정의
def clean_title(title):
    cleaned_title = title.replace('\n', ' ').replace('\t', ' ').replace('\u2019', '').replace('\u2018', '')
    return cleaned_title.strip()

search_term = input("검색어를 입력하세요: ")
link = f'https://www.nytimes.com/search?query={search_term}'
page = requests.get(link)
soup = BeautifulSoup(page.text, 'html.parser')

news_results = []

news_items = soup.find_all("li", class_="css-1l4w6pd")[:30] 
count = 0  

for news_item in news_items:
    headline_news = clean_title(news_item.find("h4", class_="css-2fgx4k").text.strip())
    link_news = news_item.find('div', class_='css-e1lvw9')
    link = link_news.find('a')['href']
    
    time_element = news_item.find("span", class_="css-bc0f0m")
    if time_element:
        time_text_raw = time_element.text.strip()
        if '|' in time_text_raw:
            time_text = time_text_raw.split('|')[1].split('Page')[0].strip().replace(',', '')  # '|' 이후 부분 추출, 'Page' 이후 내용 삭제, 쉼표 제거
        else:
            time_text = None
    else:
        time_text = None
    
    image_meta_tag = news_item.find("img", class_="css-rq4mmj")['src'].strip()
    
    if time_text is not None and time_text != '':
        news_results.append({
            "title": headline_news,
            "link": 'https://www.nytimes.com/'+link,
            "time": time_text,
            "image URL": image_meta_tag
        })
        count += 1  
    if count == 5:  
        break

print(json.dumps(news_results, indent=2))
