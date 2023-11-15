import requests
from bs4 import BeautifulSoup
import json
import re

# NC State Board of Elections scraping

res = requests.get(
    'https://cf.ncsbe.gov/CFOrgLkup/ReportDetail/?RID=209911&TP=REC')

txt = res.text
status = res.status_code

soup = BeautifulSoup(res.content, 'html.parser')

page_title = soup.title.text

page_body = soup.body

page_head = soup.head

urlLine = page_body.find_all('a')[2]

print(urlLine)

"""
scripts = page_body.find_all("script")

script = scripts[12]

txt = str(script)

splitTxt = txt.split("\n")

data = splitTxt[8]

dataStrip = data.strip(" ")

index = 0
for i in range(len(dataStrip)):
    if dataStrip[index] == "[":
        break
    index += 1

dataString = dataStrip[index:]

data_list = json.loads(dataString)

for i in data_list:
    if i['DataType'] == 'DATA':
        print(i['ReportYear'], i['ReportType'])



# Download csv file from download link
url ='https://cf.ncsbe.gov/CFOrgLkup/ExportDetailResults/?ReportID=209911&Type=REC&Title=TRICIA%20COTHAM%20COMMITTEE%20-%202023%20Mid%20Year%20Semi-Annual'

r = requests.get(url)
filename = r.headers["Content-Disposition"].split('"')[1]

with open(filename, "wb") as f_out:
    print(f"Downloading {filename}")
    f_out.write(r.content)

"""
    
"""
1. Inital Site for candidate:
https://cf.ncsbe.gov/CFOrgLkup/CommitteeGeneralResult/? name = {Name} & useOrgName=True & useCandName=True & useInHouseName=True &useAcronym=False
https://cf.ncsbe.gov/CFOrgLkup/CommitteeGeneralResult/?name=Tricia%20Cotham&useOrgName=True&useCandName=True&useInHouseName=True&useAcronym=False

data from va data. Format example:
var data = [{"OrgName":"PAT COTHAM COMMITTEE (COTHAM, PAT (MECKLENBURG))","SBoEID":"MEC-901Y08-C-001","OldID":null,"CandName":"PATRICIA COTHAM","StatusDesc":"ACTIVE (NON-EXEMPT)","OrgGroupID":37824,"Link":null},
{"OrgName":"TRICIA COTHAM COMMITTEE (COTHAM, TRICIA)","SBoEID":"STA-07985B-C-002","OldID":null,"CandName":"PATRICIA ANN COTHAM (TRICIA)","StatusDesc":"ACTIVE (NON-EXEMPT)","OrgGroupID":48236,"Link":null},
{"OrgName":"TRICIA COTHAM COMM (COTHAM, TRICIA ANN)","SBoEID":"STA-07985B-C-001","OldID":null,"CandName":"TRICIA ANN COTHAM","StatusDesc":"CLOSED","OrgGroupID":11166,"Link":null}]

Page will be:
https://cf.ncsbe.gov/CFOrgLkup/DocumentGeneralResult/? SID = {SBoEID} & OGID= {OrgGroupID}

example:
https://cf.ncsbe.gov/CFOrgLkup/CommitteeGeneralResult/?name=Tricia%20cotham&useOrgName=True&useCandName=True&useInHouseName=True&useAcronym=False
->
https://cf.ncsbe.gov/CFOrgLkup/DocumentGeneralResult/?SID=STA-07985B-C-002&OGID=48236

2. Then, for every item WITH DATA:
https://cf.ncsbe.gov/CFOrgLkup/ReportSection/?RID=209911&SID=STA-07985B-C-002&CN=TRICIA%20COTHAM%20COMMITTEE&RN=2023%20Mid%20Year%20Semi-Annual

where format is:
https://cf.nscbe.gov/CFOrgLkup/ReportSection/? RID={DataLink} & SID={SboEID} & CN={CommitteeName} & RN={ReportYear + ReportType}

data is from var data. Format example:
{"CommitteeName":"TRICIA COTHAM COMMITTEE","SBoEID":"STA-07985B-C-002","ReportYear":2023,"DocumentType":"Disclosure Report",
 "ReportType":"Mid Year Semi-Annual","IsAmendment":"N","ImageReceiptDate":"07/29/2023","DataImportDate":"07/31/2023",
 "PeriodStartDate":"01/01/2023","PeriodEndDate":"06/30/2023","ImageType":"IMAGE","DataType":"DATA","DataLink":"209911",
 "ImageLink":"ViewDocumentImage/?DID=297093"}

3. From var data, go to Section Names (can potentially just go straight here instead of doing whole process in step 2? since just need RID):
"Detailed Receipts" &/or "Detailed Expenditures" based on what you want
{"SectionName":"Detailed Receipts","Count":40,"Link":"REC"},{"SectionName":"Detailed Expenditures","Count":23,"Link":"EXP"}

Link is: https://cf.ncsbe.gov/CFOrgLkup/ReportDetail/?RID=209911&TP=REC
where format is https://cf.ncsbe.gov/CFOrgLkup/ReportDetail/? RID={DataLink} & TP = {REC or EXP (link)}

https://cf.ncsbe.gov/CFOrgLkup/ExportDetailResults/?ReportID=197047&Type=REC&Title=Tricia%20Cotham%20Committee%20-%202022%20First%20Quarter

***
to  make a new path:
path = Path('path/to/dir')
path.mkdir(parents=True)

fpath = (path / 'filename').with_suffix('.csv')
with fpath.open(mode='w+') as csvfile:
    #csv write code

***
to update csv file:
with open(csv, "a") as infile:
    writer=csv.writer(infile)
    line = whatever
    writer.writerow(line)
"""

# Open Secrets scraping

"""
Example link: https://www.opensecrets.org/search?q=Richard+yercheck&type=donors

or order=desc&q=Ronald+jackson&sort=D&type=donors 

general template: https://www.opensecrets.org/search? order = desc & q= {NAME} & sort = D & type=donors

Note: Find a way to page through data?

res = requests.get(
    'https://www.opensecrets.org/search?q=Richard+yercheck&type=donors')

txt = res.text
status = res.status_code

soup = BeautifulSoup(res.content, 'html.parser')

page_title = soup.title.text

page_body = soup.body

page_head = soup.head

tbl = soup.find_all('tbody')
for recipient in soup.find_all('tbody'):
    trs = (recipient.find_all('tr'))
    for tr in trs:
        print("\nprinting tr")
        tds = tr.find_all('td')
        indx = 0
        for td in tds:
            txt = (td.get_text()).strip()
            if indx == 1:
                txt = txt.replace("\t", "")
                print(txt.split("\n"))
            print('index = ' + str(indx))
            print(txt)
            indx += 1

For tds:
[2] = Name, address
[4] = date
[5] = amount
[6] = recipient (name, party)
[7] = state

YERCHECK, RICHARD
                                                                                MONROE, NC 28110
"""
