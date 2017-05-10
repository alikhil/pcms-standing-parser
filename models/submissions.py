from datetime import datetime
import config


def get_submissions(total_standings, range_p, group):
    """Getting submissions from total standings"""
    submissions = list()
    for table in total_standings.tables:
        for session in table.contest.sessions:
            for problem in session.submitted_problems:
                for run in problem.runs:
                    problem.name = table.contest.problem_alias[problem.alias]
                    submissions.append(Submission(
                        session.username, run, problem, table.contest.name))
    sorted_ = sorted(submissions, key=lambda s: s.unix_time, reverse=True)
    if group is not None:
        sorted_ = [sub for sub in sorted_ if sub.username.startswith(group)]

    if range_p is None:
        return sorted_

    start, end = range_p
    return [sub for sub in sorted_
            if sub.unix_time >= start and sub.unix_time <= end]


class Submission:
    """Entity in submission list"""

    def __init__(self, username, run, problem, contest_name):
        self.username = username
        self.unix_time = (run.time + config.CONTESTS_START_TIME) / 1000
        self.problem_alias = problem.alias
        self.status = "success" if run.accepted == "yes" else ""
        self.problem_name = problem.name
        self.date = datetime.fromtimestamp(
            self.unix_time).strftime("%d.%m.%Y %H:%M")
        self.contest_name = contest_name
        self.day = datetime.fromtimestamp(self.unix_time).strftime("%d-%m-%Y")
        self.month = datetime.fromtimestamp(self.unix_time).strftime("%m-%Y")
