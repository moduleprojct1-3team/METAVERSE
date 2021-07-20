import urllib.request
import datetime
import json


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


#크롤러로 데이터 가져오기 전 분류 / 인증 절차 등 사전 준비 작업
def GetNaverSearchResult(searchNode, searchText, pageStart, display):
    baseurl = "https://openapi.naver.com/v1/search/"
    nodedata = "%s.json" % searchNode 
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(searchText),
                                                        pageStart ,
                                                        display)
    url = baseurl + nodedata + parameters 
    
    
    reqDataResult = get_request_url(url)
    
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
    sNode = 'news'
    sText = '메타버스'
    dCount = 100
    jsonSearchResult = GetNaverSearchResult(sNode, sText, 1, dCount)

 
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
