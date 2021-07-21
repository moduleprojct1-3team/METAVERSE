# NAVER 크롤링 & 정제
from json.decoder import JSONDecodeError
from json.encoder import JSONEncoder
import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd
from pandas.io.json import json_normalize
# from config import *

client_id = "6T2h2n7kT0_vo_T_m_pL"
client_secret = "MpUxBwkmUP"

# encText = urllib.parse.quote("검색할 단어")
# url = "https://openapi.naver.com/v1/search/news?query=" + encText
url = ""

# 데이터 요청하여 가져오기 - 크롤러 작업
def get_request_url(url): 
    req = urllib.request.Request(url) # 검색 URL경로 지정
    req.add_header("X-Naver-Client-Id", client_id) # 애플리케이션 등록 시 발급받은 client id 값(경로 접근하기 위한 아이디)
    req.add_header("X-Naver-Client-Secret", client_secret) # 애플리케이션 등록 시 발급받은 client secret 값(경로 접근하기 위한 비밀번호)
   
    try:
        response = urllib.request.urlopen(req) # URL을 통해 데이터 요청해 결과 받음
        rescode = response.getcode()
    
        if (rescode==200):
            print("[%s] URL 요청 성공 : " % datetime.datetime.now())
            return(response.read().decode('utf-8'))
    except Exception as ex:
        print(ex)
        #print("[%s] 오류발생 : %s" %datetime.datetime.now(), url)
        print(rescode)
        return None

# 크롤러로 데이터 가져오기 전 분류/인증 절차 등 사전 준비 작업
def GetNaverSearchResult(searchNode, searchText, pageStart, display): # 분류 시작/검색 기준
    baseurl = "https://openapi.naver.com/v1/search/" # 네이버에서 필수로 지정한 url
    nodedata = "%s.json" % searchNode # 뉴스를 가져오는데 결과는 json 형식으로 가져온다
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(searchText), 
                                                                       pageStart, 
                                                                       display)                                                                    
    url = baseurl + nodedata + parameters # 모든 것 합쳐서 URL 경로명 완성
    # 비정형(or 반정형)으로 가지고 온 초기 데이터(정형일 수도 있다)
    reqDataResult = get_request_url(url) # 가져오기 위해서 URL 완성 후 처리를 위한 함수 호출
    # reqDataResult : DataLake에 저장
    if(reqDataResult == None):
        print("No Data")
        return None
    else:
        return json.loads(reqDataResult) # 데이터를 정형으로 변경함

# json파일에서 데이터 가져와 변환.
def GetDataChange(data, jsonResult):
    resultTitle = data['title']
    resultDesc = data['description']
    resultOrgLink = data['originallink']
    naverLink = data['link']
    # total = data['total']

    changeDate = datetime.datetime.strptime(data['pubDate'], 
                                                        '%a, %d %b %Y %H:%M:%S +0900') # 표시형식
    changeDateResult = changeDate.strftime('%Y-%b-%d  %H:%M:%S') # 표시형식 변경 : 년-월-일 시-분-초

    jsonResult.append({ 'title' : resultTitle, 
                        'pubDate' : changeDateResult,
                        'description' : resultDesc,
                        'link' : naverLink,
                        'originlink' : resultOrgLink
                        })
    return 

# def json_default(data):
#     rJson = json.dumps(data, default = json_default)
#     return
    

# 정적언어처럼 main함수를 지정할 수 있다.
def main(): 
    jsonDataResult = []

    sNode = 'news'
    sText = '메타버스'
    dCount = 3
    
    # 원시 데이터 가져옴(DataLake에서 정형 데이터를 가져옴 )

    jsonSearchResult = GetNaverSearchResult(sNode, sText, 1, dCount) # 결과 확인하는 함수 호출

    # while ((jsonSearchResult != None) and (jsonSearchResult['display'] != 0)):
    for data in jsonSearchResult['items']:
            GetDataChange(data, jsonDataResult)

    with open('C:\Lab\SNSDataLab\%s__%s.json'% (sText, sNode), 'w', encoding='utf-8') as filedata:
       
        if 'items' in jsonSearchResult.keys():
        #tempData = pd.DataFrame(jsonDataResult['title'][0]['pubDate']['description']['link']['originallink'])
            temp = pd.DataFrame(jsonDataResult, columns= ['title','pubDate', 'description', 'link', 'originlink'])
            temp = temp.to_json()
            
            print(temp)
            tempd = json.dumps(temp, filedata,
                            indent = 4,
                            sort_keys = True, 
                            ensure_ascii = False)# indent, sort_keys 파일 저장시 항목 순서를 정한다.
    
        filedata.write(temp) 
        # 경로명을 저장해서 할 수도 있다.

    print('%s_naver_%s.json 저장완료' %  (sText, sNode))

if __name__ == '__main__':
    main()

    # __name__ : 내장변수 / 글로벌 변수 - 파이썬에서 예약한 변수
    # naverdata.py일 경우 __name__ = naverdata(파일이름)을 저장함
    # 이 파일 안에서 함수를 실행 : __main__ 값이 이미 정해져 있음
    # 처음으로 실행하는 함수를 지정

      # 정제
    #if '' in tempData.key():
    #    xdata = tempData[0][0]
    #    ydata = tempData[0][0]
    #for data in tempData:
    #    #비교 후 
    #    xdata = 0
    #    ydata = 0
 
    # 힌트는 import pandas as pd 추가
    # xdata = pd.DataFrame(tempData['']['']...)
    # 이렇게 하면 JSON 파일 데이터를 쉽게 찾을 수 있음
    # 쉽게 if '' in tempData.keys():  <- 이 코드가 작동할 수 있는 코드를 찾는게 힌트
    # 월요일에 pandas.pydata.org 이 사이트 참조
    # 이럴경우 반복문을 최대한 줄일수 있음, 아니면 반복문 만이 답
    # 아니면 자료구조에서 사용했던 [] 이 기호를 잘 사용하면 반복문을 줄일 수 있음.
    # tempData['status'][0]['meta'][0][] 이렇게 접근하는 방법도 있음
