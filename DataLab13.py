#CSV: Comma(,) separated values
# import csv 이용해서 csv 파일 사용 : 기본 내장
# open mode에서 t/b 사용하지 않음 newline = 한줄씩 입력하겠다.
import csv
f = open(r'C:\Lab\DataLab\test.csv','w',encoding='utf-8',newline='')
csw = csv.writer(f)
csw.writerow([1,"홍길동","개발","서울"])
csw.writerow([2,"홍길동2","개발","서울2"])
f.close()


f = open(r'C:\Lab\DataLab\test.csv','r',encoding='utf-8')
csvr = csv.reader(f) #읽기 완료
for data in csvr:
    print(data)
f.close()
#tsv 파일은 Tab을 기준으로 데이터를 저장하는 파일(csv import)csv의 ,를 tab으로 바꿈
f = open(r'C:\Lab\DataLab\test.tsv','w',encoding='utf-8',newline='')
tsw = csv.writer(f,delimiter ='\t')
tsw.writerow([1,"홍길동","개발","서울"])
tsw.writerow([2,"홍길동2","개발","서울2"])
f.close()

f = open(r'C:\Lab\DataLab\test.csv','r',encoding='utf-8')
tsvr = csv.reader(f, delimiter = '\t') #읽기 완료
for data in csvr:
    print(data)
f.close()


