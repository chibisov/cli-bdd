from behave import given, when, then


DECORATORS_BY_TYPES = {
    'given': given,
    'when': when,
    'then': then,
}


class BehaveStepMixin(object):
    def build_step_func(self):
        decorator = DECORATORS_BY_TYPES[self.type_]
        @decorator(self.sentence)
        def behave_step(context, *args, **kwargs):
            self.context = context
            return self.step(*args, **kwargs)

        return behave_step

    def get_table(self):
        return self.context.table

    def get_text(self):
        return self.context.text

    def get_scenario_context(self):
        return self.context
