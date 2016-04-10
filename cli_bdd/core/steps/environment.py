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
    """Sets the environment variable.

    Examples:

    ```gherkin
    Given I set the environment variable "hello" to "world"
    ```
    """
    type_ = 'given'
    sentence = (
        'I set the environment variable "(?P<variable>.*)" '
        'to "(?P<value>.*)"'
    )

    def step(self, variable, value):
        os.environ[variable] = value


class AppendToTheEnvironmentVariable(StepBase):
    """Appends a value to the environment variable.

    Examples:

    ```gherkin
    Given I append "world" to the environment variable "hello"
    ```
    """
    type_ = 'given'
    sentence = (
        'I append "(?P<value>.*)" '
        'to the environment variable "(?P<variable>.*)"'
    )

    def step(self, value, variable):
        _append_to_the_environment_variable(variable, value)


class PrependToTheEnvironmentVariable(StepBase):
    """Prepends a value to the environment variable.

    Examples:

    ```gherkin
    Given I prepend "world" to the environment variable "hello"
    ```
    """
    type_ = 'given'
    sentence = (
        'I prepend "(?P<value>.*)" '
        'to the environment variable "(?P<variable>.*)"'
    )

    def step(self, value, variable):
        _prepend_to_the_environment_variable(variable, value)


class SetTheEnvironmentVariables(StepBase):
    """Populates the set of the environment variables.

    Examples:

    ```gherkin
    Given I set the environment variables to:
        | variable | value |
        | age      | 25    |
        | name     | gena  |
    ```
    """
    type_ = 'given'
    sentence = 'I set the environment variables to:'

    def step(self):
        for variable in self.get_table():
            os.environ[variable['variable']] = variable['value']


class AppendTheValuesToTheEnvironmentVariables(StepBase):
    """Appends the values to the set of the environment variables.

    Examples:
    ```gherkin
    I append the values to the environment variables:
        | variable | value |
        | age      | 1     |
        | name     | a     |
    ```
    """
    type_ = 'given'
    sentence = 'I append the values to the environment variables:'

    def step(self):
        for variable in self.get_table():
            _append_to_the_environment_variable(
                variable['variable'],
                variable['value']
            )


class PrependTheValuesToTheEnvironmentVariables(StepBase):
    """Prepends the values to the set of the environment variables.

    Examples:

    ```gherkin
    I prepend the values to the environment variables:
        | variable | value |
        | age      | 1     |
        | name     | a     |
    ```
    """
    type_ = 'given'
    sentence = 'I prepend the values to the environment variables:'

    def step(self):
        for variable in self.get_table():
            _prepend_to_the_environment_variable(
                variable['variable'],
                variable['value']
            )


base_steps = [
    {
        'func_name': 'set_the_environment_variable',
        'class': SetTheEnvironmentVariableBase,
    },
    {
        'func_name': 'append_to_the_environment_variable',
        'class': AppendToTheEnvironmentVariable,
    },
    {
        'func_name': 'prepend_to_the_environment_variable',
        'class': PrependToTheEnvironmentVariable,
    },
    {
        'func_name': 'set_the_environment_variables',
        'class': SetTheEnvironmentVariables,
    },
    {
        'func_name': 'append_the_values_to_the_environment_variables',
        'class': AppendTheValuesToTheEnvironmentVariables,
    },
    {
        'func_name': 'prepend_the_values_to_the_environment_variables',
        'class': PrependTheValuesToTheEnvironmentVariables,
    },
]
