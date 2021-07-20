# 메인 클래스 - 슬기
import urllib.request
import datetime
import json

# NAVER API 클라이언트 연결
client_id = "i0rOFq7sJon3SVankcLB"
client_secret = "iNHdUrvzYV"

def get_request_url(url): 
    req = urllib.request.Request(url) 
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url 요청 성공 : " % datetime.datetime.now())    
            return response.read().decode('utf-8')
    
    except Exception as ex:
        print(ex)
        print("[%s] 오류 : %s " % datetime.datetime.now(), url)
        return None