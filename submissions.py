import config
from datetime import datetime


def get_submissions(totalStandings):
    """Getting submissions from total standings"""
    submissions = list()
    for table in totalStandings.tables:
        for session in table.contest.sessions:
            for problem in session.submitted_problems:
                for run in problem.runs:
                    problem.name = table.contest.problem_alias[problem.alias]
                    submissions.append(Submission(
                        session.username, run, problem, table.contest.name))
    return sorted(submissions, key=lambda s: s.unix_time, reverse=True)


class Submission:
    """Entity in submission list"""

    def __init__(self, username, run, problem, contest_name):
        self.username = username
        self.unix_time = run.time + config.CONTESTS_START_TIME
        self.problem_alias = problem.alias
        self.status = "success" if run.accepted == "yes" else ""
        self.problem_name = problem.name
        self.date = datetime.fromtimestamp(
            self.unix_time / 1000).strftime("%d.%m.%Y %H:%M")
        self.contest_name = contest_name
