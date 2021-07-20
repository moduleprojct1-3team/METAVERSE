# <Summary> 
# - URL 요청 클래스ㅇ
# <remarks> - Client ID, Secret 변경가능

import urllib.request
import datetime

# <Summary> - URL 요청 메서드
# <param> - url : URL주소, clientId : 클라이언트 아이디, clientSecret : 클라이언트 시크릿
# <return> - 리턴값 내용

def GetRequestUrl(url, client_Id, client_Secret): # 데이터 요청하여 가져오기 - 크럴러 작업


    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_Id)
    req.add_header("X-Naver-Client-Secret", client_Secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url 요청 성공 : " % datetime.datetime.now())    
            return response.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] 오류 : %s " % datetime.datetime.now(), url)
        return None