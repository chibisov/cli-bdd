import os
import subprocess

from hamcrest import assert_that, equal_to

from testutils import TestCase

BASE_PATH = os.path.dirname(os.path.normpath(__file__))
FEATURES_PATH = os.path.join(BASE_PATH, 'features/')


class TestBehaveFunctional(TestCase):
    def test_me(self):
        stdout = subprocess.Popen(
            'behave %s -v' % FEATURES_PATH,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()[0].strip()
        stdout_lines = stdout.split('\n')
        assert_that(
            stdout_lines[-4],
            equal_to('1 feature passed, 0 failed, 0 skipped'),
            stdout
        )
        assert_that(
            stdout_lines[-3],
            equal_to('1 scenario passed, 0 failed, 0 skipped'),
            stdout
        )
        assert_that(
            stdout_lines[-2],
            equal_to('7 steps passed, 0 failed, 0 skipped, 0 undefined'),
            stdout
        )
