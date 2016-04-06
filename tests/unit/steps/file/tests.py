import os
import tempfile
import shutil

from mock import Mock
from hamcrest import (
    assert_that,
    equal_to,
    has_entries
)

from testutils import (
    TestCase,
    BehaveStepsTestMixin,
    LettuceStepsTestMixin,
    StepsSentenceRegexTestMixin,
)
from cli_bdd.core.steps.file import base_steps
from cli_bdd.behave.steps import file as behave_file
from cli_bdd.lettuce.steps import file as lettuce_file


class FileStepsMixin(object):
    def test_copy_file_or_directory__file(self):
        original_file_path = os.path.join(tempfile.gettempdir(), 'file.txt')
        original_file_text = 'some text'
        new_file_path = os.path.join(tempfile.gettempdir(), 'new_file.txt')

        # add content to original file
        with open(original_file_path, 'wr') as ff:
            ff.write(original_file_text)

        try:
            os.remove(new_file_path)
        except OSError:
            pass

        self.execute_module_step(
            'copy_file_or_directory',
            kwargs={
                'file_or_directory': 'file',
                'source': original_file_path,
                'destination': new_file_path
            }
        )
        assert_that(os.path.exists(new_file_path), equal_to(True))
        assert_that(open(new_file_path).read(), equal_to(original_file_text))

    def test_copy_file_or_directory__directory(self):
        original_dir_path = os.path.join(tempfile.gettempdir(), 'original_dir/')
        original_subdir_path = os.path.join(
            original_dir_path, 'original_dir/subdir/'
        )
        original_subdir_path_file = os.path.join(
            original_subdir_path, 'file.txt'
        )
        original_subdir_path_file_path_content = 'some content'
        new_dir_path = os.path.join(tempfile.gettempdir(), 'new_dir/')

        try:
            shutil.rmtree(original_dir_path)
        except OSError:
            pass

        # create origin dir
        os.makedirs(original_subdir_path)

        # add content to original file
        with open(original_subdir_path_file, 'wr') as ff:
            ff.write(original_subdir_path_file_path_content)

        try:
            shutil.rmtree(new_dir_path)
        except OSError:
            pass

        self.execute_module_step(
            'copy_file_or_directory',
            kwargs={
                'file_or_directory': 'directory',
                'source': original_dir_path,
                'destination': new_dir_path
            }
        )
        assert_that(os.path.exists(original_subdir_path_file), equal_to(True))
        assert_that(
            open(original_subdir_path_file).read(),
            equal_to(original_subdir_path_file_path_content)
        )


class TestFileStepsSentenceRegex(StepsSentenceRegexTestMixin, TestCase):
    steps = base_steps
    step_experiments = {
        'copy_file_or_directory': [
            {
                'value': 'I copy a file "one.txt" to "two.txt"',
                'expected': {
                    'kwargs': {
                        'file_or_directory': 'file',
                        'source': 'one.txt',
                        'destination': 'two.txt'
                    }
                }
            }
        ],
    }


class TestFileBehaveSteps(BehaveStepsTestMixin,
                          FileStepsMixin,
                          TestCase):
    module = behave_file


class TestFileLettuceSteps(LettuceStepsTestMixin,
                           FileStepsMixin,
                           TestCase):
    module = lettuce_file
