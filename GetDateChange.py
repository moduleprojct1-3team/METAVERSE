from GetNaverSearchResult import GetNaverSearchResult
import json

def GetDateChange(data, jsonResult): # 데이터를 정제 하는 부분
    resultTitle = data['title']
    resultDesc = data['description']
    resultOrgLink = data['originallink']
    naverLink = data['link']
    changeDate = datetime.datetime.strptime(data['pubDate'], 
                            '%a, %d %b %Y %H:%M:%S +0900')#표시형식
    changeDateResult = changeDate.strftime('%Y-%m-%d  %H:%M:%S') #변경 : 년-월-일 시:분:초
    jsonResult.append({ 'title':resultTitle, 
                        'description': resultDesc,
                        'link': naverLink,
                        'originallink': resultOrgLink,
                        'pubDate': changeDateResult})