import logging
import os.path as p

from datetime import datetime
from git import Repo


def get_commit_date(commit) -> str:
    commit_date = datetime.fromtimestamp(commit.committed_date)
    return str(commit_date.date())


class GitRepo:
    def __init__(self, repo_path: str = './'):
        repo_path = p.abspath(repo_path)
        if p.exists(repo_path + '/.git'):
            self.repo = Repo(repo_path)
            print('Current Repo: ', repo_path)
        else:
            logging.error('%s is not a valid path of repo!', repo_path)
            exit(0)

    def calculate_commits(self) -> list:
        dates_of_commit = list(map(get_commit_date, list(self.repo.iter_commits())))
        commits_per_day = [
            {date: dates_of_commit.count(date)} for date in set(dates_of_commit)
        ]
        commits_per_day.sort(key=lambda d: list(d.keys())[0], reverse=True)
        return commits_per_day
