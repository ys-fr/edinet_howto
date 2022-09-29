import pandas as pd
import datetime
import requests
import sys

# 0: start year, 1: start month, 2: start day
# 3: end year  , 4: end month  , 5: end day
# 6: FilePath


key = sys.args
# 最大で現在から5年前までのデータを入手することが出来る
# startには、ほしいデータの始点（最大3年前の日付）
# endには　、ほしいデータの終点（現在まで入力可能）
start = datetime.date(int(key[0]),int(key[1]),int(key[2]) );end = datetime.date(int(key[3]),int(key[4]),int(key[5]))

Day = []
dt = datetime.timedelta(days=1)
for d in range((end-start).days+1):
    start += dt
    Day.append(start)
    pass


avail_docs =[]
tmp = []
# data structure
# 0: date, 1: company name, 2: doc name
# 1:Date, 2:Company, 3:CompanyID, 4:ordinanceCode, 5:formCode
# 6:docTypeCode, 7:docID, 8:AvailableData_StartPeriod, 9: AvailableData_EndPeriod, 10:Available:xbrl, 11: Available:pdfFlag
for day in Day:
    respon = requests.get("https://disclosure.edinet-fsa.go.jp/api/v1/documents.json", params= {"date": day, "type": 2}).json()
    if respon["metadata"]["status"]!="404":
        for res in respon["results"]:
            tmp = res
            ordinance_code= res["ordinanceCode"]
            form_code= res["formCode"]
            avail_docs.append([ day, res["filerName"] ,res["secCode"], 
                               res["ordinanceCode"],  res["formCode"],  res["docTypeCode"] ,res["docID"],
                               res["periodStart"],res["periodEnd"],
                               res["xbrlFlag"],res["pdfFlag"],
                               ].copy()
                              )
            pass
        pass
    pass

avail_docs = pd.DataFrame(avail_docs)
avail_docs.columns = ["Date", "Company", "CompanyID", 
                      "ordinanceCode", "formCode", "docTypeCode", "docID",
                      "AvailableData_StartPeriod","AvailableData_EndPeriod","Available:xbrl","Available:pdfFlag"]
avail_docs.to_csv(key[-1],index=None)