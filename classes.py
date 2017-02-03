from operator import attrgetter
from itertools import groupby


def distinct(sequence):
    seen = set()
    for s in sequence:
        if s not in seen:
            seen.add(s)
    return seen


def parse_array_of(arr, typ):
    """Safe parse to list of given type"""
    if arr is None:
        return []
    elif isinstance(arr, list):
        return [typ(**elem) for elem in arr]
    else:
        return [typ(**arr)]


class Standings(object):

    def __init__(self, contest):
        self.contest = Contest(**contest)

    def get_groups(self):
        groups = list(
            set([session.username.split(" ")[0]
                for session in self.contest.sessions]))
        groups = [gr[2:] for gr in groups if gr.startswith("гр")]
        return sorted(groups)


class Contest(object):

    def __init__(self, name, time, length, status, frozen, challenge, session=None):

        self.name = name
        self.time = time
        self.length = length
        self.status = status
        self.frozen = frozen
        self.problems = parse_array_of(challenge["problem"], Problem)
        self.problem_alias = dict(
            (problem.alias, problem.name) for problem in self.problems)
        # [Problem(**c) for c in challenge["problem"]]
        self.sessions = parse_array_of(session, Session)
        self.sessions.sort(key=attrgetter("solved"), reverse=True)
        # [Session(**s) for s in session]


class Problem(object):
    """ Contains short info about problem. Just alias and name."""

    def __init__(self, alias, name):
        self.alias = alias
        self.name = name


class Session(object):

    def __init__(
            self, id, party, alias, solved, penalty, time,
            accepted, attempts, score, problem):

        self.id = id
        self.username = party
        self.alias = alias
        self.solved = solved
        self.penalty = penalty
        self.time = time
        self.accepted = accepted
        self.attempts = attempts
        self.score = score
        self.submitted_problems = parse_array_of(problem, SubmittedProblem)
        self.solved = sum(
            [problem.accepted for problem in self.submitted_problems])
        # [SubmittedProblem(**p) for p in problem]
        self.group = "all"
        group = self.username.split(" ")[0]
        if group.startswith("гр"):
            self.group += " gr" + group[2:]


class SubmittedProblem(object):

    def __init__(
            self, alias, id, solved, penalty,
            time, accepted, attempts, score, run=None):

        self.id = id
        self.alias = alias
        self.solved = solved
        self.penalty = penalty
        self.time = time
        self.accepted = accepted
        self.attempts = attempts
        self.score = score
        self.runs = parse_array_of(run, Run)
        self.status = -attempts
        if (self.accepted == 1):
            self.status = "+" + (str(attempts) if attempts > 1 else "")
        elif self.attempts == 0:
            self.status = "."


class Run(object):

    def __init__(self, accepted, time):
        self.accepted = accepted
        self.time = time


class TotalUser(object):
    """ Contains information about all contests of user"""

    def __init__(self, group):
        # Take first argument of tuple - name
        self.name = group[0]
        elems = list(group[1])
        self.contestSolvedMap = {}
        self.solved = 0
        # second tuple element is count of solved problems in that contest
        # thired tuple element is name of contest
        for elem in elems:
            self.contestSolvedMap[elem[2]] = elem[1]
            self.solved += int(elem[1])
        self.group = "all"
        group = self.name.split(" ")[0]
        if group.startswith("гр"):
            self.group += " gr" + group[2:]


class TotalStandings(object):
    """ Contains information about all concatenated
        contests and list of participants."""

    def __init__(self, standings):
        self.tables = sorted(standings, key=lambda s: s.contest.name)
        participants = [
            (session.username, session.solved, table.contest.name)
            for table in standings
            for session in table.contest.sessions]

        keyFunc = lambda f: f[0]
        grouped = groupby(sorted(participants, key=keyFunc), keyFunc)
        totalUsers = [TotalUser(group) for group in grouped]
        self.participants = sorted(
            totalUsers, key=attrgetter("solved"), reverse=True)

    def get_groups(self):
        groups = list(
            set([user.name.split(" ")[0] for user in self.participants]))
        groups = [gr[2:] for gr in groups if gr.startswith("гр")]
        return sorted(groups)


def printGroupedData(groupedData):
    for k, v in groupedData:
        print("Group {} {}".format(k, list(v)))
