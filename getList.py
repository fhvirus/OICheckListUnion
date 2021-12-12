import requests
import re
import threading
from bs4 import BeautifulSoup

oichecklistIDs = [
    "8880bb3be4f63fb3df0ba3492e221fcdf3e99ee4",
    "f3c01fab33d4ca704dec6ff75ddfa2edf5f48447",
]

pages = []
def getPage(ID):
    link = "https://oichecklist.pythonanywhere.com/view/" + ID
    pages.append(requests.get(link))

threads = []
for idx, ID in enumerate(oichecklistIDs):
    threads.append(threading.Thread(target = getPage, args = (ID, )))
    threads[idx].start()

for thread in threads:
    thread.join()

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

makeMashup = input('Make a mashup? (Y/n) ')
if makeMashup == 'n' or makeMashup == 'N':
    exit()

contest = input('Which contest(s) do you prefer? (ZCK for all) ')
allContest = (contest == 'ZCK')
contestList = []
if not allContest:
    contestList = contest.split()

yearRange = input('What\'s your preferred year range? (ZCK for all) ')
allYear = (yearRange == 'ZCK')
minYear = 0
maxYear = 0
if not allYear:
    yearRange = yearRange.split()
    minYear = int(yearRange[0])
    maxYear = int(yearRange[1])

probNum = int(input('How many problems do you want? '))

import random
unsolved = []
for ID, problem in IDtoProblem.items():
    if not (allContest or problem.contest in contestList):
        continue
    if not (allYear or (minYear <= problem.year and problem.year <= maxYear)):
        continue
    if problem.status == 2:
        unsolved.append(problem)
random.shuffle(unsolved)

if probNum <= len(unsolved):
    print ('Mashup: ')
    for problem in unsolved[0 : probNum]:
        print (problem)
else:
    print ('You\'re too strong. No more OI problems for you!')
