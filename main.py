import requests, json
from bs4 import BeautifulSoup
import os

def run():
    name = input("Enter name of official: ")
    nameURL = name.replace(" ", "%20")
    nameFile = name.replace(" ", "_")

    # Query Name of Committee
    queryUrl = f"https://cf.ncsbe.gov/CFOrgLkup/CommitteeGeneralResult/?name={nameURL}&useOrgName=True&useCandName=True&useInHouseName=True&useAcronym=False"
    actives = pullData(queryUrl, "comSearch")

    # Select Committee
    print('')
    num = 1
    for com in actives:
        print(str(num) + ": " + com['OrgName'])
        num += 1
    chosen = int(input("\nEnter number of correct committee: "))

    committeeData = actives[chosen-1]

    # Collect Relevant Reports
    sid = committeeData['SBoEID']
    ogid = committeeData['OrgGroupID']
    committeeURL = f"https://cf.ncsbe.gov/CFOrgLkup/DocumentGeneralResult/?SID={sid}&OGID={ogid}"

    allReports = pullData(committeeURL, 'allReps')

    for report in allReports:
        rid = report['DataLink']
        scrapeReports(rid, nameFile)
    

def pullData(url, step):
    steps = {'comSearch': 11, 'allReps': 12}
    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    page_body = soup.body

    scripts = page_body.find_all("script")
    script = scripts[steps[step]]

    txt = str(script)
    splitTxt = txt.split("\n")
    data = splitTxt[8]
    dataStrip = data.strip(" ")

    for i in range(len(dataStrip)):
        if dataStrip[i] == "[":
            index = i
            break
    
    dataString = dataStrip[index:]
    data_list = json.loads(dataString)

    stepParams = {'comSearch': "StatusDesc", 'allReps': "DataType"}
    stepBools = {'comSearch': "ACTIVE (NON-EXEMPT)", 'allReps': "DATA"}

    ret = []
    for i in data_list:
        if i[stepParams[step]] == stepBools[step]:
            ret.append(i)
    return ret


def scrapeReports(rid, name):

    for suffix in ['REC', 'EXP']:
        url = f"https://cf.ncsbe.gov/CFOrgLkup/ReportDetail/?RID={rid}&TP=" + suffix

        soup = BeautifulSoup((requests.get(url)).content, 'html.parser').body
        htmldata = soup.find_all('a')[2]

        downloadURL = "https://cf.ncsbe.gov/" + htmldata['href']
        downloadCSV(downloadURL, name, suffix)
        

def downloadCSV(url, name, repType):
    filename = name + repType

    if not os.path.exists(filename):   
        with open(filename, "wb") as f:
            pass
    
    response = requests.get(url)
    csvName = response.headers["Content-Disposition"].split('"')[1]
    content = response.content

    with open(filename, 'wb') as f:
        print(f"Downloading {csvName}")
        f.write(content)


if __name__ == '__main__':
    run()