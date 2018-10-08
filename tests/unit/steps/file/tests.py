import os
import shutil
import tempfile

from hamcrest import assert_that, calling, equal_to, is_not, raises

from cli_bdd.behave.steps import file as behave_file
from cli_bdd.core.steps.file import base_steps
from testutils import (
    BehaveStepsTestMixin,
    StepsSentenceRegexTestMixin,
    TestCase
)


class FileStepsMixin(object):
    def test_copy_file_or_directory__file(self):
        original_file_path = os.path.join(tempfile.gettempdir(), 'file.txt')
        original_file_text = 'some text'
        new_file_path = os.path.join(tempfile.gettempdir(), 'new_file.txt')

        # add content to original file
        with open(original_file_path, 'w+') as ff:
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
        original_dir_path = os.path.join(
            tempfile.gettempdir(),
            'original_dir/'
        )
        original_subdir_path = os.path.join(original_dir_path, 'subdir/')
        original_subdir_path_file = os.path.join(
            original_subdir_path, 'file.txt'
        )
        original_subdir_path_file_content = 'some content'
        new_dir_path = os.path.join(tempfile.gettempdir(), 'new_dir/')
        new_subdir_path_file = os.path.join(
            new_dir_path, 'subdir/file.txt'
        )

        try:
            shutil.rmtree(original_dir_path)
        except OSError:
            pass

        # create origin dir
        os.makedirs(original_subdir_path)

        # add content to original file
        with open(original_subdir_path_file, 'w+') as ff:
            ff.write(original_subdir_path_file_content)

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
            open(new_subdir_path_file).read(),
            equal_to(original_subdir_path_file_content)
        )

    def test_move_file_or_directory__file(self):
        original_file_path = os.path.join(tempfile.gettempdir(), 'file.txt')
        original_file_text = 'some text'
        new_file_path = os.path.join(tempfile.gettempdir(), 'new_file.txt')

        # add content to original file
        with open(original_file_path, 'w+') as ff:
            ff.write(original_file_text)

        try:
            os.remove(new_file_path)
        except OSError:
            pass

        self.execute_module_step(
            'move_file_or_directory',
            kwargs={
                'file_or_directory': 'file',
                'source': original_file_path,
                'destination': new_file_path
            }
        )
        assert_that(os.path.exists(original_file_path), equal_to(False))
        assert_that(os.path.exists(new_file_path), equal_to(True))
        assert_that(open(new_file_path).read(), equal_to(original_file_text))

    def test_move_file_or_directory__directory(self):
        original_dir_path = os.path.join(
            tempfile.gettempdir(),
            'original_dir/'
        )
        original_subdir_path = os.path.join(original_dir_path, 'subdir/')
        original_subdir_path_file = os.path.join(
            original_subdir_path, 'file.txt'
        )
        original_subdir_path_file_content = 'some content'
        new_dir_path = os.path.join(tempfile.gettempdir(), 'new_dir/')
        new_subdir_path_file = os.path.join(
            new_dir_path, 'subdir/file.txt'
        )

        try:
            shutil.rmtree(original_dir_path)
        except OSError:
            pass

        # create origin dir
        os.makedirs(original_subdir_path)

        # add content to original file
        with open(original_subdir_path_file, 'w+') as ff:
            ff.write(original_subdir_path_file_content)

        try:
            shutil.rmtree(new_dir_path)
        except OSError:
            pass

        self.execute_module_step(
            'move_file_or_directory',
            kwargs={
                'file_or_directory': 'directory',
                'source': original_dir_path,
                'destination': new_dir_path
            }
        )
        assert_that(os.path.exists(original_dir_path), equal_to(False))
        assert_that(os.path.exists(original_subdir_path_file), equal_to(False))
        assert_that(
            open(new_subdir_path_file).read(),
            equal_to(original_subdir_path_file_content)
        )

    def test_create_directory(self):
        dir_path = os.path.join(tempfile.gettempdir(), 'some_dir/')

        try:
            shutil.rmtree(dir_path)
        except OSError:
            pass

        self.execute_module_step(
            'create_directory',
            kwargs={
                'dir_path': dir_path
            }
        )
        assert_that(os.path.exists(dir_path), equal_to(True))
        assert_that(os.path.isdir(dir_path), equal_to(True))

        # test if directory already exists
        assert_that(
            calling(self.execute_module_step).with_args(
                'create_directory',
                kwargs={
                    'dir_path': dir_path
                }
            ),
            is_not(
                raises(OSError)
            )
        )
        assert_that(os.path.exists(dir_path), equal_to(True))
        assert_that(os.path.isdir(dir_path), equal_to(True))

    def test_change_directory(self):
        old_path = os.getcwd()
        try:
            dir_path = os.path.realpath('/tmp/')
            self.execute_module_step(
                'change_directory',
                kwargs={
                    'dir_path': dir_path
                }
            )

            assert_that(os.getcwd(), equal_to(dir_path))
        finally:
            os.chdir(old_path)

    def test_create_file_with_content(self):
        file_path = os.path.join(tempfile.gettempdir(), 'file.txt')
        content = 'hello world'

        try:
            os.remove(file_path)
        except OSError:
            pass

        self.execute_module_step(
            'create_file_with_content',
            kwargs={
                'file_path': file_path,
                'file_content': content,
            }
        )
        assert_that(os.path.exists(file_path), equal_to(True))
        assert_that(open(file_path).read(), equal_to(content))

        # test when file already exists
        self.execute_module_step(
            'create_file_with_content',
            kwargs={
                'file_path': file_path,
                'file_content': content + '1',
            }
        )
        assert_that(os.path.exists(file_path), equal_to(True))
        assert_that(open(file_path).read(), equal_to(content + '1'))

    def test_create_file_with_multiline_content(self):
        file_path = os.path.join(tempfile.gettempdir(), 'file.txt')
        content = 'hello world'

        try:
            os.remove(file_path)
        except OSError:
            pass

        self.execute_module_step(
            'create_file_with_multiline_content',
            text=content,
            kwargs={
                'file_path': file_path,
            }
        )
        assert_that(os.path.exists(file_path), equal_to(True))
        assert_that(open(file_path).read(), equal_to(content))

        # test when file already exists
        self.execute_module_step(
            'create_file_with_multiline_content',
            text=content + '1',
            kwargs={
                'file_path': file_path
            }
        )
        assert_that(os.path.exists(file_path), equal_to(True))
        assert_that(open(file_path).read(), equal_to(content + '1'))

    def test_check_file_or_directory_exist__file(self):
        file_path = os.path.join(tempfile.gettempdir(), 'file.txt')

        with open(file_path, 'wt') as ff:
            ff.write('hello')

        try:
            self.execute_module_step(
                'check_file_or_directory_exist',
                kwargs={
                    'file_or_directory': 'file',
                    'path': file_path
                }
            )
        except AssertionError:
            raise AssertionError(
                'Assertion should not fail because file exists'
            )

        # check "not" assertion
        try:
            self.execute_module_step(
                'check_file_or_directory_exist',
                kwargs={
                    'file_or_directory': 'file',
                    'path': file_path,
                    'should_not': True
                }
            )
        except AssertionError:
            pass
        else:
            raise AssertionError(
                'Assertion should fail because file exists'
            )

        # check without file

        try:
            os.remove(file_path)
        except OSError:
            pass

        try:
            self.execute_module_step(
                'check_file_or_directory_exist',
                kwargs={
                    'file_or_directory': 'file',
                    'path': file_path
                }
            )
        except AssertionError:
            pass
        else:
            raise AssertionError(
                'Assertion should fail because file does not exist'
            )

        # check "not" assertion
        try:
            self.execute_module_step(
                'check_file_or_directory_exist',
                kwargs={
                    'file_or_directory': 'file',
                    'path': file_path,
                    'should_not': True
                }
            )
        except AssertionError:
            raise AssertionError(
                'Assertion should not fail because file does not exist'
            )

    def test_check_file_or_directory_exist__directory(self):
        dir_path = os.path.join(tempfile.gettempdir(), 'some_dir/')

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        try:
            self.execute_module_step(
                'check_file_or_directory_exist',
                kwargs={
                    'file_or_directory': 'directory',
                    'path': dir_path
                }
            )
        except AssertionError:
            raise AssertionError(
                'Assertion should not fail because directory exists'
            )

        # check "not" assertion
        try:
            self.execute_module_step(
                'check_file_or_directory_exist',
                kwargs={
                    'file_or_directory': 'directory',
                    'path': dir_path,
                    'should_not': True
                }
            )
        except AssertionError:
            pass
        else:
            raise AssertionError(
                'Assertion should fail because directory exists'
            )

        # check without directory
        try:
            shutil.rmtree(dir_path)
        except OSError:
            pass

        try:
            self.execute_module_step(
                'check_file_or_directory_exist',
                kwargs={
                    'file_or_directory': 'directory',
                    'path': dir_path
                }
            )
        except AssertionError:
            pass
        else:
            raise AssertionError(
                'Assertion should fail because directory does not exist'
            )

        # check "not" assertion
        try:
            self.execute_module_step(
                'check_file_or_directory_exist',
                kwargs={
                    'file_or_directory': 'directory',
                    'path': dir_path,
                    'should_not': True
                }
            )
        except AssertionError:
            raise AssertionError(
                'Assertion should not fail because directory does not exist'
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
        'move_file_or_directory': [
            {
                'value': 'I move a file "one.txt" to "two.txt"',
                'expected': {
                    'kwargs': {
                        'file_or_directory': 'file',
                        'source': 'one.txt',
                        'destination': 'two.txt'
                    }
                }
            },
            {
                'value': 'I move a file from "one.txt" to "two.txt"',
                'expected': {
                    'kwargs': {
                        'file_or_directory': 'file',
                        'source': 'one.txt',
                        'destination': 'two.txt'
                    }
                }
            },
            {
                'value': 'I move a file named "one.txt" to "two.txt"',
                'expected': {
                    'kwargs': {
                        'file_or_directory': 'file',
                        'source': 'one.txt',
                        'destination': 'two.txt'
                    }
                }
            },
        ],
        'create_directory': [
            {
                'value': 'a directory "/tmp/test/"',
                'expected': {
                    'kwargs': {
                        'dir_path': '/tmp/test/',
                    }
                }
            },
            {
                'value': 'the directory named "/tmp/test/"',
                'expected': {
                    'kwargs': {
                        'dir_path': '/tmp/test/',
                    }
                }
            },
        ],
        'change_directory': [
            {
                'value': 'I cd to "/tmp/test/"',
                'expected': {
                    'kwargs': {
                        'dir_path': '/tmp/test/',
                    }
                }
            }
        ],
        'create_file_with_content': [
            {
                'value': 'Given a file "/tmp/test/" with "some content"',
                'expected': {
                    'kwargs': {
                        'file_path': '/tmp/test/',
                        'file_content': 'some content',
                    }
                }
            },
            {
                'value': (
                    'Given the file named "/tmp/test/" with "another content"'
                ),
                'expected': {
                    'kwargs': {
                        'file_path': '/tmp/test/',
                        'file_content': 'another content',
                    }
                }
            },
        ],
        'create_file_with_multiline_content': [
            {
                'value': 'Given a file "/tmp/test/" with',
                'expected': {
                    'kwargs': {
                        'file_path': '/tmp/test/'
                    }
                }
            },
        ],
        'check_file_or_directory_exist': [
            {
                'value': 'a file "/var/new.txt" should exist',
                'expected': {
                    'kwargs': {
                        'file_or_directory': 'file',
                        'path': '/var/new.txt',
                        'should_not': None
                    }
                }
            },
            {
                'value': 'the file named "/var/new.txt" should not exist',
                'expected': {
                    'kwargs': {
                        'file_or_directory': 'file',
                        'path': '/var/new.txt',
                        'should_not': 'not'
                    }
                }
            },
            {
                'value': 'the directory "/var/" should not exist',
                'expected': {
                    'kwargs': {
                        'file_or_directory': 'directory',
                        'path': '/var/',
                        'should_not': 'not'
                    }
                }
            },
        ]
    }


class TestFileBehaveSteps(BehaveStepsTestMixin,
                          FileStepsMixin,
                          TestCase):
    module = behave_file
