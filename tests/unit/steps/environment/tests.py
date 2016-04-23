import os
from copy import deepcopy

from hamcrest import assert_that, equal_to, has_entries

from cli_bdd.behave.steps import environment as behave_environment
from cli_bdd.core.steps.environment import base_steps
from cli_bdd.lettuce.steps import environment as lettuce_environment
from testutils import (
    BehaveStepsTestMixin,
    LettuceStepsTestMixin,
    StepsSentenceRegexTestMixin,
    TestCase
)


class EnvironmentStepsMixin(object):
    def setUp(self):
        super(EnvironmentStepsMixin, self).setUp()
        self.original_environ = deepcopy(os.environ)

    def tearDown(self):
        super(EnvironmentStepsMixin, self).tearDown()
        os.environ = self.original_environ

    def test_set_the_environment_variable(self):
        assert_that('hello' in os.environ, equal_to(False))
        self.execute_module_step(
            'set_the_environment_variable',
            kwargs={
                'variable': 'hello',
                'value': 'world'
            }
        )
        assert_that(os.environ.get('hello'), equal_to('world'))

    def test_append_to_the_environment_variable(self):
        assert_that('hello' in os.environ, equal_to(False))

        # no env variable
        self.execute_module_step(
            'append_to_the_environment_variable',
            kwargs={
                'variable': 'hello',
                'value': 'world'
            }
        )
        assert_that(os.environ.get('hello'), equal_to('world'))

        # with env variable
        self.execute_module_step(
            'append_to_the_environment_variable',
            kwargs={
                'variable': 'hello',
                'value': 'amigo'
            }
        )
        assert_that(os.environ.get('hello'), equal_to('worldamigo'))

    def test_prepend_to_the_environment_variable(self):
        assert_that('hello' in os.environ, equal_to(False))

        # no env variable
        self.execute_module_step(
            'prepend_to_the_environment_variable',
            kwargs={
                'variable': 'hello',
                'value': 'world'
            }
        )
        assert_that(os.environ.get('hello'), equal_to('world'))

        # with env variable
        self.execute_module_step(
            'prepend_to_the_environment_variable',
            kwargs={
                'variable': 'hello',
                'value': 'amigo'
            }
        )
        assert_that(os.environ.get('hello'), equal_to('amigoworld'))

    def test_set_the_environment_variables(self):
        assert_that('hello_one' in os.environ, equal_to(False))
        assert_that('hello_two' in os.environ, equal_to(False))

        self.execute_module_step(
            'set_the_environment_variables',
            table=[
                {
                    'variable': 'hello_one',
                    'value': 'world_one',
                },
                {
                    'variable': 'hello_two',
                    'value': 'world_two',
                },
            ]
        )
        assert_that(
            os.environ,
            has_entries({
                'hello_one': 'world_one',
                'hello_two': 'world_two',
            })
        )

    def test_append_the_values_to_the_environment_variables(self):
        assert_that('hello_one' in os.environ, equal_to(False))
        assert_that('hello_two' in os.environ, equal_to(False))

        # no env variables
        self.execute_module_step(
            'append_the_values_to_the_environment_variables',
            table=[
                {
                    'variable': 'hello_one',
                    'value': 'world_one',
                },
                {
                    'variable': 'hello_two',
                    'value': 'world_two',
                },
            ]
        )
        assert_that(
            os.environ,
            has_entries({
                'hello_one': 'world_one',
                'hello_two': 'world_two',
            })
        )

        # with env variables
        self.execute_module_step(
            'append_the_values_to_the_environment_variables',
            table=[
                {
                    'variable': 'hello_one',
                    'value': 'plus_one',
                },
                {
                    'variable': 'hello_two',
                    'value': 'plus_two',
                },
            ]
        )
        assert_that(
            os.environ,
            has_entries({
                'hello_one': 'world_oneplus_one',
                'hello_two': 'world_twoplus_two',
            })
        )

    def test_prepend_the_values_to_the_environment_variables(self):
        assert_that('hello_one' in os.environ, equal_to(False))
        assert_that('hello_two' in os.environ, equal_to(False))

        # no env variables
        self.execute_module_step(
            'prepend_the_values_to_the_environment_variables',
            table=[
                {
                    'variable': 'hello_one',
                    'value': 'world_one',
                },
                {
                    'variable': 'hello_two',
                    'value': 'world_two',
                },
            ]
        )
        assert_that(
            os.environ,
            has_entries({
                'hello_one': 'world_one',
                'hello_two': 'world_two',
            })
        )

        # with env variables
        self.execute_module_step(
            'prepend_the_values_to_the_environment_variables',
            table=[
                {
                    'variable': 'hello_one',
                    'value': 'plus_one',
                },
                {
                    'variable': 'hello_two',
                    'value': 'plus_two',
                },
            ]
        )
        assert_that(
            os.environ,
            has_entries({
                'hello_one': 'plus_oneworld_one',
                'hello_two': 'plus_twoworld_two',
            })
        )


class TestEnvironmentStepsSentenceRegex(StepsSentenceRegexTestMixin, TestCase):
    steps = base_steps
    step_experiments = {
        'set_the_environment_variable': [
            {
                'value': 'I set the environment variable "polina" to "sosisa"',
                'expected': {
                    'kwargs': {
                        'variable': 'polina',
                        'value': 'sosisa'
                    }
                }
            }
        ],
        'append_to_the_environment_variable': [
            {
                'value': (
                    'I append "sosisa" to the environment variable "polina"'
                ),
                'expected': {
                    'kwargs': {
                        'variable': 'polina',
                        'value': 'sosisa'
                    }
                }
            }
        ],
        'prepend_to_the_environment_variable': [
            {
                'value': (
                    'I prepend "sosisa" to the environment variable "polina"'
                ),
                'expected': {
                    'kwargs': {
                        'variable': 'polina',
                        'value': 'sosisa'
                    }
                }
            }
        ],
        'set_the_environment_variables': [
            {
                'value': 'I set the environment variables to',
                'expected': {
                    'kwargs': {}
                },
            }
        ],
        'append_the_values_to_the_environment_variables': [
            {
                'value': 'I append the values to the environment variables',
                'expected': {
                    'kwargs': {}
                },
            }
        ],
        'prepend_the_values_to_the_environment_variables': [
            {
                'value': 'I prepend the values to the environment variables',
                'expected': {
                    'kwargs': {}
                },
            }
        ],
    }


class TestEnvironmentBehaveSteps(BehaveStepsTestMixin,
                                 EnvironmentStepsMixin,
                                 TestCase):
    module = behave_environment


class TestEnvironmentLettuceSteps(LettuceStepsTestMixin,
                                  EnvironmentStepsMixin,
                                  TestCase):
    module = lettuce_environment
