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
            args=[
                'echo "hello" > %s' % file_path,
            ]
        )
        assert_that(open(file_path).read(), equal_to('hello\n'))

    def test_successfully_run_command(self):
        # no error
        self.execute_module_step(
            'successfully_run_command',
            args=[
                'echo "hello"',
            ]
        )

        # with error
        try:
            self.execute_module_step(
                'successfully_run_command',
                args=[
                    'cat /',
                ]
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
            args=[
                'rm -i %s' % file_path,
            ]
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
            args=[
                'rm -i %s' % file_path,
            ]
        )

        # file should not be removed yet
        assert_that(os.path.isfile(file_path), equal_to(True))

        # let's communicate and say Yes via step
        new_context = self.execute_module_step(
            'type_into_command',
            context=context,
            args=[
                'Y',
            ]
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
            args=[
                'output',
            ],
            text='ell'
        )

        # stdout doesn't contain exact text
        try:
            self.execute_module_step(
                'output_should_contain_text',
                context=context,
                args=[
                    'output',
                    '',
                    'exactly'
                ],
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
                args=[
                    'output',
                    'not'
                ],
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
            args=[
                'stderr',
            ],
            text='rld'
        )


class TestCommandStepsSentenceRegex(StepsSentenceRegexTestMixin, TestCase):
    steps = base_steps
    step_experiments = {
        'run_command': [
            {
                'value': 'I run `sosisa`',
                'expected': {
                    'args': ('sosisa',)
                }
            }
        ],
        'successfully_run_command': [
            {
                'value': 'I successfully run `sosisa`',
                'expected': {
                    'args': ('sosisa',)
                }
            }
        ],
        'run_command_interactively': [
            {
                'value': 'I run `sosisa` interactively',
                'expected': {
                    'args': ('sosisa',)
                }
            }
        ],
        'type_into_command': [
            {
                'value': 'I type "sosisa"',
                'expected': {
                    'args': ('sosisa',)
                }
            }
        ],
    }
#         'append_to_the_environment_variable': [
#             {
#                 'value': 'I append "polina" to the environment variable "sosisa"',
#                 'expected': {
#                     'args': ('polina', 'sosisa')
#                 }
#             }
#         ],
#         'prepend_to_the_environment_variable': [
#             {
#                 'value': 'I prepend "polina" to the environment variable "sosisa"',
#                 'expected': {
#                     'args': ('polina', 'sosisa')
#                 }
#             }
#         ],
#         'set_the_environment_variables': [
#             {
#                 'value': 'I set the environment variables to:',
#                 'expected': {
#                     'args': tuple()
#                 },
#             }
#         ],
#         'append_the_values_to_the_environment_variables': [
#             {
#                 'value': 'I append the values to the environment variables:',
#                 'expected': {
#                     'args': tuple()
#                 },
#             }
#         ],
#         'prepend_the_values_to_the_environment_variables': [
#             {
#                 'value': 'I prepend the values to the environment variables:',
#                 'expected': {
#                     'args': tuple()
#                 },
#             }
#         ],
#     }


class TestCommandBehaveSteps(BehaveStepsTestMixin,
                             CommandStepsMixin,
                             TestCase):
    module = behave_command


class TestCommandLettuceSteps(LettuceStepsTestMixin,
                              CommandStepsMixin,
                              TestCase):
    module = lettuce_command
