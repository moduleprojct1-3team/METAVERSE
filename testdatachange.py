

def GetDateChange(data, jsonResult): # 데이터를 정제 하는 부분
    resultTitle = data['title']
    resultDesc = data['description']
    resultCafeurl = data['cafeurl']
    naverLink = data['link']
    jsonResult.append({ 'title': resultTitle, 
                        'description': resultDesc,
                        'link': naverLink,
                        'cafeurl': resultCafeurl})
    return 