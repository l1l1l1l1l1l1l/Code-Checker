import unittest
import coverage
import os.path as p

from coverage import CoverageException


class Coverage:
    def __init__(self, repo_path: str = './'):
        self.repo_path = p.abspath(repo_path)

    def coverage_rate(self, output_path: str = './coverage_details') -> int:
        loader = unittest.TestLoader()
        start_dir = self.repo_path
        suite = loader.discover(start_dir, pattern='*_tests.py')

        runner = unittest.TextTestRunner()

        cov = coverage.coverage()
        cov.start()

        runner.run(suite)

        cov.stop()
        cov.save()
        try:
            return cov.html_report(directory=output_path)
        except CoverageException:
            return 0


if __name__ == '__main__':
    print(Coverage(f'{p.dirname(p.abspath(__file__))}/../../').coverage_rate())
