import logging
import os.path as p
import subprocess

from datetime import datetime
from datetime import timedelta
from git import Repo


def get_commit_date(commit) -> str:
    commit_date = datetime.fromtimestamp(commit.committed_date)
    return str(commit_date.date())


def last_day(date: str) -> str:
    result = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)
    return datetime.strftime(result, '%Y-%m-%d')


class GitRepo:
    def __init__(self, repo_path: str = './'):
        self.repo_path = p.abspath(repo_path)
        if p.exists(self.repo_path + '/.git'):
            self.repo = Repo(self.repo_path)
            print('Current Repo: ', self.repo_path)
        else:
            logging.error('%s is not a valid path of repo!', self.repo_path)
            exit(0)

    def commit_info(self) -> list:
        dates_of_commit = list(map(get_commit_date, list(self.repo.iter_commits())))
        commits_per_day = [
            [date, dates_of_commit.count(date), self.hits_of_code(last_day(date), date)]
            for date in set(dates_of_commit)
        ]
        commits_per_day.sort(key=lambda _: list(_[0]), reverse=True)
        return commits_per_day

    def hits_of_code(self, start: str, before: str) -> int:
        hoc = subprocess.getoutput(
            f'hoc -s {start} -b {before} -d {self.repo_path}')
        try:
            return int(hoc)
        except ValueError as err:
            logging.error('Get hoc failed with error: %s', err)
            return 0

    def print_commit_info(self) -> None:
        commit_info = self.commit_info()
        print('\n   date    | commit |  hoc\n'.center(87, '-'))
        for daily_info in commit_info:
            print(daily_info[0], '|   ', daily_info[1], '  |  ', daily_info[2])
