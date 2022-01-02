from orm import RecordInfo, RecordList, RecordVer

query = list(RecordInfo.select())
for i in query:
    print(i.rid)
    pass