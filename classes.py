from operator import attrgetter


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


class Contest(object):

    def __init__(self, name, time, length, status, frozen, challenge, session):

        self.name = name
        self.time = time
        self.length = length
        self.status = status
        self.frozen = frozen
        self.problems = parse_array_of(challenge["problem"], Problem)
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


class TotalStandings(object):
    """ Contains information about all concatenated
        contests and list of participants."""

    def __init__(self):
        pass
