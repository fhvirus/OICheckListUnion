import requests
import re
from bs4 import BeautifulSoup

oichecklistIDs = [
    "8880bb3be4f63fb3df0ba3492e221fcdf3e99ee4",
    "f3c01fab33d4ca704dec6ff75ddfa2edf5f48447",
]

oichecklistLink = "https://oichecklist.pythonanywhere.com/view/" + oichecklistIDs[0]

page = requests.get(oichecklistLink)

soup = BeautifulSoup(page.text, 'html.parser')
header = soup.select('h1')
print (header)

ansiColor = [
    '\033[0;41m',
    '\033[0;43m',
    '\033[0;42m',
    '\033[0m'
]

def setOutput(stat, nl):
    if not nl:
        print(ansiColor[stat], end = '')
    else:
        print(ansiColor[stat])

import parseTable
import getIDs

# tableFile = open('table-sample.txt', 'r')
# tableText = tableFile.read()
# soup = BeautifulSoup(tableText, 'html.parser')

tableRows = soup.select('div.table-responsive > table > tr')
contests, IDtoProblem = parseTable.parseTable(tableRows)

for listID in oichecklistIDs:
    link = "https://oichecklist.pythonanywhere.com/view/" + listID
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    script = soup.select('script')[-1].text
    problemStatus = getIDs.getProblemStatus(script)
    for status, IDs in problemStatus.items():
        for ID in IDs:
            problem = IDtoProblem[ID]
            problem.status = status
            if contests[problem.contest][problem.year][problem.day].status == 2:
                contests[problem.contest][problem.year][problem.day].status = 1
    header = soup.select('h1')[0]
    print ('Parsed ' + header.text)

for contestName, years in contests.items():
    print (contestName)
    for year, days in years.items():
        print (year)
        for day, problems in days.items():
            setOutput(problems.status, False)
            print (problems, end = '')
            setOutput(3, True)
