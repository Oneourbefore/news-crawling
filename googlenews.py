import json
import requests
from bs4 import BeautifulSoup

def clean_title(title):
    cleaned_title = title.replace('\n', ' ').replace('\t', ' ').replace('\u2019','').replace('\u2018','')
    return cleaned_title.strip()  # 좌우 공백 제거 후 반환

def getNewsData(search_term):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    search_url = "https://www.google.com/search?q={}&gl=us&tbm=nws&num=100".format(search_term)
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = []

    scroll_height = 2000
    while scroll_height < 6000:  

        for index, el in enumerate(soup.select("div.SoaBEf")):
            if index >= 7:
                break
            news_link = el.find("a")["href"]
            news_response = requests.get(news_link, headers=headers)
            news_soup = BeautifulSoup(news_response.content, "html.parser")
            # 이미지 가져오기
            image_meta_tag = news_soup.find("meta", property="og:image")
            if image_meta_tag and image_meta_tag["content"]:  # 이미지가 있고 null이 아닌 경우에만 추가
                news_image = image_meta_tag["content"]
                # title에서 \n, \t 등을 제거하고 공백 제거
                title = clean_title(el.select_one("div.MBeuO").get_text())
                news_results.append(
                    {
                        "link": news_link,
                        "title": title,
                        "image": news_image,
                        "date": el.select_one(".LfVVr").get_text()
                    }
                )
            
        scroll_height += 2000  

    for news in news_results:
        if news["image"]:  # 이미지가 null이 아닌 경우에만 출력
            print(json.dumps(news, indent=2))


search_term = input("검색어를 입력하세요: ")
getNewsData(search_term)
