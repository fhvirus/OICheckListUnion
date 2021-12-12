import requests
import re
from bs4 import BeautifulSoup

oichecklistIDs = [
    "8880bb3be4f63fb3df0ba3492e221fcdf3e99ee4",
    "f3c01fab33d4ca704dec6ff75ddfa2edf5f48447",
]


pages = []
for ID in oichecklistIDs:
    link = "https://oichecklist.pythonanywhere.com/view/" + ID
    pages.append(requests.get(link))

import parseTable
import getIDs

# tableFile = open('table-sample.txt', 'r')
# tableText = tableFile.read()
# soup = BeautifulSoup(tableText, 'html.parser')

soup0 = BeautifulSoup(pages[0].text, 'html.parser')
tableRows = soup0.select('div.table-responsive > table > tr')
contests, IDtoProblem = parseTable.parseTable(tableRows)

for page in pages:
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
    print ('Parsed ' + ' '.join(header.text.split()))

import os
width = os.get_terminal_size().columns
bar = '#' * width

for contestName, years in contests.items():
    print (bar)
    print (contestName.center(width))
    for year, days in years.items():
        row = ' '
        for day, problems in days.items():
            row += str(problems) + ' '
        print (row)
