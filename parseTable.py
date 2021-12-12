import re

# Status:
# 0 - Not Available
# 1 - Solved / Seen / Known
# 2 - Unsolved

class Problem:
    def __init__(self, ID, name, status, contest, year, day):
        self.ID = ID
        self.name = name
        self.status = status
        self.contest = contest
        self.year = year
        self.day = day

class Contest:
    def __init__(self, name, year, Type, day, problems):
        self.name = name
        self.year = year
        self.Type = Type
        self.day = day
        self.problems = problems
        self.status = 2
    def __str__(self):
        res = self.name + ' ' + self.year
        if self.Type == 1:
            res += ' Round ' + str(self.day)
        elif self.Type == 2:
            res += ' Day ' + str(self.day)
        return res


def parseTable(tableRows):
    contests = dict()
    IDtoProblem = dict()

    contestTitlePattern = re.compile(r"(.*) (\d+)$")

    for contest in tableRows :
        title = contest.select('td:nth-child(1) > a')[0]
        match = contestTitlePattern.findall(title.text)[0]
        contestName, contestYear = match
        # print ('\033[1m')
        # print ('[ ' + contestName + ' ' + contestYear + ' ]')
        # print ('\033[0m')

        if contests.get(contestName) == None:
            contests[contestName] = dict()
        if contests[contestName].get(contestYear) == None:
            contests[contestName][contestYear] = dict()

        current = contests[contestName][contestYear]

        problems = contest.find_all('td', {"data-toggle": "popover"})

        # Type:
        # 0 - Single contest
        # 1 - Multiple round
        # 2 - Multiple day
        contestType = 0
        sample = problems[0]['data-title'].split()
        if sample[2] == 'Round' :
            contestType = 1
        elif sample[2] == 'Day' :
            contestType = 2

        lastDay = 0
        for problem in problems:
            ID = int(problem['id'])
            name = "".join(problem.text.split())

            status = 0
            if problem['class'][0] == 'table-light' :
                status = 2

            day = 0
            if contestType != 0:
                day = int(problem['data-title'].split()[3].rstrip(':'))

            obj = Problem(ID, name, status, contestName, contestYear, day)
            IDtoProblem[ID] = obj

            if current.get(day) == None:
                current[day] = Contest(contestName, contestYear, contestType, day, [])
            current[day].problems.append(ID)

            if day != lastDay :
                lastDay = day

    print ("Done parsing")

    for ID, problem in IDtoProblem.items():
        if problem.status == 0:
            contests[problem.contest][problem.year][problem.day].status = 0

    return contests, IDtoProblem
