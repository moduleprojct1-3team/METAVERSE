import urllib.request
import datetime
import json
import pandas as pd


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
    resultTitle = data['title'].replace("<b>", "*").replace("</b>", "*")
    resultDesc = data['description'].replace("<b>", "*").replace("</b>", "*")
    resultOrgLink = data['originallink']
    naverLink = data['link']
    changeDate = datetime.datetime.strptime(data['pubDate'], 
                            '%a, %d %b %Y %H:%M:%S +0900')
    changeDateResult = changeDate.strftime('%Y-%m-%d  %H:%M:%S')
    jsonResult.append({ '제목':resultTitle, 
                        '내용': resultDesc,
                        'link': naverLink,
                        'originallink': resultOrgLink,
                        '날짜': changeDateResult})
    return 


def GetBlogDateChange(data, jsonResult):
    resultTitle = data['title'].replace("<b>", "*").replace("</b>", "*")
    resultDesc = data['description'].replace("<b>", "*").replace("</b>", "*")
    resultBlogLink = data['bloggerlink']
    naverLink = data['link']
    resultDate = data['postdate']
    jsonResult.append({ '제목': resultTitle, 
                        '내용': resultDesc,
                        'link': naverLink,
                        'bloggerlink': resultBlogLink,
                        '날짜': resultDate})
    return 


def GetCafeDateChange(data, jsonResult):
    resultTitle = data['title'].replace("<b>", "*").replace("</b>", "*")
    resultDesc = data['description'].replace("<b>", "*").replace("</b>", "*")
    resultCafeurl = data['cafeurl']
    naverLink = data['link']
    jsonResult.append({ '제목': resultTitle, 
                        '내용': resultDesc,
                        'link': naverLink,
                        'cafeurl': resultCafeurl})
    return 


def main():
    jsonDataResult1 = []
    jsonDataResult2 = []
    jsonDataResult3 = []

    #sNode = ['news', 'blog', 'cafearticle']
    sText = '메타버스'
    dCount = 100
    jsonSearchResult1 = {}
    jsonSearchResult2 = {}
    jsonSearchResult3 = {}
    
    #for node in sNode:

    jsonSearchResult1= GetNaverSearchResult('news', sText, 1, dCount)
    jsonSearchResult2= GetNaverSearchResult('blog', sText, 1, dCount)
    jsonSearchResult3 =GetNaverSearchResult('cafearticle', sText, 1, dCount)

    #if node == "news":
    for data in jsonSearchResult1['items']:
             GetNewsDateChange(data, jsonDataResult1)
    #elif node == "blog":
    for data in jsonSearchResult2['items']:
             GetBlogDateChange(data, jsonDataResult2)
    #elif node == "cafearticle":
    for data in jsonSearchResult3['items']:
             GetCafeDateChange(data, jsonDataResult3)
        
    
    
    with open('통합연습2.json', 'w', encoding= 'utf-8') as filedata:
       # if 'items' in jsonSearchResult1.keys():
            # tempData = pd.DataFrame(jsonSearchResult['items'][0]['title']['pubDate']['description']['link']['originallink'])
            News = pd.DataFrame(jsonDataResult1, columns= ['제목', '내용','날짜', 'link', 'originallink'])
            Blog = pd.DataFrame(jsonDataResult2, columns= ['제목', '내용','날짜', 'link'])
            Cafe = pd.DataFrame(jsonDataResult3, columns= ['제목', '내용', 'link'])
    with pd.ExcelWriter('메타.xlsx') as writer: 
                News.to_excel(writer, sheet_name = 'News')
                Blog.to_excel(writer, sheet_name = 'Blog')
                Cafe.to_excel(writer, sheet_name = 'Cafe')
            #temp = temp.to_json(force_ascii=False, indent=4)
        # rjson = json.dumps(jsonTotalData, indent=4, sort_keys=True, ensure_ascii=False)
        #filedata.write(temp)
    

if __name__ == '__main__':
    main()