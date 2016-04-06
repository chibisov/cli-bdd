import os
from copy import deepcopy
import tempfile

from mock import Mock
from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
)

from testutils import (
    TestCase,
    BehaveStepsTestMixin,
    LettuceStepsTestMixin,
    StepsSentenceRegexTestMixin,
)
from cli_bdd.core.steps.command import base_steps
from cli_bdd.behave.steps import command as behave_command
from cli_bdd.lettuce.steps import command as lettuce_command


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
                equal_to('cat: /: Is a directory (exit code 1)')
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
        context.command_response['communicate']('Y')

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
        new_context = self.execute_module_step(
            'type_into_command',
            context=context,
            kwargs={
                'input_': 'Y',
            }
        )

        # file should be removed
        assert_that(os.path.isfile(file_path), equal_to(False))

    def test_output_should_contain_text(self):
        context = Mock()
        context.command_response = {
            'stdout': 'hello',
            'stderr': 'world'
        }

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
            pass
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
        except AssertionError as e:
            pass
        else:
            raise AssertionError("stdout does contain exact text")

        # stderr contains text
        self.execute_module_step(
            'output_should_contain_text',
            context=context,
            kwargs={
                'output': 'stderr',
            },
            text='rld'
        )

    def test_exit_status_should_be(self):
        context = Mock()
        context.command_response = {
            'returncode': 1,
        }

        self.execute_module_step(
            'exit_status_should_be',
            context=context,
            kwargs={
                'exit_status': '1'
            }
        )

        # stdout doesn't contain exact text
        try:
            self.execute_module_step(
                'exit_status_should_be',
                context=context,
                kwargs={
                    'should_not': 'not',
                    'exit_status': '1'
                }
            )
        except AssertionError as e:
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
