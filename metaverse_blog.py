import urllib.request
import datetime
import json


client_id = "i0rOFq7sJon3SVankcLB"
client_secret = "iNHdUrvzYV"

def get_request_url(url): # 데이터 요청하여 가져오기 - 크럴러 작업
    req = urllib.request.Request(url) #검색 URL 경로 지정
    req.add_header("X-Naver-Client-Id", client_id) # 경로 접근하기 위한 아이디 - naver에서 발급
    req.add_header("X-Naver-Client-Secret", client_secret) #경로 접근하기 위한 비밀번호 - naver에서 발급

    try:
        response = urllib.request.urlopen(req) # URL을 통해 데이터 요청해서 결과 받음
        if response.getcode() == 200: # 200 코드 번호면 성공 400/500 은 Naver 문서에서 확인
            print("[%s] Url 요청 성공 : " % datetime.datetime.now())    
            return response.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] 오류 : %s " % datetime.datetime.now(), url)
        return None


#크롤러로 데이터 가져오기 전 분류 / 인증 절차 등 사전 준비 작업
def GetNaverSearchResult(searchNode, searchText, pageStart, display): # 분류 시작/검색 기준
    baseurl = "https://openapi.naver.com/v1/search/" # 네이버에서 필수로 지정한 url
    nodedata = "%s.json" % searchNode # 뉴스를 가져오는데 결과는 json 파일 형식
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(searchText), #단어
                                                        pageStart , # 검색 시작점
                                                        display) #검색 결과 레코드 수
    url = baseurl + nodedata + parameters # 모든 것 합쳐서 URL 경로명 완성
    
    # 비정형(반정형) 가지고 온 초기 데이터(또는 정형일 수 있다) 
    reqDataResult = get_request_url(url) #가져오기 위해서 URL 완성 후 처리를 위한 함수 호출
    #reqDataResult : DataLake 저장
    if(reqDataResult == None): #결과가 있는지 없는지 화긴
        print("Data가 없습니다.")
        return None
    else:
        return json.loads(reqDataResult) # 데이터를 정형으로 변경함

def GetDateChange(data, jsonResult): # 데이터를 정제 하는 부분
    resultTitle = data['title']
    resultDesc = data['description']
    resultBlogLink = data['bloggerlink']
    naverLink = data['link']
    resultDate = data['postdate']
    jsonResult.append({ 'title': resultTitle, 
                        'description': resultDesc,
                        'link': naverLink,
                        'bloggerlink': resultBlogLink,
                        'postdate': resultDate})
    return 

def main(): # 정적언어 처럼 시작함수를 지정할 수 있다.
    jsonDataResult = []
    sNode = 'blog' #news / blog 항목을 선택 (move)
    sText = '메타버스'
    dCount = 100
    # 원시 데이터 가져옴(DataLake 에서 정형 데이터를 가져옴)
    jsonSearchResult = GetNaverSearchResult(sNode, sText, 1, dCount) # 결과 확인 하는 함수 호출

    #while ((jsonSearchResult != None) and (jsonSearchResult['display'] != 0)): #무한 루프 가능성 높음
    for data in jsonSearchResult['items']:
        GetDateChange(data, jsonDataResult)

    with open('%s_naver_%s.json' % (sText, sNode), 'w', encoding='utf-8') as filedata:
        rJson = json.dumps(jsonDataResult, 
                            indent=4,
                            sort_keys=True,
                            ensure_ascii=False )
        filedata.write(rJson)

    print('%s_naver_%s.json 저장완료' % ("메타버스", sNode))

if __name__ == '__main__':
    main()

    # __name__ : 내장변수 /  글로벌 변수 - 파이썬에서 정한(예약한) 이미 있는 변수
    # naverdata.py 일 경우 __name__ = naverdata (파일 이름)을 저장함
    # 이 파일 안에서 함수를 실행 - __main__ 값이 이미 정해져 있음 예약
    # 첫 실행하는 함수를 지정

      # 정제
    #if '' in tempData.key():
    #    xdata = tempData[0][0]
    #    ydata = tempData[0][0]-
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