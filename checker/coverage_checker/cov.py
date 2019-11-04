import os.path as p
import subprocess


class Coverage:
    def __init__(self, repo_path: str = './'):
        self.repo_path = p.abspath(repo_path)

    def coverage_rate(self) -> int:
        rate = subprocess.getoutput(f'{p.dirname(p.abspath(__file__))}/cov.sh {self.repo_path}')
        try:
            return int(rate)
        except ValueError:
            return int(-1)


if __name__ == '__main__':
    print(Coverage('/Users/xinyuzhang/Vivian/CityU/SoftwareEngineering/Project7/Codes/repo_for_test').coverage_rate())
