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


def GetNewsDateChange(data, jsonResult):
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


def GetBlogDateChange(data, jsonResult):
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


def GetCafeDateChange(data, jsonResult):
    resultTitle = data['title']
    resultDesc = data['description']
    resultCafeurl = data['cafeurl']
    naverLink = data['link']
    jsonResult.append({ 'title': resultTitle, 
                        'description': resultDesc,
                        'link': naverLink,
                        'cafeurl': resultCafeurl})
    return 


def main():
    jsonDataResult1 = []
    jsonDataResult2 = []
    jsonDataResult3 = []

    sNode = ['news', 'blog', 'cafearticle']
    sText = '메타버스'
    dCount = 100

    for node in sNode:

        jsonSearchResult = GetNaverSearchResult(node, sText, 1, dCount)

        if node == "news":
            for data in jsonSearchResult['items']:
                GetNewsDateChange(data, jsonDataResult1)
        elif node == "blog":
            for data in jsonSearchResult['items']:
                GetBlogDateChange(data, jsonDataResult2)
        elif node == "cafearticle":
            for data in jsonSearchResult['items']:
                GetCafeDateChange(data, jsonDataResult3)
        
    jsonTotalData = jsonDataResult1 + jsonDataResult2 + jsonDataResult3
    
    with open('통합연습2.json', 'w', encoding= 'utf-8') as filedata:
        rjson = json.dumps(jsonTotalData, indent=4, sort_keys=True, ensure_ascii=False)
        filedata.write(rjson)
    

if __name__ == '__main__':
    main()