# <Summary> 
# - URL 요청 클래스
# <remarks> - Client ID, Secret 변경가능

import urllib.request
import datetime
import json

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
    
    
# =============================================================================================

def GetNaverSearchResult(searchNode, searchText, pageStart, display):
    baseurl = "https://openapi.naver.com/v1/search/" 
    nodedata = "%s.json" % searchNode 
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(searchText), #단어
                                                        pageStart , # 검색 시작점
                                                        display) #검색 결과 레코드 수
    url = baseurl + nodedata + parameters # 모든 것 합쳐서 URL 경로명 완성
    
    reqDataResult = GetRequestUrl(url)
    if(reqDataResult == None): 
        print("Data가 없습니다.")
        return None
    else:
        return json.loads(reqDataResult) 

def GetDateChange(data, jsonResult): 
    resultTitle = data['title']
    resultDesc = data['description']
    resultOrgLink = data['originallink']
    naverLink = data['link']
    changeDate = datetime.datetime.strptime(data['pubDate'], 
                            '%a, %d %b %Y %H:%M:%S +0900')
    changeDateResult = changeDate.strftime('%Y-%m-%d  %H:%M:%S')
    jsonResult.append({ 'title':resultTitle, 
                        'description': resultDesc,
                        'link': naverLink,
                        'originallink': resultOrgLink,
                        'pubDate': changeDateResult})
    return 

def main(): 
    jsonDataResult = []
    sNode = 'news' #news / blog 항목을 선택 (move)
    sText = '메타버스'
    dCount = 100
    jsonSearchResult = GetNaverSearchResult(sNode, sText, dCount)

    
    for data in jsonSearchResult['items']:
        GetDateChange(data, jsonDataResult)

    with open('%s_naver_%s.json' % (sText, sNode), 'w', encoding='utf-8') as filedata:
        rJson = json.dumps(jsonDataResult, 
                            indent=4,
                            sort_keys=True,
                            ensure_ascii=False )
        filedata.write(rJson)

    print('%s_naver_%s.json 저장완료' % (sText, sNode))

if __name__ == '__main__':
    main()
