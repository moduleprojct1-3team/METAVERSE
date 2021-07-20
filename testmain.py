import urllib.request
import datetime
import json

def main(): # 정적언어 처럼 시작함수를 지정할 수 있다.
    jsonDataResult = []
    sNode = 'cafearticle' #news / blog 항목을 선택 (move)
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

    print('%s_naver_%s.json 저장완료' % (sText, sNode))