import os

from cli_bdd.core.steps.base import StepBase


def _append_to_the_environment_variable(variable, value):
    if variable not in os.environ:
        os.environ[variable] = ''
    os.environ[variable] += value


def _prepend_to_the_environment_variable(variable, value):
    if variable not in os.environ:
        os.environ[variable] = ''
    os.environ[variable] = '%s%s' % (value, os.environ[variable])


# todo: a mocked home directory
# https://github.com/cucumber/aruba/blob/eefb1fd5f538fc017574464919f44057f8c2d914/lib/aruba/cucumber/environment.rb#L1


class SetTheEnvironmentVariableBase(StepBase):
    type_ = 'given'
    sentence = 'I set the environment variable "(.*)" to "(.*)"'

    def step(self, variable, value):
        os.environ[variable] = value


class AppendToTheEnvironmentVariable(StepBase):
    type_ = 'given'
    sentence = 'I append "(.*)" to the environment variable "(.*)"'

    def step(self, variable, value):
        _append_to_the_environment_variable(variable, value)


class PrependToTheEnvironmentVariable(StepBase):
    type_ = 'given'
    sentence = 'I prepend "(.*)" to the environment variable "(.*)"'

    def step(self, variable, value):
        _prepend_to_the_environment_variable(variable, value)


class SetTheEnvironmentVariables(StepBase):
    type_ = 'given'
    sentence = 'I set the environment variables to:'

    def step(self):
        for variable in self.get_table():
            os.environ[variable['variable']] = variable['value']


class AppendTheValuesToTheEnvironmentVariables(StepBase):
    type_ = 'given'
    sentence = 'I append the values to the environment variables:'

    def step(self):
        for variable in self.get_table():
            _append_to_the_environment_variable(
                variable['variable'],
                variable['value']
            )


class PrependTheValuesToTheEnvironmentVariables(StepBase):
    type_ = 'given'
    sentence = 'I prepend the values to the environment variables:'

    def step(self):
        for variable in self.get_table():
            _prepend_to_the_environment_variable(
                variable['variable'],
                variable['value']
            )


base_steps = {
    'set_the_environment_variable': SetTheEnvironmentVariableBase,
    'append_to_the_environment_variable': AppendToTheEnvironmentVariable,
    'prepend_to_the_environment_variable': PrependToTheEnvironmentVariable,
    'set_the_environment_variables': SetTheEnvironmentVariables,
    'append_the_values_to_the_environment_variables': AppendTheValuesToTheEnvironmentVariables,
    'prepend_the_values_to_the_environment_variables': PrependTheValuesToTheEnvironmentVariables,
}
