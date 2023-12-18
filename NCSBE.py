import requests, json
from bs4 import BeautifulSoup
import os
import csv

# Relevant functions for grabbing information from NCSBE data collections.

def run():
    # Runs a search for candidate committee financial reports. Queries input of a name, then searches NCSBE reports to compile the reports into a
    # receipts and expenditures file in the data folder. Does not currently check for duplicates; implement once database integrated.
    # Works for both candidate committees and NC-based PACs.

    name = input("Enter last name of official: ").lower()
    nameURL = name.replace(" ", "%20")

    # Query Name of Committee
    queryUrl = f"https://cf.ncsbe.gov/CFOrgLkup/CommitteeGeneralResult/?name={nameURL}&useOrgName=True&useCandName=True&useInHouseName=True&useAcronym=False"
    actives = pullData(queryUrl, "comSearch")

    # Select Committee
    if len(actives) > 0:
        if len(actives)==1:
            chosen = 1
        else:
            print('')
            num = 1
            for com in actives:
                print(str(num) + ": " + com['OrgName'])
                num += 1
            chosen = int(input("\nEnter number of correct committee: "))
    else:
        print("No committees found")
        return

    # Properly reformat organization name to be used in search
    committeeData = actives[chosen-1]
    orgName = str(committeeData['OrgName'])
    orgName = orgName.replace(" ", "_")
    for char in ["(", ")",]:
        orgName= orgName.replace(char, "")

    # Collect Relevant Reports
    sid = committeeData['SBoEID']
    ogid = committeeData['OrgGroupID']
    committeeURL = f"https://cf.ncsbe.gov/CFOrgLkup/DocumentGeneralResult/?SID={sid}&OGID={ogid}"

    # Adds all relevant reports to a list to be compiled
    allReports = pullData(committeeURL, 'allReps')

    # Call scrapeReports, which pull the relevant data from receipt and expenditure reports to be downloaded as a CSV
    for report in allReports:
        rid = report['DataLink']
        scrapeReports(rid, orgName)
    

def pullData(url, step):
    # Creates a list of all the active reports that should be downloaded to CSV.

    # Pull list of relevant reports for the committee
    steps = {'comSearch': 11, 'allReps': 12}
    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    page_body = soup.body

    # Parse webpage to identify the correct data
    scripts = page_body.find_all("script")
    script = scripts[steps[step]]

    txt = str(script)
    splitTxt = txt.split("\n")
    data = splitTxt[8]
    dataStrip = data.strip(" ")

    # Reformate data to be accurately collected
    for i in range(len(dataStrip)):
        if dataStrip[i] == "[":
            index = i
            break
    
    dataString = dataStrip[index:]
    data_list = json.loads(dataString)

    stepParams = {'comSearch': "StatusDesc", 'allReps': "DataType"}
    stepBools = {'comSearch': "ACTIVE (NON-EXEMPT)", 'allReps': "DATA"}

    # For each pulled report, add it to the list if it's Active and has Data
    ret = []
    for i in data_list:
        if i[stepParams[step]] == stepBools[step]:
            ret.append(i)
    return ret


def scrapeReports(rid, orgName):
    #Function that scrapes all mindivudal reports for a committee, receipts and expenditures.

    for suffix in ['REC', 'EXP']:
        url = f"https://cf.ncsbe.gov/CFOrgLkup/ReportDetail/?RID={rid}&TP=" + suffix

        try:
            response = requests.get(url)
            if response.status_code ==200:
                soup = BeautifulSoup((requests.get(url)).content, 'html.parser').body
                htmldata = soup.find_all('a')[2]

                # Download the report as a CSV, add it to aggreated receipts or expenditures CSV
                downloadURL = "https://cf.ncsbe.gov/" + htmldata['href']
                downloadCSV(downloadURL, suffix, orgName)
            else:
                print(f"Failed to fetch data for {suffix}")
        except Exception as e:
            print(f"Error occured: {e}")


def downloadCSV(url, repType, orgName):
    # Downlaods a chosen report to the relevant csv. URL is report download url, repType is REC or EXP, orgName is committee name.
    folder_name = "data"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = os.path.join(folder_name, orgName + "_" + repType + ".csv")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            csvName = response.headers["Content-Disposition"].split('"')[1]
            content = response.content

            mode = 'a' if os.path.exists(filename) else 'w'
            
            with open(filename, mode, newline ='') as f:
                start = 2
                if mode == 'w':
                    start = 1
            
                # Read content with CSV reader and write to file
                csv_data = content.decode('utf-8').splitlines()
                csv_writer = csv.writer(f)
                for row in csv_data[start:-1]:
                    csv_writer.writerow(row.split(','))

                if start == 1:
                    print(f"Data {csvName} written to {filename}")

                else:
                    print(f"Data {csvName} appended {filename}")
    
        else:
            print(f"Failed to download CSV for {url}")
    
    except Exception as e:
        print(f"Error downloading {url} CSV: {e}")

if __name__ == '__main__':
    run()