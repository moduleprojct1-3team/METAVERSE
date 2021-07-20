# <Summary> - URL 완성 및 초기데이터 로드 클래스
# <Remarks> - 없음

import json
import urllib.request
# <Summary> - URL 완성 및 초기데이터 로드 메서드
# <Remarks> - 없음
def GetNaverSearchResult(searchNode, searchText, pageStart, display): 
    baseurl ="https://openapi.naver.com/v1/search/" 
    nodedata ="%s.json" % searchNode 
    parameters = "?query=%s&start=%s&display=%s" %(urllib.parse.quote(searchText),
                                                                         pageStart, 
                                                                         display) 
                                                                         

    url = baseurl + nodedata + parameters 
    
    reqDataResult = get_request_url(url)
    
    if(reqDataResult == None): 
        print("Data가 없습니다.")
        return None
    else:
        return json.loads(reqDataResult) 