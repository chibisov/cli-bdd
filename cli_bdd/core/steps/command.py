import difflib
import StringIO

import pexpect
from hamcrest import (
    assert_that,
    contains_string,
    equal_to,
    greater_than,
    greater_than_or_equal_to,
    is_,
    is_not,
    less_than,
    less_than_or_equal_to
)

from cli_bdd.core.steps.base import StepBase


def run(command, fail_on_error=False, interactively=False):
    child = pexpect.spawn('/bin/sh', ['-c', command], echo=False)
    child.logfile_read = StringIO.StringIO()
    child.logfile_send = StringIO.StringIO()
    if not interactively:
        child.expect(pexpect.EOF)
        if fail_on_error and child.exitstatus > 0:
            raise Exception(
                '%s (exit code %s)' % (
                    child.logfile_read.getvalue(),
                    child.exitstatus
                )
            )
    return {
        'child': child,
    }


def ensure_command_finished(child):
    return child.expect(pexpect.EOF)


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
        child = self.get_scenario_context().command_response['child']
        child.logfile_read.truncate(0)  # todo: test me
        child.sendline(input_)


class GotInteractiveDialogCommand(StepBase):
    """Waits for a dialog.

    By default waits for 1 second. Timeout could be changed by providing
    `in N seconds` information.

    Examples:

    ```gherkin
    When I got "Password:" for interactive dialog
    When I got "Password:" for interactive dialog in 1 second
    When I got "Name .*: " for interactive dialog in 0.01 seconds
    ```
    """
    type_ = 'when'
    sentence = (
        'I got "(?P<dialog_matcher>[^"]*)" for interactive dialog'
        '( in (?P<timeout>(\d*[.])?\d+) seconds?)?'
    )

    def step(self, dialog_matcher, timeout):
        if not timeout:  # todo: test default timeout
            timeout = 1

        timeout = float(timeout)
        try:
            self.get_scenario_context().command_response['child'].expect(
                dialog_matcher,
                timeout=timeout
            )
        except pexpect.exceptions.TIMEOUT:
            raise AssertionError(
                'Have been waiting for interactive dialog '
                'for more than %s seconds' % timeout
            )


class OutputShouldContainText(StepBase):
    '''Checks the command output (stdout, stderr).

    Examples:

    ```gherkin
    Then the output should contain:
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
        'should( (?P<should_not>not))? contain( (?P<exactly>exactly))?'
    )

    def step(self, output, should_not=False, exactly=False):
        child = self.get_scenario_context().command_response['child']
        ensure_command_finished(child)
        output = 'stdout' if output == 'output' else output

        # todo: separate stdout and stderr
        # todo: test replace
        data = child.logfile_read.getvalue().replace('\r\n', '\n')
        data_lines = data.splitlines()
        if data.endswith('\n'):
            data_lines.append('')

        expected = self.get_text().encode('utf-8')  # todo: test encode
        expected_lines = expected.splitlines()
        if expected.endswith('\n'):
            expected_lines.append('')

        bool_matcher = is_not if should_not else is_
        comparison_matcher = equal_to if exactly else contains_string
        try:
            assert_that(
                data,
                bool_matcher(
                    comparison_matcher(expected)
                )
            )
        except AssertionError:
            if comparison_matcher == equal_to and bool_matcher == is_:
                diff = '\n'.join(
                    difflib.context_diff(
                        data_lines,
                        expected_lines
                    )
                )
                raise AssertionError('Comparison error. Diff:\n' + diff)
            else:
                raise


class OutputShouldContainLines(StepBase):
    '''Checks the command output number of lines.

    Examples:

    ```gherkin
    Then the output should contain 3 lines
    Then the output should not contain 3 lines
    Then the output should contain up to 3 lines
    Then the output should contain less than 3 lines
    Then the output should contain at least 1 line
    Then the output should contain more than 1 line
    ```
    '''
    type_ = 'then'
    sentence = (
        'the (?P<output>(output|stderr|stdout)) '
        'should( (?P<should_not>not))? '
        'contain( '
        '(?P<comparison>(up to|at least|more than|less than)))? '
        '(?P<count>\d+) lines?'
    )

    def step(self, output, should_not=False, comparison=None, count=None):
        child = self.get_scenario_context().command_response['child']
        ensure_command_finished(child)
        output = 'stdout' if output == 'output' else output
        comparison = (comparison or '').strip()
        count = int(count)

        # todo: separate stdout and stderr
        # todo: test stderr
        data = child.logfile_read.getvalue().strip()
        number_of_lines = len(data.splitlines())

        bool_matcher = is_not if should_not else is_
        comparison_matcher = {
            '': equal_to,
            'at least': greater_than_or_equal_to,
            'up to': less_than_or_equal_to,
            'less than': less_than,
            'more than': greater_than,
        }[comparison]

        assert_that(
            number_of_lines,
            bool_matcher(
                comparison_matcher(count)
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
        child = self.get_scenario_context().command_response['child']

        ensure_command_finished(child)

        assert_that(
            child.exitstatus,
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
        'func_name': 'got_interactive_dialog',
        'class': GotInteractiveDialogCommand
    },
    {
        'func_name': 'output_should_contain_text',
        'class': OutputShouldContainText
    },
    {
        'func_name': 'output_should_contain_lines',
        'class': OutputShouldContainLines
    },
    {
        'func_name': 'exit_status_should_be',
        'class': ExitStatusShouldBe
    }
]
