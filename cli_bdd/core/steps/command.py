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
    type_ = 'when'
    sentence = 'I run `([^`]*)`'

    def step(self, command):
        self.get_scenario_context().command_response = run(command)


class SuccessfullyRunCommand(StepBase):
    type_ = 'when'
    sentence = 'I successfully run `(.*?)`'  # todo: with timeout

    def step(self, command):
        self.get_scenario_context().command_response = run(
            command,
            fail_on_error=True
        )


class RunCommandInteractively(StepBase):
    type_ = 'when'
    sentence = 'I run `([^`]*)` interactively'

    def step(self, command):
        self.get_scenario_context().command_response = run(
            command,
            interactively=True
        )


class TypeIntoCommand(StepBase):
    type_ = 'when'
    sentence = 'I type "([^"]*)"'

    def step(self, input_):
        response = self.get_scenario_context().command_response['communicate'](
            input_
        )
        self.get_scenario_context().command_response = {
            'stdout': response[0],
            'stderr': response[1],
        }


class OutputShouldContainText(StepBase):
    type_ = 'then'
    sentence = 'the (output|stderr|stdout) should( not)? contain( exactly)?:'

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


base_steps = {
    'run_command': RunCommand,
    'successfully_run_command': SuccessfullyRunCommand,
    'run_command_interactively': RunCommandInteractively,
    'type_into_command': TypeIntoCommand,
    'output_should_contain_text': OutputShouldContainText,
}
