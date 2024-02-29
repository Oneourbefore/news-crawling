import requests
Client_ID='En09kbQorCTHYr0_07IO'
Client_Secret='UVs9ctsJOX'
Source_Lang='ko' #ko
Target_Lang='en' #en 
Text='안녕하세요 동국대학교 학생입니다~'


headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    f'X-Naver-Client-Id': Client_ID,
    f'X-Naver-Client-Secret': Client_Secret,
}
data = f'source={Source_Lang}&target={Target_Lang}&text={Text}'.encode()

response = requests.post('https://openapi.naver.com/v1/papago/n2mt', headers=headers, data=data)
print(response.json()['message']['result']['translatedText']) #Good to meet you.