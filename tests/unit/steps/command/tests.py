import os
import tempfile

import pexpect
from hamcrest import assert_that, equal_to

from cli_bdd.behave.steps import command as behave_command
from cli_bdd.core.steps.command import base_steps
from cli_bdd.lettuce.steps import command as lettuce_command
from testutils import (
    BehaveStepsTestMixin,
    LettuceStepsTestMixin,
    StepsSentenceRegexTestMixin,
    TestCase
)


class CommandStepsMixin(object):
    def test_command_run(self):
        file_path = os.path.join(tempfile.gettempdir(), 'test.txt')

        try:
            os.remove(file_path)
        except OSError:
            pass

        self.execute_module_step(
            'run_command',
            kwargs={
                'command': 'echo "hello" > %s' % file_path,
            }
        )
        assert_that(open(file_path).read(), equal_to('hello\n'))

    def test_successfully_run_command(self):
        # no error
        self.execute_module_step(
            'successfully_run_command',
            kwargs={
                'command': 'echo "hello"',
            }
        )

        # with error
        try:
            self.execute_module_step(
                'successfully_run_command',
                kwargs={
                    'command': 'cat /',
                }
            )
        except Exception as e:
            assert_that(
                str(e),
                equal_to('cat: /: Is a directory\r\n (exit code 1)')
            )
        else:
            raise AssertionError(
                'Should fail when response is not successfull'
            )

    def test_run_command_interactively(self):
        file_path = os.path.join(tempfile.gettempdir(), 'test_interactive.txt')
        with open(file_path, 'wr') as ff:
            ff.write('Some text')

        context = self.execute_module_step(
            'run_command_interactively',
            kwargs={
                'command': 'rm -i %s' % file_path,
            }
        )

        # file should not be removed yet
        assert_that(os.path.isfile(file_path), equal_to(True))

        # let's communicate and say Yes
        context.command_response['child'].sendline('Y')
        context.command_response['child'].expect(pexpect.EOF)

        # file should be removed
        assert_that(os.path.isfile(file_path), equal_to(False))

    def test_type_into_command(self):
        file_path = os.path.join(tempfile.gettempdir(), 'test_interactive.txt')
        with open(file_path, 'wr') as ff:
            ff.write('Some text')

        context = self.execute_module_step(
            'run_command_interactively',
            kwargs={
                'command': 'rm -i %s' % file_path,
            }
        )

        # file should not be removed yet
        assert_that(os.path.isfile(file_path), equal_to(True))

        # let's communicate and say Yes via step
        self.execute_module_step(
            'type_into_command',
            context=context,
            kwargs={
                'input_': 'Y',
            }
        )
        context.command_response['child'].expect(pexpect.EOF)

        # file should be removed
        assert_that(os.path.isfile(file_path), equal_to(False))

    def test_got_interactive_dialog(self):
        file_path = os.path.join(tempfile.gettempdir(), 'test_interactive.txt')
        with open(file_path, 'wr') as ff:
            ff.write('Some text')

        for matcher, valid in (
            ('remove test_interactive.txt', False),
            ('remove .*/test_interactive.txt', True)
        ):
            context = self.execute_module_step(
                'run_command_interactively',
                kwargs={
                    'command': 'rm -i %s' % file_path,
                }
            )

            # file should not be removed yet
            assert_that(os.path.isfile(file_path), equal_to(True))

            # let's wait for a dialog
            try:
                self.execute_module_step(
                    'got_interactive_dialog',
                    context=context,
                    kwargs={
                        'dialog_matcher': matcher,
                        'timeout': '0.1'
                    },
                )
            except AssertionError:
                if valid:
                    raise AssertionError(
                        'Should not fail with timeout '
                        'error for valid dialog match "%s"' % matcher
                    )
            else:
                if not valid:
                    raise AssertionError(
                        'Should fail with timeout '
                        'error for invalid dialog match "%s"' % matcher
                    )

    def test_output_should_contain_text__stdout(self):
        context = self.execute_module_step(
            'run_command',
            kwargs={
                'command': 'echo "hello"',
            }
        )

        # stdout contains text
        self.execute_module_step(
            'output_should_contain_text',
            context=context,
            kwargs={
                'output': 'output',
            },
            text='ell'
        )

        # stdout doesn't contain exact text
        try:
            self.execute_module_step(
                'output_should_contain_text',
                context=context,
                kwargs={
                    'output': 'output',
                    'exactly': True
                },
                text='ell'
            )
        except AssertionError as e:
            assert_that(
                str(e),
                equal_to(
                    'Comparison error. Diff:\n'
                    '*** \n'
                    '\n'
                    '--- \n'
                    '\n'
                    '***************\n'
                    '\n'
                    '*** 1,2 ****\n'
                    '\n'
                    '! hello\n'
                    '! \n'
                    '--- 1 ----\n'
                    '\n'
                    '! ell'
                )
            )
        else:
            raise AssertionError("stdout doesn't contain exact text")

        # stdout does contain exact text
        try:
            self.execute_module_step(
                'output_should_contain_text',
                context=context,
                kwargs={
                    'output': 'output',
                    'should_not': 'not'
                },
                text='ell'
            )
        except AssertionError:
            pass
        else:
            raise AssertionError("stdout does contain exact text")

    def test_output_should_contain_text__new_line_highlight(self):
        # expected does not contain new line
        context = self.execute_module_step(
            'run_command',
            kwargs={
                'command': 'echo "hello"',
            }
        )

        try:
            self.execute_module_step(
                'output_should_contain_text',
                context=context,
                kwargs={
                    'output': 'output',
                    'exactly': True
                },
                text='hello'
            )
        except AssertionError as e:
            assert_that(
                str(e),
                equal_to(
                    'Comparison error. Diff:\n'
                    '*** \n'
                    '\n'
                    '--- \n'
                    '\n'
                    '***************\n'
                    '\n'
                    '*** 1,2 ****\n'
                    '\n'
                    '  hello\n'
                    '- \n'
                    '--- 1 ----\n'
                )
            )
        else:
            raise AssertionError("stdout does not contain exact text")

        # response does not contain new line
        context = self.execute_module_step(
            'run_command',
            kwargs={
                'command': 'printf "hello"',
            }
        )

        try:
            self.execute_module_step(
                'output_should_contain_text',
                context=context,
                kwargs={
                    'output': 'output',
                    'exactly': True
                },
                text='hello\n'
            )
        except AssertionError as e:
            assert_that(
                str(e),
                equal_to(
                    'Comparison error. Diff:\n'
                    '*** \n'
                    '\n'
                    '--- \n'
                    '\n'
                    '***************\n'
                    '\n'
                    '*** 1 ****\n'
                    '\n'
                    '--- 1,2 ----\n'
                    '\n'
                    '  hello\n'
                    '+ '
                )
            )
        else:
            raise AssertionError("stdout does not contain exact text")

    def test_output_should_contain_text__stderr(self):
        not_existing_file_path = os.path.join(
            tempfile.gettempdir(),
            'not_exists.txt'
        )

        # remove non existing file
        try:
            os.remove(not_existing_file_path)
        except OSError:
            pass

        error_context = self.execute_module_step(
            'run_command',
            kwargs={
                'command': 'rm %s' % not_existing_file_path,
            }
        )

        # stderr contains text
        self.execute_module_step(
            'output_should_contain_text',
            context=error_context,
            kwargs={
                'output': 'stderr',
            },
            text='No such file or directory'
        )

    def test_exit_status_should_be(self):
        not_existing_file_path = os.path.join(
            tempfile.gettempdir(),
            'not_exists.txt'
        )

        # remove non existing file
        try:
            os.remove(not_existing_file_path)
        except OSError:
            pass

        error_context = self.execute_module_step(
            'run_command',
            kwargs={
                'command': 'rm %s' % not_existing_file_path,
            }
        )

        # should be
        self.execute_module_step(
            'exit_status_should_be',
            context=error_context,
            kwargs={
                'exit_status': '1'
            }
        )

        # shouldn't be
        try:
            self.execute_module_step(
                'exit_status_should_be',
                context=error_context,
                kwargs={
                    'should_not': 'not',
                    'exit_status': '1'
                }
            )
        except AssertionError:
            pass
        else:
            raise AssertionError("exit status equals 1")


class TestCommandStepsSentenceRegex(StepsSentenceRegexTestMixin, TestCase):
    steps = base_steps
    step_experiments = {
        'run_command': [
            {
                'value': 'I run `sosisa`',
                'expected': {
                    'kwargs': {
                        'command': 'sosisa'
                    }
                }
            }
        ],
        'successfully_run_command': [
            {
                'value': 'I successfully run `sosisa`',
                'expected': {
                    'kwargs': {
                        'command': 'sosisa'
                    }
                }
            }
        ],
        'run_command_interactively': [
            {
                'value': 'I run `sosisa` interactively',
                'expected': {
                    'kwargs': {
                        'command': 'sosisa'
                    }
                }
            }
        ],
        'type_into_command': [
            {
                'value': 'I type "sosisa"',
                'expected': {
                    'kwargs': {
                        'input_': 'sosisa'
                    }
                }
            }
        ],
        'got_interactive_dialog': [
            {
                'value': (
                    'I got "Password:" for interactive dialog in 1 second'
                ),
                'expected': {
                    'kwargs': {
                        'dialog_matcher': 'Password:',
                        'timeout': '1'
                    }
                }
            },
            {
                'value': (
                    'I got "Name .*: " for interactive dialog in 0.05 seconds'
                ),
                'expected': {
                    'kwargs': {
                        'dialog_matcher': 'Name .*: ',
                        'timeout': '0.05'
                    }
                }
            },
            {
                'value': 'I got "Login:" for interactive dialog',
                'expected': {
                    'kwargs': {
                        'dialog_matcher': 'Login:',
                        'timeout': None
                    }
                }
            },
        ],
        'exit_status_should_be': [
            {
                'value': 'the exit status should be 1',
                'expected': {
                    'kwargs': {
                        'should_not': None,
                        'exit_status': '1'
                    }
                }
            },
            {
                'value': 'the exit status should not be 2',
                'expected': {
                    'kwargs': {
                        'should_not': 'not',
                        'exit_status': '2'
                    }
                }
            }
        ]
    }


class TestCommandBehaveSteps(BehaveStepsTestMixin,
                             CommandStepsMixin,
                             TestCase):
    module = behave_command


class TestCommandLettuceSteps(LettuceStepsTestMixin,
                              CommandStepsMixin,
                              TestCase):
    module = lettuce_command
