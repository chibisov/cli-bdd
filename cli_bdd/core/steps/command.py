import subprocess
import os

from hamcrest import (
    assert_that,
    contains_string,
    equal_to,
    is_not,
    is_,
)

from cli_bdd.core.steps.base import StepBase


def run(command, fail_on_error=False, interactively=False):
    # https://docs.python.org/2/library/subprocess.html#popen-constructor
    popen = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if interactively:
        stdout = popen.stdout
        stderr = popen.stderr
        returncode = None
    else:
        stdout, stderr = popen.communicate()
        if fail_on_error and popen.returncode > 0:
            raise Exception('%s (exit code %s)' % (stderr.strip(), popen.returncode))
        returncode = popen.returncode
    return {
        'stdout': stdout,
        'stderr': stderr,
        'returncode': returncode,
        'communicate': popen.communicate
    }


class RunCommand(StepBase):
    """Runs a command.

    Examples:

    ```gherkin
    When I run `echo hello`
    ```
    """
    type_ = 'when'
    sentence = 'I run `(?P<command>[^`]*)`'

    def step(self, command):
        self.get_scenario_context().command_response = run(command)


class SuccessfullyRunCommand(StepBase):
    """Runs a command and checks it for successfull status.


    Examples:

    ```gherkin
    When I successfully run `echo hello`
    ```
    """
    type_ = 'when'
    sentence = 'I successfully run `(?P<command>.*)`'  # todo: with timeout

    def step(self, command):
        self.get_scenario_context().command_response = run(
            command,
            fail_on_error=True
        )


class RunCommandInteractively(StepBase):
    """Runs a command in interactive mode.

    Examples:

    ```gherkin
    When I run `rm -i hello.txt` interactively
    ```
    """
    type_ = 'when'
    sentence = 'I run `(?P<command>[^`]*)` interactively'

    def step(self, command):
        self.get_scenario_context().command_response = run(
            command,
            interactively=True
        )


class TypeIntoCommand(StepBase):
    """Types an input into the previously ran in interactive mode command.

    Examples:

    ```gherkin
    When I type "Yes"
    ```
    """
    type_ = 'when'
    sentence = 'I type "(?P<input_>[^"]*)"'

    def step(self, input_):
        response = self.get_scenario_context().command_response['communicate'](
            input_
        )
        self.get_scenario_context().command_response = {
            'stdout': response[0],
            'stderr': response[1],
        }


class OutputShouldContainText(StepBase):
    '''Checks the command output (stdout, stderr).

    Examples:

    ```gherkin
    Then the the output should contain:
        """
        hello
        """

    Then the output should contain exactly:
        """
        hello
        """

    Then the stderr should not contain exactly:
        """
        hello
        """
    ```
    '''
    type_ = 'then'
    sentence = (
        'the (?P<output>(output|stderr|stdout)) '
        'should( (?P<should_not>not))? contain( (?P<exactly>exactly))?:'
    )

    def step(self, output, should_not=False, exactly=False):
        output = 'stdout' if output == 'output' else output
        data_data = self.get_scenario_context().command_response[output]
        bool_matcher = is_not if should_not else is_
        comparison_matcher = equal_to if exactly else contains_string
        assert_that(
            data_data,
            bool_matcher(
                comparison_matcher(self.get_text())
            )
        )


class ExitStatusShouldBe(StepBase):
    """Checks the command status code.

    Examples:

    ```gherkin
    Then the exit status should be 1
    Then the exit status should not be 1
    ```
    """
    type_ = 'then'
    sentence = (
        'the exit status should( (?P<should_not>not))? '
        'be (?P<exit_status>\d+)'
    )

    def step(self, should_not=False, exit_status=None):
        exit_status = int(exit_status)
        bool_matcher = is_not if should_not else is_
        assert_that(
            self.get_scenario_context().command_response['returncode'],
            bool_matcher(
                equal_to(exit_status)
            )
        )


base_steps = [
    {
        'func_name': 'run_command',
        'class': RunCommand
    },
    {
        'func_name': 'successfully_run_command',
        'class': SuccessfullyRunCommand
    },
    {
        'func_name': 'run_command_interactively',
        'class': RunCommandInteractively
    },
    {
        'func_name': 'type_into_command',
        'class': TypeIntoCommand
    },
    {
        'func_name': 'output_should_contain_text',
        'class': OutputShouldContainText
    },
    {
        'func_name': 'exit_status_should_be',
        'class': ExitStatusShouldBe
    }
]
