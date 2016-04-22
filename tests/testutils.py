import unittest
import re

from mock import Mock, patch
from hamcrest import (
    assert_that,
    equal_to,
)

from cli_bdd.behave import steps as behave_steps_root_module
from cli_bdd.lettuce import steps as lettuce_steps_root_module
from cli_bdd.lettuce.steps.mixins import LettuceStepMixin


class TestCase(unittest.TestCase):
    pass


class StepsSentenceRegexTestMixin(object):
    step_experiments = None
    steps = None

    def test_experiments(self):
        for step_func_name, step_exp in self.step_experiments.items():
            sentence = self._get_sentence_by_step_func_name(step_func_name)
            for exp in step_exp:
                result = re.search(sentence, exp['value'])
                if result is None and exp['expected']['kwargs']:
                    raise AssertionError(
                        'Could not match any data by regex:\n%s\nfor value:\n%s' % (
                            sentence,
                            exp['value']
                        )
                    )
                assert_that(
                    result.groupdict(),
                    equal_to(exp['expected']['kwargs']),
                    {
                        'value': exp['value'],
                        'sentence': sentence
                    }
                )

    def _get_sentence_by_step_func_name(self, step_func_name):
        for step in self.steps:
            if step['func_name'] == step_func_name:
                return step['class'].sentence
        raise 'Could not find step with func_name "%s"' % step_func_name


class StepsTestMixin(object):
    module = None
    root_module = None

    def execute_module_step(self, name, context=None, kwargs={}, table=[], text=None):
        assert_that(
            getattr(self.module, name),
            equal_to(getattr(self.root_module, name))
        )
        context = context or Mock()
        return self._execute_module_step(
            name,
            context=context,
            kwargs=kwargs,
            table=table,
            text=text,
        )

    def _execute_module_step(self, name, context, kwargs, table, text):
        raise NotImplementedError()


class BehaveStepsTestMixin(StepsTestMixin):
    module = None
    root_module = behave_steps_root_module

    def _execute_module_step(self, name, context, kwargs, table, text):
        context.table = table
        context.text = text
        getattr(self.module, name)(context, **kwargs)
        return context


class LettuceStepsTestMixin(StepsTestMixin):
    module = None
    root_module = lettuce_steps_root_module

    def _execute_module_step(self, name, context, kwargs, table, text):
        step_context = Mock()
        step_context.hashes = table
        step_context.multiline = text

        with patch.object(LettuceStepMixin, 'get_scenario_context', lambda self: context):
            getattr(self.module, name)(step_context, **kwargs)
        return context
